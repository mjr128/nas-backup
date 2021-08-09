#!/usr/bin/python3

class Disk:
    letter = ''
    name = ''
    totalSize = 0
    usedSize = 0
    freeSize = 0
    partitionID = 0
    
    def __init__(self, letter, name, totalSize, usedSize, freeSize, partitionID):
        self.letter = letter
        self.totalSize = totalSize
        self.usedSize = usedSize
        self.freeSize = freeSize
        self.partitionID = partitionID

