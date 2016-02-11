#!/usr/bin/env python
# encoding: utf-8
import os
import sys
import argparse
import numpy
import networkx as nx

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
  parser.add_argument('--folder',  required=True)
  parser.add_argument('--fileprefix',  required=True)
  parser.add_argument('--amount',  required=True)
  parser.add_argument('--seed',    required=False)
  args = parser.parse_args()

  if args.seed:
    numpy.random.seed(int(args.seed))

  network = load_from_edge_list(args.network)

  if not os.path.exists(args.folder):
    os.mkdir(args.folder)

  for n in xrange(int(args.amount)):
    T = get_random_spanning_tree(network)
    treename = '%s%s' % (args.fileprefix, n)
    filename = os.path.join(args.folder, treename)
    write_edge_list(filename, T)

  sys.exit(0)
