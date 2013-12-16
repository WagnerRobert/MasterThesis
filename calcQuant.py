__author__ = 'delur'

import os


def calc_quant(kmerfile_path, protein2location, tree):
    neg_list = []
    neg_sum = 0.0
    max_neg_sum = 0.0
    pos_list = []
    pos_sum = 0.0
    max_pos_sum = 0.0

    f = open(kmerfile_path, 'r')
    for n in f:
        tmp = n.rstrip().split(' ')

        if float(tmp[1]) < 0:
            neg_list.append(tmp)
            neg_sum += float(tmp[1])
        else :
            pos_list.append(tmp)
            pos_sum += float(tmp[1])
    pos_list.reverse()

    max_pos_sum = pos_sum
    max_neg_sum = neg_sum

    factor = 1.0
    step = 0.05

    pos_numbers = []
    neg_numbers = []

    while (factor > 0):
        current_pos_quant = max_pos_sum * factor
        current_neg_quant = max_neg_sum * factor

        while pos_sum > current_pos_quant:
            tmp = pos_list.pop()
            pos_sum -= float(tmp[1])
        while neg_sum < current_neg_quant:
            tmp = neg_list.pop()
            neg_sum -= float(tmp[1])

        pos_numbers.append( len(pos_list) )
        neg_numbers.append( len(neg_list) )

        factor -= step

    #prepare n

    posline = []
    posline.append("+")
    posline.append(protein2location[os.path.basename(kmerfile_path).split('.')[0]])
    for num in pos_numbers:
        posline.append(str(num))
    posline.append(os.path.basename(kmerfile_path).split('.')[0])

    negline = []
    negline.append("-")
    negline.append(protein2location[os.path.basename(kmerfile_path).split('.')[0]])
    for num in neg_numbers:
        negline.append(str(num))
    negline.append(os.path.basename(kmerfile_path).split('.')[0])

    return (posline,negline)



def calc_svm(svm_path, protein2location, tree):
    svm_result = []
    for root, dirs, files in os.walk(svm_path):
        for filename in files:
            svm_result.append(calc_quant(os.path.join(svm_path,filename), protein2location, tree))
    return svm_result


def avg_splits_help_func(split):
    tmp =[]
    for i in range(len(split[0])):
        if i == 0:
            tmp.append(split[0][i])
        elif i == 1:
            tmp.append(split[0][i])
        elif i >= 0+2 and i <= 2+19:
            avg = 0.0
            for element in split:
                avg +=  float(element[i])
            avg = avg / len( split )
            tmp.append(int(avg))
        elif i == (len(split[0]) -1):
            names = ""
            for element in split:
                names +=  "|"+element[i]
            names = names.lstrip('|')
            tmp.append(names)
    return tmp


def average_splits(svm_result, svm_split):
    pos_split_for = []
    pos_split_against = []
    neg_split_for = []
    neg_split_against = []

    for entry in svm_result: #sort the entries returned from the quant cound based on whether they are predicted to fork left or right in the svm tree
        if entry[0][1] in svm_split[0]: # the split[0] list has elements that fork left, these are not leaves in most of the cases
            tmp = entry[0]
            tmp[1] = svm_split[0]
            neg_split_against.append(tmp) # Entry[0] has the quant above 0, so this quant shows kmers that contradict the prediction
            tmp = entry[1]
            tmp[1] = svm_split[0]
            neg_split_for.append(tmp) # Entry[1] hast the quant below 0, so this quant shows kmers that support the prediction
        elif entry[0][1] in svm_split[1]: # the split[1] list has the elements that fork right, these are leaf nodes in most cases (so final predictions)
            tmp = entry[0]
            tmp[1] = svm_split[1]
            pos_split_for.append(tmp) # Entry[0] hast the quant above 0, so this quant shows kmers that support the prediction
            tmp = entry[1]
            tmp[1] = svm_split[1]
            pos_split_against.append(tmp) # Entry[1] hast the quant below 0, so this quant shows kmers that contradict the prediction


    print avg_splits_help_func(pos_split_for)
    print avg_splits_help_func(pos_split_against)
    print avg_splits_help_func(neg_split_for)
    print avg_splits_help_func(neg_split_against)




def calc(filepath_prepared, protein2location, tree):
    for root, dirs, files in os.walk(filepath_prepared):
        if root == filepath_prepared:
            for dirname in dirs:
                print dirname
                svm_result = calc_svm(os.path.join(filepath_prepared, dirname), protein2location, tree)
                average_splits(svm_result, tree[dirname])
    return None