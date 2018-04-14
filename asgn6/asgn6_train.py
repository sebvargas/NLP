#CPSC475 Dr.DePalma Fall 2016 asgn6_train
#Probabilistic Part of Speech Tagger
#Sebastian Vargas
#id: avargas
#
#To run on linux, go to your terminal then go to the directory in which
# this program is stored. Then type "python asgn6_train.py" in the command line
#This should execute the program to train the HMM

import csv
import sys
import random
import simplejson
import json
#from random import *
import nltk
import numpy as np
import pickle
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
   # print(brown_train)
    fp = open('test.txt', 'w')
    for t1 in brown_test:
        fp.write("\n".join(["%s %s" % (t1[0], t1[1])])+"\n")
    #test.write('\n'.join('%s %s' % x for x in brown_test))
    fp.close()
    
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
    start ={}
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
    makeMatrixA(countTransBigram, dictA, matrixA,tagList)
    #print(matrixA)
    makeMatrixB(countTags,dictB, matrixB)
    #print(matrixB)
    
    for item in tagList:
        start[item] = 1;

    ##
    #saves lists and matrices to files
    with open('stateList.json','w') as fp:
        json.dump(tagList, fp)
    fp.close()
    with open('start.json','w') as fp:
        json.dump(start, fp)
    fp.close()

    with open('matrixA.json','w') as fp:
        json.dump(matrixA, fp)
    fp.close()
    with open('matrixB.json','w') as fp:
        json.dump(matrixB, fp)
    fp.close()

###################################################
# make_brown_test(brown_test,brown_train,brown_tag_new)
#   takes 10% of the brown corpus and puts it into
#   brown_test and the remaining 90% goes to brown_train.
#   all the parameters must be iterable lists.

def make_brown_test(brown_test,brown_train,brown_tag_new):
    counter = len(brown_tag_new)
    random_item = random.randint(1,counter-100000)
    del brown_train[random_item:random_item+700000]

    rando2 = random.randint(1,len(brown_train)-30000)
    for i in range(30000):
        brown_test.append(brown_train[rando2 + i - 1])
    


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
def makeMatrixA(countTransBigram, dictA, matrixA, tagList):
    ####use logs for probabilities
    #### pg 188!
    totalDict = {} #dictionary containing frequencies
    rowDict = {} #placeholder dictionary for the rows of the matrix
    for item in countTransBigram:
        if not item[0] in totalDict:
            totalDict[item[0]] = countTransBigram[item]
        else:
            totalDict[item[0]] += countTransBigram[item]
    #print("totalDict: ")
    #print(totalDict)
    for item in countTransBigram:
        dictA[item] = (countTransBigram[item] / (1.0*(totalDict[item[0]])))
    #print("dictA: ")
    #print(dictA)
    
    #print("tagList: ")
    #print(tagList)


    for tag in tagList:
        for nextTag in tagList:
            if not (tag in matrixA):
                if not((tag,nextTag) in dictA):
                    rowDict[nextTag] = 0
                else:
                    rowDict[nextTag] = dictA[(tag,nextTag)]
                matrixA[tag] = rowDict
            elif not (nextTag in matrixA[tag]):
                rowDict = matrixA[tag]
                if not ((tag,nextTag) in dictA):
                    rowDict[nextTag] = 0
                else:
                    rowDict[nextTag] = dictA[(tag,nextTag)]
                matrixA[tag] = rowDict
            rowDict = {}

    
###################################################
# makeMatrixB(countTags,dictB, matrixB)
#   Emission probability matrix 
#   makes the matrix B of the Hidden Markov Model
#   where it takes a dictionary countTags and stores it
#   into a dictionary matrixB where the keys are the words tags
#   and the values are dictionaries where keys are tags and
#   values are probabilities
def makeMatrixB(countTags,dictB, matrixB):
    ####use logs for probabilities
    #### pg 188!
    totalDict = {} #dictionary containing frequencies
    rowDict = {}
    for item in countTags:
        if not item[1] in totalDict:
            totalDict[item[1]] = countTags[item]
        else:
            totalDict[item[1]] += countTags[item]
            
    for item in countTags:
        dictB[item] = (countTags[item]/(1.0*(totalDict[item[1]])))
    for item in countTags:
        if not (item[1] in matrixB):
            rowDict[item[0]] = dictB[item]
            matrixB[item[1]] = rowDict
            
        if not (item[0] in matrixB[item[1]]):
            rowDict = matrixB[item[1]]
            rowDict[item[0]] = dictB[item]
            matrixB[item[1]] = rowDict
        rowDict = {}
    

###################################################
# makeTransList(brownList)
#   Takes the transition state (part-of-speech tag)
#   from a tuple and stores it into an ordered list
def makeTransList(brownList,transList):
    length = len(brownList)
    for i in range(length):
        #if brownList[i][1] not in transList:
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
    
########################################
# creates a list of n-grams
#
def find_ngrams(input_list, n):
    return zip(*[input_list[i:] for i in range(n)])


main()

