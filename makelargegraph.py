
import sys
import math
import random


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("ERROR: Not enough or too many arguments")
        exit()
    
    # num nodes
    n = int(sys.argv[1])
    # num nodes per row
    span = 5 # hardcoded for now

    nodes = set()
    edges = set()

    # create a 2D array of nodes, where each row represents a "row" of <span> nodes
    num_nodes_made = 0
    node_rows = []
    num_rows = math.ceil(n / span)
    for i in range(num_rows):
        node_rows.append([])
        for j in range(span):
            if num_nodes_made < n:
                node = str(i) + "-" + str(j)
                num_nodes_made += 1
                nodes.add(node)
                node_rows[i].append(node)

    # print(num_nodes_made)
    # print(len(nodes))
    # print(node_rows)

    # for every row, every node in the row will point to every node in every other row
    # the result is a very dense graph with no backedges/cycles
    for r1 in range(len(node_rows) - 1):
        source_row = node_rows[r1]
        for r2 in range(r1 + 1, len(node_rows)):
            dest_row = node_rows[r2]

            for source_node in source_row:
                for dest_node in dest_row:
                    edges.add((source_node, dest_node))
                    # print((source_node, dest_node))
    # print(len(edges))

    node_list = []
    for node in nodes:
        node_list.append(node)
    nodes_str = " ".join(node_list)

    root_edges = []
    for i in range(span):
        root_edges.append("root,0-" + str(i))

    edge_list = []
    for edge in edges:
        edge_list.append(edge[0] + "," + edge[1])
    edge_list += root_edges
    edges_str = " ".join(edge_list)

    random.shuffle(edge_list)
    delete_edges_str = " ".join(edge_list)

    root_edges = []
    for i in range(span):
        root_edges.append("root,0-" + str(i))
    
    print("root " + nodes_str)
    print(edges_str)
    print(delete_edges_str)
    # print(len(edge_list))
