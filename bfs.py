
# James Wu (wujames)

import argparse
from collections import deque


class BFS:

    # { 1, 2, 3 }
    nodes = set()
    # { (1, 2), (2, 3), (1, 3) }
    edges = set()
    num_nodes = 0
    num_unreachable = 0
    unreachable_nodes = set()

    # { 1: {}, 2: { 1 }, 3: { 1, 2 } }
    parents_of = {}
    # { 1: { 2, 3 }, 2: { 3 }, 3: {} }
    children_of = {}
    # { 1: 0, 2: 1, 3: 1 }
    level_of = {}

    root = ""


    def __init__(self, nodes, edges, root):
        self.nodes = nodes.copy()
        self.edges = edges.copy()
        self.num_nodes = len(nodes)
        self.num_unreachable = 0
        self.root = root
        # initialize parents_of and children_of
        parents_of = {}
        children_of = {}
        for edge in edges:
            u = edge[0]
            v = edge[1]
            if v not in parents_of:
                parents_of[v] = set()
            parents_of[v].add(u)
            if u not in children_of:
                children_of[u] = set()
            children_of[u].add(v)

        # perform bfs
        # assume the first node in nodes is the root
        bfs_list = deque([ root ])
        level_of = {}
        level_of[root] = 0
        visited_nodes = set()
        visited_nodes.add(root)
        while len(bfs_list) > 0:
            curr_node = bfs_list.popleft()
            # print("pop:", curr_node)
            # if curr_node has children, potentially add them to bfs_list
            if curr_node in children_of:
                for v in children_of[curr_node]:
                    if v not in visited_nodes:
                        visited_nodes.add(v)
                        bfs_list.append(v)
                        level_of[v] = level_of[curr_node] + 1

        # initialize level_of for nodes not reached in bfs
        for node in nodes:
            if node not in level_of:
                level_of[node] = "infinity"
                self.num_unreachable += 1
                self.unreachable_nodes.add(node)

        self.parents_of = parents_of
        self.children_of = children_of
        self.level_of = level_of

    
    def printAfterInit(self):
        print("nodes:", self.nodes)
        print("edges:", self.edges)
        print("num_nodes:", self.num_nodes)
        print("num_unreachable:", self.num_unreachable)
        print("unreachable_nodes:", self.unreachable_nodes)
        
        print("parents_of:", self.parents_of)
        print("children_of:", self.children_of)
        print("level_of:", self.level_of)


    def printTree(self, num_deletions):
        edges = self.edges
        level_of = self.level_of
        num_unreachable = self.num_unreachable
        unreachable_nodes = self.unreachable_nodes

        print("****************************************")
        print("After", str(num_deletions), "deletions:")
        print("Edges still remaining:")
        print(edges)
        print("Num unreachable nodes:", num_unreachable, "\n")

        nodes_on_this_level = {}
        for i in range(self.num_nodes):
            nodes_on_this_level[i] = set()
        for node in level_of:
            lvl = level_of[node]
            if lvl != "infinity":
                nodes_on_this_level[lvl].add(node)

        # trivially print the root node
        print("Level: 0 --------------------")
        for node in nodes_on_this_level[0]:
            print(node)
        # print every node on each following level, along with its current parent (format: "node <- parent")
        for i in range(1, self.num_nodes):
            print("Level:", i, "--------------------")
            lvl_nodes = nodes_on_this_level[i]
            lvl_nodes = list(lvl_nodes)
            lvl_nodes.sort()
            for node in lvl_nodes:
                print(node)
        # print every node that is now unreachable
        print("Level: infinity --------------------")
        unreachable_nodes = list(unreachable_nodes)
        unreachable_nodes.sort()
        for node in unreachable_nodes:
            print(node)
        print("\n")


    def printTreeReachability(self, num_deletions):
        edges = self.edges
        level_of = self.level_of
        num_unreachable = self.num_unreachable
        unreachable_nodes = self.unreachable_nodes

        print("****************************************")
        print("After", str(num_deletions), "deletions:")
        print("Edges still remaining:")
        print(edges)
        print("Num unreachable nodes:", num_unreachable, "\n")

        nodes_on_this_level = {}
        for i in range(self.num_nodes):
            nodes_on_this_level[i] = set()
        for node in level_of:
            lvl = level_of[node]
            if lvl != "infinity":
                nodes_on_this_level[lvl].add(node)

        # trivially print the root node
        print("Reachable nodes --------------------")
        for node in nodes_on_this_level[0]:
            print(node)
        # print every node on each following level, along with its current parent (format: "node <- parent")
        for i in range(1, self.num_nodes):
            lvl_nodes = nodes_on_this_level[i]
            lvl_nodes = list(lvl_nodes)
            lvl_nodes.sort()
            for node in lvl_nodes:
                print(node)
        # print every node that is now unreachable
        print("Unreachable nodes --------------------")
        unreachable_nodes = list(unreachable_nodes)
        unreachable_nodes.sort()
        for node in unreachable_nodes:
            print(node)
        print("\n")


    def deleteEdge(self, edge):
        u = edge[0]
        v = edge[1]
        self.edges.remove(edge)

        self.parents_of[v].remove(u)
        self.children_of[u].remove(v)


    # Simply performs dfs
    def performBFS(self):
        nodes = self.nodes
        edges = self.edges
        root = self.root
        # initialize parents_of and children_of
        parents_of = {}
        children_of = {}
        for edge in edges:
            u = edge[0]
            v = edge[1]
            if v not in parents_of:
                parents_of[v] = set()
            parents_of[v].add(u)
            if u not in children_of:
                children_of[u] = set()
            children_of[u].add(v)

        # perform bfs
        # assume the first node in nodes is the root
        bfs_list = deque([ root ])
        level_of = {}
        level_of[root] = 0
        visited_nodes = set()
        visited_nodes.add(root)
        while len(bfs_list) > 0:
            curr_node = bfs_list.popleft()
            # print("pop:", curr_node)
            # if curr_node has children, potentially add them to bfs_list
            if curr_node in children_of:
                for v in children_of[curr_node]:
                    if v not in visited_nodes:
                        visited_nodes.add(v)
                        bfs_list.append(v)
                        level_of[v] = level_of[curr_node] + 1

        # initialize level_of for nodes not reached in bfs
        for node in nodes:
            if node not in level_of:
                level_of[node] = "infinity"
                self.num_unreachable += 1
                self.unreachable_nodes.add(node)

        self.parents_of = parents_of
        self.children_of = children_of
        self.level_of = level_of


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=False, default="input", help="Name of input file")
    parser.add_argument('-m', action='store_true', help="Flag to allow for manual edge deletion")
    parser.add_argument('-r', action='store_true', help="Flag to keep track of reachability instead of levels")
    args = parser.parse_args()
    # print('input file:', args.input)
    # print('manual edge deletion:', args.m)
    input_file = args.input
    manual_deletion = args.m
    reachability = args.r

    nodes = set()
    edges = set()
    root = ""
    edges_to_delete = []
    with open(input_file) as f:
        lines = f.readlines()
        nodes_list = lines[0].split()
        # assume first node in list is the root
        root = nodes_list[0]
        for node in nodes_list:
            nodes.add(node)
        edges_list = lines[1].split()
        for edge in edges_list:
            edge = edge.split(",")
            if len(edge) != 2 or edge[0] not in nodes or edge[1] not in nodes:
                print("ERROR: Edges provided are not good")
                exit()
            edges.add((edge[0], edge[1]))

        if not manual_deletion:
            edges_to_delete_list = lines[2].split()
            if len(edges_to_delete_list) != len(edges):
                print("ERROR: Not enough or too many edges to delete")
                exit()
            for edge in edges_to_delete_list:
                edge = edge.split(",")
                if len(edge) != 2 or edge[0] not in nodes or edge[1] not in nodes or (edge[0], edge[1]) not in edges:
                    print("ERROR: Edges provided for deletion are not good")
                    exit()
                edges_to_delete.append((edge[0], edge[1]))

    bfs = BFS(nodes, edges, root)
    # estree.printAfterInit()

    if not manual_deletion:
        print("\nedges to delete:", edges_to_delete, "\n")
        if reachability:
            bfs.printTreeReachability(0)
        else:
            bfs.printTree(0)

        for i, edge_to_delete in enumerate(edges_to_delete):
            bfs.deleteEdge(edge_to_delete)
            print("Deleting edge:", edge_to_delete)
            # print(edge_to_delete[1])
            if reachability:
                bfs.performBFS()
                bfs.printTreeReachability(i + 1)
            else:
                bfs.performBFS()
                bfs.printTree(i + 1)

    else:
        if reachability:
            bfs.printTreeReachability(0)
        else:
            bfs.printTree(0)
        num_deleted = 0
        num_edges = len(edges)
        while num_deleted < num_edges:
            print("Input the " + str(num_deleted + 1) + "-th edge to delete (or enter \"quit\"):")
            edge_to_delete = input()
            if edge_to_delete == "quit":
                print("Goodbye")
                break

            edge = edge_to_delete.split(",")
            if len(edge) != 2 or edge[0] not in nodes or edge[1] not in nodes:
                print("ERROR: Edge provided is not good; please try again")
                continue
            if (edge[0], edge[1]) not in edges:
                print("ERROR: Edge provided is not in the graph; please try again")
                continue

            edge_to_delete = (edge[0], edge[1])
            edges.remove(edge_to_delete)
            bfs.deleteEdge(edge_to_delete)
            print("Deleting edge:", edge_to_delete)
            if reachability:
                bfs.performBFS()
                bfs.printTreeReachability(num_deleted + 1)
            else:
                bfs.performBFS()
                bfs.printTree(num_deleted + 1)

            num_deleted += 1
