import random
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
    for i in range(1, len(edges)):
        for j in range(i+1, len(edges)):
            print "DERP"
    return edges
