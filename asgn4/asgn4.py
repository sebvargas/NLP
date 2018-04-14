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
# This iterates through the input string to feed the FST
# characters
# There are 4 'main' states for the 4 different output
# each of which has other states for the various
# character values they can have

def StateManager(initialString):
    i = 1
    print(firstLetter(initialString))
    length = len(initialString)
    stateCounter = 0
    pos = 1
    digitState = 1
    
    while digitState != 4:
        if pos < length:
            char = initialString[pos]
            if digitState == 1:
                
                digitState = digitState + firstDigit(char, stateCounter)
                pos = pos + 1
            elif digitState == 2:
                
                digitState = digitState + secondDigit(char, stateCounter)
                pos = pos + 1
            elif digitState == 3:
                
                digitState = digitState + thirdDigit(char, stateCounter)
                pos = pos + 1
        else:
              digitState = digitState + 1
            
           
############################
# First Digit
#
# This prints the first digit. Since I cannot keep track of previous
# digits, each digit is a state in the machine
def firstDigit(char, stateCounter):
        if transition(char) == stateCounter:
            stateCounter = 0
        else:
            stateCounter = transition(char)
        if stateCounter != 0:
            print(stateCounter)
            return 1
        return 0
    
############################
# Second Digit
#
# This prints the second digit. Since I cannot keep track of previous
# digits, each digit is a state in the machine
def secondDigit(char, stateCounter):
        if transition(char) == stateCounter:
            stateCounter = 0
        else:
            stateCounter = transition(char)
        if stateCounter != 0:
            print(stateCounter)
            return 1
        return 0
    
############################
# Third Digit
#
# This prints the third digit. Since I cannot keep track of previous
# digits, each digit is a state in the machine 
def thirdDigit(char, stateCounter):
        if transition(char) == stateCounter:
            stateCounter = 0
        else:
            stateCounter = transition(char)
        if stateCounter != 0:
            print(stateCounter)
            return 1
        return 0
    
############################
# State Transition
#
# Depending on the character, the machine can go to various states
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
# Transiton 0
#
# Prints the first letter
def firstLetter(initialString):
    return initialString[0]

def main():
    StateManager(raw_input("Type in a name: \n"))
    
main()

