#!/usr/bin/env python



import readResults
import readTree
import prepareOutput




import os
import sys

__author__ = 'delur'





#filepaths of input files
filepath_result = sys.argv[1]
filepath_tree = sys.argv[2]
filepath_kmerweights = sys.argv[3]

#filepaths of output files
filepath_prepared = sys.argv[4]
uniprot = sys.argv[5]

protein2location = readResults.read(filepath_result)

#import Uniprot
#Uniprot.getUniprotEntries(protein2location, uniprot)

tree = readTree.read(filepath_tree)

prepareOutput.prepare(filepath_kmerweights, filepath_prepared)
#import checkOrder
#checkOrder.check(filepath_prepared, protein2location, tree)

#import calcQuant
#calcQuant.calc(filepath_prepared, protein2location, tree)

import quantListing
svmlvl= "SVM_0"
quant =0.3
kmerlist = quantListing.doList(filepath_prepared, protein2location, tree, quant)

import blast_kmers
slice = 0.0
precision = blast_kmers.blast(kmerlist, svmlvl, "cellmemb", tree[svmlvl], protein2location, uniprot, slice)

#import plots
#values = []
#score = 0.0
#bestquant = -1
#bestslice = -1
#for i in range(1, 20):
#    tmp = []
#    values.append(tmp)
#    for j in range(0,20):
#        quant = float(i) * 0.05
#        kmerlist = quantListing.doList(filepath_prepared, protein2location, tree, quant)
#
#        svmlvl= "SVM_0"
#        slice = float(j) * 0.05
#
#        precision = blast_kmers.blast(kmerlist, svmlvl, "cellmemb", tree[svmlvl], protein2location, uniprot, slice)
#        values[i-1].append( precision )
#        if precision > score:
#            score = precision
#            bestquant = quant
#            bestslice = slice
#
#print "Best avg precision was " + str(score) + " reached with quant " + str(bestquant) + " and slice " + str(bestslice)
#plots.contour(values)
#print str(protein2location)
#print str(tree)