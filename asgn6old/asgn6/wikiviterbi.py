#CPSC475 Dr.DePalma Fall 2016 asgn6_test
#Probabilistic Part of Speech Tagger
#Sebastian Vargas
#id: avargas
#
#To run on linux, go to your terminal then go to the directory in which
# this program is stored. Then type "python asgn6_test.py insert string here"
# in the command line
#This should execute the program


import sys
import pandas
from pandas import DataFrame
import nltk
import numpy as np
import simplejson
#import asgn6_train
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



states = ['Healthy', 'Fever']

observations = ['normal', 'cold', 'dizzy']

start_probability = {'Healthy': 0.6, 'Fever': 0.4}

transition_probability = {

   'Healthy' : {'Healthy': 0.7, 'Fever': 0.3},

   'Fever' : {'Healthy': 0.4, 'Fever': 0.6}

   }

emission_probability = {

   'Healthy' : {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},

   'Fever' : {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6}

   }
sentences = ["The","Fulton","County","Grand","Jury","said"]

infileA="matrixA.xlsx"
infileB="matrixB.xlsx"
#brown_train_file = "brown_train.txt"
#f = open('brown_train.txt', 'r')
#brown_train = simplejson.load(f)
#f.close()
#sentences = ["boy","and","find","the",";"]

Apandas = pandas.read_excel(infileA,sheetname="Matrix A") 
#print Apandas
rownames = Apandas.index.tolist()
A=np.array(Apandas)

Bpandas = pandas.read_excel(infileB,sheetname='Matrix B')
#print Bpandas
B=np.array(Bpandas)
statenames = Bpandas.index.tolist()
priors=np.expand_dims(np.array(A[0,:]),1)
for i in range(len(priors)-1):
    priors[i] = 1
    
viterbi(sentences, statenames, priors, A, B)


#viterbi(observations,states, start_probability, transition_probability, emission_probability)

#pi=np.expand_dims(np.array(A[0,:]),1)