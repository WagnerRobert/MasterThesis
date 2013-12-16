__author__ = 'delur'

import os
import operator


def do_sum(filepath):
    total = 0.0
    f = open(filepath, 'r')
    for line in f:
        total += float(line.rstrip().split(' ')[1])
    return total


def infork(location, tree):
    is_infork = False
    if location in tree[0]:
        is_infork = True
    if location in tree[1]:
        is_infork = True
    return is_infork


def check_svm(svm_path, protein2location, tree):
    print svm_path
    svm = {}
    for root, dirs, files in os.walk(svm_path):
        for filename in files:
            svm[filename.split('.')[0]] = do_sum(os.path.join(root, filename))

    for name,value in sorted(svm.iteritems(), key=operator.itemgetter(1)):
        if infork(protein2location[name], tree[os.path.basename(svm_path)]):
            print protein2location[name] +"\t"+ str(value) +"\t" + name




def check(filepath_prepared, protein2location, tree):
    """
    The added kmerweights for each file in a SVM directory should show an order over all files
     that enables separation in the predictions based on this order. This is checked here.
    @param filepath_prepared: path to the prepared directory
    @return: None
    """
    for root, dirs, files in os.walk(filepath_prepared):
        if root == filepath_prepared:
            for dirname in dirs:
                check_svm(os.path.join(filepath_prepared, dirname), protein2location, tree)

    return None