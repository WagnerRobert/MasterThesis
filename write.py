import os
import subprocess
import urllib2

__author__ = 'delur'


def fasta(name, sequence, fastapath, overwrite):
    filetext = ">" + name + "\n"
    filetext += sequence

    if not os.path.exists(fastapath):
        os.makedirs(fastapath)

    if os.path.isfile(os.path.join(fastapath, name + ".fa")):
        if overwrite:
            f= open(os.path.join(fastapath, name + ".fa"), 'w')
            f.write(filetext)
            f.close()
    else:
       f= open(os.path.join(fastapath, name + ".fa"), 'w')
       f.write(filetext)
       f.close()


    return None


def blast(name, fasta, blastpath, overwrite):
    if not os.path.exists(blastpath):
        os.makedirs(blastpath)
    if os.path.isfile(os.path.join(blastpath, name + ".blast")):
        if overwrite:
            subprocess.call(['/usr/bin/blastpgp', '-F', 'F' ,'-a', '1', '-j', '3' ,'-b', '3000', '-e', '1', '-h', '1e-3', '-d', '/var/tmp/rost_db/data/big/big_80', '-i' ,os.path.join(fasta, name + ".fa"),'-o',os.path.join(blastpath, name + ".blast"), '-C', 'tmpfile.chk', '-Q', 'tmpfile.blastPsiMat'])
    else:
        subprocess.call(['/usr/bin/blastpgp', '-F', 'F' ,'-a', '1', '-j', '3' ,'-b', '3000', '-e', '1', '-h', '1e-3', '-d', '/var/tmp/rost_db/data/big/big_80', '-i' ,os.path.join(fasta, name + ".fa"),'-o',os.path.join(blastpath, name + ".blast"), '-C', 'tmpfile.chk', '-Q', 'tmpfile.blastPsiMat'])

    return None


def uniprot(proteines, uniprot, overwrite):
    foundEntries = []
    if not os.path.exists(uniprot):
        os.makedirs(uniprot)
    for protein in proteines:

        tmp = protein.split('-')[0].split('#')[0]
        if os.path.isfile(os.path.join(uniprot, tmp + ".txt")):
            if overwrite:
                response =  urllib2.urlopen("http://www.uniprot.org/uniprot/" + tmp + ".txt")
                entry = response.read()
                if str(entry) == "":
                    print "Did not find uniprot entry for: " + tmp + " !"
                else:
                    f = open(os.path.join(uniprot, tmp+".txt"), 'w')
                    f.write(entry )
                    f.close()
                    foundEntries.append(tmp)
            else:
                foundEntries.append(tmp)
        else:
            response =  urllib2.urlopen("http://www.uniprot.org/uniprot/" + tmp + ".txt")
            entry = response.read()
            if str(entry) == "":
                    print "Did not find uniprot entry for: " + tmp + " !"
            else:
                f = open(os.path.join(uniprot, tmp+".txt"), 'w')
                f.write(entry)
                f.close()
                foundEntries.append(tmp)
    print foundEntries
    return foundEntries