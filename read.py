import os

__author__ = 'delur'


def blast(name, blast):
    f = open (os.path.join(blast, name + ".blast"), 'r')

    run3 = False

    ProfileProteines = []

    for line in f:
        if "round 3" in line:
            run3 = True
        if run3:
            if line.startswith("tr|") or line.startswith("sp|"):
                ProfileProteines.append(line.split('|')[1])
            elif  "|" in line and  not line.startswith(">"):
                print line
    f.close()
    return ProfileProteines
