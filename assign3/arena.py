import random
from operator import itemgetter


def initPopulation(popSize, strSize):
    pop = []
    for i in range(popSize):
        pop.append({"cut": list(bin(random.randrange(2 ** (int(strSize) - 1), 2 ** int(strSize)))[2:])})
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


def tournSelect(edges, population, survivalSize, tournSize, replacement, penaltyCoefficient = 0):
    selected = []
    if replacement == True:
        for i in range(int(survivalSize)):
            tournSelect = []
            #build a tournament by selecting random items in the popuation
            for j in range(int(tournSize)):
                popIndex = random.randint(0, len(population) - 1)
                tournSelect.append({"cut" : population[popIndex]["cut"] , "fitness": calculateFitness(edges, population[popIndex]["cut"], penaltyCoefficient)})
            #select the most fit in the tournament
            tournSelect = sorted(tournSelect, key=itemgetter('fitness'), reverse=True)
            selected.append(tournSelect[0])
    else:
        for i in range(int(survivalSize)):
            tournSelect = []
            #build a tournament by selecting random items in the popuation
            for j in range(int(tournSize)):
                popIndex = random.randint(0, len(population) - 1)
                tournSelect.append({"cut" : population[popIndex]["cut"] , "fitness": calculateFitness(edges, population[popIndex]["cut"], penaltyCoefficient)})
            del population[popIndex]
            #select the most fit in the tournament
            tournSelect = sorted(tournSelect, key=itemgetter('fitness'), reverse=True)
            selected.append(tournSelect[0])
    return selected


def fitPropSelect(edges, population, survivalSize):
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


def recombinate(edges, parents, recombType, numSplits = None, penaltyCoefficient = 0):
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
            splitSize = len(parents[0]['cut']) / numSplits
            for i in range(len(parents) - 1):
                parent1 = parents[i]['cut']
                parent2 = parents[i + 1]['cut']
                cut = []
                curParent = 1
                curPosition = 0
                while curPosition < len(parent1):
                    if curParent == 1:
                        cut[curPosition:] = parent1[curPosition:curPosition + splitSize]
                        curParent = 0
                    else:
                        cut[curPosition:] = parent2[curPosition:curPosition + splitSize]
                        curParent = 1
                    curPosition += splitSize
                children.append({"cut" :cut, "fitness": calculateFitness(edges, cut, penaltyCoefficient)})
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
            children.append({"cut": cut, "fitness": calculateFitness(edges, cut, penaltyCoefficient)})
    else:
        print "INVALID RECOMBINATION TYPE IN CONFIG FILE"
    return children


def mutate(edges, population, penaltyCoefficient):
    for i in range(len(population)):
        numMutations = random.randrange(0,len(population[0]["cut"]))
        for j in range(numMutations):
            #pick a random index to flip
            index = random.randrange(0, len(population[0]["cut"]))
            if population[i]["cut"][index] == '0':
                population[i]["cut"][index] = '1'
            else:
                population[i]["cut"][index] = '0'
        population[i]["fitness"] = calculateFitness(edges, population[i]["cut"], penaltyCoefficient)
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
#        population[i]["fitness"] = calculateFitness(edges, population[i]["cut"], penaltyCoefficient)
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
        if numCuts == 0:
            return float("-inf")  # the graph wasn't cut so return infinity
        else:
            return float(numCuts / 2) / min(cut.count('0'), cut.count('1')) * -1
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
        if numCuts == 0:
            return  float("-inf")  # the graph wasn't cut so return infinity
        else:
            return (float(numCuts / 2) / min(cut.count('0'), cut.count('1')) * -1) - (numSubgraphs * float(penaltyCoefficient))


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
            curNode = int(edgeIter.next())
            curNodeGraph = cut[curNode - 1]
        reachable = [curNode]
        explorable = []

        #loop until all nodes in the graph are explored
        while exploredNodes.count(1) < cut.count(graph):
            for edgeIndex in range(len(edges[str(curNode)])):
                adjacentNode = int(edges[str(curNode)][edgeIndex])
                if cut[adjacentNode - 1] == curNodeGraph and adjacentNode not in reachable:
                    reachable.append(adjacentNode)
                    explorable.append(adjacentNode)
                if cut[adjacentNode - 1] != curNodeGraph:
                    numCuts += 1
                   # print "%d : %d" %(curNode, adjacentNode)
            exploredNodes[curNode - 1] = 1

            while len(explorable) > 0:
                curNode = explorable.pop()
                curNodeGraph = cut[curNode - 1]
                for edgeIndex in range(len(edges[str(curNode)])):
                    adjacentNode = int(edges[str(curNode)][edgeIndex])
                    if cut[adjacentNode - 1] == curNodeGraph and adjacentNode not in reachable:
                        reachable.append(adjacentNode)
                        explorable.append(adjacentNode)
                    if cut[adjacentNode - 1] != curNodeGraph:
                        #print "%d : %d" %(curNode, adjacentNode)
                        numCuts += 1
                exploredNodes[curNode - 1] = 1
            if exploredNodes.count(1) < cut.count(graph):
                curNode = int(edgeIter.next())
                curNodeGraph = cut[curNode - 1]
                while curNodeGraph != graph or exploredNodes[curNode -1] == 1:
                    curNode = int(edgeIter.next())
                    curNodeGraph = cut[curNode - 1]
                reachable = [curNode]
                explorable = []
            numSubgraphs += 1
    return [int(numSubgraphs), int(numCuts)]
