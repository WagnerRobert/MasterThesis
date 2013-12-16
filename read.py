import os

__author__ = 'delur'


def blast(name, blast):
    f = open (os.path.join(blast, name + ".blast"))

    run3 = False

    ProfileProteines = []

    for line in f:
        if "round 3" in line:
            if line.startswith("tr|") or line.startswith("sp|"):
                ProfileProteines.append(line.split('|')[1])
    return ProfileProteines
