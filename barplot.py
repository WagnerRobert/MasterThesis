from pylab import *
import numpy as np

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



def plot(count_result):

    leftpos = count_result[0]
    print len(leftpos)
    leftpos = slice(leftpos, 0.85, 1.0)
    print len(leftpos)
    #leftpos = leftpos[0:int(len(leftpos)*0.20)]
    y = getValue(leftpos, 1)
    names = tuple(getValue(leftpos, 0))
    N = len(leftpos)

    ind = np.arange(N)  # the x locations for the groups
    width = 0.35       # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, y, width, color='r')

    # add some
    ax.set_ylabel('Frequency')
    ax.set_title('Kmers')
    ax.set_xticks(ind+width)
    ax.set_xticklabels( names, rotation = 315  )

    def autolabel(rects):
        # attach some text labels
        index = 0
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., height , "%.2f" % round(leftpos[index][1], 2) , ha='center', va='bottom', rotation=45)
            index += 1

    autolabel(rects1)
    upperY = leftpos[0][1]  * 1.05
    lowerY = leftpos[len(leftpos) -1][1] * 0.95
    ylim(  lowerY , upperY)

    leftX = -1
    rightX = len(leftpos)
    xlim(leftX, rightX)

    plt.show()
    return None