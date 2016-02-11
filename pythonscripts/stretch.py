#!/usr/bin/env python
# encoding: utf-8
from __future__ import division
from pprint import pprint
import os
import sys
import argparse
import numpy
import networkx as nx
import filehandler as fh
import get_apsp as apsp

def is_spanning_tree(tree, network = None, source = 1, draw = True):
  #S = nx.dfs_tree(tree, source).to_undirected()

  if network and tree.number_of_nodes() != network.number_of_nodes():
    print "Tree has %d of %d necessary nodes." % (tree.number_of_nodes(), network.number_of_nodes())
    return False

  if len(nx.connected_components(tree)) > 1:
    print "Tree is actually a forest."
    return False

  if tree.number_of_edges() != (tree.number_of_nodes() - 1):
    print "Tree contains at least one cycle. |E|=|V|-1 does not hold."
    return False

  return True

def get_stretch(network, h, d): # Undirected networks!
  ''' Calculates `stretch` for given distance matrices (h=spanningtree, d=network). '''
  n = network.number_of_nodes()
  T, total = numpy.empty(shape=(n, n)), 0

  for source in network.nodes_iter():
    for target in network.nodes_iter():
      i, j = source-1, target-1
      if source != target:
        local_tau = h[i,j] / d[i,j]
        total += local_tau
     
      #  T[i][j] = local_tau
       # print "-"
      #else:
        # Local stretch is only defined for distinct nodes i,j
      #  T[i][j] = 0

  global_stretch = (1.0 / (n * (n - 1))) * total
  #print "%d Nodes, Global Stretch: %3.5f" % (n, global_stretch)
  return global_stretch#, T

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--network', required=True)
  parser.add_argument('--tree',    required=True)
  args = parser.parse_args()

  assert os.path.exists(args.network), ""

  if not os.path.exists(args.network):
    print "File given by --network not found."
    sys.exit(128)

  if not os.path.exists(args.tree):
    print "File given by --tree not found."
    sys.exit(128)


  graph = fh.load_from_edge_list(args.network)

  filename = "%s.%s" % (args.network, "apsp")

  if os.path.exists(filename):
    D = numpy.loadtxt(filename, delimiter=",")
   # print "Loaded from file."
  else:
    D = apsp.get_distance_matrix_from_graph(graph, filename)

 # pprint(D)

  tree = fh.load_from_edge_list(args.tree)

  if not is_spanning_tree(tree):
    print "Given tree %s is not a spanning tree." % tree
    sys.exit(10)

  H = apsp.get_distance_matrix_from_graph(tree)

 # pprint(H)

  # Write the tau matrix to disk and print the global stretch to stdout.
  #global_stretch, local_stretch = get_stretch(graph, H, D)
  global_stretch = get_stretch(graph, H, D)
  # tau_matrix_f = "%s-tau.txt" % args.tree

 # pprint(local_stretch)

  # numpy.savetxt(tau_matrix_f, local_stretch, fmt='%.5f', delimiter=",", newline="\n")
  print "%.5f" % global_stretch
  sys.exit(0)
