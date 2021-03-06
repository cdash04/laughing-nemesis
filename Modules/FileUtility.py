#!/usr/bin/python

import sys
import glob
from BiologicalAbundanceContigObject import *

def checkFiles(listOfFile):
    for i in listOfFile:
        if not isValid(i):
            raise IOError.error("File"+str(i)+"can't be opened")

def isValid(file_name):
    valid = True
    try:
        a = open(file_name, 'r')
        a.close()
    except:
        valid = False
    return valid

def countLines(file_name):
    lines = 0
    try:
        for i in open(file_name):
            lines += 1
    except:
        lines = 0
    if lines == 0:
        raise IOError("File "+str(file)+" is empty")
    return lines

def testValidity():
    if len(sys.argv)==3:
        try:
            directory = sys.argv[1]
            numberOfBestMatch = int(sys.argv[2])
        except:
            print(__doc__)
            sys.exit(1)
    elif len(sys.argv) == 4:
        try:
            directory = sys.argv[1]
            pathToContigsIdFile = sys.argv[3]
            tempFile = open(pathToContigsIdFile, 'r')
            tempFile.close()
            numberOfBestMatch = int(sys.argv[2])
        except:
            print(__doc__)
            sys.exit(1)
    else:
        print(__doc__)
        sys.exit(1)
    try:
        tempFile = open(directory+"/_DeNovoAssembly/Contigs.tsv", 'r')
        tempFile.close()
    except:
        IOError("Unable to open: "+directory+"/_DeNovoAssembly/Contigs.tsv")
        sys.exit(1)

def readPathsFile(pathToContigsIdFile):
    #TODO: verifier que si les fichiers ont ou non le ContigIdentifications.tsv a la fin.
    contigIdentificationsFiles = []
    try:
        tempfile = open(pathToContigsIdFile,'r')
        tempfile.close()
    except:
        raise IOError("Unable to open: "+pathToContigsIdFile)
    for lines in open(pathToContigsIdFile, 'r'):
        contigIdentificationsFiles.append(lines[0:len(lines)-1])
    return contigIdentificationsFiles

def getPathsFromDirectory(directory):
    command = "find "+directory+"| grep ContigIdentifications.tsv"
    files = glob.glob(directory+"/*/ContigIdentifications.tsv")
    return files

def readContigsTSVfile(pathToFile):
    directory = pathToFile+"/_DeNovoAssembly/Contigs.tsv"
    biologicalAbundanceContigs = {}
    for lines in open(directory, 'r'):
        if lines == "":
            break
        elif lines[0] == "#":
            continue
        else:
            name = lines.split()[0]
            length = int(lines.split()[2])
            coloredKmer = int(lines.split()[3])
            coverage_depth = int(lines.split()[5])
            newBiologicalAbundanceContig = BiologicalAbundanceContigObject(name,length,coloredKmer, coverage_depth)
            #print(name);
            biologicalAbundanceContigs[name] = newBiologicalAbundanceContig
    return biologicalAbundanceContigs

def readContigIdentificationFiles(files, biologicalAbundanceContigs):
    for line in open(files, 'r'):
        if line == "":
            break
        if line[0] == '#':
            continue
        else:
            try:
                contigName = line.split()[0]
                sequenceName = line.split('\t')[6]
                sequenceLength = int(line.split('\t')[7])
                matches = int(line.split('\t')[8])
                biologicalAbundanceContigs[contigName].addNewContigIdentification(sequenceName,
                                                                                  sequenceLength,
                                                                                  matches)
            except:
                message = "File: " + \
                          files + \
                          " can not be read or do not correspond to the usual patern." + \
                          " It has been discarded"
                warning(message)
def read_fasta_file(fasta):
    sequences = {}
    name = ""
    for line in open(fasta, 'r'):
        if line[0] == ">":
            name = line[1:].split()[0]
            sequences[name] = ""
        else:
            sequences[name] += line
    return sequences
