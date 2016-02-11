#!/usr/bin/env python
# encoding: utf-8
""" This is a non generic version of an APSP calculation for a network. Networks need to be
represented by sequentially numbered nodes starting at 1. This constraint allows faster calculation
than in the generic version since no dictionaries are needed to reference cells in the matrix.
"""
from __future__ import division
import os
import sys
import argparse
import numpy
import networkx as nx
import filehandler as fh

def get_distance_matrix_from_graph(network, filename = None, normalize = False):
  """ Returns and optionally stores the distance matrix for a given network.
  Simple BFS is used for calculation. Be aware that this only works for unweighted networks. 
  Since the implementation uses a Numpy matrix for storing the distances, less memory is needed 
  compared to the NetworkX BFS implementation. Additionally, using sets instead of dicts where
  possible gains some extra performance.
  
  Parameters
  ----------
  network : a NetworkX graph (ATTENTION: nodes need to be sequentially numbered starting at 1!)
  nodelist : list of network nodes to which the distance matrix should be restricted (optional)
  filename : destination for storing the matrix (optional)
  normalize : whether or not the resulting matrix entries should be normalized by dividing by the 
    diameter of the network (default: False)
  
  Returns
  -------
  A Numpy matrix storing all pairs shortest paths for the given network (or the nodes in the given nodelist).
  """

  n = nx.number_of_nodes(network)
  D = numpy.zeros((n,n))

  for n in network:
    level = 0
    levelnodes = {n}
    seen = set()
        
    while levelnodes:
        worklist = levelnodes
        levelnodes = set()
        for target in worklist:
            if target not in seen:
                D[n-1, target-1] = level
                seen.add(target)
                levelnodes.update(network[target])
        level = level + 1
        
  if normalize:
    D = D/float(D.max())

  if filename:
    numpy.savetxt(filename, D, fmt='%s', delimiter=',', newline='\n')

  return D
  
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('network', help="network (as edgelist) for which to calculate APSP")
  parser.add_argument('-n', '--normalize', action='store_true', help="normalize the matrix by dividing all entries by the diameter of the network")
  args = parser.parse_args()

  if not os.path.exists(args.network):
    print "File given by network argument not found."
    sys.exit(128)

  graph = fh.load_from_edge_list(args.network)
  
  if args.normalize:
    ext = "apnp"
  else:
    ext = "apsp"

  filename = "%s.%s" % (args.network, ext)
  
  if not os.path.exists(filename):
    get_distance_matrix_from_graph(graph, filename, args.normalize)   
    
  sys.exit(0)