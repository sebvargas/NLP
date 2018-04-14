#CPSC475 Dr.DePalma Fall 2016 asgn3
#Minimum Edit Distance
#Sebastian Vargas

#Import Libraries
import numpy

#Initializing
targetString = ""
sourceString = ""
sourceArray = ["#"]
targetArray = ["#"]
nestedArray = []
pathArray = []

def getStrings():
    "gets the two strings from the user"
    global targetString
    global sourceString
    targetString = raw_input("Input the target string \n")
    sourceString = raw_input("Input the source string \n")
    return

def minEditDistance(source, target):
    global targetString
    global sourceString
    global targetArray
    global sourceArray
    global pathArray
    
    #Array is made
    n = len(sourceString)
    m = len(targetString)
    for i in range(0, n):
        sourceArray.append(source[i])
    for i in range(0, m):
        targetArray.append(target[i])
        
    #Array is made of lists of lists
    for i in range(0,n+1):
        nestedArray.append([])
        for j in range(0,m+1):
            nestedArray[i].append([])
            
    #fill the first row and first column with the initial values
    for i in range(0,m+1):
        nestedArray[0][i] = i
    for i in range(0,n+1):
        nestedArray[i][0] = i
    
    #Recurrence relation
    for i in range(1,n+1):
        for j in range(1,m+1):
            nestedArray[i][j] = min(nestedArray[i-1][j] + delCost(sourceArray[i]),
                                   nestedArray[i-1][j-1] + subCost(sourceArray[i],targetArray[j]),
                                   nestedArray[i][j-1] + insCost(targetArray[j]))
       #     if (nestedArray[i][j] == nestedArray[i-1][j]):
       #         pathArray.append([i-1,j])
       #     elif (nestedArray[i][j] == nestedArray[i-1][j-1]):
       #         pathArray.append([i-1,j-1])
       #     elif (nestedArray[i][j] == nestedArray[i][j-1]):
       #         pathArray.append([i,j-1])
            
    print("Minimum Edit distance: " + str(nestedArray[m][n]))

    
    #nestedArray[0][0] = "pi"
    #print(nestedArray)
    #print(nestedArray[0][0])
    return

def computeAlignment():
    global nestedArray
    global pathArray
    global sourceString
    global targetString
    
    n = len(sourceString)
    m = len(targetString)
    loc = [n,m]
    pathArray.append(loc)
    i = n
    j = m
    pathVal = nestedArray[m][n]
    #while loc[0] != 0 and loc[1] !=0:
    while loc != [0,0]:
        pathVal = min(nestedArray[i-1][j],nestedArray[i-1][j-1],nestedArray[i][j-1])
        
        if (pathVal == nestedArray[i-1][j] and pathVal!= 0):
            loc = [i-1,j]
            pathArray.append(loc)
            i = i - 1
        elif (pathVal == nestedArray[i-1][j-1] and pathVal!= 0):
            loc = [i-1,j-1]
            pathArray.append(loc)
            i = i - 1
            j = j - 1
        elif (pathVal == nestedArray[i][j-1] and pathVal!= 0):
            loc = [i,j-1]
            pathArray.append(loc)
            j = j - 1
        print("loc: " + str(loc))
    return

def printArray(array):
    for i in range(0, len(sourceArray)):
        print(array[i])
    return

def delCost(letter):
    if (letter != ' '):
        return 1
    return 0
                                   
def insCost(letter):
    if (letter != ' '):
        return 1
    return 0
                                   
def subCost(srcLetter,tarLetter):
    if (srcLetter == tarLetter):
        return 0
    return 2

def backTracePrint():
    global pathArray
    global sourceArray
    global targetArray

    pathArray.reverse()
    
    for i in range(len(pathArray)-1, 0, -1):
        print("backTrace" + str(pathArray[i]))
        if (pathArray[i][0] < pathArray[i - 1][0] and pathArray[i][1] < pathArray[i - 1][1]):
            print("1")
        elif (pathArray[i][1] < pathArray[i - 1][1]):
            print("1")
        elif (pathArray[i][0] < pathArray[i - 1][0]):
            print("1")

def main():
    getStrings()
    minEditDistance(sourceString, targetString)
    printArray(nestedArray)
    computeAlignment()
    backTracePrint()
    print(pathArray)
    print(sourceArray)
    print(targetArray)
    return
main()

