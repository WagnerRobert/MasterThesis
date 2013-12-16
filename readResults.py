__author__ = 'delur'


def read(filepath_result):
    """
    reads the result file, that contains names of the proteins and their predicted location
    @rtype : dict with protein names as keys and their predicted location as values
    """
    protein2location = {}

    f = open( filepath_result, 'r')
    for line in f:
        if not line.startswith("#"):
            tmp = line.rstrip().split('\t')
            protein2location[tmp[0]] = tmp[1]
    f.close()

    return protein2location