
## Overview

The estree.py program takes in a graph and a series of edge deletions and outputs the reachability or levels of each node after each edge deletion.
The edges to be deleted can be input in the input file or manually through the command line.
The user can also specify whether they would like the algorithm to output either the reachability of nodes after each edge deletion or the levels of each node after each edge deletion. Note that if the reachability option is selected, the program will check if the input graph is acyclic: if not, the program will terminate.

## Algorithm Details

The algorithms used for updating levels of nodes after each edge deletion is based on my submission for Homework 3, question 5b. This results in a total update time of O(nm), where n is the number of nodes, and m is the number of edges.
The algorithm used for updating reachability of nodes after each edge deletion is based on my submission for Homework 3, question 5c. This results in a total update time of O(m).

## How to Run

Below is the format for how to run this program in the terminal:

> python3 estree.py [\-\-input <filename\>] [-m] [-r]

Options:

> --input: Name of the input file. If not provided, the default name is "input".

> -m: Flag to allow for manual edge deletion. If not provided, edges to be deleted will be read from the input file.

> -r: Flag to keep track of reachability instead of levels. If not provided, the algorithm will keep track of levels of each node after every deletion.

Example: if the user would like to run the program to keep track of node reachability, using input file "myinput", and with manual edge deletion enabled, this is the command the user should run:

> python3 estree.py \-\-input myinput -m -r

## Input Format

The format of the input file should consist of three lines. The first line is a list of nodes (strings) delimited with spaces. The first node is assumed to be the root node. The second line is a list of edges delimited with spaces, where each edge follows the format "<source node\>,<target node\>". The third line is a list of edges to be deleted, and the order of the edges is determined by the order in which they were listed. Every edge listed in the second line must be deleted exactly once.

If the user would like to manually input edges to be deleted in the terminal, the program will prompt the user for each edge to be input. Edges provided must be in the format "<source node\>,<target node\>", or else the user will be prompted again for an edge to be deleted. Note that if the user selects the option to manually input edges, the third line of the input file would be optional and redundant.

## BFS Algorithm

The bfs.py program was written to provide a baseline to compare the performance of the ES-tree algorithm. Its usage is similar to that of estree.py. Note that the BFS algorithm uses the same BFS functionality no matter if the user selects the levels option or the reachability option.

The BFS algorithm is O(m^2) overall, where m is the number of edges.

## Auto-Generating a Large, Dense Graph

The makelargegraph.py program auto-generates graphs of large input sizes. For a graph with n nodes, the graph would partition the nodes into groups of <span\> nodes (where <span\> is hardcoded to 5 for now); essentially, the algorithm would create n/5 "rows" of nodes. Then, the nodes would be connected with edges: every node in a row would have a directed edge to all nodes of all "lower" rows. Finally, A node would be added at the top, designated as the root node, and connected to the nodes in the topmost row. The result is a very dense DAG; by design, there are no back-edges, since all edges point "downwards". For edge removal, the order in which edges are removed is determined randomly.

Below is the format for how to run this program in the terminal (where <num nodes\> is the number of non-root nodes in the graph):

> python3 makelargegraph.py <num nodes\>
