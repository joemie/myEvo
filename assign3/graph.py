def buildGraph(myFileBuffer):
    edges = {}
    for line in myFileBuffer:
        startNode = line[0:line.index(" ")]
        endNode = line[line.index(" ") + 1:]
        temp = []
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
