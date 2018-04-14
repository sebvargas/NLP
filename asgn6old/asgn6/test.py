# -*- coding: utf-8 -*-
"""
Add second test to viterbi algorithm by phvu found here: 
ttp://phvu.net/2013/12/06/sweet-implementation-of-viterbi-in-python/
https://github.com/phvu/misc/tree/master/viterbi
The test replicates the POS tag results from edition 3 of Jurafsky & Martin.
The toy numerical example can be found in section 9.4.3
Currently the whole draft can be found here: 
http://web.stanford.edu/~jurafsky/slp3/
Note: Terminology: 
Jurafsky & Martin : " state observation likelihood" =  "emission probability"
                    " transition probability" =  "trigram probability."
@author: Christian Geng, christian.c.geng@gmail.com
"""

import viterbi
import pandas
from pandas import DataFrame
import nltk
import numpy as np

infileA="matrixA.xlsx"
infileB="matrixB.xlsx"

def viterbi (priors,transition,emission,observations):
    """Return the best path, given an HMM model and a sequence of observations"""
    # A - initialise stuff
    nSamples = len(observations[0])
    nStates = transition.shape[0] # number of states
    c = np.zeros(nSamples) #scale factors (necessary to prevent underflow)
    viterbi = np.zeros((nStates,nSamples)) # initialise viterbi table
    psi = np.zeros((nStates,nSamples)) # initialise the best path table
    best_path = np.zeros(nSamples); # this will be your output

    # B- appoint initial values for viterbi and best path (bp) tables - Eq (32a-32b)
    viterbi[:,0] = priors.T * emission[:,observations[0]]
    c[0] = 1.0/np.sum(viterbi[:,0])
    viterbi[:,0] = c[0] * viterbi[:,0] # apply the scaling factor
    psi[0] = 0;

    # C- Do the iterations for viterbi and psi for time>0 until T
    for t in range(1,nSamples): # loop through time
        for s in range (0,nStates): # loop through the states @(t-1)
            trans_p = viterbi[:,t-1] * self.transition[:,s]
            psi[s,t], viterbi[s,t] = max(enumerate(trans_p), key=operator.itemgetter(1))
            viterbi[s,t] = viterbi[s,t]*self.emission[s,observations[t]]

        c[t] = 1.0/np.sum(viterbi[:,t]) # scaling factor
        viterbi[:,t] = c[t] * viterbi[:,t]

    # D - Back-tracking
    best_path[nSamples-1] =  viterbi[:,nSamples-1].argmax() # last state
    for t in range(nSamples-1,0,-1): # states of (last-1)th to 0th time step
        best_path[t-1] = psi[best_path[t],t]

    return best_path

Apandas = pandas.read_excel(infileA,sheetname="Matrix A") 
print Apandas
rownames = Apandas.index.tolist()
A=np.array(Apandas)
A = np.nan_to_num(A)
print A

Bpandas = pandas.read_excel(infileB,sheetname='Matrix B')
print Bpandas
B=np.array(Bpandas)
B = np.nan_to_num(B)
statenames = Bpandas.index.tolist()
print B

trans=A[1:,:]
pi=np.expand_dims(np.array(A[0,:]),1)
decoder = viterbi(pi,trans, B,B)

""" do the decoding """
#states =  decoder.Decode(np.arange(5))
#result = np.array(statenames)[states].tolist()
#sentence = Bpandas.columns.tolist()
#resultTagged = zip(sentence,result)

#correct=' Janet/NNP will/MD back/VB the/DT bill/NN'
#correct=[nltk.str2tuple(x) for x in correct.split()]
#print (resultTagged)
#assert (resultTagged==correct)

#print "PASSED"
