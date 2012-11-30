import random
import sys
from operator import itemgetter
def buildGraph(numNodes):
    edges = {}
    edgeFlags = list(bin(random.randrange(2 ** (11025), 2 ** 11026))[2:])
    flagIndex = 0
    for i in range(1, numNodes):
        edges[i] = []
    for i in range(1,numNodes):
        for j in range(i+1, numNodes):
            if int(edgeFlags[flagIndex]) == 1:
                edges[i].append(j)
                edges[j].append(i)
            flagIndex += 1
    return edges

def mutateGraph(edges):
    mutationValues = map(int, str(random.randrange(2 ** (1000), 2 ** 1001)))
    mutationIndex = 0
    for i in range(1, len(edges)):
        for j in range(i+1, len(edges)):
            if(mutationValues[mutationIndex] == 0 and mutationValues[mutationIndex+1] == 0):
                #small chance of deleting all edges
                for index in range(len(edges[i])):
                    edges[edges[i][index]].remove(i)
                edges[i] = []
            if(j in edges[i] and mutationValues[mutationIndex] < 3):
                #large chance of deleting an edge
                edges[i].remove(j)
                edges[j].remove(i)
            if(j not in edges[i] and mutationValues[mutationIndex] < 3):
                #large chance of adding an edge
                edges[i].append(j)
                edges[j].append(i)
            mutationIndex += 1
            #make sure not to run off the end of the list
            if(mutationIndex >= len(mutationValues) - 1):
                mutationIndex = 0
    return edges

def recombinateGraphs(graph1, graph2):
    child = {}
    for i in range(1, len(graph1)+1):
        child[i] = []
    for i in range(1, len(graph1)+1):
        g1Node = graph1[i]
        g2Node = graph2[i]
        for j in range(i, len(graph2)+1):
            if j in g1Node:
                g1Flag = True
            else:
                g1Flag = False
            if j in g2Node:
                g2Flag = True
            else:
                g2Flag = False
            if g1Flag and g2Flag:
                child[i].append(j)
                child[j].append(i)
            elif g1Flag and not g2Flag:
                #chance to add edge
                bit = random.getrandbits(1)
                if bit == 1:
                    child[i].append(j)
                    child[j].append(i)
            elif g2Flag and not g1Flag:
                #chance to add edge
                bit = random.getrandbits(1)
                if bit == 1:
                    child[i].append(j)
                    child[j].append(i)
    return child

def randomSelectGraphs(population, size):
    selected = []
    for i in range(int(size)):
        selected.append(random.choice(population))
    return selected

def tournSelectGraphs(population, survivalSize, tournSize, replacement):
    selected = []
    tPopulation = population[:]
    if replacement == True:
        for i in range(int(survivalSize)):
            tournSelect = []
            #build a tournament by selecting random items in the popuation
            for j in range(int(tournSize)):
                popIndex = random.randint(0, len(tPopulation) - 1)
                tournSelect.append(tPopulation[popIndex])
            #select the most fit in the tournament
            tournSelect = sorted(tournSelect, key=itemgetter("fitness"), reverse=True)
            selected.append(tournSelect[0])
    else:
        for i in range(int(survivalSize)):
            tournSelect = []
            #build a tournament by selecting random items in the popuation
            for j in range(int(tournSize)):
                if(len(tPopulation) > 1):
                    popIndex = random.randint(0, len(tPopulation) - 1)
                    tournSelect.append(tPopulation[popIndex])
                else:
                    print "GRAPH TOURNAMENT POPULATION EMPTY"
                    sys.exit()
            del tPopulation[popIndex]
            #select the most fit in the tournament
            tournSelect = sorted(tournSelect, key=itemgetter("fitness"), reverse=True)
            selected.append(tournSelect[0])
    return selected
