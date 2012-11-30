import random
from tree import *
def randomSymbol():
    symbols = ["+", "-", "*", "/","pow"]
    return random.choice(symbols)


def initializeTree(tree, terminalChance, depth, maxTreeDepth):
    if depth == maxTreeDepth:
        return
    if depth == maxTreeDepth - 2:
        newSymbol = random.randrange(0,100)
    elif random.randrange(0,100) <= terminalChance:
        newSymbol = random.randrange(0,100)
    else:
        newSymbol = randomSymbol()
    print "LEFT " + " : " + str(depth) + " : " + str(newSymbol)
    tree.left = initializeTree(Tree(newSymbol), terminalChance, depth + 1, maxTreeDepth)
    if depth == maxTreeDepth - 2:
        newSymbol = random.randrange(0,100)
    elif random.randrange(0,100) <= terminalChance:
        newSymbol = random.randrange(0, 100)
    else:
        newSymbol = randomSymbol()
    print "RIGHT " + " : " + str(depth) + " : " + str(newSymbol)
    tree.right = initializeTree(Tree(newSymbol), terminalChance, depth + 1, maxTreeDepth)
    return tree

def print_tree(tree):
    if tree == None: return
    print tree.data,
    print_tree(tree.left)
    print_tree(tree.right)


def print_tree_inorder(tree):
    if tree == None: return

    print_tree_inorder(tree.left)
    print tree.data,
    print_tree_inorder(tree.right)
