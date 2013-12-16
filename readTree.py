__author__ = 'delur'


def read(filepath_tree):
    """
    reads the tree.txt file that describes the branching of the svm tree
    @rtype : dict with the SVM folder names as keys and the branching on that lvl as value.
    """
    tree = {}

    f = open(filepath_tree)
    for line in f:
        tmp = line.rstrip().split('\t')
        tree[tmp[0]] = tmp[1].split(':')
    f.close()

    return tree
