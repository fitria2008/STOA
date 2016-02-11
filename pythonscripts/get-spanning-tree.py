#!/usr/bin/env python
# encoding: utf-8
import os
import sys
import argparse
import numpy
import networkx as nx
import matplotlib.pyplot as plt

def get_random_spanning_tree(network):
  root = numpy.random.randint(1, len(network)+1)
  return get_spanning_tree_from_graph(network, root)

def get_spanning_tree_from_graph(network, root = None):
  return nx.dfs_tree(network, root).to_undirected()

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
  parser.add_argument('--filename', required=True)
  parser.add_argument('--root',    required=False)
  args = parser.parse_args()

  network = load_from_edge_list(args.network)

  if args.root and int(args.root) > 0:
    T = get_spanning_tree_from_graph(network, int(args.root))
  else:
    T = get_random_spanning_tree(network)

  write_edge_list(args.filename, T)
  sys.exit(0)

