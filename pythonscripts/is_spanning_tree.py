#!/usr/bin/env python
# encoding: utf-8
import os
import sys
import argparse
import networkx as nx
#import matplotlib.pyplot as plt

def is_spanning_tree(tree, network = None, source = 1, draw = True):
  #S = nx.dfs_tree(tree, source).to_undirected()

  #if draw:
  #  nx.draw_graphviz(tree)
  #  plt.show()

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

def write_edge_list(filename, network):
  with open(filename, 'w+') as fh:
    [fh.write("%d, %d\n" % (source, target)) for source, target, weight in nx.to_edgelist(network)]

def load_from_edge_list(filename):
  edgelist = []
  with open(filename, 'r') as fh:
    for line in fh.readlines():
      source, target = line.split(',')
      edgelist.append((int(source), int(target)))

  return nx.from_edgelist(edgelist)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--network', required=True)
  parser.add_argument('--tree',    required=True)
  args = parser.parse_args()

  tree = load_from_edge_list(args.tree)

  if is_spanning_tree(tree):
    sys.exit(0)

  sys.exit(1)
