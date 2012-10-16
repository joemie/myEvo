currently all paths are relative 

--------------------
CONFIG FILE FORMAT |
--------------------
\dataFiles\example.dat  -data file
7               - seed
5               - numRuns
100             - numEvals
\logFiles\logEx.txt    -log file
\solnFiles\solutionEx.txt -solution file
.05             - penalty coefficient for an unconnected graph
tournament | 10 | r - parent selection (tournament/fitprop/random | tourn Size | r/nr) r = replacement nr = no replacement
npoint | 3      - recomb type (uniform/npoint | n)
+               - survival strategy (+/,)
tournament | 10 | r - survival selection (tournament/trunc/random/fitprop | tourn Size | tourn Size | r/nr) r = replacement nr = no replacement
100             - termination criteria (num evals before termination | diversity)
500             - population size
250             - parent size
50              - children size
100             - survival size
1c - Assignment 1c