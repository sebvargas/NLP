#CPSC475 Dr.DePalma Fall 2016 asgn6
#Probabilistic Part of Speech Tagger
#Sebastian Vargas
#id: avargas
#
#To run on linux, go to your terminal then go to the directory in which
# this program is stored. Then type "python asgn6.py" in the command line
#This should execute the program

import random
#from random import *
import nltk
import numpy as np
#import pydecode
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame
from nltk.corpus import brown
from collections import Counter


def main():
    #length of the brown corpus is 1161192
    brown_tag = nltk.corpus.brown.tagged_words()
    brown_tag_new = [(tup[0].encode('ascii'),tup[1].encode('ascii')) for tup in brown_tag]    
    brown_train = brown_tag_new
    brown_test = []
    make_brown_test(brown_test,brown_train,brown_tag_new)
    
    #print(brown_test)
    
    dictA = {}
    dictB = {}
    tagList = []
    transList = []
    transBigram = []
    countTransBigram = {}
    bigram = []
    countTags = {}
    matrixA = {}
    matrixB = {}

   
#   transBigram is a list of tuples of adjacent
#   tags.
#   Example:
#   ("I", PP) ("want", VB) would form an element (PP,VB)
#   in transBigram
    makeTagList(brown_tag_new, tagList)
    makeTransList(brown_train, transList)
    transBigram = find_ngrams(transList, 2)
    countTransBigram = countAllBigrams(transBigram)
    countTags = countAllBigrams(brown_train)
    makeMatrixA(countTransBigram, dictA, matrixA)
    makeMatrixB(countTags,dictB, matrixB)

                                
    #print(len(matrixA))
    #print(len(matrixB))
    #print(len(tagList))
    #T = pd.DataFrame(matrixA).fillna(0)
    #E = pd.DataFrame(matrixB).fillna(0)
    #print(T)
    #print(E)
#    for item in matrixA:
#        for x in matrixA[item]:
#            print(matrixA[item][x])
#        break;
    #read_dictionary = np.load('dictA.npy')
    #print(read_dictionary)

#####################################################
#   co
#
#
#
class HMM:
    def _init_(self,a,b):
        self.a

###################################################
# make_brown_test(brown_test,brown_train,brown_tag_new)
#   takes 10% of the brown corpus and puts it into
#   brown_test and the remaining 90% goes to brown_train.
#   all the parameters must be iterable lists.
def make_brown_test(brown_test,brown_train,brown_tag_new):
    counter = len(brown_tag_new)
    limit = counter/10 #10% of the corpus. modify 10 to change percentage
    #print("limit is: " + str(limit))
    while limit > 0:
        random_item = random.randint(1,counter-1)
        #print("item removed is: " + str(brown_tag_new[random_item]))
        #print("at position: " + str(random_item))
        brown_test.append(brown_tag_new[random_item])
        del brown_train[random_item]
        counter = counter - 1
        limit = limit - 1
        
##################################################
# makeTagList(brown_tag_new, tagList)
#   makes a list of all tags
def makeTagList(brown_tag_new, tagList):
    for item in brown_tag_new:
        if not (item[1] in tagList):
            tagList.append(item[1])

        
###################################################
# makeMatrixA(countTransBigram, dictA, matrixA)
#   Transition probability matrix 
#   makes the matrix A of the Hidden Markov Model
#   where it takes a dictionary countTransBigram and stores it
#   into a dictionary dictA where the key is
#   a POS tag and the value is a dictionary of
#   probabilities of following states
#   countTransBigram is a dictionary of tuples of adjacent
#   tags with the values being their frequencies
#   Example:
#   ("I", PP) ("want", VB) would form a key (PP,VB)
#   in countTransBigram
def makeMatrixA(countTransBigram, dictA, matrixA):
    totalDict = {} #dictionary containing frequencies
    rowDict = {} #placeholder dictionary for the rows of the matrix
    for item in countTransBigram:
        if not item[0] in totalDict:
            totalDict[item[0]] = countTransBigram[item]
        else:
            totalDict[item[0]] += countTransBigram[item]
    for item in countTransBigram:
        dictA[item] = (countTransBigram[item] / (1.0*(totalDict[item[0]])))
    for item in countTransBigram:
        if not item[0] in matrixA:
            rowDict[item[1]] = dictA[item]
            matrixA[item[0]] = rowDict
        elif not item[1] in matrixA[item[0]]:
            rowDict = matrixA[item[0]]
            rowDict[item[1]] = dictA[item]
            matrixA[item[0]] = rowDict
        rowDict = {}
    
    excelA = pd.DataFrame(matrixA).fillna(0)
    writer = pd.ExcelWriter('matrixA.xlsx', engine='xlsxwriter')
    excelA.to_excel(writer, sheet_name='Matrix A')
    writer.save()
    #print(excelA)
    
###################################################
# makeMatrixB(countTags,dictB, matrixB)
#   Emission probability matrix 
#   makes the matrix B of the Hidden Markov Model
#   where it takes a dictionary countTags and stores it
#   into a dictionary matrixB where the keys are the words tags
#   and the values are dictionaries where keys are tags and
#   values are probabilities
def makeMatrixB(countTags,dictB, matrixB):
    totalDict = {} #dictionary containing frequencies
    rowDict = {}
    for item in countTags:
        if not item[0] in totalDict:
            totalDict[item[0]] = countTags[item]
        else:
            totalDict[item[0]] += countTags[item]
    for item in countTags:
        dictB[item] = (countTags[item]/(1.0*(totalDict[item[0]])))
    for item in countTags:
        if not item[0] in matrixB:
            rowDict[item[1]] = dictB[item]
            matrixB[item[0]] = rowDict
            
        if not item[1] in matrixB[item[0]]:
            rowDict = matrixB[item[0]]
            rowDict[item[1]] = dictB[item]
            matrixB[item[0]] = rowDict
        rowDict = {}
    excelB = pd.DataFrame(matrixB).fillna(0)
    writer = pd.ExcelWriter('matrixB.xlsx', engine='xlsxwriter')
    excelB.to_excel(writer, sheet_name='Matrix B')
    writer.save()
    #print(excelB)
    

###################################################
# makeTransList(brownList)
#   Takes the transition state (part-of-speech tag)
#   from a tuple and stores it into an ordered list
def makeTransList(brownList,transList):
    length = len(brownList)
    for i in range(length):
        transList.append(brownList[i][1])
        
####################################################    
# makeTransSet(brown_tag_new, transSet)
#   gets all the tags from the brown corpus
def makeTransSet(brown_tag_new, transSet):
    length = len(brown_tag_new)
    for i in range(length):
        transSet.add(brown_tag_new[i][1])

####################################################    
# makeTransBigram(brown_tag_new, transList)
#   gets all the 87 tags from the brown corpus
def makeTransBigram(transList, transBigram):
     transBigram = find_ngrams(transList, 2)
     countTransBigram = countAllBigrams(transBigram)
     print(countTransBigram)


################################
# counts the number of bigrams
#
def countAllBigrams(bigramArray):
    return Counter(bigramArray)


##########################
# prints a list as sentence,
# replacing </s> with periods and removing <s>
#
def printSentences(string):
    
    string = [x for x in string if x != "<s>"]
    string = ["." if x=="</s>" else x for x in string]
    print(' '.join(string))

    
########################################
# creates a list of n-grams
#
def find_ngrams(input_list, n):
    return zip(*[input_list[i:] for i in range(n)])
    
main()
