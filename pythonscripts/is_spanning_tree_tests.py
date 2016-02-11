#!/usr/bin/env python
# encoding: utf-8
import os
import sys
import unittest
import networkx as nx
from is_spanning_tree import load_from_edge_list,\
                             write_edge_list,\
                             is_spanning_tree

class TestIsSpanningTree(unittest.TestCase):

  def test_load_from_edge_list(self):
    network = load_from_edge_list("tests/simple_graph_loadtest.txt")
    self.assertEqual(network.number_of_nodes(), 3)
    self.assertEqual(network.number_of_edges(), 2)

  def test_given_simple_graph_with_cycles(self):
    tree = load_from_edge_list("tests/simple_tree_with_cycle.txt")
    self.assertEqual(tree.number_of_nodes(), 4)
    self.assertEqual(is_spanning_tree(tree, draw = False), False)

  def test_given_forest(self):
    tree = load_from_edge_list("tests/simple_tree_with_components.txt")
    self.assertEqual(tree.number_of_nodes(), 5)
    self.assertEqual(is_spanning_tree(tree, draw = False), False)

  def test_given_simple_graph_without_cycles(self):
    tree = load_from_edge_list("tests/simple_tree_no_cycles.txt")
    self.assertEqual(tree.number_of_nodes(), 4)
    self.assertEqual(is_spanning_tree(tree, draw = False), True)

    tree = load_from_edge_list("tests/simple_graph_loadtest.txt")
    self.assertEqual(tree.number_of_nodes(), 3)
    self.assertEqual(is_spanning_tree(tree, draw = False), True)

  def test_given_spanning_tree(self):
    pass

if __name__ == '__main__':
  unittest.main()

