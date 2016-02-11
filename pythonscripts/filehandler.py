#!/usr/bin/env python
# encoding: utf-8
import os
import sys
import argparse
import networkx as nx

def load_from_edge_list(filename):
  edgelist = []
  with open(filename, 'r') as fh:
    for line in fh.readlines():
      source, target = line.split(',')
      edgelist.append((int(source), int(target)))

  return nx.from_edgelist(edgelist)

def write_edge_list(filename, network):
  with open(filename, 'w+') as file:
    [file.write("%d, %d\n" % (source, target)) for source, target, weight in nx.to_edgelist(network)]
    
def write_list(filename, list):
  with open(filename, 'w+') as file:
    for entry in list:
      file.write("%s\n" % entry)
    
def write_string(filename, string):
  with open(filename, 'w+') as file:
    file.write(string)
    
def append_string(filename, string):
  with open(filename, 'a') as file:
    file.write(string)