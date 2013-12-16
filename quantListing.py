import operator
import os
import barplot
import dotplot
import Branch

__author__ = 'delur'




def list_protein(filepath, quant):
    neg_list = []
    neg_sum = 0.0
    max_neg_sum = 0.0
    pos_list = []
    pos_sum = 0.0
    max_pos_sum = 0.0

    # read the prepared kmerfile of the protein and add entries to the neg or pos list depending on leading sign
    # also calc total sum of the pos and neg list in the pos_sum and neg_sum variable
    protein = open(filepath, 'r')
    for kmer in protein:
        tmp = kmer.rstrip().split(' ')

        if float(tmp[1]) < 0:
            neg_list.append(tmp)
            neg_sum += float(tmp[1])
        else :
            pos_list.append(tmp)
            pos_sum += float(tmp[1])
    pos_list.reverse()


    # calculate the quant values, then remove the smales value from each quant list until there are only entries
    # above the quant left
    pos_quant = pos_sum * quant
    neg_quant = neg_sum * quant
    while pos_sum > pos_quant:
        tmp = pos_list.pop()
        pos_sum -= float(tmp[1])
    while neg_sum < neg_quant:
        tmp = neg_list.pop()
        neg_sum -= float(tmp[1])

    return (pos_list, neg_list)


def list_svm(filepath_svm, protein2location, tree, quant):
    """
    Executes list_protein for each protein in filepath_prepared (the SVM directory)

    Returns a dict with the protein name as key and a tuple as value, containing the list of elements in the pos quant
    in [0] and the list of elements in the neg quant in [1]
    @param filepath_svm:
    @param protein2location:
    @param tree:
    @param quant:
    """
    proteines = {}

    for root, dirs, files in os.walk(filepath_svm):
        if root == filepath_svm:
            for file in files:
                name = os.path.basename(file).rsplit('.')[0]
                if protein2location[name] in tree[os.path.basename(root)][0] or protein2location[name] in tree[os.path.basename(root)][1]:
                    proteines[name] = list_protein(os.path.join(filepath_svm, file), quant)

    # initialze the final locations list
    locations = {}
    for protein in proteines:
        locations[protein2location[protein]] = []
    # fill the final location list
    for protein in proteines:
        loc = protein2location[protein]
        locations[loc].append(proteines[protein])


    return locations


def count(locations, svm_result):
    grouppro = {}
    groupcon = {}

    numproteins = 0
    for location in locations:
        #print location
        numproteins += len(svm_result[location])
        for protein_kmers in svm_result[location]:
            for kmer in  protein_kmers[0]: # these kmers are supporting the descision to classify these proteins as left branch
                if grouppro.has_key(kmer[0]):
                    grouppro[kmer[0]] += 1
                else:
                    grouppro[kmer[0]] = 1
            for kmer in  protein_kmers[1]: # these kmers are against the descision to classify these proteins as left branch
                if groupcon.has_key(kmer[0]):
                    groupcon[kmer[0]] += 1
                else:
                    groupcon[kmer[0]] = 1

    def makefract(group, numproteins):
        tmp = {}
        for kmer in group:
            tmp[kmer] = group[kmer]/ float(numproteins)
        return tmp

    grouppro = makefract(grouppro, numproteins)
    groupcon = makefract(groupcon, numproteins)
    return grouppro,groupcon


def count_svm(svm_result, tree, svm):
    group0pro = {}
    group0con = {}
    group1pro = {}
    group1con = {}

    # process all kmers that fall in group0 (left branch of the svm)
    group0pro, group0con = count(tree[0].split(','), svm_result)

    # process all kmers that fall in group1 (right branch of the svm)
    group1con, group1pro = count(tree[1].split(','), svm_result)


    group0proList = sorted(group0pro.iteritems(), key=operator.itemgetter(1), reverse=True)
    group0conList = sorted(group0con.iteritems(), key=operator.itemgetter(1), reverse=True)
    group1proList = sorted(group1pro.iteritems(), key=operator.itemgetter(1), reverse=True)
    group1conList = sorted(group1con.iteritems(), key=operator.itemgetter(1), reverse=True)

    branch = Branch.Branch(svm, tree, group0proList, group0conList, group1proList, group1conList)

    return branch


def graph(count_result):
    #barplot.plot(count_result)
    dotplot.plot(count_result)

def doList(filepath_prepared, protein2location, tree, quant):
    """
    Executes the list_svm function for each svm directoy in filepath_prepared
    (the prepared directory containing the svm dirs)



    @param filepath_prepared: directory that contains all the  
    @param protein2location:
    @param tree:
    @param quant:
    """

    kmerlist = {}
    for root, dirs, files in os.walk(filepath_prepared):
        if root == filepath_prepared:
            for dirname in dirs:
                #print dirname
                svm_result = list_svm(os.path.join(filepath_prepared, dirname), protein2location, tree, quant)
                count_result = count_svm(svm_result, tree[dirname], dirname)
                #graph(count_result)
                kmerlist[dirname] = count_result

    return kmerlist