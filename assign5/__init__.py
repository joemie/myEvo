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
from random import choice
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
numNodes = int(configBuffer[0])
graphPopSize = int(configBuffer[1])
if int(configBuffer[2]) == 00:
    seed = startTime
else:
    seed = configBuffer[2]
random.seed(seed)
numRuns = configBuffer[3]
numEvals = configBuffer[4]
logFile = open(str(configBuffer[5]), 'a+')
solutionFile = open(str(configBuffer[6]), 'a+')
objectiveType = str(configBuffer[7])
penaltyCoefficient = str(configBuffer[8])
parentSelType = str(configBuffer[9]).split("|")[0].strip()
if(parentSelType == "tournament"):
    pTournSize = str(configBuffer[9].split("|")[1])
    pReplace = str(configBuffer[9].split("|")[2]).strip()
else:
    pTournSize = 0
recombType = str(configBuffer[10]).split("|")[0].strip()
if(recombType == "npoint"):
    numSplits = str(configBuffer[10].split("|")[1])
else:
    numSplits = 0
survivalStrategy = str(configBuffer[11]).strip()
survivalType = str(configBuffer[12]).split("|")[0].strip()
if(survivalType == "tournament"):
    survivalTournSize = str(configBuffer[12].split("|")[1])
    survivalReplace = str(configBuffer[12].split("|")[2]).strip()
else:
    survivalTournSize = 0
evalsUntilTermination = str(configBuffer[13].split("|")[0])
diversityRange = str(configBuffer[13].split("|")[1])
populationSize = int(configBuffer[14])
parentSize = int(configBuffer[15])
childrenSize = int(configBuffer[16])
survivalSize = int(configBuffer[17])
samplingSize = int(configBuffer[18])
parentSelTypeGraph = str(configBuffer[19]).split("|")[0].strip()
if(parentSelType == "tournament"):
    pTournSizeGraph = str(configBuffer[19].split("|")[1])
    pReplaceGraph = str(configBuffer[19].split("|")[2]).strip()
else:
    pTournSizeGraph = 0
survivalStrategyGraph = str(configBuffer[20]).strip()
survivalTypeGraph = str(configBuffer[21]).split("|")[0].strip()
if(survivalTypeGraph == "tournament"):
    survivalTournSizeGraph = str(configBuffer[21].split("|")[1])
    survivalReplaceGraph = str(configBuffer[21].split("|")[2]).strip()
else:
    survivalTournSizeGraph = 0
parentSizeGraph = int(configBuffer[22])
childrenSizeGraph = int(configBuffer[23])
survivalSizeGraph = int(configBuffer[24])
solutionFileGraph = open(str(configBuffer[25]), 'a+')

print configFile
print logFile

logFile.write("SESSION START : %s\n" % startTime)
logFile.write("SESSION SEED  : %s\n" % seed)
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
logFile.write("GRAPH POPULATION SIZE: %s\n" % str(graphPopSize))
logFile.write("SAMPLING SIZE %s\n" % str(samplingSize))
if parentSelTypeGraph == "tournament":
    logFile.write("PARENT SELECTION : %s T-SIZE: %s REPLACE: %s\n" % (parentSelTypeGraph,  str(pTournSizeGraph), pReplaceGraph))
else:
    logFile.write("PARENT SELECTION TYPE: %s \n" % parentSelTypeGraph)
logFile.write("GRAPH SURVIVAL STRATEGY: %s \n" % survivalStrategyGraph)
if survivalTypeGraph == "tournament":
    logFile.write("GRAPH SURVIVAL SELECTION: %s T-SIZE: %s REPLACE: %s\n" % (survivalTypeGraph, str(survivalTournSizeGraph), survivalReplaceGraph))
else:
    logFile.write("GRAPH SURVIVAL SELECTION: %s " % survivalTypeGraph + "\n")

graphs = []

#global is the best in ALL runs
bestParetoFront = []
globalBestCut = []
globalBestFitness = float("-inf")
globalBestAvgFitness = float("-inf")
globalBestFitnessGraph = float("-inf")
globalBestAvgFitnessGraph = float("-inf")
globalBestGraph = {}
lastEvals = []
for i in range(int(numRuns)):
    runStart =  Decimal(time.time() * 1000)
    #reinitialize the population for each run
    population = initPopulation(populationSize, numNodes)
    for index in range(graphPopSize):
        graphs.append({"edges":buildGraph(numNodes), "fitness": 0, "evalCount": 0})
    #calculate the fitness for each item in the cut population
    for curIndex in range(populationSize):
        for graphIndex in range(int(graphPopSize * (samplingSize/100.0))):  #this is 10
            tempGraph = choice(graphs)
            tempCut = choice(population)
            #make sure a graph isn't evaluatied more than the sampling size allows
            t = 0
            while(tempGraph["evalCount"] == int(samplingSize * 2)):
                tempGraph = choice(graphs)
                t += 1
                if t % 10000 == 0:
                    print "TOP TOP"

            #make sure a cut isn't evaluatied more than the sampling size allows
            t = 0
            while(tempCut["evalCount"] == int(samplingSize * 2)):
                tempCut = choice(population)
                t += 1
                if t % 10000 == 0:
                    print "TOP BOT"
            fitnessList = calculateFitness(tempGraph["edges"], population[curIndex]["cut"], penaltyCoefficient)
            tempCut["fitness"] += fitnessList[0]
            tempCut["cutCount"] += fitnessList[1]
            tempCut["vertCount"] += fitnessList[2]
            tempGraph["fitness"] += fitnessList[0]
            tempGraph["evalCount"] += 1
            tempCut["evalCount"] += 1
    #make the fitness of a graph an average and inverse
    for index in range(graphPopSize):
        if graphs[index]["evalCount"] != 0:
            graphs[index]["fitness"] = 1/(graphs[index]["fitness"] / graphs[index]["evalCount"])
            graphs[index]["evalCount"] = 0
    #make the fitness of a cut an average
    for index in range(len(population)):
        if population[index]["evalCount"] != 0:
            population[index]["fitness"] = population[index]["fitness"] / population[index]["evalCount"]
            population[index]["cutCount"] = population[index]["cutCount"] / population[index]["evalCount"]
            population[index]["vertCount"] = population[index]["vertCount"] / population[index]["evalCount"]
            population[index]["evalCount"] = 0
    #sort the cut population by levels of dominance
    if objectiveType == "MOEA":
        population = sortByDomination(population)
    #local is the best for each run
    runBestFitness = float("-inf")
    runBestFitnessGraph = float("-inf")
    runBestCut = []
    runBestGraph = []
    lastEvals = []
    logFile.write("RUN: " + str(i + 1) + "\n")
    print("RUN: " + str(i + 1))
    j = 0
    while j < int(numEvals):
        if parentSelTypeGraph == "tournament":
            if pReplace == "r":
                graphParents = tournSelectGraphs(graphs, parentSizeGraph, pTournSizeGraph, True)
            elif pReplace == "nr":
                graphParents = tournSelectGraphs(graphs, parentSizeGraph, pTournSizeGraph, False)
            else:
                print "INVALID PARENT SELECTION PARAMETER"
                sys.exit()
        elif parentSelTypeGraph == "random":
            graphParents = randomSelect(graphs, parentSizeGraph)
        else:
            print "INVALID PARENT SELECTION TYPE FOR GRAPHS"
            sys.exit()
        #select cut cutParents
        if parentSelType == "tournament":
            if pReplace == "r":
                cutParents = tournSelect(population, parentSize, pTournSize, True, objectiveType, penaltyCoefficient)
            elif pReplace in 'nr':
                cutParents = tournSelect(population, parentSize, pTournSize, False, objectiveType, penaltyCoefficient)
            else:
                print "INVALID PARENT SELECTION PARAMETER"
                sys.exit()
        elif parentSelType == "fitprop":
            cutParents = fitPropSelect(edges, population, parentSize)
        elif parentSelType == "random":
            cutParents = randomSelect(population, parentSize)
        else:
            print "INVALID PARENT SELECTION TYPE"
            sys.exit()
        #make graph children by recombination
        graphChildren = []
        for newIndex in range(len(graphParents) - 1):
            graphChildren.append({"edges": recombinateGraphs(graphParents[newIndex]["edges"], graphParents[newIndex+1]["edges"]), "evalCount": 0})
        #make cut children by recombination
        children = recombinate(cutParents, recombType, objectiveType, int(numSplits), penaltyCoefficient)[0:childrenSize]
        #mutate graph children
        for index in range(len(graphChildren)):
            graphChildren[index]["edges"] =  mutateGraph(graphChildren[index]["edges"])
            graphChildren[index]["fitness"] = 0
            graphChildren[index]["evalCount"] = 0
        #mutate cut children
        children = mutate(children, objectiveType, penaltyCoefficient)
        if objectiveType == "MOEA":
            children = sortByDomination(children)
        #set the cut population depending on the survival strategy
        if survivalStrategy == "+":
            population = children + cutParents
        elif survivalStrategy == "-":
            population = children
        else:
            print "INVALID SURVIVAL STRATEGY"
            sys.exit()
        if survivalStrategyGraph == "+":
            graphPopulation = graphChildren + graphParents
        elif survivalStrategyGraph == "-":
            graphPopulation = graphChildren
        else:
            print "INVALID SURVIVAL STRATEGY GRAPH"
            sys.exit()
        #calculate the fitness for each item in the cut population
        for curIndex in range(len(population)):
            for graphIndex in range(int(len(graphPopulation) * (samplingSize/100.0))):
                tempGraph = choice(graphPopulation)
                tempCut = choice(population)
                #make sure a graph isn't evaluatied more than the sampling size allows
                t = 0
                while(tempGraph["evalCount"] == samplingSize):
                    tempGraph = choice(graphPopulation)
                    t += 1
                    if t % 10000 == 0:
                        print "BOT TOP"
                #make sure a cut isn't evaluatied more than the sampling size allows
                t = 0
                while(tempCut["evalCount"] == samplingSize*2):
                    tempCut = choice(population)
                    t += 1
                    if t % 10000 == 0:
                        print "BOT BOT"
                fitnessList = calculateFitness(tempGraph["edges"], population[curIndex]["cut"], penaltyCoefficient)
                tempCut["fitness"] += fitnessList[0]
                tempCut["cutCount"] += fitnessList[1]
                tempCut["vertCount"] += fitnessList[2]
                tempGraph["fitness"] += fitnessList[0]
                tempGraph["evalCount"] += 1
                tempCut["evalCount"] += 1
                #increment number of evals
                j += 1
        #make the fitness of a graph an average and inverse
        for index in range(len(graphPopulation)):
            if graphPopulation[index]["evalCount"] != 0:
                graphPopulation[index]["fitness"] = 1/(graphPopulation[index]["fitness"] / graphPopulation[index]["evalCount"])
                graphPopulation[index]["evalCount"] = 0
        #make the fitness of a cut an average
        for index in range(len(population)):
            if population[index]["evalCount"] != 0:
                population[index]["fitness"] = population[index]["fitness"] / population[index]["evalCount"]
                population[index]["cutCount"] = population[index]["cutCount"] / population[index]["evalCount"]
                population[index]["vertCount"] = population[index]["vertCount"] / population[index]["evalCount"]
                population[index]["evalCount"] = 0
        #select cut survivors
        if survivalType == "tournament":
            if survivalReplace == "r":
                population = tournSelect(population, survivalSize, survivalTournSize, True, objectiveType, penaltyCoefficient)
            elif survivalReplace == "nr":
                population = tournSelect(population, survivalSize, survivalTournSize, False, objectiveType, penaltyCoefficient)
            else:
                print "INVALID SURVIVAL SELECTION PARAMETER"
                sys.exit()
            if objectiveType == "SOEA":
                population = sorted(population, key=itemgetter("fitness"), reverse=True)
            if objectiveType == "MOEA":
                population = sorted(population, key=itemgetter("domLevel"), reverse=False)
        elif survivalType == "truncation":
            if objectiveType == "SOEA":
                population = sorted(population, key=itemgetter("fitness"), reverse=True)[0:survivalSize]
            if objectiveType == "MOEA":
                population = sorted(population, key=itemgetter("domLevel"), reverse=False)[0:survivalSize]
        elif survivalType == "fitprop":
            population = sorted(fitPropSelect(edges, population, survivalSize), key=itemgetter("fitness"), reverse=True)
        elif survivalType == "random":
            population = sorted(randomSelect(population, size), key=itemgetter("fitness"), reverse=True)
        else:
            print "INVALID SURVIVAL TYPE"
            sys.exit()
        localBestFitness = population[0]["fitness"]
        localBestFitnessGraph = graphPopulation[0]["fitness"]
        localAvgFitness = averageFitness(population)
        localAvgFitnessGraph = averageFitness(graphPopulation)
        logFile.write('\t' + str(j + 1) + "\t" + str(localAvgFitness) + "\t" + str(localBestFitness) + "\t" + str(localAvgFitnessGraph) + "\t" + str(localBestFitnessGraph) + "\n")
        logFile.flush()
        #update the cut runBestFitness if needed
        if localBestFitness > runBestFitness:
            lastEvals = []
            runBestFitness = localBestFitness
            runBestCut = population[0]["cut"]
            #update cut globalBestFitness if needed
            if runBestFitness > globalBestFitness:
                globalBestFitness = localBestFitness
                globalBestCut = population[0]["cut"]
        #update the graph runBestFitness if needed
        if localBestFitnessGraph > runBestFitnessGraph:
            runBestFitnessGraph = localBestFitnessGraph
            runBestGraph = graphPopulation[0]["edges"]
            if runBestFitnessGraph > globalBestFitnessGraph:
                globalBestFitnessGraph = localBestFitnessGraph
                solutionFileGraph.write(str(localBestFitnessGraph) + "\n")
                solutionFileGraph.write(str(runBestGraph) + "\n")
                globalBestGraph = graphPopulation[0]["edges"]
        if globalBestAvgFitness < localAvgFitness:
            solutionFile.write("NEW BEST: " + str(localAvgFitness) + "\n")
            globalBestAvgFitness = localAvgFitness
            for newIndex in range(len(population)):
                curIndy = population[i]
                if objectiveType == "MOEA":
                    if curIndy["domLevel"] == 0:
                        bestParetoFront.append(curIndy)
                        solutionFile.write(str(bestParetoFront[newIndex]["cutCount"]) + "\t" + str(bestParetoFront[newIndex]["vertCount"]) + "\t" + str(bestParetoFront[newIndex]["fitness"]) + "\t" + str(bestParetoFront[newIndex]["cut"]) + "\n")
                    else:
                        break
        if globalBestAvgFitnessGraph < localAvgFitnessGraph:
            globalBestAvgFitnessGraph = localAvgFitnessGraph
        #termination condition - reset cut population if there isn't enough variance
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
        #write the avg and best cut fitness for the last evaluation
        if j + 1 == int(numEvals):
            logFile.write('\t' + str(j + 1) + '\t' + str(localAvgFitness) + "\t" + str(localBestFitness) + '\n')
    runEnd =  Decimal(time.time() * 1000)
    print "TIME: " + str(runEnd - runStart) + "\n"
if objectiveType == "SOEA":
    solutionFile.write(str(globalBestFitness) + "\n")
    solutionFile.write(str(globalBestCut) + "\n")
    solutionFileGraph.write(str(globalBestFitnessGraph) + "\n")
    solutionFileGraph.write(str(globalBestGraph) + "\n")
    print (str(globalBestFitness))
    print (str(globalBestCut))
    solutionFile.close()
if objectiveType == "MOEA":
    solutionFileGraph.write(str(globalBestFitnessGraph) + "\n")
    solutionFileGraph.write(str(globalBestGraph) + "\n")
    for i in range(len(bestParetoFront)):
        solutionFile.write(str(bestParetoFront[i]["cutCount"]) + "\t" + str(bestParetoFront[i]["vertCount"]) + "\t" + str(bestParetoFront[i]["fitness"]) + "\t" + str(bestParetoFront[i]["cut"]) + "\n")
endTime = Decimal(time.time() * 1000)
logFile.write("SESSION END   : %s" % endTime + "\n")
logFile.write("SESSION Length: %s" % (endTime - startTime) + "\n")
logFile.close()
print "DONE"
