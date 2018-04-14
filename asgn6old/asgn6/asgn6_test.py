#CPSC475 Dr.DePalma Fall 2016 asgn6_test
#Probabilistic Part of Speech Tagger
#Sebastian Vargas
#id: avargas
#
#To run on linux, go to your terminal then go to the directory in which
# this program is stored. Then type "python asgn6_test.py insert string here"
# in the command line
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

def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    for st in states:
        stprob = 0
        if(not (st in emit_p) or not(obs[0] in emit_p[st])):
            stprob = 0
        else:
            stprob = emit_p[st][obs[0]]
        V[0][st] = {"prob": start_p[st] * stprob, "prev": None}

    # Run Viterbi when t > 0

    for t in range(1, len(obs)):
        V.append({})
        for st in states:
            max_tr_prob = max(V[t-1][prev_st]["prob"]*trans_p[prev_st][st] for prev_st in states)
            for prev_st in states:
                if V[t-1][prev_st]["prob"] * trans_p[prev_st][st] == max_tr_prob:
                    mprob = 0
                    if(not(st in emit_p) or not(obs[t] in emit_p[st])):
                        mprob = 0
                    else:
                        mprob = emit_p[st][obs[t]]
                    max_prob = max_tr_prob * mprob
                    V[t][st] = {"prob": max_prob, "prev": prev_st}
                    break
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

    #print 'The steps of states are ' + ' '.join(opt) + ' with highest probability of %s' % max_prob
    optnew =  [word.encode('ascii') for word in opt]    
    tup = zip(optnew,obs)
    print(tup)
    


def main():
    argList = sys.argv
    observations = argList[1:]
    with open('stateList.json', 'r') as fp:
        stateList = json.load(fp)
    fp.close

    with open('start.json', 'r') as fp:
        start = json.load(fp)
    fp.close
    
    with open('matrixA.json', 'r') as fp:
        matrixA = json.load(fp)

    fp.close

    with open('matrixB.json', 'r') as fp:
        matrixB = json.load(fp)
        #print(matrixB)
    fp.close

    viterbi(observations, stateList, start,  matrixA, matrixB)
main()


