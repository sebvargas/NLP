#CPSC475 Dr.DePalma Fall 2016 asgn4
#Finite State Transducer of Soundex
#Sebastian Vargas
#id: avargas
#
#To run on linux, go to your terminal then go to the directory in which
# this program is stored. Then type "python asgn4.py" in the command line
#This should execute the program


#########################
# State Manager
#
#
def StateManager(initialString):
    i = 1
    print(firstLetter(initialString))
    length = len(initialString)
    stateCounter = 0
    pos = 1
    while pos < length:
        if transition(initialString[pos]) == stateCounter:
            stateCounter = 0
        else:
            stateCounter = transition(initialString[pos])
        if stateCounter != 0:
            print(stateCounter)

        #transition(stateCounter)
        pos = pos + 1
        
    
############################
# State Transition
#
#
def transition(char):
    x = 0;
    if char in 'aeiouwyAEIOUWY':
        x = 0
    elif char in 'bfpvBFPV':
        x = 1
    elif char in 'cgjkqsxzCGJKQSXZ':
        x = 2
    elif char in 'dtDT':
        x = 3
    elif char in 'lL':
        x = 4
    elif char in 'mnMN':
        x = 5
    elif char in 'rR':
        x = 6
    return x
    

#############################
# removeVowels
#
#
def removeVowels(char):
    return 0

#############################
# replaceLetters
#
#
#############################
# Transiton 0
#
#
def firstLetter(initialString):
    return initialString[0]

#############################
# State 1
#
# 
def initialize():
    initialString = ""
    initialString = raw_input("Type in name to implement Soundex: \n")
    
    
    return





##################
# State Transducer
# 
# This function basically manages the transitions between the states

def StateTransducer(initialString):

    dupString = list(initialString)
    bannedLetters = "aeiouwyAEIOUWY"
    numberedLetters = "bfpvcgjkqsxzdtlmnrBFPVCGJKQSXZDTLMNR"
    SoundexString = []
    #Keeps the first letter of the name
    Transducer1(dupString, SoundexString)

    nameLength = len(initialString)
    pos = 1
    
    while pos < nameLength:
        if initialString[pos] in bannedLetters:
            Transducer2(pos, dupString)
        elif initialString[pos] in numberedLetters:
            Transducer3(pos, dupString)
        pos = pos + 1
        
    Transducer4(dupString) 
    Transducer5(dupString)
    
    print("Output: " + "".join(dupString))

    
#################
# Transducer1
# keeps the first letter of the name
def Transducer1(initialString, dupString):

    dupString.append(initialString[0])
    
###############################  
# Transducer2
# removes all letters that are a e i o u w y
def Transducer2(pos, dupString):
    
    dupString[pos] = ""

###############################    
# Transducer3
# replaces b,f,p,v with 1
# c, g, j, k, q, s, x, z with 2
# d, t with 3
# l with 4
# m, n with 5
# r with  6
# and avoids duplicates

def Transducer3(pos, dupString):

    seq1 = "bfpvBFPV"
    seq2 = "cgjkqsxzCGJKQSXZ"
    seq3 = "dtDT"
    seq4 = "lL"
    seq5 = "mnMN"
    seq6 = "rR"

    j = 1
    while dupString[pos - j] == "":
        j = j + 1

    if dupString[pos] in seq1:
        if dupString[pos - j] != "1":
            dupString[pos] = "1"
        else:
            dupString[pos] = ""
            
    elif dupString[pos] in seq2:
        if dupString[pos - j] != "2":
            dupString[pos] = "2"
        else:
            dupString[pos] = ""

            
    elif dupString[pos] in seq3:
        if dupString[pos - j] != "3":
            dupString[pos] = "3"
        else:
            dupString[pos] = ""

    elif dupString[pos] in seq4:
        if dupString[pos - j] != "4":
            dupString[pos] = "4"
        else:
            dupString[pos] = ""

        
    elif dupString[pos] in seq5:
        if dupString[pos - j] != "5":
            dupString[pos] = "5"
        else:
            dupString[pos] = ""


    elif dupString[pos] in seq6:
        if dupString[pos - j] != "6":
            dupString[pos] = "6"
        else:
            dupString[pos] = ""

###############################    
# Transducer4
# Add zeroes to the end of the string if necessary
# or slice the string if necessary
#

def Transducer4(dupString):
    
    length = len("".join(dupString))
    #print(length)
    if length > 4:
        for i in range(4, length):
            dupString[i] = ""

def Transducer5(dupString):
    length = len("".join(dupString))
    if length < 4:
        for i in range(length, 5):
            if dupString[i] == "":
                 dupString[i] = "0"
    
def main():
 #   initialString = ""
 #   modeString = ""
 #   while(1):
 #       initialString = raw_input("Type 'quit' to close the program  or \n"
 #                                 "Type in name to implement Soundex: \n")
 #       if initialString == "quit":
 #           break
 #       
 #       StateTransducer(initialString)
 #   return
 
    print(StateManager(raw_input("input a number \n")))
    return
main()

