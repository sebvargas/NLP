import nltk
import re
from nltk.util import transitive_closure, invert_graph
from nltk.compat import (string_types, total_ordering, text_type,
                         python_2_unicode_compatible, unicode_repr)
from nltk.parse.api import ParserI

_ARROW_RE = re.compile(r'\s* -> \s*', re.VERBOSE)
_PROBABILITY_RE = re.compile(r'( \[ [\d\.]+ \] ) \s*', re.VERBOSE)
_TERMINAL_RE = re.compile(r'( "[^"]+" | \'[^\']+\' ) \s*', re.VERBOSE)
_DISJUNCTION_RE = re.compile(r'\| \s*', re.VERBOSE)
def main():
    #tokens = ["book", "the", "flight", "through", "Houston"]
    tokens = []
    #grammar = []
    with open('string.txt', 'r') as f:
        for line in f:
            for word in line.split():
                tokens.append(word)
    tokens = ["book", "the", "flight", "through", "Texas"]
    print(tokens)
    
    gf = open("grammar.txt", 'r')
    grammarCode = gf.readlines()
    gf.close()
    #print grammarCode

    grammar = fromstring(grammarCode)
    #print grammar
    parser = nltk.ChartParser(grammar)
    #print parser
    while True:
        try:
            for tree in parser.parse(tokens):
                print(tree)
            print("Yes, this string can be generated by the language")

            break
        except ValueError:
            print("No, this string cannot be generated by the language")
            break
           
def fromstring(input, encoding=None):
    """
    Return the ``CFG`` corresponding to the input string(s).

    :param input: a grammar, either in the form of a string or as a list of strings.
    """
    start, productions = read_grammar(input, standard_nonterm_parser,
                                          encoding=encoding)
    return CFG(start, productions)

def read_grammar(input, nonterm_parser, probabilistic=False, encoding=None):
    """
    Return a pair consisting of a starting category and a list of
    ``Productions``.

    :param input: a grammar, either in the form of a string or else
        as a list of strings.
    :param nonterm_parser: a function for parsing nonterminals.
        It should take a ``(string, position)`` as argument and
        return a ``(nonterminal, position)`` as result.
    :param probabilistic: are the grammar rules probabilistic?
    :type probabilistic: bool
    :param encoding: the encoding of the grammar, if it is a binary string
    :type encoding: str
    """
    if encoding is not None:
        input = input.decode(encoding)
    if isinstance(input, string_types):
        lines = input.split('\n')
    else:
        lines = input

    start = None
    productions = []
    continue_line = ''
    for linenum, line in enumerate(lines):
        line = continue_line + line.strip()
        if line.startswith('#') or line=='': continue
        if line.endswith('\\'):
            continue_line = line[:-1].rstrip()+' '
            continue
        continue_line = ''
        try:
            if line[0] == '%':
                directive, args = line[1:].split(None, 1)
                if directive == 'start':
                    start, pos = nonterm_parser(args, 0)
                    if pos != len(args):
                        raise ValueError('Bad argument to start directive')
                else:
                    raise ValueError('Bad directive')
            else:
                # expand out the disjunctions on the RHS
                productions += _read_production(line, nonterm_parser, probabilistic)
        except ValueError as e:
            raise ValueError('Unable to parse line %s: %s\n%s' %
                             (linenum+1, line, e))

    if not productions:
        raise ValueError('No productions found!')
    if not start:
        start = productions[0].lhs()
    return (start, productions)

def _read_production(line, nonterm_parser, probabilistic=False):
    """
    Parse a grammar rule, given as a string, and return
    a list of productions.
    """
    pos = 0

    # Parse the left-hand side.
    lhs, pos = nonterm_parser(line, pos)

    # Skip over the arrow.
    m = _ARROW_RE.match(line, pos)
    if not m: raise ValueError('Expected an arrow')
    pos = m.end()

    # Parse the right hand side.
    probabilities = [0.0]
    rhsides = [[]]
    while pos < len(line):
        # Probability.
        m = _PROBABILITY_RE.match(line, pos)
        if probabilistic and m:
            pos = m.end()
            probabilities[-1] = float(m.group(1)[1:-1])
            if probabilities[-1] > 1.0:
                raise ValueError('Production probability %f, '
                                 'should not be greater than 1.0' %
                                 (probabilities[-1],))

        # String -- add terminal.
        elif line[pos] in "\'\"":
            m = _TERMINAL_RE.match(line, pos)
            if not m: raise ValueError('Unterminated string')
            rhsides[-1].append(m.group(1)[1:-1])
            pos = m.end()

        # Vertical bar -- start new rhside.
        elif line[pos] == '|':
            m = _DISJUNCTION_RE.match(line, pos)
            probabilities.append(0.0)
            rhsides.append([])
            pos = m.end()

        # Anything else -- nonterminal.
        else:
            nonterm, pos = nonterm_parser(line, pos)
            rhsides[-1].append(nonterm)

    if probabilistic:
        return [ProbabilisticProduction(lhs, rhs, prob=probability)
                for (rhs, probability) in zip(rhsides, probabilities)]
    else:
        return [Production(lhs, rhs) for rhs in rhsides]

_STANDARD_NONTERM_RE = re.compile('( [\w/][\w/^<>-]* ) \s*', re.VERBOSE)

def standard_nonterm_parser(string, pos):
    m = _STANDARD_NONTERM_RE.match(string, pos)
    if not m: raise ValueError('Expected a nonterminal, found: '
                               + string[pos:])
    return (Nonterminal(m.group(1)), m.end())
class Nonterminal(object):
    """
    A non-terminal symbol for a context free grammar.  ``Nonterminal``
    is a wrapper class for node values; it is used by ``Production``
    objects to distinguish node values from leaf values.
    The node value that is wrapped by a ``Nonterminal`` is known as its
    "symbol".  Symbols are typically strings representing phrasal
    categories (such as ``"NP"`` or ``"VP"``).  However, more complex
    symbol types are sometimes used (e.g., for lexicalized grammars).
    Since symbols are node values, they must be immutable and
    hashable.  Two ``Nonterminals`` are considered equal if their
    symbols are equal.

    :see: ``CFG``, ``Production``
    :type _symbol: any
    :ivar _symbol: The node value corresponding to this
        ``Nonterminal``.  This value must be immutable and hashable.
    """
    def __init__(self, symbol):
        """
        Construct a new non-terminal from the given symbol.

        :type symbol: any
        :param symbol: The node value corresponding to this
            ``Nonterminal``.  This value must be immutable and
            hashable.
        """
        self._symbol = symbol
        self._hash = hash(symbol)
class Production(object):
    """
    A grammar production.  Each production maps a single symbol
    on the "left-hand side" to a sequence of symbols on the
    "right-hand side".  (In the case of context-free productions,
    the left-hand side must be a ``Nonterminal``, and the right-hand
    side is a sequence of terminals and ``Nonterminals``.)
    "terminals" can be any immutable hashable object that is
    not a ``Nonterminal``.  Typically, terminals are strings
    representing words, such as ``"dog"`` or ``"under"``.

    :see: ``CFG``
    :see: ``DependencyGrammar``
    :see: ``Nonterminal``
    :type _lhs: Nonterminal
    :ivar _lhs: The left-hand side of the production.
    :type _rhs: tuple(Nonterminal, terminal)
    :ivar _rhs: The right-hand side of the production.
    """

    def __init__(self, lhs, rhs):
        """
        Construct a new ``Production``.

        :param lhs: The left-hand side of the new ``Production``.
        :type lhs: Nonterminal
        :param rhs: The right-hand side of the new ``Production``.
        :type rhs: sequence(Nonterminal and terminal)
        """
        if isinstance(rhs, string_types):
            raise TypeError('production right hand side should be a list, '
                            'not a string')
        self._lhs = lhs
        self._rhs = tuple(rhs)
        self._hash = hash((self._lhs, self._rhs))


    def lhs(self):
        """
        Return the left-hand side of this ``Production``.

        :rtype: Nonterminal
        """
        return self._lhs


    def rhs(self):
        """
        Return the right-hand side of this ``Production``.

        :rtype: sequence(Nonterminal and terminal)
        """
        return self._rhs

    def __len__(self):
        """
        Return the length of the right-hand side.

        :rtype: int
        """
        return len(self._rhs)


    def is_nonlexical(self):
        """
        Return True if the right-hand side only contains ``Nonterminals``

        :rtype: bool
        """
        return all(is_nonterminal(n) for n in self._rhs)


    def is_lexical(self):
        """
        Return True if the right-hand contain at least one terminal token.

        :rtype: bool
        """
        return not self.is_nonlexical()

    def __str__(self):
        """
        Return a verbose string representation of the ``Production``.

        :rtype: str
        """
        result = '%s -> ' % unicode_repr(self._lhs)
        result += " ".join(unicode_repr(el) for el in self._rhs)
        return result

    def __repr__(self):
        """
        Return a concise string representation of the ``Production``.

        :rtype: str
        """
        return '%s' % self

    def __eq__(self, other):
        """
        Return True if this ``Production`` is equal to ``other``.

        :rtype: bool
        """
        return (type(self) == type(other) and
                self._lhs == other._lhs and
                self._rhs == other._rhs)

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if not isinstance(other, Production):
            raise_unorderable_types("<", self, other)
        return (self._lhs, self._rhs) < (other._lhs, other._rhs)

    def __hash__(self):
        """
        Return a hash value for the ``Production``.

        :rtype: int
        """
        return self._hash
class CFG(object):
    """
    A context-free grammar.  A grammar consists of a start state and
    a set of productions.  The set of terminals and nonterminals is
    implicitly specified by the productions.

    If you need efficient key-based access to productions, you
    can use a subclass to implement it.
    """
    def __init__(self, start, productions, calculate_leftcorners=True):
        """
        Create a new context-free grammar, from the given start state
        and set of ``Production``s.

        :param start: The start symbol
        :type start: Nonterminal
        :param productions: The list of productions that defines the grammar
        :type productions: list(Production)
        :param calculate_leftcorners: False if we don't want to calculate the
            leftcorner relation. In that case, some optimized chart parsers won't work.
        :type calculate_leftcorners: bool
        """
        if not is_nonterminal(start):
            raise TypeError("start should be a Nonterminal object,"
                            " not a %s" % type(start).__name__)

        self._start = start
        self._productions = productions
        self._categories = set(prod.lhs() for prod in productions)
        self._calculate_indexes()
        self._calculate_grammar_forms()
        if calculate_leftcorners:
            self._calculate_leftcorners()

    def _calculate_indexes(self):
        self._lhs_index = {}
        self._rhs_index = {}
        self._empty_index = {}
        self._lexical_index = {}
        for prod in self._productions:
            # Left hand side.
            lhs = prod._lhs
            if lhs not in self._lhs_index:
                self._lhs_index[lhs] = []
            self._lhs_index[lhs].append(prod)
            if prod._rhs:
                # First item in right hand side.
                rhs0 = prod._rhs[0]
                if rhs0 not in self._rhs_index:
                    self._rhs_index[rhs0] = []
                self._rhs_index[rhs0].append(prod)
            else:
                # The right hand side is empty.
                self._empty_index[prod.lhs()] = prod
            # Lexical tokens in the right hand side.
            for token in prod._rhs:
                if is_terminal(token):
                    self._lexical_index.setdefault(token, set()).add(prod)

    def _calculate_leftcorners(self):
        # Calculate leftcorner relations, for use in optimized parsing.
        self._immediate_leftcorner_categories = dict((cat, set([cat])) for cat in self._categories)
        self._immediate_leftcorner_words = dict((cat, set()) for cat in self._categories)
        for prod in self.productions():
            if len(prod) > 0:
                cat, left = prod.lhs(), prod.rhs()[0]
                if is_nonterminal(left):
                    self._immediate_leftcorner_categories[cat].add(left)
                else:
                    self._immediate_leftcorner_words[cat].add(left)

        lc = transitive_closure(self._immediate_leftcorner_categories, reflexive=True)
        self._leftcorners = lc
        self._leftcorner_parents = invert_graph(lc)

        nr_leftcorner_categories = sum(map(len, self._immediate_leftcorner_categories.values()))
        nr_leftcorner_words = sum(map(len, self._immediate_leftcorner_words.values()))
        if nr_leftcorner_words > nr_leftcorner_categories > 10000:
            # If the grammar is big, the leftcorner-word dictionary will be too large.
            # In that case it is better to calculate the relation on demand.
            self._leftcorner_words = None
            return

        self._leftcorner_words = {}
        for cat in self._leftcorners:
            lefts = self._leftcorners[cat]
            lc = self._leftcorner_words[cat] = set()
            for left in lefts:
                lc.update(self._immediate_leftcorner_words.get(left, set()))

    @classmethod

    def fromstring(cls, input, encoding=None):
        """
        Return the ``CFG`` corresponding to the input string(s).

        :param input: a grammar, either in the form of a string or as a list of strings.
        """
        start, productions = read_grammar(input, standard_nonterm_parser,
                                          encoding=encoding)
        return CFG(start, productions)


    def start(self):
        """
        Return the start symbol of the grammar

        :rtype: Nonterminal
        """
        return self._start

    # tricky to balance readability and efficiency here!
    # can't use set operations as they don't preserve ordering


    def productions(self, lhs=None, rhs=None, empty=False):
        """
        Return the grammar productions, filtered by the left-hand side
        or the first item in the right-hand side.

        :param lhs: Only return productions with the given left-hand side.
        :param rhs: Only return productions with the given first item
            in the right-hand side.
        :param empty: Only return productions with an empty right-hand side.
        :return: A list of productions matching the given constraints.
        :rtype: list(Production)
        """
        if rhs and empty:
            raise ValueError("You cannot select empty and non-empty "
                             "productions at the same time.")

        # no constraints so return everything
        if not lhs and not rhs:
            if not empty:
                return self._productions
            else:
                return self._empty_index.values()

        # only lhs specified so look up its index
        elif lhs and not rhs:
            if not empty:
                return self._lhs_index.get(lhs, [])
            elif lhs in self._empty_index:
                return [self._empty_index[lhs]]
            else:
                return []

        # only rhs specified so look up its index
        elif rhs and not lhs:
            return self._rhs_index.get(rhs, [])

        # intersect
        else:
            return [prod for prod in self._lhs_index.get(lhs, [])
                    if prod in self._rhs_index.get(rhs, [])]


    def leftcorners(self, cat):
        """
        Return the set of all nonterminals that the given nonterminal
        can start with, including itself.

        This is the reflexive, transitive closure of the immediate
        leftcorner relation:  (A > B)  iff  (A -> B beta)

        :param cat: the parent of the leftcorners
        :type cat: Nonterminal
        :return: the set of all leftcorners
        :rtype: set(Nonterminal)
        """
        return self._leftcorners.get(cat, set([cat]))


    def is_leftcorner(self, cat, left):
        """
        True if left is a leftcorner of cat, where left can be a
        terminal or a nonterminal.

        :param cat: the parent of the leftcorner
        :type cat: Nonterminal
        :param left: the suggested leftcorner
        :type left: Terminal or Nonterminal
        :rtype: bool
        """
        if is_nonterminal(left):
            return left in self.leftcorners(cat)
        elif self._leftcorner_words:
            return left in self._leftcorner_words.get(cat, set())
        else:
            return any(left in self._immediate_leftcorner_words.get(parent, set())
                       for parent in self.leftcorners(cat))


    def leftcorner_parents(self, cat):
        """
        Return the set of all nonterminals for which the given category
        is a left corner. This is the inverse of the leftcorner relation.

        :param cat: the suggested leftcorner
        :type cat: Nonterminal
        :return: the set of all parents to the leftcorner
        :rtype: set(Nonterminal)
        """
        return self._leftcorner_parents.get(cat, set([cat]))


    def check_coverage(self, tokens):
        """
        Check whether the grammar rules cover the given list of tokens.
        If not, then raise an exception.

        :type tokens: list(str)
        """
        missing = [tok for tok in tokens
                   if not self._lexical_index.get(tok)]
        if missing:
            missing = ', '.join('%r' % (w,) for w in missing)
            raise ValueError("Grammar does not cover some of the "
                             "input words: %r." % missing)

    def _calculate_grammar_forms(self):
        """
        Pre-calculate of which form(s) the grammar is.
        """
        prods = self._productions
        self._is_lexical = all(p.is_lexical() for p in prods)
        self._is_nonlexical = all(p.is_nonlexical() for p in prods
                                  if len(p) != 1)
        self._min_len = min(len(p) for p in prods)
        self._max_len = max(len(p) for p in prods)
        self._all_unary_are_lexical = all(p.is_lexical() for p in prods
                                          if len(p) == 1)


    def is_lexical(self):
        """
        Return True if all productions are lexicalised.
        """
        return self._is_lexical


    def is_nonlexical(self):
        """
        Return True if all lexical rules are "preterminals", that is,
        unary rules which can be separated in a preprocessing step.

        This means that all productions are of the forms
        A -> B1 ... Bn (n>=0), or A -> "s".

        Note: is_lexical() and is_nonlexical() are not opposites.
        There are grammars which are neither, and grammars which are both.
        """
        return self._is_nonlexical


    def min_len(self):
        """
        Return the right-hand side length of the shortest grammar production.
        """
        return self._min_len


    def max_len(self):
        """
        Return the right-hand side length of the longest grammar production.
        """
        return self._max_len


    def is_nonempty(self):
        """
        Return True if there are no empty productions.
        """
        return self._min_len > 0


    def is_binarised(self):
        """
        Return True if all productions are at most binary.
        Note that there can still be empty and unary productions.
        """
        return self._max_len <= 2


    def is_flexible_chomsky_normal_form(self):
        """
        Return True if all productions are of the forms
        A -> B C, A -> B, or A -> "s".
        """
        return self.is_nonempty() and self.is_nonlexical() and self.is_binarised()


    def is_chomsky_normal_form(self):
        """
        Return True if the grammar is of Chomsky Normal Form, i.e. all productions
        are of the form A -> B C, or A -> "s".
        """
        return (self.is_flexible_chomsky_normal_form() and
                self._all_unary_are_lexical)

    def __repr__(self):
        return '<Grammar with %d productions>' % len(self._productions)

    def __str__(self):
        result = 'Grammar with %d productions' % len(self._productions)
        result += ' (start state = %r)' % self._start
        for production in self._productions:
            result += '\n    %s' % production
        return result
def is_nonterminal(item):
    """
    :return: True if the item is a ``Nonterminal``.
    :rtype: bool
    """
    return isinstance(item, Nonterminal)
def is_terminal(item):
    """
    Return True if the item is a terminal, which currently is
    if it is hashable and not a ``Nonterminal``.

    :rtype: bool
    """
    return hasattr(item, '__hash__') and not isinstance(item, Nonterminal)


class ChartParser(ParserI):
    
    class LeafInitRule(AbstractChartRule):
        NUM_EDGES=0

        def apply(self, chart, grammar):
            for index in range(chart.num_leaves()):
                new_edge = LeafEdge(chart.leaf(index), index)
                if chart.insert(new_edge, ()):
                    yield new_edge
                    
    BU_LC_STRATEGY = [LeafInitRule(),
                  EmptyPredictRule(),
                  BottomUpPredictCombineRule(),
                  SingleEdgeFundamentalRule()]
    """
    A generic chart parser.  A "strategy", or list of
    ``ChartRuleI`` instances, is used to decide what edges to add to
    the chart.  In particular, ``ChartParser`` uses the following
    algorithm to parse texts:

    | Until no new edges are added:
    |   For each *rule* in *strategy*:
    |     Apply *rule* to any applicable edges in the chart.
    | Return any complete parses in the chart
    """
    def __init__(self, grammar, strategy=BU_LC_STRATEGY, trace=0,
                 trace_chart_width=50, use_agenda=True, chart_class=Chart):
        """
        Create a new chart parser, that uses ``grammar`` to parse
        texts.

        :type grammar: CFG
        :param grammar: The grammar used to parse texts.
        :type strategy: list(ChartRuleI)
        :param strategy: A list of rules that should be used to decide
            what edges to add to the chart (top-down strategy by default).
        :type trace: int
        :param trace: The level of tracing that should be used when
            parsing a text.  ``0`` will generate no tracing output;
            and higher numbers will produce more verbose tracing
            output.
        :type trace_chart_width: int
        :param trace_chart_width: The default total width reserved for
            the chart in trace output.  The remainder of each line will
            be used to display edges.
        :type use_agenda: bool
        :param use_agenda: Use an optimized agenda-based algorithm,
            if possible.
        :param chart_class: The class that should be used to create
            the parse charts.
        """
        self._grammar = grammar
        self._strategy = strategy
        self._trace = trace
        self._trace_chart_width = trace_chart_width
        # If the strategy only consists of axioms (NUM_EDGES==0) and
        # inference rules (NUM_EDGES==1), we can use an agenda-based algorithm:
        self._use_agenda = use_agenda
        self._chart_class = chart_class

        self._axioms = []
        self._inference_rules = []
        for rule in strategy:
            if rule.NUM_EDGES == 0:
                self._axioms.append(rule)
            elif rule.NUM_EDGES == 1:
                self._inference_rules.append(rule)
            else:
                self._use_agenda = False

    def grammar(self):
        return self._grammar

    def _trace_new_edges(self, chart, rule, new_edges, trace, edge_width):
        if not trace: return
        print_rule_header = trace > 1
        for edge in new_edges:
            if print_rule_header:
                print('%s:' % rule)
                print_rule_header = False
            print(chart.pretty_format_edge(edge, edge_width))

    def chart_parse(self, tokens, trace=None):
        """
        Return the final parse ``Chart`` from which all possible
        parse trees can be extracted.

        :param tokens: The sentence to be parsed
        :type tokens: list(str)
        :rtype: Chart
        """
        if trace is None: trace = self._trace
        trace_new_edges = self._trace_new_edges

        tokens = list(tokens)
        self._grammar.check_coverage(tokens)
        chart = self._chart_class(tokens)
        grammar = self._grammar

        # Width, for printing trace edges.
        trace_edge_width = self._trace_chart_width // (chart.num_leaves() + 1)
        if trace: print(chart.pretty_format_leaves(trace_edge_width))
        
        if self._use_agenda:
            # Use an agenda-based algorithm.
            for axiom in self._axioms:
                new_edges = list(axiom.apply(chart, grammar))
                trace_new_edges(chart, axiom, new_edges, trace, trace_edge_width)

            inference_rules = self._inference_rules
            agenda = chart.edges()
            # We reverse the initial agenda, since it is a stack
            # but chart.edges() functions as a queue.
            agenda.reverse()
            while agenda:
                edge = agenda.pop()
                for rule in inference_rules:
                    new_edges = list(rule.apply(chart, grammar, edge))
                    if trace:
                        trace_new_edges(chart, rule, new_edges, trace, trace_edge_width)
                    agenda += new_edges

        else:
            # Do not use an agenda-based algorithm.
            edges_added = True
            while edges_added:
                edges_added = False
                for rule in self._strategy:
                    new_edges = list(rule.apply_everywhere(chart, grammar))
                    edges_added = len(new_edges)
                    trace_new_edges(chart, rule, new_edges, trace, trace_edge_width)

        # Return the final chart.
        return chart

    def parse(self, tokens, tree_class=Tree):
        chart = self.chart_parse(tokens)
        return iter(chart.parses(self._grammar.start(), tree_class=tree_class))



main()