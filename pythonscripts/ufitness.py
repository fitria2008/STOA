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
  S = nx.dfs_tree(tree, source).to_undirected()

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

def get_local_fitness(m_set, mt_set, debug = False):
  ''' Returns the local fitness for the two given sets M & M_T (see paper).'''
  _intersection = mt_set.intersection(m_set)
  local_fitness = len(_intersection) / len(mt_set)
  
  if debug:
    pprint({ 'M': m_set, 'M_T': mt_set, 'intersection': _intersection, 'localfitness': local_fitness }, width=80)

  return local_fitness

def get_shortest_neighbour_set(target, dist_graph, G, neighbours):
  neighbour_set = set([])
  for neighbour in neighbours:
    if dist_graph > 1:
      if G[neighbour-1, target-1] == dist_graph-1:
        neighbour_set.add(neighbour)

    else:
      if neighbour == target:
        neighbour_set.add(neighbour)
  
  return neighbour_set

def get_local_tree_fitness(network, D, tree, H, debug = False):
  n = network.number_of_nodes()
  F, total = numpy.empty(shape=(n, n)), 0

  for source in network.nodes_iter():
    for target in network.nodes_iter():
      neighbours_net = network.neighbors_iter(source)
      neighbours_tree = tree.neighbors_iter(source)
      
      dist_net = D[source-1, target-1]
      dist_tree = H[source-1, target-1]
     
      if source != target:
        # print "-- Checking neighbours... --"
        m_set = get_shortest_neighbour_set(target, dist_net, D, neighbours_net)            
        mt_set = get_shortest_neighbour_set(target, dist_tree, H, neighbours_tree)
        
        local_fitness = get_local_fitness(m_set,mt_set)
       # F[source-1][target-1] = local_fitness
        total += local_fitness

  local_tree_fitness = (1.0 / (n * (n - 1))) * total
 
 # pprint(F)

  return local_tree_fitness#, F

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
  # fitness, fitness_matrix = get_local_tree_fitness(graph, D, tree, H, debug = False)
  fitness = get_local_tree_fitness(graph, D, tree, H, debug = False)

 # pprint(fitness_matrix)

  # numpy.savetxt("%s-tau.txt" % args.tree, fitness_matrix, fmt='%.5f', delimiter=",", newline="\n")
  print "%.5f" % fitness
  sys.exit(0)
