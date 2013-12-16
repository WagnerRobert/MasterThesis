__author__ = 'delur'

import os
import operator
import math


def makedir(dirpath):
    """
    Creates directories if they do not exist yet
    @type dirpath: path to the directory that might be created
    """
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)


def process(filepath, filepath_prepared):
    """
    Sorts the entries in the filepath file by value instead of name.
     Divides them by a factor given at the last line of each file.
     Then writes them to the prepared directory keeping the same file structure.
    prepared directory
    @param filepath: string path to a single kmerfile
    @param filepath_prepared: string path to the prepared directory
    """
    kmers = {}
    factor = 0

    f = open(filepath,'r')
    for line in f:
        tmp = line.rstrip().split(' ')
        if len(tmp) > 1:
            kmers[tmp[0].rstrip(':')] = float(tmp[1])
        else:
            factor = math.sqrt(float(tmp[0]))
    f.close()

    outpath = os.path.split(os.path.dirname(filepath))[1]
    filepath_prepared = os.path.join(filepath_prepared, outpath)
    filepath_prepared = os.path.join(filepath_prepared, os.path.basename(filepath))
    f = open(filepath_prepared, 'w')
    for kmer, value in sorted(kmers.iteritems(), key=operator.itemgetter(1)):
        f.write( kmer + " " + str(value / factor) + "\n")
    f.close()




def prepare(filepath_kmerweights, filepath_prepared):
    """
    Creates filestructure equal do the kmerweights directory in filpath_prepared.
    Then sorts the kmerweights files by value instead of key and divides them by the factor
    that is given as last line of each kmerfile.
    @param filepath_kmerweights: string path to the kmerweights directory
    @param filepath_prepared: string path to the prepared directory
    """
    #create the prepared directory if needed
    makedir(filepath_prepared)
    for root, dirs, files in os.walk(filepath_kmerweights):
        if root == filepath_kmerweights:
            for dirname in dirs:
                #create the SVM directories if needed
                makedir( os.path.join(filepath_prepared,dirname))
        for filename in files:
            process(os.path.join(root,filename), filepath_prepared)