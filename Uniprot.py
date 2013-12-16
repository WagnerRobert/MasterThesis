import os

__author__ = 'delur'

import urllib2


def getUniprotEntries(protein2location, uniprot):
    if not os.path.exists(uniprot):
        os.makedirs(uniprot)
    for protein in protein2location:
        tmp = protein.split('-')[0].split('#')[0]
        response =  urllib2.urlopen("http://www.uniprot.org/uniprot/" + tmp + ".txt")
        f = open(os.path.join(uniprot, tmp+".txt"), 'w')
        f.write(response.read() )
        f.close()

    return None