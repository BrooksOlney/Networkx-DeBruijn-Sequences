# Networkx-DeBruijn-Sequences

This repository provides a python script that uses numpy and networkx to generate unique binary (k=2) De Bruijn sequences (https://en.wikipedia.org/wiki/De_Bruijn_sequence). This is done by constructing a De Bruijn graph with a single parameter, _n_, which defines the desired length of every substring in the De Bruijn sequence. 

### De Bruijn Graphs
A De Bruijn graph (https://en.wikipedia.org/wiki/De_Bruijn_graph) is a directed graph that represents the overlaps between length-_n_ sequences of _m_ symbols. In our case, we are only working with binary, so we only have 2 symbols (_m=2_). A binary De Bruijn graph has 2<sup>n</sup> vertices which correspond to all possible binary sequences of length-_n_ and edges where valid De Bruijn transitions occur. A valid transition occurs when we take the value of the current vertex and shift it left by one, then append a new bit to the rightmost side, forming the value of another vertex. For example, if we set _n=4_ then one vertex would be at _1010_ and it would have edges with vertices _0100_ and _0101_. Note that in this example, the edges would be labeled 0 and 1 respectively.

To find sequences from the De Bruijn graph, we must compute Hamiltonian Cycles. However, these are difficult to compute, but we can reduce the problem to solving for Eulerian Cycles within an (_n - 1_)-D De Bruijn graph. This allows us to use built-in functions in networkx to find sequences.

# Dependencies
* Python 3+ 
* Numpy 1.20.1
* Networkx 2.5.1

# How to Run
Currently there is just one main script, debruijn.py, which has a main function that defines how large _n_ is, and how many sequences to generate. However you can import the class into another script and use it as you see fit.