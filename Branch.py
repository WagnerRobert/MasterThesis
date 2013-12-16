__author__ = 'delur'


class Branch(object):
    svm = ""
    branch = []

    group0proList = []
    group0conList = []
    group1proList = []
    group1conList = []

    def __init__(self, svm, branch, group0proList, group0conList, group1proList, group1conList):
        self.svm = svm
        self.branch = branch
        self.group0proList = group0proList
        self.group0conList = group0conList
        self.group1proList = group1proList
        self.group1conList = group1conList