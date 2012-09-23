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
tournament | 10 - parent selection (tournament/fitprop/random | tourn Size)
npoint | 3      - recomb type (uniform/npoint | n)
+               - survival strategy (+/,)
tournament | 10 - survival selection (tournament/trunc/random/fitprop | tourn Size)
100             - termination criteria (num evals before termination)
500             - population size
250             - parent size
50              - children size
100             - survival size
1c - Assignment 1c