import sys
import random
from operator import itemgetter


def initPopulation(popSize, strSize):
    pop = []
    for i in range(popSize):
        pop.append({"cut": list(bin(random.randrange(2 ** (int(strSize) - 1), 2 ** int(strSize)))[2:]), "fitness": 0, "cutCount": 0, "vertCount":0, "evalCount": 0})
    return pop


def averageFitness(population):
    totalFitness = 0
    popSize = 0
    for i in range(len(population)):
        curFit = population[i]["fitness"]
        #only increase the total fitness if a cut was actually made
        if curFit != float("-inf"):
            totalFitness += curFit
            popSize = popSize + 1
    return totalFitness / popSize


def tournSelect(population, survivalSize, tournSize, replacement, objectiveType, penaltyCoefficient = 0):
    selected = []
    tPopulation = population[:]
    if replacement == True:
        uid = 0
        for i in range(int(survivalSize)):
            tournSelect = []
            #build a tournament by selecting random items in the popuation
            for j in range(int(tournSize)):
                popIndex = random.randint(0, len(population) - 1)
                if objectiveType == "SOEA":
                    tournSelect.append(population[popIndex])
                if objectiveType == "MOEA":
                     tournSelect.append({"cut" : population[popIndex]["cut"] , "fitness": population[popIndex]["fitness"], "cutCount":  population[popIndex]["cutCount"], "vertCount":  population[popIndex]["vertCount"], "domLevel": population[popIndex]["domLevel"], "uid": uid})
                uid += 1
            #select the most fit in the tournament
            if objectiveType == "SOEA":
                tournSelect = sorted(tournSelect, key=itemgetter('fitness'), reverse=True)
            elif objectiveType == "MOEA":
                tournSelect = sorted(tournSelect, key=itemgetter("domLevel"), reverse=False)
            else:
                print "INVALID OBJECTIVE TYPE\n"
                sys.exit()
            selected.append(tournSelect[0])
    else:
        uid = 0
        for i in range(int(survivalSize)):
            tournSelect = []
            #build a tournament by selecting random items in the popuation
            for j in range(int(tournSize)):
                if len(tPopulation) > 1:
                    popIndex = random.randint(0, len(tPopulation) - 1)
                    if objectiveType == "SOEA":
                        tournSelect.append({"cut" : tPopulation[popIndex]["cut"] , "fitness":  tPopulation[popIndex]["fitness"], "cutCount": tPopulation[popIndex]["cutCount"], "vertCount": tPopulation[popIndex]["vertCount"], "uid": uid})
                    if objectiveType == "MOEA":
                        tournSelect.append({"cut" : tPopulation[popIndex]["cut"] , "fitness":  tPopulation[popIndex]["fitness"], "cutCount": tPopulation[popIndex]["cutCount"], "vertCount": tPopulation[popIndex]["vertCount"], "uid": uid, "domLevel": tPopulation[popIndex]["domLevel"]})
                    uid += 1
                else:
                    print "CUT TOURNAMENT POPULATION EMPTY"
                    sys.exit()
            del tPopulation[popIndex]
            #select the most fit in the tournament
            if objectiveType == "SOEA":
                tournSelect = sorted(tournSelect, key=itemgetter('fitness'), reverse=True)
            elif objectiveType == "MOEA":
                tournSelect = sorted(tournSelect, key=itemgetter("domList"), reverse=False)
            else:
                print "INVALID OBJECTIVE TYPE\n"
                sys.exit()
            selected.append(tournSelect[0])
    return selected


def randomSelect(population, size):
    selected = []
    for i in range(int(size)):
        selected.append(random.choice(population))
    return selected


def fitPropSelect(population, survivalSize):
    propPop = []
    totalFitness = 0
    for i in range(len(population)):
        curFit = population[i]["fitness"]
        #only increase the fitness if a cut was made
        if curFit != float("-inf"):
            totalFitness += curFit
            propPop.append({"cut": population[i]["cut"], "fitness": curFit})
    #fitness proportion = fitness(element) / sum(fitness(all elements))
    for i in range(len(propPop)):
        propPop[i]["propFit"] = propPop[i]["fitness"] / totalFitness
    propPop = sorted(propPop, key=itemgetter("propFit"))
    return propPop[0:survivalSize]


def recombinate(parents, recombType, objectiveType, numSplits = None, penaltyCoefficient = 0):
    children = []
    if recombType == "npoint" and numSplits == None:
        print "INVALID CALL TO RECOMBINATE - SPLIT SIZE NOT SPECIFIED"
    elif recombType == "npoint" and numSplits != None:
        if len(parents[0]['cut']) < numSplits:
            print "INVALID CALL TO RECOMBINATE - SPLIT SIZE TOO LARGE"
        else:
            #split size of 2
            #000011110000 - p1
            #111111111111 - p2
            #001111110011 - child
            pCutSize = len(parents[0]['cut'])
            maxSplitRange = pCutSize / numSplits + 1
            for index in range(len(parents) - 1):
                parent0 = parents[index]['cut']
                parent1 = parents[index + 1]['cut']
                splitStart = 0
                curParent = 0
                curPosition = 0
                cut = []
                for i in range(numSplits):
                    splitEnd = splitStart + random.randrange(maxSplitRange * i, maxSplitRange * (i + 1))
                    splitSize = splitEnd - splitStart
                    if curParent == 0:
                        cut[curPosition:] = parent0[curPosition:curPosition + splitSize]
                        curParent = 1
                    else:
                        cut[curPosition:] = parent1[curPosition:curPosition + splitSize]
                        curParent = 0
                    curPosition += splitSize
                    splitStart += splitSize
                if curPosition < pCutSize:
                    if curParent == 0:
                        cut[curPosition:] = parent0[curPosition:]
                    else:
                        cut[curPosition:] = parent1[curPosition:]
                children.append({"cut": cut, "fitness": 0, "cutCount": 0, "vertCount": 0, "evalCount": 0, "uid": index})
#            splitSize = len(parents[0]['cut']) / numSplits
#            for i in range(len(parents) - 1):
#                parent1 = parents[i]['cut']
#                parent2 = parents[i + 1]['cut']
#                cut = []
#                curParent = 1
#                curPosition = 0
#                while curPosition < len(parent1):
#                    if curParent == 1:
#                        cut[curPosition:] = parent1[curPosition:curPosition + splitSize]
#                        curParent = 0
#                    else:
#                        cut[curPosition:] = parent2[curPosition:curPosition + splitSize]
#                        curParent = 1
#                    curPosition += splitSize
#                fitnessList = calculateFitness(edges, cut, penaltyCoefficient)
#                children.append({"cut" :cut, "fitness": fitnessList[0], "cutCount": fitnessList[1], "vertCount": fitnessList[2]})
    elif recombType == "uniform":
        for i in range(len(parents) - 1):
            parent1 = parents[i]['cut']
            parent2 = parents[i + 1]['cut']
            cut = []
            #list of binary numbers that is the same length as a parent
            #if the element is 0 append parent1[element]
            splitList= list(bin(random.randrange(2 ** (int(len(parent1)) - 1), 2 ** int(len(parent1))))[2:])
            for j in range(len(splitList)):
                if j == 0:
                    cut.append(parent1[j])
                else:
                    cut.append(parent2[j])
            children.append({"cut": cut, "fitness": 0, "cutCount":0, "vertCount": 0, "evalCount": 0, "uid": i})
    else:
        print "INVALID RECOMBINATION TYPE IN CONFIG FILE"
    return children


def mutate(population, objectiveType, penaltyCoefficient):
    for i in range(len(population)):
        numMutations = random.randrange(0,len(population[0]["cut"]))
        for j in range(numMutations):
            #pick a random index to flip
            index = random.randrange(0, len(population[0]["cut"]))
            if population[i]["cut"][index] == '0':
                population[i]["cut"][index] = '1'
            else:
                population[i]["cut"][index] = '0'
        population[i]["fitness"] = 0
        population[i]["cutCount"] = 0
        population[i]["vertCount"] = 0
        population[i]["evalCount"] = 0
    return population
#    only 1 call to random but slower
#    for i in range(len(population)):
#        #generate a list of binaries flip the element if flipList[j] is 1
#        flipList = list(bin(random.randrange(2 ** (int(len(population[0]["cut"])) - 1), 2 ** int(len(population[0]["cut"]))))[2:])
#        for j in range(len(flipList)):
#            if flipList[j] == '1' and population[i]["cut"][j] == '0':
#                population[i]["cut"][j] = '1'
#            elif flipList[j] == '1' and population[i]["cut"][j] == '1':
#                population[i]["cut"][j] = '0'
#        fitnessList = calculateFitness(edges, population[i]["cut"], penaltyCoefficient)
#        population[i]["fitness"] = fitnessList[0]
#        population[i]["cutCount"] = fitnessList[1]
#        population[i]["vertCount"] = fitnessList[2]
#    return population


def calculateFitness(edges, cut, penaltyCoefficient = 0):

    numCuts = 0
    if penaltyCoefficient == 0:
        #there is no penalty for an unconnected subgraph
        for key in edges.iterkeys():
            for edgeIndex in range(len(edges[key])):
                value = edges[key][edgeIndex]
                if cut[int(key) - 1] != cut[int(value) - 1]:
                    numCuts += 1
        #[fitness, [numerator, denominator]]
        if numCuts == 0:
            return [float("-inf"), float("inf"), float("-inf")]
        else:
            return [float(numCuts / 2) / min(cut.count('0'), cut.count('1')) * -1, float(numCuts / 2), min(cut.count('0'), cut.count('1'))]
    else:
        #penalize an unconnected subgraph
        tempGraph0 = countSubgraphsAndCuts(edges, cut, '0')
        tempGraph1 = countSubgraphsAndCuts(edges, cut, '1')
        numZeroSubgraphs = tempGraph0[0]
        numZeroCuts = tempGraph0[1]
        numOneSubgraphs = tempGraph1[0]
        numOneCuts = tempGraph1[1]
        numCuts = numZeroCuts + numOneCuts
        numSubgraphs = numZeroSubgraphs + numOneSubgraphs
        #[fitness, [numerator, denominator]]
        if numCuts == 0:
            return [float("-inf"), float("inf"), float("-inf")]
        elif numSubgraphs == 2:
            return [(float(numCuts / 2) / min(cut.count('0'), cut.count('1')) * -1), float(numCuts / 2), min(cut.count('0'), cut.count('1'))]
        else:
            return [(float(numCuts / 2) / min(cut.count('0'), cut.count('1')) * -1) - (numSubgraphs * float(penaltyCoefficient)), float(numCuts / 2), min(cut.count('0'), cut.count('1'))]


def countSubgraphsAndCuts(edges, cut, graph):
    numSubgraphs = 0
    exploredNodes = [0]*len(cut)
    edgeIter = edges.iterkeys()
    curNode = int(edgeIter.next())
    curNodeGraph = cut[curNode - 1]
    numCuts = 0
    if cut.count(graph) >= 1:
        #ensures the node belongs to the correct graph
        while curNodeGraph != graph:
            try:
                curNode = int(edgeIter.next())
            except:
                return [int(numSubgraphs), int(numCuts)]
            curNodeGraph = cut[curNode - 1]
        reachable = [curNode]
        explorable = []

        #loop until all nodes in the graph are explored
        while exploredNodes.count(1) < cut.count(graph):
            for edgeIndex in range(len(edges[curNode])):
                adjacentNode = int(edges[curNode][edgeIndex])
                if cut[adjacentNode - 1] == curNodeGraph and adjacentNode not in reachable:
                    reachable.append(adjacentNode)
                    explorable.append(adjacentNode)
                if cut[adjacentNode - 1] != curNodeGraph:
                    numCuts += 1
            exploredNodes[curNode - 1] = 1
            while len(explorable) > 0:
                curNode = explorable.pop()
                curNodeGraph = cut[curNode - 1]
                for edgeIndex in range(len(edges[curNode])):
                    adjacentNode = int(edges[curNode][edgeIndex])
                    if cut[adjacentNode - 1] == curNodeGraph and adjacentNode not in reachable:
                        reachable.append(adjacentNode)
                        explorable.append(adjacentNode)
                    if cut[adjacentNode - 1] != curNodeGraph:
                        numCuts += 1
                exploredNodes[curNode - 1] = 1
            if exploredNodes.count(1) < cut.count(graph):
                try:
                    curNode = int(edgeIter.next())
                except StopIteration:
                    return [int(numSubgraphs), int(numCuts)]
                curNodeGraph = cut[curNode - 1]
                while curNodeGraph != graph or exploredNodes[curNode -1] == 1:
                    try:
                        curNode = int(edgeIter.next())
                    except StopIteration:
                        return [int(numSubgraphs), int(numCuts)]
                    curNodeGraph = cut[curNode - 1]
                reachable = [curNode]
                explorable = []
            numSubgraphs += 1
    return [int(numSubgraphs), int(numCuts)]


def sortByDomination(population):
    domList = calculateDominationList(population)
    for i in range(len(domList)):
        curLevel = domList[i]
        for j in range(len(curLevel)):
            population[curLevel[j]["uid"]]["domLevel"] = i
    return sorted(population, key=itemgetter("domLevel"), reverse = False)



def calculateDominationList(population):
    domList = determineDomination(population)
    domLevels = []
    topLevel = []
    for curIndy in domList:
        if len(curIndy["dominatedBy"]) == 0:
            topLevel.append(curIndy)
            domList.remove(curIndy)
    domLevels.append(topLevel)
    domLevels.append([])
    while(len(domList) > 0):
        curIndy = domList.pop(0)
        for i in range(1, len(domLevels)):
            curLevel = domLevels[i]
            validLevel = True
            if len(curLevel) == 0:
                curLevel.append(curIndy)
                break
            #check if any individuals in the level dominate the current individual
            for j in range(len(curLevel)):
                levelIndy = curLevel[j]
                if curIndy["uid"] in levelIndy["dominates"]:
                    validLevel = False
                    break
            if validLevel:
                #check if curIndy dominates any individuals in the level, remove them
                for levelIndy in curLevel:
                    if levelIndy["uid"] in curIndy["dominates"]:
                        curLevel.remove(levelIndy)
                        domList.append(levelIndy)
                curLevel.append(curIndy)
            elif i == len(domLevels)-1:
                domLevels.append([curIndy])
    return domLevels


def determineDomination(population):
    domList = []
    for i in range(len(population)):
        curIndy = population[i]
        curDomList = {"uid": curIndy["uid"], "dominates": [], "dominatedBy": []}
        for j in range(len(population)):
            if i != j:
                nextIndy = population[j]
                if dominates(curIndy, nextIndy):
                    #curIndy dominates nextIndy
                    curDomList["dominates"].append(nextIndy["uid"])
                elif dominates(nextIndy, curIndy):
                    #nextIndy dominates curIndy
                    curDomList["dominatedBy"].append(nextIndy["uid"])
        domList.append(curDomList)
    return domList


def dominates(challenger, individual):
    if challenger["cutCount"] < individual["cutCount"] and challenger["vertCount"] > individual["vertCount"]:
        return True
    else:
        return False



