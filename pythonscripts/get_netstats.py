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
  
  degree = 2.0 * len(network.edges()) / len(network)
  stats = 'average node degree: %.3f' % degree
  density = nx.density(network)
  stats = '%s\ndensity: %.3f' % (stats, density)
  cluster = nx.average_clustering(network)
  stats = '%s\naverage clustering: %.3f' % (stats, cluster)
  diameter = nx.diameter(network)
  stats = '%s\ndiameter: %d' % (stats, diameter)
  fh.write_string("%s_stats.txt" % filename, stats)
    
  distribution = nx.degree_histogram(network)
  dist = [("degree, frequency")]
  dist.extend([("%d, %d" % (position, value)) for position, value in enumerate(distribution)])
  fh.write_list("%s_dist.txt" % filename, dist)
  
  
  
  