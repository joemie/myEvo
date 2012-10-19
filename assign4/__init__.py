
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
objectiveType = str(configBuffer[6]);
penaltyCoefficient = str(configBuffer[7])
parentSelType = str(configBuffer[8]).split("|")[0].strip()
if(parentSelType == "tournament"):
    pTournSize = str(configBuffer[8].split("|")[1])
    pReplace = str(configBuffer[8].split("|")[2]).strip()
else:
    pTournSize = 0
recombType = str(configBuffer[9]).split("|")[0].strip()
if(recombType == "npoint"):
    numSplits = str(configBuffer[9].split("|")[1])
else:
    numSplits = 0
survivalStrategy = str(configBuffer[10]).strip()
survivalType = str(configBuffer[11]).split("|")[0].strip()
if(survivalType == "tournament"):
    survivalTournSize = str(configBuffer[11].split("|")[1])
    survivalReplace = str(configBuffer[11].split("|")[2]).strip()
else:
    survivalTournSize = 0
evalsUntilTermination = str(configBuffer[12].split("|")[0])
diversityRange = str(configBuffer[12].split("|")[1])
populationSize = int(configBuffer[13])
parentSize = int(configBuffer[14])
childrenSize = int(configBuffer[15])
survivalSize = int(configBuffer[16])

print configFile
print logFile
logFile.write("SESSION START : %s\n" % startTime)
logFile.write("SESSION SEED  : %s\n" % seed)
logFile.write("CONFIG FILE : %s\n" % inFile)
if parentSelType == "tournament":
    logFile.write("PARENT SELECTION : %s T-SIZE: %s REPLACE: %s\n" % (parentSelType,  str(pTournSize),pReplace))
else:
    logFile.write("PARENT SELECTION TYPE: %s \n" % parentSelType)
logFile.write("SURVIVAL STRATEGY: %s \n" % survivalStrategy)
if survivalType == "tournament":
    logFile.write("SURVIVAL SELECTION: %s T-SIZE: %s REPLACE: %s\n" % (survivalType, str(survivalTournSize), survivalReplace))
else:
    logFile.write("SURVIVAL SELECTION: %s " % survivalType + "\n")
if recombType == "npoint":
    logFile.write("RECOMBINATION: %s  N-SIZE: %s\n" % (recombType, str(numSplits)))
else:
    logFile.write("RECOMBINATION: %s\n" % recombType)
logFile.write("MUTATION: BIT FLIP\n")
logFile.write("EVALS UNTIL TERMINATION: %s\n" % evalsUntilTermination)
logFile.write("POPULATION SIZE: %s\n" % str(parentSize))
logFile.write("OFFSPRING SIZE: %s\n" % str(childrenSize))
numNodes = inFileBuffer[0]
numEdges = inFileBuffer[1]
numCuts = 0
edges = buildGraph(inFileBuffer[2:])
#global is the best in ALL runs
globalBestCut = []
globalBestFitness = float("-inf")
lastEvals = []
for i in range(int(numRuns)):
    runStart =  Decimal(time.time() * 1000)
    #reinitialize the population for each run
    population = initPopulation(populationSize, numNodes)
    #calculate the fitness for each item in the population
    for curIndex in range(len(population)):
        fitnessList = calculateFitness(edges, population[curIndex]["cut"], penaltyCoefficient)
        population[curIndex]["fitness"] = fitnessList[0]
        population[curIndex]["cutCount"] = fitnessList[1]
        population[curIndex]["vertCount"] = fitnessList[2]
        population[curIndex]["uid"] = curIndex
    #sort the population by levels of dominance
    if objectiveType == "MOEA":
        population = sortByDomination(population)
    runBestFitness = float("-inf")
    #local is the best for each run
    runBestCut = []
    lastEvals = []
    logFile.write("RUN: " + str(i + 1) + "\n")
    print("RUN: " + str(i + 1))
    for j in range(int(numEvals)):
        #select parents
        if parentSelType == "tournament":
            if pReplace == "r":
                parents = tournSelect(edges, population, parentSize, pTournSize, True, objectiveType, penaltyCoefficient)
            elif pReplace in 'nr':
                parents = tournSelect(edges, population, parentSize, pTournSize, False, objectiveType, penaltyCoefficient)
            else:
                print "INVALID PARENT SELECTION PARAMETER"
                sys.exit()
        elif parentSelType == "fitprop":
            parents = fitPropSelect(edges, population, parentSize)
        elif parentSelType == "random":
            parents = randomSelect(population, parentSize)
        else:
            print "INVALID PARENT SELECTION TYPE"
            sys.exit()
        #make children by recombination
        children = recombinate(edges, parents, recombType, objectiveType, int(numSplits), penaltyCoefficient)[0:childrenSize]
        #mutate children
        children = mutate(edges, children, objectiveType, penaltyCoefficient)
        #set the population depending on the survival strategy
        if survivalStrategy == "+":
            population = children + parents
        elif survivalStrategy == "-":
            population = children
        else:
            print "INVALID SURVIVAL STRATEGY"
            sys.exit()

        #select survivors
        if survivalType == "tournament":
            if survivalReplace == "r":
                population = sorted(tournSelect(edges, population, survivalSize, survivalTournSize, True, objectiveType, penaltyCoefficient), key=itemgetter("fitness"), reverse=True)
            elif survivalReplace == "nr":
                population = sorted(tournSelect(edges, population, survivalSize, survivalTournSize, False, objectiveType, penaltyCoefficient), key=itemgetter("fitness"), reverse=True)
            else:
                print "INVALID SURVIVAL SELECTION PARAMETER"
                sys.exit()
        elif survivalType == "truncation":
            population = sorted(population, key=itemgetter("fitness"), reverse=True)[0:survivalSize]
        elif survivalType == "fitprop":
            population = sorted(fitPropSelect(edges, population, survivalSize), key=itemgetter("fitness"), reverse=True)
        elif survivalType == "random":
            population = sorted(randomSelect(population, size), key=itemgetter("fitness"), reverse=True)
        else:
            print "INVALID SURVIVAL TYPE"
            sys.exit()
        localBestFitness = population[0]["fitness"]
        localAvgFitness = averageFitness(population)
        logFile.write('\t' + str(j + 1) + "\t" + str(localAvgFitness) + "\t" + str(localBestFitness) + "\n")
        logFile.flush()
        #update the runBestFitness if needed
        if localBestFitness > runBestFitness:
            lastEvals = []
            runBestFitness = localBestFitness
            runBestCut = population[0]["cut"]
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
                    fitnessList = calculateFitness(edges, population[curIndex]["cut"], penaltyCoefficient)
                    population[curIndex]["fitness"] = fitnessList[0]
                    population[curIndex]["cutCount"] = fitnessList[1]
                    population[curIndex]["vertCount"] = fitnessList[2]
                    population[curIndex]["uid"] = curIndex
        #write the avg and best fitness for the last evaluation
        if j + 1 == int(numEvals):
            logFile.write('\t' + str(j + 1) + '\t' + str(localAvgFitness) + "\t" + str(localBestFitness) + '\n')
    runEnd =  Decimal(time.time() * 1000)
    print runEnd - runStart
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
