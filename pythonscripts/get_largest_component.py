#!/usr/bin/env python
# encoding: utf-8
import os
import sys
import argparse
import numpy
import networkx as nx
import filehandler as fh

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--network', required=True)
  parser.add_argument('--filename', required=True)
 
  args = parser.parse_args()
  
  network = fh.load_from_edge_list(args.network)
  if (nx.is_connected(network)):
    print 'already a connected graph'
  else:
    largest = nx.connected_component_subgraphs(network)[0]
    fh.write_edge_list(args.filename, largest)
      
  sys.exit(0)
  
  
 