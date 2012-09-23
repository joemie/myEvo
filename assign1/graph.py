import time
import sys
import random
import os
from graph import *
from decimal import Decimal
#example data structure
#edges = { 1 : [2,3,4], 2: [3,4,5]}
#1 connected to 2, 3, 4
#2 connected to 3, 4, 5
def buildGraph(myFileBuffer):
    edges = {}
    for line in myFileBuffer:
        startNode = line[0:line.index(" ")]
        endNode = line[line.index(" ") + 1:]
        temp = []
        #if the node already exists get the list associated with that edge
        #append to it and then update the edges data structure
        if startNode in edges:
            temp = list(edges.pop(startNode))
            temp.append(endNode)
            edges[startNode] = temp
        else:
            edges[startNode] = list(endNode)
        if endNode in edges:
            temp = list(edges.pop(endNode))
            temp.append(startNode)
            edges[endNode] = temp
        else:
            edges[endNode] = list(startNode)
    return edges


def calculateFitness(edges, cut):
    numCuts = 0
    for key in edges.iterkeys():
        for edgeIndex in range(len(edges[key])):
            value = edges[key][edgeIndex]
            #if start node and end node are in different groups increment numCuts
            if cut[int(key) - 1] != cut[int(value) - 1]:
                numCuts += 1
    if numCuts == 0:
        return float('inf') # the graph wasn't cut so return infinity
    else:
        return float(numCuts / 2) / min(cut.count('0'), cut.count('1'))

