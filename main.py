#!/usr/bin/env python
import read

import readResults
import readTree
import prepareOutput




import os
import sys

__author__ = 'delur'



#filepath dict
paths = {}

#filepaths of input files
filepath_result = sys.argv[1]
paths["resultfile"] = sys.argv[1]
filepath_tree = sys.argv[2]
filepath_kmerweights = sys.argv[3]

#filepaths of output files
filepath_prepared = sys.argv[4]
uniprot = sys.argv[5]
blast = sys.argv[6]
fastapath = sys.argv[7]
multiplefastapath = sys.argv[8]
paths["mfasta"]= sys.argv[8]
paths["msa"]= sys.argv[9]
paths["polyphobius"] = sys.argv[10]

paths["pdf"]= sys.argv[11]
paths["clustalo"] = sys.argv[12]

protein2location = readResults.read(filepath_result)
resultfile_info = read.resultfile(paths)

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


print "Set to top " + str(quant) + " quant."
for entry in sorted(kmerlist):
    print "On level " + entry + " there are " + str(len(kmerlist[entry].group0proList)) +" kmers in group0proList."
    print "On level " + entry + " there are " + str(len(kmerlist[entry].group1proList)) +" kmers in group1proList."

import blast_kmers
slice = 0.0
precision = blast_kmers.blast(kmerlist, svmlvl, "cellmemb", tree[svmlvl], protein2location, uniprot, slice, blast, fastapath, multiplefastapath, paths, resultfile_info)

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