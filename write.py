import os
import subprocess
import urllib2

__author__ = 'delur'


def fasta(name, sequence, fastapath, overwrite):
    filetext = ">" + name + "\n"
    filetext += sequence + "\n"

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
    print blastpath
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
    #print foundEntries
    return foundEntries


def multiple_fasta(proteinname_sequence, multiplefastapath, overwrite):

    filetext = ""
    for i in range(len(proteinname_sequence)) :
        name = proteinname_sequence[i][0]
        sequence = proteinname_sequence[i][1]
        filetext += ">" + name + "\n"
        filetext += sequence + "\n\n"

    if not os.path.exists(multiplefastapath):
        os.makedirs(multiplefastapath)

    if os.path.isfile(os.path.join(multiplefastapath, proteinname_sequence[0][0] + ".fa")):
        if overwrite:
            f= open(os.path.join(multiplefastapath, proteinname_sequence[0][0] + ".fa"), 'w')
            f.write(filetext)
            f.close()
    else:
       f= open(os.path.join(multiplefastapath, proteinname_sequence[0][0] + ".fa"), 'w')
       f.write(filetext)
       f.close()


    return None


def multiple_sequence_alignment(mfasta_name, mfastapath, msapath, overwrite):
    if not os.path.exists(msapath):
        os.makedirs(msapath)
    if os.path.isfile(os.path.join(msapath, mfasta_name + ".msa")):
        if overwrite:
            subprocess.call(['/home/delur/Desktop/master/test/clustalo', '-i' ,os.path.join(mfastapath, mfasta_name + ".fa"),'-o',os.path.join(msapath, mfasta_name + ".msa"), '--outfmt=clu', '--force', '--wrap=9999'])
    else:
        subprocess.call(['/home/delur/Desktop/master/test/clustalo', '-i' ,os.path.join(mfastapath, mfasta_name + ".fa"),'-o',os.path.join(msapath, mfasta_name + ".msa"), '--outfmt=clu', '--wrap=9999'])

    return None


def mfasta_cleanup(query_protein_name, path, overwrite):
    if not os.path.exists(path):
        os.makedirs(path)
    for root, dirs, files in os.walk(path):
        for file in files:
            if query_protein_name in file and file.endswith(".fa"):
                subprocess.call(['uniqueprot', '-i' ,os.path.join(path, file),'-o',os.path.join(path, query_protein_name + ".clean"), '-t', '20'])