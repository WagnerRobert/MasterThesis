import math
import os

__author__ = 'delur'

import wx

app = None
frame = None

def get_sequence(entry):
    start = -1
    end = -1
    sequence = ""
    for i in range(len(entry)):
        if entry[i].startswith("SQ"):
            start = i+1
        if entry[i].startswith("//"):
            end = i

    for i in range(start, end):
        sequence += entry[i]

    sequences = sequence.split(' ')

    sequence = ""
    for line in sequences:
        sequence += line

    return sequence


def print_sequence(sequence, tmr, kmers):
    print  ">" * 80
    length = len(sequence)

    start = 0
    while (start + 80) <= length:
        print sequence[start:start+80]
        print tmr[start:start+80]
        print kmers[start:start+80]
        print ""
        start += 80

    print sequence[start:length]
    print tmr[start:length]
    print kmers[start:length]
    print ""
    print  ">" * 80


def get_transmembrane(entry, sequence):

    transmembrane = []
    for i in range(len(entry)):
        if entry[i].startswith("FT   TRANSMEM"):
            if "Potential" in entry[i]:
                pass
            else:
                transmembrane.append(entry[i])


    def cleanup(line):
        line = line.split()
        return line[2:4]
    for i in range(len(transmembrane)):
        transmembrane[i] = cleanup(transmembrane[i])

    return createTmrString (sequence, transmembrane)





def draw_sequence(sequence, transmembrane_regions):
    numInfoLines = 2
    numLineBreaks = math.ceil(len(sequence)/80.0)

    def markTransmembrane(dc, transmembrane_regions):
        dc.SetPen(wx.Pen(wx.BLACK, 0))
        dc.SetBrush(wx.RED_BRUSH)


        tmr = []
        for entry in transmembrane_regions:
            if math.ceil(int(entry[0]) / 80.0) == math.ceil(int(entry[1]) / 80.0):
                tmr.append( (int(entry[0]) % 80, int(entry[1]) % 80.0, math.trunc(int(entry[1]) / 80.0) ) )
            else:
                tmr.append( (int(entry[0]) % 80, math.ceil(int(entry[0]) / 80.0) * 80, math.trunc(int(entry[0]) / 80.0) ) )
                tmr.append( (math.trunc(int(entry[1]) / 80.0) * 80, int(entry[1]) % 80, math.trunc(int(entry[1]) / 80.0) ) )
                pass

        for entry in tmr:
            for i in range(int(entry[0]), int(entry[1])):
                width = 20
                dc.DrawRectangle( i* width, entry[2]*(numInfoLines+1) * width , 19, 19 )

    def writeSequence(dc, sequence):
        dc.SetPen(wx.Pen(wx.BLACK, 1))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)

        row = 0
        while len(sequence)>0:

            subsequence = sequence[:80]
            for i in range(len(subsequence)):
                width = 20
                dc.DrawRectangle( i* width, row * width, 19, 19 )
                dc.DrawLabel(subsequence[i],wx.Rect( i* width, row * 20, 19, 19), wx.ALIGN_CENTER_HORIZONTAL)

            sequence = sequence[80:]
            row += numInfoLines +1





    class DrawPanel(wx.Frame):

        """Draw a line to a panel."""

        def __init__(self):
            wx.Frame.__init__(self,None, title="Draw on Panel")
            self.Bind(wx.EVT_PAINT, self.OnPaint)



        def OnPaint(self, event=None):
            dc = wx.PaintDC(self)
            dc.Clear()
            markTransmembrane(dc, transmembrane_regions)
            writeSequence(dc, sequence)


    app = wx.App(False)
    frame = DrawPanel()
    frame.Show()
    app.MainLoop()


def getKmersPositionList(groupList, sequence, slice):
    #print groupList
    poslist = []
    for entry in groupList:
        if entry[0] in sequence and float(entry[1]) > slice:

            running = True
            pos = 0
            while (running):
                pos = sequence.find(entry[0], pos+1)
                if pos == -1:
                    running = False
                else:
                    poslist.append(pos)
    poslist = sorted(poslist)

    #print poslist
    return getKmersString(poslist, sequence)


def getKmersString(kmers, sequence):

    kmersStringList = []
    kmersStringList = [0]*(len(sequence) - len(kmersStringList))


    if len(kmers) > 0:
        j = 0
        for i in range(len(sequence)):
            if i < int(kmers[j]):
                pass
            else:
                if i == int(kmers[j]):
                    kmersStringList[i] += 1
                    kmersStringList[i+1] += 1
                    kmersStringList[i+2] += 1
                    j +=1
                    if j >= len(kmers):
                        break

    kmerString = ""
    for number in kmersStringList:
        if number == 0:
            kmerString += " "
        else:
            kmerString += str(number)

    return kmerString


def evaluate(sequence, tmr, kmers):
    kmerInTmr = 0
    kmerOutTmr = 0

    for i in range(len(kmers)):
        if kmers[i] is not ' ':
            if tmr[i] is '=':
                kmerInTmr += int(kmers[i])
                #kmerInTmr += 1
            else:
                kmerOutTmr += int(kmers[i])
                #kmerOutTmr += 1

    print str((kmerInTmr+kmerOutTmr)/3) + " Kmers "
    print str(kmerInTmr) + " kmer amino acids were inside transmembrane regions."
    print str(kmerOutTmr) + " kmer amino acids were outside transmembrane regions."
    print str(kmerInTmr/float(kmerInTmr+kmerOutTmr)) + " precision."


    return kmerInTmr/float(kmerInTmr+kmerOutTmr)


def createTmrString(sequence, transmembrane_regions):
    tmr = ""
    j = 0


    if len(transmembrane_regions) > 0:
        for i in range(len(sequence)):
            if i < int(transmembrane_regions[j][0]):

                tmr += " "
            else:
                if i < int(transmembrane_regions[j][1]):
                    tmr += "="
                else:
                    j +=1
                    if j >= len(transmembrane_regions):
                        break

    while len(tmr) < len(sequence):
        tmr += " "
    return tmr


def getEntry(protein, uniprotlocation):
    entry = ""
    filelocation = os.path.join(uniprotlocation,  protein + ".txt")

    f = open(filelocation, 'r')
    for line in f:
        entry += line
    f.close()

    entry = entry.split('\n')

    return entry


def blast(kmerlist, svm, location, tree, protein2location, uniprot, slice):
    counter = 0.0
    precision = 0.0

    for protein in protein2location:
        if protein2location[protein] == location:
            tmp = protein.split('-')[0].split('#')[0]
            print tmp
            entry = getEntry(tmp, uniprot)
            if "Reviewed" not in entry[0]:
                print "Protein has not been reviewed!"
                print "" 
                continue
            sequence = get_sequence(entry)
            tmr = get_transmembrane(entry, sequence)
            kmers = getKmersPositionList(kmerlist[svm].group1proList, sequence, slice)

            #print sequence
            #print_sequence(sequence, tmr, kmers)
            if '1' in kmers and '=' in tmr:
                precision += evaluate(sequence, tmr, kmers)
                counter += 1.0
            elif '=' in tmr:
                print "No kmer hits under these settings, protein is not counted."
            elif '1' in kmers:
                print "protein has no FT TRANSMEM entries that are validated, protein is not counted"
            print ""
    print ""

    if counter > 0:
        print str(precision/counter) +" average prescision over all " + str(int(counter)) + " proteines with uniprot tmr regions."
        return precision/counter
    else:
        print "No counted proteins under this setting ."
        return -1








    #draw_sequence(sequence, transmembrane_regions)

    return None