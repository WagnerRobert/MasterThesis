import sys

__author__ = 'delur'


def print_array(alignement_array, query_sequence, profileprotein_sequence):
    first_line = "\t\t"
    for i in range(len(query_sequence) ):
        first_line+= query_sequence[i] + "\t"
    print first_line

    for i in range(len(profileprotein_sequence )+1):
        if i == 0:
            row_sequence = "\t"
        else:
            row_sequence = profileprotein_sequence[i-1] + "\t"
        for cloumn in alignement_array[i]:
            row_sequence += str(cloumn) + "\t"
        print row_sequence.rstrip()


def traceBack(query_sequence, profileprotein_sequence, alignement_array, match, mismatch, gap):
    best_alignments = []
    highest_score = 0
    for y in range(len(profileprotein_sequence) ):
        for x in range(len(query_sequence)):
            if alignement_array[y+1][x+1] > highest_score:
                highest_score = alignement_array[y+1][x+1]
                best_alignments = []
                best_alignments.append( (y,x))
            elif alignement_array[y+1][x+1] == highest_score:
                best_alignments.append( (y,x))

    print best_alignments
    print highest_score

    aligned_query = ""
    aligned_profprot = ""

    y = 0
    x = 0
    for yxtuple in best_alignments:
        y = yxtuple[0]
        x = yxtuple[1]
        aligned_query = ""
        aligned_profprot = ""
        curScore = alignement_array[y][x]
        while  curScore != 0:
            if alignement_array[y-1][x-1] +match ==  alignement_array[y][x] or alignement_array[y-1][x-1] + mismatch  ==  alignement_array[y][x]:

                aligned_query = query_sequence[x] + aligned_query
                aligned_profprot = profileprotein_sequence[y] + aligned_profprot
                x -= 1
                y -= 1
            elif alignement_array[y][x-1] +gap ==  alignement_array[y][x]:
                aligned_query = query_sequence[x] + aligned_query
                aligned_profprot = "-" + aligned_profprot
                x -= 1
            else:
                sys.exit("HUGE FAIL.")
            curScore = alignement_array[y][x]

        aligned_query = query_sequence[x] + aligned_query
        aligned_profprot = profileprotein_sequence[y] + aligned_profprot

        print aligned_query
        print aligned_profprot

def align(query_sequence, profileprotein_sequence):
    print query_sequence
    print profileprotein_sequence

    match = 2
    mismatch = -2
    gap = -1

    alignement_array = [[0 for x in xrange(len(query_sequence)+1)] for x in xrange(len(profileprotein_sequence)+1)]

    for y in range(len(profileprotein_sequence)):
        for x in range( len(query_sequence) ):

            match_mismatch =  alignement_array[y][x] + (match if query_sequence[x] == profileprotein_sequence[y] else mismatch)
            gap_in_profseq =  alignement_array[y+1][x] + gap

            score = match_mismatch if match_mismatch > gap_in_profseq else gap_in_profseq

            alignement_array[y+1][x+1] = score if score > 0 else 0

    #print alignement_array
    print_array(alignement_array, query_sequence, profileprotein_sequence)

    traceBack(query_sequence,profileprotein_sequence, alignement_array, match, mismatch, gap)


    return None