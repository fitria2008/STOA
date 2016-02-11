#!/usr/bin/env python
# encoding: utf-8

"""
Generic version of APSP calculation. Although being slightly slower than the version used for 
the genetic algorithm, arbitrary unicode strings can be used to identify nodes. Additionally, 
calculation can be restricted to a list of nodes and optionally a normalization can be performed.
"""

from __future__ import division
import os
import sys
import argparse
import numpy
import networkx as nx
import codecs
import operator

def parse_nodelist(filename):
  with codecs.open(filename, 'r', 'utf-8') as f:
    nodelist = [line.strip() for line in f if not (line.startswith(u'#') or len(line.strip())==0)]
  
  return nodelist
  
def write_mapping(filename, mapping):
  sortedMap = sorted(mapping.items(), key=operator.itemgetter(1))
  with codecs.open(filename, 'w', 'utf-8') as f:
    for node, id in sortedMap:
        f.write('%s %s\n' % (id, node))
        
  return

def get_distance_matrix_from_graph(network, nodelist):
  """ Returns and optionally stores the distance matrix for a given network.
  Nodes in are arranged in the matrix according to their 
  Without the floyd parameter, simple BFS is used for APSP calculation. Be
  aware that this only works for unweighted networks. Since the implementation
  uses a Numpy matrix for storing the distances, less memory is needed compared
  to the NetworkX implementation.  
  
  Parameters
  ----------
  network : a NetworkX graph
  nodelist : list of network nodes to which the distance matrix should be restricted (optional)
 
  Returns
  -------
  A tuple containing the Numpy matrix storing all pairs shortest paths for the given network (or the nodes in the given nodelist) 
  and the mapping of nodes to matrix indices.
  """
  if nodelist:
    apspnodes = nodelist
  else:
    apspnodes = network.nodes()
  
  mapping = {}
  for index, node in enumerate(apspnodes):
    mapping.update({node:index})
     
  nodeset = set(apspnodes)
  n = len(apspnodes)
  D = numpy.zeros((n,n))
  for node in apspnodes:
    level = 0
    levelnodes = {node}
    seen = {}
        
    while levelnodes:
        worklist = levelnodes
        levelnodes = {}
        for target in worklist:
            if target not in seen:
                if target in nodeset:
                    D[mapping[node], mapping[target]] = level
                seen[target] = level
                
                try:
                    levelnodes.update(network[target])
                except KeyError:
                    print "Error: The specified node '%s' could not be found in the network" % target
                    sys.exit(1)
        level = level + 1
    
  return D, mapping
  
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('network', help="File containing the network (as edgelist) for which to calculate APSP")
  parser.add_argument('-l', '--nodelist', help="File containing a list of nodes to limit the calculation to")
  parser.add_argument('-d', '--delimiter', default=', ', help="Delimiter used to separate nodes in the edgelist (default: ', ')")
  parser.add_argument('-n', '--normalize', action='store_true', help="Normalize the matrix by dividing all entries by the diameter of the network")
  args = parser.parse_args()

  if not os.path.exists(args.network):
    print "File given by network argument not found."
    sys.exit(1)

  # Parse network and nodelist
  graph = nx.read_edgelist(args.network, delimiter=args.delimiter)
  nodelist = None if not args.nodelist else parse_nodelist(args.nodelist)
        
  ext = 'apnp' if args.normalize else 'apsp'
  filename = "%s.%s" % (args.network, ext)
  
  if not os.path.exists(filename):
    D, mapping = get_distance_matrix_from_graph(graph, nodelist)
    outformat = '%0.1f'
    
    # Normalize values by network diameter
    if args.normalize:
        D = D/float(D.max())
        outformat = '%0.4f'
    
    # Write matrix and mapping to file
    numpy.savetxt(filename, D, fmt=outformat, delimiter=args.delimiter, newline='\n')
    write_mapping('%s.mapping' % filename, mapping)
    
  sys.exit(0)