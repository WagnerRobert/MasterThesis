__author__ = 'delur'


def print_array(alignement_array, query_sequence, profileprotein_sequence):
    first_line = "    "
    for i in range(len(query_sequence) ):
        first_line+= query_sequence[i] + " "
    print first_line

    for i in range(len(profileprotein_sequence )+1):
        if i == 0:
            row_sequence = "  "
        else:
            row_sequence = profileprotein_sequence[i-1] + " "
        for cloumn in alignement_array[i]:
            row_sequence += str(cloumn) + " "
        print row_sequence.rstrip()


def traceBack(query_sequence, profileprotein_sequence, alignement_array):
    best_alignments = []
    highest_score = 0
    for y in range(len(profileprotein_sequence) ):
        for x in range(len(query_sequence)):
            if alignement_array[y][x] > highest_score:
                highest_score = alignement_array[y][x]
                best_alignments = []
                best_alignments.append( (y,x))
            elif alignement_array[y][x] == highest_score:
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
        curScore = alignement_array[y][x]
        while  curScore != 0:
            if alignement_array[y-1][x-1] > alignement_array[y-1][x]:
                aligned_query = query_sequence[x] + aligned_query
                aligned_profprot = profileprotein_sequence[y] + aligned_profprot
                x -= 1
                y -= 1
            else:
                aligned_query = query_sequence[x] + aligned_query
                aligned_profprot = "-" + aligned_profprot
                y -= 1
            curScore = alignement_array[y][x]

        print aligned_query
        print aligned_profprot

def align(query_sequence, profileprotein_sequence):
    print query_sequence
    print profileprotein_sequence

    match = 1
    mismatch = 0
    gap = -1

    alignement_array = [[0 for x in xrange(len(query_sequence)+1)] for x in xrange(len(profileprotein_sequence)+1)]

    for y in range(len(profileprotein_sequence)):
        for x in range( len(query_sequence) ):

            match_mismatch =  alignement_array[y][x] + (match if query_sequence[x] == profileprotein_sequence[y] else mismatch)
            gap_in_profseq =  alignement_array[y][x+1] + gap

            score = match_mismatch if match_mismatch > gap_in_profseq else gap_in_profseq

            alignement_array[y+1][x+1] = score if score > 0 else 0

    #print alignement_array
    print_array(alignement_array, query_sequence, profileprotein_sequence)

    traceBack(query_sequence,profileprotein_sequence, alignement_array)


    return None