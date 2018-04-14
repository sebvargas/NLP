#CPSC475 Dr.DePalma Fall 2016 asgn6_train
#Probabilistic Part of Speech Tagger
#Sebastian Vargas
#id: avargas
#
#To run on linux, go to your terminal then go to the directory in which
# this program is stored. Then type "python asgn6.py" in the command line
#This should execute the program

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
    #f = open('brown_train.txt','w')
    #simplejson.dump(brown_train,f)
    #f.close()

    #g = open('brown_test.txt','w')
    #simplejson.dump(brown_test,g)
    #g.close()
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

    wikiTrain =[("normal","Healthy"),("normal","Healthy"),
                ("normal","Healthy"),("normal","Healthy"),
                ("normal","Healthy"),("cold","Healthy"),
                ("cold","Healthy"),

                    
                
                ("cold","Healthy"),
                ("dizzy","Fever"),("dizzy","Healthy"),
                ("dizzy","Fever"),("dizzy","Healthy"),
                ("dizzy","Fever"),("dizzy","Healthy"),
                ("dizzy","Fever"),("dizzy","Healthy"),
                
                ("dizzy","Fever"),("dizzy","Fever"),
                ("cold","Fever"),("cold","Fever"),
                ("normal","Fever"),("cold","Fever"),
                ("normal","Fever"),
                ]
    
    wikiDictA = {}
    wikiDictB = {}
    #stateList = ["Healthy","Fever"]
    stateList = []
    wikiTransList = []
    wikiTransBigram = []
    wikiCountTransBigram = {}
    wikiBigram = []
    wikiCountTags = {}
    wikiMatrixA = {}
    wikiMatrixB = {}
    start = {}
#   transBigram is a list of tuples of adjacent
#   tags.
#   Example:
#   ("I", PP) ("want", VB) would form an element (PP,VB)
#   in transBigram
 #   makeTagList(wikiTrain, stateList)
#    c = open('tagList.txt','w')
#    simplejson.dump(brown_test,c)
#    c.close()
    makeTagList(wikiTrain, stateList)
    makeTransList(wikiTrain, wikiTransList)
    wikiTransBigram = find_ngrams(wikiTransList, 2)
    wikiCountTransBigram = countAllBigrams(wikiTransBigram)
    wikiCountTags = countAllBigrams(wikiTrain)
    makeMatrixA(wikiCountTransBigram, wikiDictA, wikiMatrixA,stateList)
    #print(MatrixA)
    makeMatrixB(wikiCountTags,wikiDictB, wikiMatrixB)
    #print(MatrixB)
    for item in stateList:
        start[item] = 1;
    observations = ['normal', 'cold', 'dizzy']
    viterbi(observations, stateList, start,  wikiMatrixA, wikiMatrixB)


    with open('stateList.json','w') as fp:
        json.dump(stateList, fp)
    fp.close()
    with open('start.json','w') as fp:
        json.dump(start, fp)
    fp.close()

    with open('matrixA.json','w') as fp:
        json.dump(wikiMatrixA, fp)
    fp.close()
    with open('matrixB.json','w') as fp:
        json.dump(wikiMatrixB, fp)
    fp.close()

"""
    makeTagList(brown_tag_new, tagList)
    #makeTransList(wikiTrain, wikiTransList)
    makeTransList(brown_train, transList)
    transBigram = find_ngrams(transList, 2)
    countTransBigram = countAllBigrams(transBigram)
    countTags = countAllBigrams(brown_train)
    makeMatrixA(countTransBigram, dictA, matrixA,tagList)
    print(matrixA)
    makeMatrixB(countTags,dictB, matrixB)
    print(matrixB)
    sentences = ["the","Fulton","County","Grand","Jury","said"]
    for item in tagList:
        start[item] = 1;

    viterbi(sentences, tagList, start,  matrixA, matrixB)
    with open('data.json','w') as fp:
        json.dump(matrixA, fp)
   
    with open('matrixB.json','w') as fp:
        json.dump(matrixB, fp)
     
"""



    
    #

###################################################
# make_brown_test(brown_test,brown_train,brown_tag_new)
#   takes 10% of the brown corpus and puts it into
#   brown_test and the remaining 90% goes to brown_train.
#   all the parameters must be iterable lists.
def make_brown_test(brown_test,brown_train,brown_tag_new):
    counter = len(brown_tag_new)
    limit = (3*counter)/10000 #10% of the corpus. modify 10 to change percentage
    #print("limit is: " + str(limit))
    setWords = limit/10
    #random_item = random.randint(1,counter-1)
    i = 0
    while setWords > 0:
        
        #print("item removed is: " + str(brown_tag_new[random_item]))
        #print("at position: " + str(random_item))
        brown_test.append(brown_tag_new[i])
        del brown_train[i]
        setWords = setWords - 1
        i += 1
        #limit = limit - 1
        
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
  #  excelA = pd.DataFrame(matrixA).fillna(0)
   # writer = pd.ExcelWriter('matrixA.xlsx', engine='xlsxwriter')
  #  excelA.to_excel(writer, sheet_name='Matrix A')
  #  writer.save()
"""
    for item in countTransBigram:
        if not item[0] in matrixA:
            rowDict[item[1]] = dictA[item]
            matrixA[item[0]] = rowDict
        elif not item[1] in matrixA[item[0]]:
            rowDict = matrixA[item[0]]
            rowDict[item[1]] = dictA[item]
            matrixA[item[0]] = rowDict
        rowDict = {}
"""
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

   # excelB = pd.DataFrame(matrixB).fillna(0)
   # writer = pd.ExcelWriter('matrixB.xlsx', engine='xlsxwriter')
    #excelB.to_excel(writer, sheet_name='Matrix B')
   # writer.save()
    #print(excelB)
    

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


def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    for st in states:

        V[0][st] = {"prob": start_p[st] * emit_p[st][obs[0]], "prev": None}

    # Run Viterbi when t > 0

    for t in range(1, len(obs)):

        V.append({})

        for st in states:

            max_tr_prob = max(V[t-1][prev_st]["prob"]*trans_p[prev_st][st] for prev_st in states)

            for prev_st in states:

                if V[t-1][prev_st]["prob"] * trans_p[prev_st][st] == max_tr_prob:

                    max_prob = max_tr_prob * emit_p[st][obs[t]]

                    V[t][st] = {"prob": max_prob, "prev": prev_st}

                    break

    for line in dptable(V):

        print line

    opt = []

    # The highest probability

    max_prob = max(value["prob"] for value in V[-1].values())

    previous = None

    # Get most probable state and its backtrack

    for st, data in V[-1].items():

        if data["prob"] == max_prob:

            opt.append(st)

            previous = st

            break

    # Follow the backtrack till the first observation

    for t in range(len(V) - 2, -1, -1):

        opt.insert(0, V[t + 1][previous]["prev"])

        previous = V[t + 1][previous]["prev"]


    print 'The steps of states are ' + ' '.join(opt) + ' with highest probability of %s' % max_prob


def dptable(V):

    # Print a table of steps from dictionary

    yield " ".join(("%12d" % i) for i in range(len(V)))

    for state in V[0]:

        yield "%.7s: " % state + " ".join("%.7s" % ("%f" % v[state]["prob"]) for v in V)




    



#viterbi(observations,states, start_probability, transition_probability, emission_probability)

#pi=np.expand_dims(np.array(A[0,:]),1)

main()

