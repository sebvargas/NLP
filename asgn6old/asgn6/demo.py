def demo():
    """
    A demonstration of the probabilistic parsers.  The user is
    prompted to select which demo to run, and how many parses should
    be found; and then each parser is run on the same demo, and a
    summary of the results are displayed.
    """
    import sys, time
    from nltk import tokenize
    
    from nltk.grammar import toy_pcfg1, toy_pcfg2

    # Define two demos.  Each demo has a sentence and a grammar.
    demos = [('I saw the man with my telescope', toy_pcfg1),
             ('the boy saw Jack with Bob under the table with a telescope', toy_pcfg2)]

    # Ask the user which demo they want to use.
    print()
    for i in range(len(demos)):
        print('%3s: %s' % (i+1, demos[i][0]))
        print('     %r' % demos[i][1])
        print()
    print('Which demo (%d-%d)? ' % (1, len(demos)))
    try:
        snum = int(sys.stdin.readline().strip())-1
        sent, grammar = demos[snum]
    except:
        print('Bad sentence number')
        return

    # Tokenize the sentence.
    tokens = sent.split()

    parser = ViterbiParser(grammar)
    all_parses = {}

    print('\nsent: %s\nparser: %s\ngrammar: %s' % (sent,parser,grammar))
    parser.trace(3)
    t = time.time()
    parses = parser.parse_all(tokens)
    time = time.time()-t
    average = (reduce(lambda a,b:a+b.prob(), parses, 0)/len(parses)
               if parses else 0)
    num_parses = len(parses)
    for p in parses:
        all_parses[p.freeze()] = 1

    # Print some summary statistics
    print()
    print('Time (secs)   # Parses   Average P(parse)')
    print('-----------------------------------------')
    print('%11.4f%11d%19.14f' % (time, num_parses, average))
    parses = all_parses.keys()
    if parses:
        p = reduce(lambda a,b:a+b.prob(), parses, 0)/len(parses)
    else: p = 0
    print('------------------------------------------')
    print('%11s%11d%19.14f' % ('n/a', len(parses), p))

    # Ask the user if we should draw the parses.
    print()
    print('Draw parses (y/n)? ')
    if sys.stdin.readline().strip().lower().startswith('y'):
        from nltk.draw.tree import draw_trees
        print('  please wait...')
        draw_trees(*parses)

    # Ask the user if we should print the parses.
    print()
    print('Print parses (y/n)?')
    if sys.stdin.readline().strip().lower().startswith('y'):
        for parse in parses:
            print(parse)

if __name__ == '__main__':
    demo()
