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
        line = line.rstrip()
        i+=1
        if i > 3:
            if not line == "" and not line.startswith(" "):
                name = line.split(' ', 1)[0]
                sequence = line.rsplit(' ', 1)[1]
            #print name + " : " + sequence
            msa.append( (name, sequence))

    #print msa
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


def resultfile(paths):
    """
    reads the result file, that contains names of the proteins and their predicted location
    @rtype : dict with protein names as keys and their predicted location as values
    """
    result_info = {}

    f = open( paths["resultfile"], 'r')
    for line in f:
        if not line.startswith("#"):
            tmp = line.rstrip().split('\t')
            result_info[tmp[0]] = (tmp[1], tmp[2])
    f.close()

    return result_info
