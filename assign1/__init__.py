#import logging
#logging.basicConfig(level=logging.DEBUG, filename=configBuffer[3])
#logging.debug('in de boog')
import time
import sys
import random
import os
from graph import *
from decimal import Decimal

startTime = Decimal(time.time() * 1000)
args = sys.argv[1:]
configFile = None
#load config file
if len(args) == 0:
    configFile = open("default.cfg")
elif os.path.isfile(str(args[0])):
    configFile = open(str(args[0]))
else:
    print "INVALID CONFIG FILE"
    sys.exit()
print configFile
configBuffer = configFile.read().splitlines()
#start parsing the config file
inFile = open(configBuffer[0])
inFileBuffer = inFile.read().splitlines()
logFile = open(str(configBuffer[4]), 'a+')
#seed the random number generator
#if the config file is set to 00 seed with timestamp
if int(configBuffer[1]) == 00:
    seed = startTime
else:
    seed = configBuffer[1]
random.seed(seed)
numRuns = configBuffer[2]
numEvals = configBuffer[3]
solutionFile = open(str(configBuffer[5]), 'a+')
print configFile
print logFile
logFile.write("RESULT LOG \n")
logFile.write("SESSION START : %s" % startTime + "\n")
logFile.write("SESSION SEED  : %s" % seed + "\n")
logFile.write("CONFIG FILE: %s" % inFile + "\n")

numNodes = inFileBuffer[0]
numEdges = inFileBuffer[1]
numCuts = 0
edges = buildGraph(inFileBuffer[2:])
bestCut = []
for i in range(int(numRuns)):
    bestFitness = float('inf')
    logFile.write("RUN: " + str(i + 1) + "\n")
    print("RUN: " + str(i + 1))
    for j in range(int(numEvals) + 1):
        #generate a random cut
        cut = list(bin(random.randrange(2 ** (int(numNodes) - 1), 2 ** int(numNodes)))[2:])
        #tTime = Decimal(time.time() * 1000)
        fitness = calculateFitness(edges, cut)
        #print "CALC FIT: " + str(Decimal(time.time() * 1000) - tTime)
        #update the best fitness if the one found is better
        if fitness < bestFitness:
            bestFitness = fitness
            bestCut = cut
            logFile.write('\t' + str(j + 1) + '\t' + str(fitness) + '\n')
    #log the best solution for each run
    solutionFile.write(str(bestFitness) + "\n")
    solutionFile.write(str(bestCut) + "\n")

solutionFile.close()
inFile.close
endTime = Decimal(time.time() * 1000)
logFile.write("SESSION END   : %s" % endTime + "\n")
logFile.write("SESSION Length: %s" % (endTime - startTime) + "\n")

logFile.close()
print "DONE"
