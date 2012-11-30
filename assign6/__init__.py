import time
import sys
import random
import os
from decimal import Decimal
from tree import *
from functions import *

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
inFile = configBuffer[0]
logFile = open(str(configBuffer[1]), 'a+')
solnFile = open(str(configBuffer[2]), 'a+')
if int(configBuffer[3]) == 00:
    seed = startTime
else:
    seed = configBuffer[3]
random.seed(seed)
maxTreeDepthInit = int(configBuffer[4])
maxNumNodesInit = 0
for i in range(maxTreeDepthInit):
    maxNumNodesInit += 2**i
maxTreeDepthEvo = int(configBuffer[5])
maxNumNodesEvo = 0
for i in range(maxTreeDepthEvo):
    maxNumNodesEvo += 2**i
numRuns = int(configBuffer[6])
numEvals = int(configBuffer[7])
terminalChance = int(configBuffer[8])

logFile.write("SESSION START : %s\n" % startTime)
logFile.write("SESSION SEED  : %s\n" % seed)
logFile.write("CONFIG FILE: %s\n" % str(configFile))
logFile.write("DATA FILE: %s\n" % str(inFile))
logFile.write("SOLUTION FILE: %s\n" % str(solnFile))

#initialize root node
root = Tree(randomSymbol())
curParent = root
changeParent = 2

root = initializeTree(Tree(randomSymbol()), terminalChance, 0, maxTreeDepthInit)
print "\nNORMAL"
print_tree(root)
print "\nIN_ORDER"
print_tree_inorder(root)
print "\n"
#for i in range(maxNumNodesInit+2): #+2 bc we start at 1
#    print i
#    if i == 0:
#        #root node has already been declared
#        i += 1
#    curNode = Tree()
#    if random.randrange(0,100) <= terminalChance:
#        #terminal
#        curNode.data = random.randrange(0,100)
#    else:
#        curNode.data = randomSymbol()
#    if changeParent == 0:
#        changeParent = 2
#        print "CP"
#    changeParent -= 1


endTime = Decimal(time.time() * 1000)
logFile.write("SESSION END   : %s" % endTime + "\n")
logFile.write("SESSION LENGTH: %s" % (endTime - startTime) + "\n")
logFile.close()
print "DONE"
