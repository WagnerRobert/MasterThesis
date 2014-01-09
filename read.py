import os

__author__ = 'delur'


def blast(name, blast):
    f = open (os.path.join(blast, name + ".blast"), 'r')

    run3 = False

    ProfileProteines = []

    for line in f:
        if "round 3" in line:
            run3 = True
        if run3:
            if line.startswith("tr|") or line.startswith("sp|"):
                ProfileProteines.append(line.split('|')[1])
            elif  "|" in line and  not line.startswith(">"):
                print line
    f.close()
    return ProfileProteines


def multiple_sequence_alignment(protein_name, paths):
    msa = []
    f = open (os.path.join(paths["msa"], protein_name + ".msa"), 'r')

    #skipp clustalO header
    #f.read()
    #f.read()
    #f.read()

    i = 0
    for line in f:
        i+=1
        if i > 3:
            if not line.startswith(" "):
                name = line.rstrip().split(' ', 1)[0]
                sequence = line.rstrip().rsplit(' ', 1)[1]
            #print name + " : " + sequence
            msa.append( (name, sequence))

    print msa
    f.close()
    return msa


def polyphobius(protein_name, paths):

    tmr = []
    f = open (os.path.join(paths["polyphobius"], protein_name + ".poly"), 'r')


    for line in f:
            if  line.startswith("FT   TRANSMEM"):
                tmp = line.rstrip().split()
                start = int(tmp[2])
                end = int(tmp[3])
                tmr.append( (start, end))

    f.close()
    return tmr