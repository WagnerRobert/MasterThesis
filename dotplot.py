from pylab import *
import numpy as np
import Branch

__author__ = 'delur'

def slice(leftpos, lowerBound, upperBound):
    tmp = []
    for tuple in leftpos:
        if tuple[1] > lowerBound and tuple[1] <= upperBound:
            tmp.append(tuple)

    return tmp

def getValue(leftpos, index):
    tmp = []
    for tuple in leftpos:
        tmp.append(tuple[index])

    return tmp


def plot_data(kmer_data, branch, svm, procon):
    print len(kmer_data)
    #kmer_data = slice(kmer_data, 0.60, 1.0)
    print len(kmer_data)

    x = np.arange(len(kmer_data))
    y = getValue(kmer_data, 1)
    names = tuple(getValue(kmer_data, 0))

    test = plt.plot(x,y, 'ro')

    for X,Y in zip(x,y):
        plt.text(X,Y*1.01, "%.2f" % round(kmer_data[X][1], 2), rotation = 45)
    plt.xticks(x, names, rotation = 315)

    plt.ylabel("Frequency")
    plt.xlabel("Kmers")
    plt.title("Kmer-Frequency " + procon + " Plot for " + str(branch) + " in " + svm + " for all Kmers with frequency between 0.85 and 1.0")

    upperY = kmer_data[0][1]  * 1.05
    lowerY = kmer_data[len(kmer_data) -1][1] * 0.95
    ylim(  lowerY , upperY)

    leftX = -1
    rightX = len(kmer_data)
    xlim(leftX, rightX)
    plt.show()


def plot(count_result):

    plot_data(count_result.group0proList, count_result.branch[0], count_result.svm, "pro")
    plot_data(count_result.group0conList, count_result.branch[0], count_result.svm, "con")
    plot_data(count_result.group1proList, count_result.branch[1], count_result.svm, "pro")
    plot_data(count_result.group1conList, count_result.branch[1], count_result.svm, "con")





    return None