########################################################
# CYK Parser, NLP Final Fall 2016
#   by Cody Valle, Jinous Esmaeili, Sebastian Vargas
#   ---------------------------------------------------
#   This program uses the CYK parser to check if a
#   string is defined in a grammar


#######################################################
#   LHSCheck(rules, setRules)
#       goes through each tuple in rules
#       and appends the left hand side of
#       of the rule to a set SetRules
#       This determines the non-terminals
def LHSCheck(rules, setRules):
    for rule in rules:
        setRules.append(rule[0])
    return set(setRules)

########################################################
#   RHSCheck(rules, LHSSet, RHSSet)
#       goes through each tuple in rules
#       and appends the right hand side of
#       of the rule to a set RHSSet which
#       determines the terminals
def RHSCheck(rules, LHSSet, RHSSet):
    for rule in rules:
        for tokens in rule[1]:
            if tokens not in LHSSet:
                RHSSet.append(tokens)
    return set(RHSSet)

#######################################################
#   getRules()
#       reads a text file and returns a list of tuples
#       where the first item is the rule before the ->
#       and the second is after.
def getRules():
    rules = []
    with open('grammar.txt', 'r') as f:
        for line in f:
            s = line.split('->')
            RHSs = s[1].strip().split('|')
            for r in RHSs:
                rules.append((s[0].strip(), r.strip().split()))
    return rules

#######################################################
#   getTokens()
#       reads a text file and returns the string
#       to be tested on as an array of words
def getTokens():
    # Parse the string
    tokens = []
    with open('string.txt', 'r') as f:
        for line in f:
            for word in line.split():
                tokens.append(word)
    return tokens

########################################################
#   CYKMatrix(tokens, rules)
#       creates the CYK matrix
def CYKMatrix(tokens, rules):
    # Create the matrix
    matrix = [[[] for _ in range(len(tokens))] for _ in range(len(tokens))]
    # Fill in the first diagonal
    for i in range(len(tokens)):
        word = tokens[i]
        cell = []
        for r in rules:
            if word in r[1]:
                cell.append(r[0])
        matrix[i][i] = cell

    # Fills in every other diagonal until the last    
    for j in range(1,len(tokens)):
        for i in range(j, len(tokens)):
            i2 = i - j
            first = []
            while i2 >= 0:
                if len(matrix[i-j][i2]) > 0:
                    first += matrix[i-j][i2]
                i2 -= 1
            second = matrix[i-j+1][i]
            cell = []
            for r in rules:
                if len(r[1]) > 1 and r[1][0] in first:
                    if r[1][1] in second:
                        cell.append(r[0])
            matrix[i-j][i] = cell
    return matrix

# Run the program
def main():
    from tabulate import tabulate
    rules = getRules()
    LHSSet = []
    RHSSet = []
    setRules = []
    LHSSet = LHSCheck(rules,setRules)
    RHSSet = RHSCheck(rules, LHSSet, RHSSet)
    tokens = getTokens()
    matrix = CYKMatrix(tokens, rules)
    
    print 'Yes' if 'S' in matrix[0][len(tokens)-1] else 'No'

    #print(tabulate(matrix)) #Uncomment this line to seethe matrix

if __name__ == '__main__':
    main()
