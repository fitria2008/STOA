#!/usr/bin/env python
# encoding: utf-8
import os
import sys
import argparse
import numpy
import networkx as nx
import filehandler as fh

#Constants
RESTART_PROB = 0.15 

def get_randomwalk_graphs(network, filename, count):  
  root = numpy.random.randint(1, len(network)+1)
  graph = nx.Graph()
  graph.add_node(root)
  actualNode = root
  
  while len(graph) < count:
    if numpy.random.random() < RESTART_PROB:
      actualNode = root
    else:
      neighbors = network.neighbors(actualNode)
      nextNode = neighbors[numpy.random.randint(len(neighbors))]
      graph.add_edge(actualNode, nextNode)
      actualNode = nextNode
  fh.write_edge_list("%s-RW.txt" % filename, graph)  
  
  for node in graph.nodes():
    for neighbor in network.neighbors(node):
      if (graph.has_node(neighbor)):
        graph.add_edge(node, neighbor)
        
  fh.write_edge_list("%s-IRW.txt" % filename, graph) 

def get_randomdeletion_graph(network, filename, count):
  while len(network) > count:
    toRemove = numpy.random.choice(network.nodes())
    if toRemove not in nx.articulation_points(network):
      network.remove_node(toRemove)
     
  fh.write_edge_list("%s-RD.txt" % filename, network)      
  
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--network', required=True)
  parser.add_argument('--filename', required=True)
  parser.add_argument('--count', required=False)
  args = parser.parse_args()
  
  if not os.path.exists(args.network):
    print "File given by --network not found."
    sys.exit(128)

  network = fh.load_from_edge_list(args.network)
  
  filename = os.path.splitext(args.filename)[0]
   
  if args.count:
    count = (int)(args.count)
    if count > len(network):
      print 'Value --count greater then number of network nodes.'
      sys.exit(128)
  else:
    count = len(network)
  
  get_randomwalk_graphs(network, filename, count)
  get_randomdeletion_graph(network, filename, count)
  
  sys.exit(0)