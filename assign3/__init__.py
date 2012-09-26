#import logging
#logging.basicConfig(level=logging.DEBUG, filename=configBuffer[3])
#logging.debug('in de boog')
#tTime = Decimal(time.time() * 1000)
#fitness = calculateFitness(edges, cut)
#print "CALC FIT: " + str(Decimal(time.time() * 1000) - tTime)
import time
import sys
import random
import os
from graph import *
from arena import *
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
configBuffer = configFile.read().splitlines()
#parse config file
inFile = open(configBuffer[0])
inFileBuffer = inFile.read().splitlines()
logFile = open(str(configBuffer[4]), 'a+')
if int(configBuffer[1]) == 00:
    seed = startTime
else:
    seed = configBuffer[1]
random.seed(seed)
numRuns = configBuffer[2]
numEvals = configBuffer[3]
logFile = open(str(configBuffer[4]), 'a+')
solutionFile = open(str(configBuffer[5]), 'a+')
parentSelType = str(configBuffer[6]).partition("|")[0].strip()
if(parentSelType == "tournament"):
    pTournSize = str(configBuffer[6].partition("|")[2])
else:
    pTournSize = 0
recombType = str(configBuffer[7]).partition("|")[0].strip()
if(recombType == "npoint"):
    numSplits = str(configBuffer[7].partition("|")[2])
else:
    numSplits = 0
survivalStrategy = str(configBuffer[8]).strip()
survivalType = str(configBuffer[9]).partition("|")[0].strip()
if(survivalType == "tournament"):
    survivalTournSize = str(configBuffer[9].partition("|")[2])
else:
    survivalTournSize = 0
evalsUntilTermination = str(configBuffer[10].partition("|")[0])
diversityRange = str(configBuffer[10].partition("|")[2])
populationSize = int(configBuffer[11])
parentSize = int(configBuffer[12])
childrenSize = int(configBuffer[13])
survivalSize = int(configBuffer[14])
print configFile
print logFile
logFile.write("SESSION START : %s" % startTime + "\n")
logFile.write("SESSION SEED  : %s" % seed + "\n")
logFile.write("CONFIG FILE : %s" % inFile + "\n")
if parentSelType == "tournament":
    logFile.write("PARENT SELECTION : %s T-SIZE: %s" % (parentSelType,  str(pTournSize)) + "\n")
else:
    logFile.write("PARENT SELECTION TYPE: %s " % parentSelType + "\n")
logFile.write("SURVIVAL STRATEGY: %s " %survivalStrategy + "\n")
if survivalType == "tournament":
    logFile.write("SURVIVAL SELECTION: %s T-SIZE: %s" % (survivalType, str(survivalTournSize)) + "\n")
else:
    logFile.write("SURVIVAL SELECTION: %s " % survivalType + "\n")
if recombType == "npoint":
    logFile.write("RECOMBINATION: %s  N-SIZE: %s" % (recombType, str(numSplits)) + "\n")
else:
    logFile.write("RECOMBINATION: %s" % recombType + "\n")
logFile.write("MUTATION: BIT FLIP\n")
logFile.write("EVALS UNTIL TERMINATION: %s" %evalsUntilTermination + "\n")
logFile.write("POPULATION SIZE: " + str(parentSize) + "\n")
logFile.write("OFFSPRING SIZE: " + str(childrenSize) + "\n")
numNodes = inFileBuffer[0]
numEdges = inFileBuffer[1]
numCuts = 0
edges = buildGraph(inFileBuffer[2:])
#global is the best in ALL runs
globalBestCut = []
globalBestFitness = float("-inf")
lastEvals = []
for i in range(int(numRuns)):
    #reinitialize the population for each run
    population = initPopulation(populationSize, numNodes)
    #calculate the fitness for each item in the population
    for curIndex in range(len(population)):
        population[curIndex]["fitness"] = calculateFitness(edges, population[curIndex]["cut"],.5)
    runBestFitness = float("-inf")
    #local is the best for each run
    lobalBestCut = []
    lastEvals = []
    logFile.write("RUN: " + str(i + 1) + "\n")
    print("RUN: " + str(i + 1))
    for j in range(int(numEvals)):
        #select parents
        if parentSelType == "tournament":
            parents = tournSelect(edges, population, parentSize, pTournSize, True)
        elif parentSelType == "fitprop":
            parents = fitPropSelect(edges, population, parentSize)
        elif parentSelType == "random":
            print "IN RANDOM"
            #TODO:
        else:
            print "INVALID PARENT SELECTION TYPE"
            sys.exit()
        #make children by recombination
        children = recombinate(edges, parents, recombType, int(numSplits))[0:childrenSize]
        #mutate children
        children = mutate(edges, children)
        #select survivors
        if survivalType == "tournament":
            population = sorted(tournSelect(edges, children + parents, survivalSize, survivalTournSize, False), key=itemgetter("fitness"), reverse=True)
        elif survivalType == "truncation":
            population = sorted(children + parents, key=itemgetter("fitness"), reverse=True)[0:survivalSize]
        elif survivalType == "fitprop":
            print "IN FITPROP"
            #TODO:
        elif survivalType == "random":
            print "IN RANDOM"
            #TODO:
        else:
            print "INVALID SURVIVAL TYPE"
            sys.exit()
        localBestFitness = population[0]["fitness"]
        localAvgFitness = averageFitness(population)
        #update the localBestFitness if needed
        if localBestFitness > runBestFitness:
            lastEvals = []
            runBestFitness = localBestFitness
            runBestCut = population[0]["cut"]
            logFile.write('\t' + str(j + 1) + '\t' + str(localAvgFitness) + "\t" + str(localBestFitness) + '\n')
            logFile.flush()
            #update globalBestFitness if needed
            if runBestFitness > globalBestFitness:
                globalBestFitness = localBestFitness
                globalBestCut = population[0]["cut"]
         #termination condition - reset population if there isn't enough variance
        if len(lastEvals) < evalsUntilTermination:
            lastEvals.append({"bestFitness": localBestFitness, "avgFitness": localAvgFitness})
        else:
            lastEvals.pop(0)
            lastEvals.append({"bestFitness": localBestFitness, "avgFitness": localAvgFitness})
            low = min(item["avgFitness"] for item in lastEvals)
            high = max(item["avgFitness"] for item in lastEvals)
            if high - low <= diversityRange:
                print "RESET: " + str(j)
                population = initPopulation(populationSize, numNodes)
                for curIndex in range(len(population)):
                    population[curIndex]["fitness"] = calculateFitness(edges, population[curIndex]["cut"])
        #write the avg and best fitness for the last evaluation
        if j + 1 == int(numEvals):
            logFile.write('\t' + str(j + 1) + '\t' + str(localAvgFitness) + "\t" + str(localBestFitness) + '\n')
solutionFile.write(str(globalBestFitness) + "\n")
solutionFile.write(str(globalBestCut) + "\n")
print (str(globalBestFitness))
print (str(globalBestCut))
solutionFile.close()
inFile.close
endTime = Decimal(time.time() * 1000)
logFile.write("SESSION END   : %s" % endTime + "\n")
logFile.write("SESSION Length: %s" % (endTime - startTime) + "\n")
logFile.close()
print "DONE"
