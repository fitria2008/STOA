#!/usr/bin/env python
# encoding: utf-8
""" This is a non generic version of an APSP calculation for a network using the NetworkX package. 
Networks need to be represented by sequentially numbered nodes starting at 1. This constraint allows 
faster calculation than in the generic version since no dictionaries are needed to reference cells in 
the matrix.
"""
from __future__ import division
import os
import sys
import argparse
import numpy
import networkx as nx
import filehandler as fh

def get_distance_matrix_from_graph(network, filename = None, floyd = True):
  """ Returns and optionally stores the distance matrix for a given network. 
  By default the networkX BFS implementation is used.
      
  Parameters
  ----------
  network : a NetworkX graph (ATTENTION: nodes need to be sequentially numbered starting at 1!)
  filename : destination for storing the matrix (optional)
  floyd : set to true to use floyd warshall instead of BFS
  
  Returns
  -------
  A Numpy matrix storing all pairs shortest paths for the given network (or the nodes in the given nodelist).
  """

  n = nx.number_of_nodes(network)
  if floyd:
    D = nx.floyd_warshall_numpy(network)
  else:
    D_dict = nx.all_pairs_shortest_path_length(network)
    D = numpy.zeros((n,n))
    for row, col_dict in D_dict.iteritems():
        for col in col_dict:
            D[row-1,col-1] = col_dict[col]
    
  if filename:
    numpy.savetxt(filename, D, fmt='%s', delimiter=",", newline="\n")

  return D
  
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--network', required=True)
  args = parser.parse_args()

  assert os.path.exists(args.network), ""

  if not os.path.exists(args.network):
    print "File given by --network not found."
    sys.exit(128)

  graph = fh.load_from_edge_list(args.network)

  filename = "%s.%s" % (args.network, "apsp")
  
  if not os.path.exists(filename):
    get_distance_matrix_from_graph(graph, filename, False)
    
  sys.exit(0)