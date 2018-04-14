#CPSC475 Dr. DePalma Fall 2016 asgn2
#Zipf Test
#Sebastian Vargas id: avargas

#Import libraries
import matplotlib.pyplot as plt
import math
import os.path
import re

#Initializing
wordsList = []
frequencyList = []
sortedWordsList = []
sortedFrequencyList = []
textString = ""
wordsListAll = []
textDictionary = {}
sortedValues = []


#File Validity and Existence
if(os.path.exists('austen-sense.txt')):
    book = open('austen-sense.txt')
    textString = book.read()
    book.close()
else:
    print('The file cannot be found')


#4.Normalize text
def normalize():
    global textString
    global wordsListAll
    wordsListAll = re.split('\W+', textString) 
    print("Normalized text")
    return

#5.Dictionary Creation
def createDictionary():
    global wordsListAll
    global textDictionary
    global wordsList
    global frequencyList

    #loop stores words in dictionary
    for i in range(0,len(wordsListAll)):
        word = wordsListAll[i]
        if word not in textDictionary:
            textDictionary[word] = 1
        else:
            textDictionary[word] += 1

    #puts the words into a list
    wordsList = textDictionary.keys()
    #frequency of list
    frequencyList = textDictionary.values() 
    print("Dictionary compiled")
    return

#5(cont). Sort the list
def SortLists():
    
    global wordsList
    global frequencyList
    global sortedWordsList
    global sortedFrequencyList

    #Frequency sorted in descending order
    for i in range(0,len(wordsList)):
        index = 0
        x = 0
        for j in range(0,len(wordsList)):
            y = frequencyList[j]
            if (y > x):
                x = y
                index = j
        #adds to the list
        sortedFrequencyList.append(frequencyList.pop(index))
        sortedWordsList.append(wordsList.pop(index))
    print("Words and frequencies have been sorted")
    return


#Table with rank, frequency of word that occurs
def createFrequencyTable(): #Number 5 Step 3
    #Declarations
    global sortedKeys
    global textDictionary
    global reversedDictionary
    global sortedWordsList
    global sortedFrequencyList

    #Display rank, word on the list and number of times it occurs.
    for i in range(0,len(sortedWordsList)):
        print(str(i+1) + ": '" + sortedWordsList[i] + "' appeared " + str(sortedFrequencyList[i]) + " time(s)")
    print("Done")
    return

#6. Sample plot Zipf's law 
def ZipfsLaw():

    # Plots each point based on Zipf's distribution with the number of points being equivalent to the number in our
    #text file
    for i in range(0,len(sortedFrequencyList)):
        plt.plot([math.log(1.0/(i+1))],[math.log(i+1.0)],'ro')
    plt.show()
    print("Example Graph")
    return

#7. Plot log(freq) vs. log(rank) to check if Zipf's law applies
def EmmaZipfPlot():
    global sortedFrequencyList
    for i in range(0,len(sortedFrequencyList)):
        plt.plot([math.log(sortedFrequencyList[i])],[math.log(i+1.0)],'ro')
    plt.show()
    print("Emma Plot")
    return



def main():
    print("Zipfian Plot Tester")
    raw_input("4.press enter to normalize the text")
    normalize()
    print("")
    raw_input("5.press enter to compile a dictionary with word frequencies")
    createDictionary()
    print("")
    raw_input("5(cont).press enter to sort lists of words from the dictionary by frequency")
    SortLists()
    print("")
    raw_input("5(cont).press enter to create table of frequencies and words")
    createFrequencyTable()
    print("")
    raw_input("6.press enter to examine a graph of Zipf's Law. Close when done")
    ZipfsLaw()
    print("")
    raw_input("7.press enter to plot and check whether the text follows a the Zipfian distribution. close when done")
    EmmaZipfPlot()
    print("")
    raw_input("fin")
    return

main()
