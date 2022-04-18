
# James Wu (wujames)

from detectcycles import Graph
import argparse
from collections import deque


class ESTree:

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

    # A: "from previous level": A[u] contains the node that serves as the current parent to u
    # { 4: 3, 5: 4, 6: 5 }
    A = {}
    # B: "from the current or deeper levels": this set contains all nodes "discarded" in the search for a potential parent for u
    # { 4: { 5, 6 }, 5: { 6 }, 6: {} }
    B = {}
    # C: "not checked yet": this set contains all nodes whose levels we have not checked yet; these are the nodes we will be sampling candidate parents from
    # { 4: { 1, 2 }, 5: { 2, 3 }, 6: { 1, 2, 3 } }
    C = {}


    def __init__(self, nodes, edges, root):
        self.nodes = nodes.copy()
        self.edges = edges.copy()
        self.num_nodes = len(nodes)
        self.num_unreachable = 0
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

        # perform bfs and initialize A, the current/direct parents of each node
        # assume the first node in nodes is the root
        bfs_list = deque([ root ])
        level_of = {}
        level_of[root] = 0
        visited_nodes = set()
        visited_nodes.add(root)
        A = {}
        while len(bfs_list) > 0:
            curr_node = bfs_list.popleft()
            # print("pop:", curr_node)
            # if curr_node has children, potentially add them to bfs_list
            if curr_node in children_of:
                for v in children_of[curr_node]:
                    if v not in visited_nodes:
                        # print("visit:", v)
                        visited_nodes.add(v)
                        bfs_list.append(v)
                        A[v] = curr_node
                        level_of[v] = level_of[curr_node] + 1

        # initialize level_of for nodes not reached in bfs
        for node in nodes:
            if node not in level_of:
                level_of[node] = "infinity"
                self.num_unreachable += 1
                self.unreachable_nodes.add(node)

        # initialize C, the potential, as-of-yet unconsidered parents of each node
        # note: for a node to be placed in C, it must have a non-infinite level
        # also initialize B for each node, though it should be empty
        B = {}
        C = {}
        for node in nodes:
            # the root node or unreachable nodes should not have B or C data
            if level_of[node] == "infinity" or level_of[node] == 0:
                continue
            C[node] = set()
            B[node] = set()
            for u in parents_of[node]:
                # if some parent of this node is unreachable or is already the current parent (A), don't consider it for C
                if level_of[u] != "infinity" and u != A[node]:
                    C[node].add(u)

        self.parents_of = parents_of
        self.children_of = children_of
        self.level_of = level_of
        self.A = A
        self.B = B
        self.C = C

    
    def printAfterInit(self):
        print("nodes:", self.nodes)
        print("edges:", self.edges)
        print("num_nodes:", self.num_nodes)
        print("num_unreachable:", self.num_unreachable)
        print("unreachable_nodes:", self.unreachable_nodes)
        
        print("parents_of:", self.parents_of)
        print("children_of:", self.children_of)
        print("level_of:", self.level_of)

        print("A:", self.A)
        print("B:", self.B)
        print("C:", self.C)


    def printTree(self, num_deletions):
        edges = self.edges
        level_of = self.level_of
        num_unreachable = self.num_unreachable
        unreachable_nodes = self.unreachable_nodes
        A = self.A

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
                print(node, "<-", A[node])
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
        A = self.A

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
                print(node, "<-", A[node])
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

        if v in self.A:
            if self.A[v] == u:
                self.A[v] = None
        if v in self.C:
            if u in self.C[v]:
                self.C[v].remove(u)


    # (Let i denote the level of u to be updated)
    # UpdateLevel(u):
    #   If u does not have a parent, or if u's current parent (node in set A) has increased its level to greater than i-1, place it in set B, and now, u must find a new parent:
    #       For node in set C:
    #           If node is level i or greater, place that node in set B. That node is "discarded".
    #           Else that node becomes the new parent, so place it in set A. Note that u's level does not change. Return from function.
    #       Once all nodes in C have been exhausted, reset all nodes with incoming edges to u by setting A:={} and B:={} and setting C as the set of all nodes with incoming edges to u.
    #       Then, increment the level of u.
    #       If the level of u is n, set the level of u to infinity. Then call UpdateLevel(v) for all nodes v with outgoing edges from u.
    #       Else call UpdateLevel(v) for all nodes v with outgoing edges from u. Then call UpdateLevel(u) to repeat the process of finding a parent for u.
    #   Else do nothing (node u gets to keep its parent).
    def updateLevel(self, u):
        i = self.level_of[u]
        # (do not update level of nodes that are unreachable or the root node)
        if i == "infinity" or i == 0:
            return

        # If u does not have a parent, or if u's current parent (node in set A) has increased its level to greater than i-1, place it in set B, and now, u must find a new parent:
        if self.A[u] == None or self.level_of[self.A[u]] == "infinity" or self.level_of[self.A[u]] > (i - 1):
            # (place current parent into set B)
            if self.A[u] != None:
                self.B[u].add(self.A[u])
            # For node in set C:
            while self.C[u]:
                # (this node is the potential new current parent for u)
                node = self.C[u].pop()
                # If node is level i or greater, place that node in set B. That node is "discarded".
                if self.level_of[node] == "infinity" or self.level_of[node] >= i:
                    self.B[u].add(node)
                # Else that node becomes the new parent, so place it in set A. Note that u's level does not change. Return from function.
                else:
                    self.A[u] = node
                    return
            
            # Once all nodes in C have been exhausted, reset all nodes with incoming edges to u by setting A:={} and B:={} and setting C as the set of all nodes with incoming edges to u.
            self.A[u] = None
            self.B[u] = set()
            self.C[u] = set()
            for node in self.parents_of[u]:
                if self.level_of[node] == "infinity":
                    self.B[u].add(node)
                else:
                    self.C[u].add(node)
            # Then, increment the level of u.
            self.level_of[u] += 1
            # If the level of u is n, set the level of u to infinity. Then call UpdateLevel(v) for all nodes v with outgoing edges from u.
            if self.level_of[u] == self.num_nodes:
                self.level_of[u] = "infinity"
                self.num_unreachable += 1
                self.unreachable_nodes.add(u)
                if u in self.children_of:
                    for node in self.children_of[u]:
                        self.updateLevel(node)
            # Else call UpdateLevel(v) for all nodes v with outgoing edges from u. Then call UpdateLevel(u) to repeat the process of finding a parent for u.
            else:
                if u in self.children_of:
                    for node in self.children_of[u]:
                        self.updateLevel(node)
                self.updateLevel(u)


    # (Let i denote the level of u to be updated)
    # UpdateLevel(u):
    #   If u's current parent (node in set A) has become unreachable, place it in set B, and now, u must find a new parent that is reachable:
    #       For node in set C:
    #           If node is unreachable, place that node in set B. That node is "discarded".
    #           Else that node becomes the new parent, so place it in set A. Return from function.
    #       Once all nodes in C have been exhausted, that means there is no reachable node with an incoming edge to u. Thus, u is now unreachable.
    #       Call UpdateLevel(v) for all nodes v with outgoing edges from u.
    #   Else do nothing (node u gets to keep its parent).
    def updateLevelReachability(self, u):
        i = self.level_of[u]
        # (do not update level of nodes that are unreachable or the root node)
        if i == "infinity" or i == 0:
            return

        # (if a node's level is infinity, it is unreachable; otherwise, it is reachable)
        # If u's current parent (node in set A) has become unreachable, place it in set B, and now, u must find a new parent that is reachable:
        if self.A[u] == None or self.level_of[self.A[u]] == "infinity":
            # (place current parent into set B)
            if self.A[u] != None:
                self.B[u].add(self.A[u])
            # For node in set C:
            while self.C[u]:
                # (this node is the potential new current parent for u)
                node = self.C[u].pop()
                # If node is unreachable, place that node in set B. That node is "discarded".
                if self.level_of[node] == "infinity":
                    self.B[u].add(node)
                # Else that node becomes the new parent, so place it in set A. Return from function.
                else:
                    self.A[u] = node
                    return
            
            # Once all nodes in C have been exhausted, that means there is no reachable node with an incoming edge to u. Thus, u is now unreachable.
            self.A[u] = None
            self.B[u] = set()
            self.C[u] = set()
            self.level_of[u] = "infinity"
            self.num_unreachable += 1
            self.unreachable_nodes.add(u)
            # Call UpdateLevel(v) for all nodes v with outgoing edges from u.
            if u in self.children_of:
                for node in self.children_of[u]:
                    self.updateLevelReachability(node)


def isGraphCyclic(graphnodes, graphedges):
    nodes = graphnodes.copy()
    edges = graphedges.copy()
    nodes_list = list(nodes)
    node_to_int = {}
    graph = Graph(len(nodes))

    # convert all nodes (str) into int form, since the Graph code only works with ints
    for i, node in enumerate(nodes):
        node_to_int[node] = i
    # add edges to graph, where nodes are in int form
    for edge in edges:
        u = edge[0]
        v = edge[1]
        graph.addEdge(node_to_int[u], node_to_int[v])
    # return whether graph has cycle
    if graph.isCyclic() == 1:
        return True
    else:
        return False


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

    estree = ESTree(nodes, edges, root)
    # estree.printAfterInit()

    # check if graph is cyclic
    if reachability and isGraphCyclic(nodes, edges):
        print("ERROR: Graph is cyclic, so reachability cannot be determined")
        exit()

    if not manual_deletion:
        print("\nedges to delete:", edges_to_delete, "\n")
        if reachability:
            estree.printTreeReachability(0)
        else:
            estree.printTree(0)

        for i, edge_to_delete in enumerate(edges_to_delete):
            estree.deleteEdge(edge_to_delete)
            print("Deleting edge:", edge_to_delete)
            # print(edge_to_delete[1])
            if reachability:
                estree.updateLevelReachability(edge_to_delete[1])
                estree.printTreeReachability(i + 1)
            else:
                estree.updateLevel(edge_to_delete[1])
                estree.printTree(i + 1)

    else:
        if reachability:
            estree.printTreeReachability(0)
        else:
            estree.printTree(0)
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
            estree.deleteEdge(edge_to_delete)
            print("Deleting edge:", edge_to_delete)
            if reachability:
                estree.updateLevelReachability(edge_to_delete[1])
                estree.printTreeReachability(num_deleted + 1)
            else:
                estree.updateLevel(edge_to_delete[1])
                estree.printTree(num_deleted + 1)

            num_deleted += 1
