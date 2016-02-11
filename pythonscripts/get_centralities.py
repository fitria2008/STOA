#!/usr/bin/env python
# encoding: utf-8
import os
import sys
import argparse
import networkx as nx
import filehandler as fh

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--network', required=True)
  args = parser.parse_args()
  
  if not os.path.exists(args.network):
    print "File given by --network not found."
    sys.exit(128)

  filename = os.path.splitext(args.network)[0]
  
  network = fh.load_from_edge_list(args.network)

  degreecentral = nx.degree_centrality(network)
  stats = 'node, degree centrality'
  for node in network.nodes():
   stats = '%s\n%s, %.3f' % (stats, node, degreecentral[node])
  fh.write_string("%s_d_centrality.txt" % filename, stats)
 
  closenesscentral = nx.closeness_centrality(network)
  stats = 'node, closeness centrality'
  for node in network.nodes():
   stats = '%s\n%s, %.3f' % (stats, node, closenesscentral[node])
  fh.write_string("%s_c_centrality.txt" % filename, stats)
  
  betweennesscentral = nx.betweenness_centrality(network)
  stats = 'node, betweenness centrality'
  for node in network.nodes():
   stats = '%s\n%s, %.3f' % (stats, node, betweennesscentral[node])
  fh.write_string("%s_b_centrality.txt" % filename, stats)