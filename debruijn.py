import numpy as np
import networkx as nx

from time import time

class DeBruijnGraph:

    def __init__(self, n):
        """ Creates the nodes and edges for a De Bruijn graph over GF(2) with parameter n dictating the size of the nodes.

            For example, if you need De Bruijn sequences with 1024 distinct subsequences, then each subsequence will require 10 bits, so n=10.

            De Bruijn sequences are constructed by creating an (n-1)-D De Bruijn Graph, whose nodes are each a distinct binary value from 0 to n-1, 
            and edges represent valid transitions in a De Bruijn sequence. We then use networkx to compute an Eulerian circuit from the graph, which then
            is used to construct a De Bruijn sequence. This process is fairly computationally intensive, with trials of (n=21) taking around 2 minutes per sequence.

        Args:
            n (int): Length of each subsequence within the desired De Bruijn sequence. 
        """

        self.n = n
        self.k = n - 1
        self.bit_mask =  (1 << (self.k)) - 1
        
        self.vertices = np.arange(2**self.k)

        e1 = ((self.vertices << 1) + 1) & self.bit_mask
        e2 = (self.vertices << 1) & self.bit_mask

        possible = np.array([np.vstack([self.vertices, e1, np.repeat(1, len(e1))]), np.vstack([self.vertices, e2, np.repeat(0, len(e2))])])
        edges = np.hstack(possible).T

        self.edges = np.array([*map(tuple, edges)])

    def shuffle_db_graph(self):
        """
            Returns a networkx DiGraph() implementing a De Bruijn graph. 

            Edges are added in a random permutation so we can find unique De Bruijn sequences.
        """

        np.random.shuffle(self.edges)

        G = nx.DiGraph()
        G.add_weighted_edges_from(self.edges)
        return G 

    def gen_multiple_sequences(self, n):
        """ 
            Returns n unique De Bruijn sequences according to the configuration defined by the underlying class.

            Constructs multiple De Bruijn graphs and uses networkx to compute an Eulerian circuit for each graph. 
            From that circuit, a De Bruijn sequence is generated.
        """

        seqs = []
        for i in range(n):
            
            # generate random DB graph
            G = self.shuffle_db_graph()

            # find eulerian path, construct sequence from the edge links
            seqPath = nx.eulerian_path(G)
            seq = self.seq_from_path(G, seqPath)

            seqs.append(seq)

        return seqs

    def seq_from_path(self, G, path):
        """ 
            Generates a De Bruijn sequence from a given path and De Bruijn graph.
        """

        debruijn = ''.join(map(str, (G.get_edge_data(*e)['weight'] for e in path)))
        debruijn += debruijn[:self.k]
        return debruijn

    def gen_indices_from_sequence(self, sequence, k):
        """
            Generates a list of indices (memory addresses) from a given De Bruijn sequence.
        """

        return [int(sequence[i:i+k], 2) for i in range(0, len(sequence) - k)]


if __name__ == "__main__":
    n = 5
    dbg = DeBruijnGraph(n)
    s = time()
    seqs = dbg.gen_multiple_sequences(100)
    inds = dbg.gen_indices_from_sequence(seqs[0], n)
    print(time() - s)
    with open(f"{n}-bit_sequences.txt", 'w') as dbfile:
        for seq in seqs:
            dbfile.write(f'{seq}\n')

