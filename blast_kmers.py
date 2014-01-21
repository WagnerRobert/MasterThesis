import math
import os
import sys
import alignment
import read
import write

__author__ = 'delur'



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
            elif "similarity" in entry[i]:
                pass
            else:
                #print entry
                #transmembrane.append(entry[i])
                pass
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


def process_query_protein(query_protein, uniprot, overwrite, fasta, kmerlist, blast, slice):
    query_protein_name = query_protein.split('-')[0].split('#')[0]
    print query_protein_name
    entry = getEntry(query_protein_name, uniprot)
    if "Reviewed" not in entry[0]:
        print "Protein has not been reviewed!"
        print ""
        return "ERROR"
    query_sequence = get_sequence(entry)
    #print sequence
    write.fasta(query_protein_name, query_sequence, fasta, overwrite)
    write.blast(query_protein_name, fasta, blast, overwrite)
    profileProteins = read.blast(query_protein_name, blast)
    profileProteins = write.uniprot(profileProteins, uniprot, overwrite)
    qtmr = get_transmembrane(entry, query_sequence)
    qkmers = getKmersPositionList(kmerlist, query_sequence, slice)

    return query_protein_name, entry, query_sequence, profileProteins, qtmr, qkmers


def process_profile_protein(profile_protein, uniprot, kmerlisting, noreviewcount, reviewcount , slice):
    entry = getEntry(profile_protein, uniprot)
    if "Reviewed" not in entry[0]:
        #print "Protein has not been reviewed!"
        noreviewcount += 1
        #continue
    else:
        reviewcount += 1

    profileprotein_sequence = get_sequence(entry)
    #print "\t" + sequence
    tmr = get_transmembrane(entry, profileprotein_sequence)
    kmers = getKmersPositionList(kmerlisting, profileprotein_sequence, slice)

    return entry, profileprotein_sequence, tmr, kmers, noreviewcount, reviewcount


def kmer_match(kmerlisting, msa):
    import re
    matches = {}
    for kmer_tuple in kmerlisting:
        kmer = kmer_tuple[0]

        pattern = ""
        for letter in kmer:
            pattern += letter + "[-]*"

        pattern = pattern[0:len(pattern)-4]
        regex = re.compile(pattern)

        for i in range (len(msa)):
            name, sequence = msa[i]
            match = regex.search(sequence)
            if  match:
                if name in matches:
                    pass
                else:
                    matches[name] = []
                matches[name].append(match.span())

    return matches


def getFeatures(entry):
    features = {}

    for line in entry:
        if line.startswith("FT   "):
            print line
            tmp = line.rstrip().split()
            if len(tmp) > 3 :
                if tmp[1] in features:
                    pass
                else:
                   features[tmp[1]] = []

                try:
                    start = int(tmp[2])
                    end = int(tmp[3])
                    if "By similarity" in line or "Potential" in line or "Propable" in line :
                        features[tmp[1]].append( (start, end, False) )
                    else:
                        features[tmp[1]].append( (start, end, True) )
                except ValueError:
                    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!Encountered slight Problem"
                    continue



    print features
    return features


def create_plot(query_protein_sequence, pos_matches, neg_matches, transmembrane_regions, entry, numProfileProteins, resultfile_info, paths):
    name = query_protein_sequence[0]
    sequence = query_protein_sequence[1]

    pos_count = [0] * len(sequence)
    for protein in pos_matches:
        for start,end in pos_matches[protein]:
            for j in range(start, end):
                pos_count[j] += 1

    neg_count = [0] * len(sequence)
    for protein in neg_matches:
        for start,end in neg_matches[protein]:
            for j in range(start, end):
                neg_count[j] += 1


    pos_count_noGaps = []
    neg_count_noGaps = []
    seq_noGap = ""
    text = ""
    for i in range(len(sequence)):
        if sequence[i] == '-':
            pass
        else:
            text += str(pos_count[i])
            pos_count_noGaps += [pos_count[i]]
            neg_count_noGaps += [neg_count[i]]
            seq_noGap += sequence[i]

    for i in range(len(pos_count_noGaps)):
        pos_count_noGaps[i] = pos_count_noGaps[i] * 100 / numProfileProteins
        neg_count_noGaps[i] = neg_count_noGaps[i] * 100 / numProfileProteins
    import matplotlib.pyplot as plt

    x = range(1, len(seq_noGap)+1)
    plt.clf()
    plt.cla()
    #print len(x)
    plt.plot(x,pos_count_noGaps, color='#336699')
    plt.plot(x, neg_count_noGaps, color='#CC0000')
    plt.ylabel('Coverage')

    long_name = ""
    location = ""
    confidence = ""
    for protein in resultfile_info:
        if name in protein:
            long_name = protein
            location = resultfile_info[protein][0]
            confidence = resultfile_info[protein][1]
    plt.title(long_name + "|" + location + "|"+ confidence +"|" + str(numProfileProteins) + " Profile Proteins")
    ax = plt.gca()


    plt.xticks(x, seq_noGap)




    ax.set_yticks( [0,50,100,150,200])
    ax.set_yticklabels(["0", "50", "100", "150", "200"])
    ax.yaxis.grid(True)
    #ax.xaxis.grid(True)

    ypos = -20
    height = 20
    for start,end in transmembrane_regions:
        rect = plt.Rectangle((start - 0.5, ypos), (end-start)+1, height, facecolor="#FFFF00", hatch='\\')
        plt.gca().add_patch(rect)
    #rect.set_alpha(0.5)

    #rect = plt.Rectangle((20 - 0.5, -30), 20, 10, facecolor="#0000FF")
    #rect.set_alpha(0.5)
    #plt.gca().add_patch(rect)

    features = getFeatures(entry)

    for feature in features:
        if feature == "TURN":
            color = "#4169e1"
        elif feature == "STRAND":
            color = "#8470ff"
        elif feature == "HELIX":
            color = "#20b2aa"
        elif feature == "CHAIN":
            color = "#000000"
            continue
        elif feature == "METAL":
            color = "#708090"
        elif feature == "NP_BIND":
            color = "#eedd82"
        elif feature == "BINDING":
            color = "#ff8c00"
        elif feature == "ACT_SITE":
            color = "#ff0000"
        elif feature == "DOMAIN":
            color = "#32cd32"
        elif feature == "INIT_MET":
            color = "#a52a2a"
        elif feature == "TRANSMEM":
            color = "#FFFF00"
        elif feature == "TOPO_DOM":
            color = "#FF4500"
        elif feature == "CONFLICT":
            color = "#40e0d0"
        elif feature == "SIGNAL":
            color = "#800080"
        else:
            print feature
            color = "#FF1493"
        ypos = ypos - height

        for start,end, experimental in features[feature]:
            if experimental:
                rect = plt.Rectangle((start - 0.5, ypos), end-start + 1, height, facecolor=color)
            else:
                rect = plt.Rectangle((start - 0.5, ypos), end-start + 1, height, facecolor=color, hatch='//')
            plt.gca().add_patch(rect)


    #for i in range (0,6):
    fig = plt.gcf()
    fig.set_size_inches(2+ (len(x)/10),4)
    plt.ylim( -10 +ypos, 200)
    plt.xlim( plt.xlim()[0], len(seq_noGap)+1)
    #plt.xlim( (i*200,i*200 + 200))
    plt.tight_layout()
    plt.savefig(os.path.join(paths["pdf"], name + ".pdf"))




def blast(kmerlist, svm, location, tree, protein2location, uniprot, slice,blast, fasta, multiplefastapath, paths, resultfile_info):

    # Variables later used for statistics
    counter = 0.0
    precision = 0.0
    reviewcount = 0
    noreviewcount = 0


    #start with all proteines in the results.txt file
    for query_protein in protein2location:
        #select those that have the desired location
        if protein2location[query_protein] == location:
            #for each protein of the desired location:
            #cleans up the query protein name, removes added additional tags
            #get the uniprot entry
            #from that entry get the sequence
            #use the sequence to blast
            #from the blast get the profile proteines
            #also get the transmembrane regions
            #and get the positions on wich kmers match

            overwrite = False #if override is True, all existent files will be freshly generated

            if location in tree[0]:
                pos_kmerlisting = kmerlist[svm].group0proList #pos_kmerlisting contains all kmers that will be searched for
                neg_kmerlisting = kmerlist[svm].group0conList
            elif location in tree[1]:
                pos_kmerlisting = kmerlist[svm].group1proList #pos_kmerlisting contains all kmers that will be searched for
                neg_kmerlisting = kmerlist[svm].group1conList
            else:
                sys.exit("Did not find location in tree file.")
            query_protein_name, entry, query_sequence, profileProteins, qtmr, qkmers = process_query_protein(query_protein,uniprot, overwrite, fasta, pos_kmerlisting, blast, slice)
            proteinname_sequence =[]
            proteinname_sequence.append( (query_protein_name, query_sequence) )

            for profile_protein in profileProteins:
                #for each profile protein:
                #get the uniprot entry
                #from that entry get the sequence
                #and the transmembrane regions
                #and search for kmers in that sequence

                if query_protein_name == profile_protein:
                    pass
                else:
                    #but only if its not the query protein
                    prof_prot_entry, profileprotein_sequence, tmr, kmers, norev, rev = process_profile_protein(profile_protein, uniprot, pos_kmerlisting, noreviewcount, reviewcount, slice)
                    noreviewcount = norev
                    reviewcount = rev

                    proteinname_sequence.append( (profile_protein, profileprotein_sequence) )

                    #print query_sequence
                    #print qkmers
                    #print profileprotein_sequence
                    #print kmers

                    #random stuff for the homebrewed alignment, that is properbly no longer needed
                    #inside_kmer = False
                    #kmer = ""
                    #for i in range(len(profileprotein_sequence)):
                    #
                    #    if  kmers[i] == " " and not inside_kmer:
                    #        pass
                    #    elif kmers[i] != " ":
                    #        inside_kmer = True
                    #        kmer += profileprotein_sequence[i]
                    #    elif kmers[i] == " " and inside_kmer:
                    #        #kmer = profileprotein_sequence[i - len(kmer)-1] + kmer + profileprotein_sequence[i]
                    #        print kmer
                    #        alignment.align(query_sequence, kmer)
                    #        inside_kmer = False
                    #        kmer = ""

                    if '1' in kmers and '=' in tmr:
                        precision += evaluate(profileprotein_sequence, tmr, kmers)
                        counter += 1.0
                    elif '=' in tmr:
                        print "No kmer hits under these settings, protein is not counted."
                    elif '1' in kmers:
                        #print "protein has no FT TRANSMEM entries that are validated, protein is not counted"
                        pass
                    #alignment.align(query_sequence, profileprotein_sequence)

            write.multiple_fasta(proteinname_sequence, multiplefastapath, overwrite)
            write.mfasta_cleanup(query_protein_name, paths["mfasta"], overwrite)
            write.multiple_sequence_alignment(query_protein_name,paths, overwrite)
            msa = read.multiple_sequence_alignment(query_protein_name, paths)
            pos_matches = kmer_match(pos_kmerlisting, msa)
            neg_matches = kmer_match(neg_kmerlisting, msa)
            transmembrane_regions = read.polyphobius(query_protein_name, paths)

            hit = False
            for name, sequence in msa:
                if name == query_protein_name:
                    create_plot((name,sequence), pos_matches, neg_matches, transmembrane_regions, entry, len(msa), resultfile_info, paths)
                    hit = True
                    break
            print "No hit found!"
            #sys.exit("Stop.")

            # evaluation vor the query sequence
            #print sequence
            #print_sequence(sequence, tmr, kmers)
    #        if '1' in kmers and '=' in tmr:
    #            precision += evaluate(sequence, tmr, kmers)
    #            counter += 1.0
    #        elif '=' in tmr:
    #            print "No kmer hits under these settings, protein is not counted."
    #        elif '1' in kmers:
    #            print "protein has no FT TRANSMEM entries that are validated, protein is not counted"
    #        print ""
    print str(reviewcount) + " entries from swissprot."
    print str(noreviewcount) + " entries from TrEMBL."
    print ""

    if counter > 0:
        print str(precision/counter) +" average prescision over all " + str(int(counter)) + " proteines with uniprot tmr regions."
        return precision/counter
    else:
        print "No counted proteins under this setting ."
        return -1







    #import wx
    #draw_sequence(sequence, transmembrane_regions)

    return None