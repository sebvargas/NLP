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

Apandas = pandas.read_excel(infileA,sheetname="Matrix A") 
#print Apandas
rownames = Apandas.index.tolist()
A=np.array(Apandas)
#print A

Bpandas = pandas.read_excel(infileB,sheetname='Matrix B')
#print Bpandas
B=np.array(Bpandas)
statenames = Bpandas.index.tolist()
#print B

trans=A[0:,:]
pi=np.expand_dims(np.array(A[0,:]),1)
#print trans
decoder = viterbi.Decoder(pi,trans, B)

""" do the decoding """
states =  decoder.Decode(np.arange(5))
result = np.array(statenames)[states].tolist()
#sentence = Bpandas.columns.tolist()
sentence = ["Today","is","a","good","day"]
resultTagged = zip(sentence,result)
resultnew = [(tup[0].encode('ascii'),tup[1].encode('ascii')) for tup in resultTagged]  
#correct=' Janet/NNP will/MD back/VB the/DT bill/NN'
#correct=[nltk.str2tuple(x) for x in correct.split()]
print (resultnew)
#assert (resultTagged==correct)

#print "PASSED"
