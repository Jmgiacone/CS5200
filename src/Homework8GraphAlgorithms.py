from random import randrange, randint
from queue import PriorityQueue
from math import inf


def main():
    # Create the data structure for storing a graph
    # Use a list of dictionaries, where each dict is int->int
    # Where the first int is the node id and the second is the weight of the edge

    # Generate random graphs
    for n in [10, 20, 30, 40, 50]:
        # Max edges: n(n-1) -> directed
        #            (n(n-1))/2 -> undirected
        max_edges = n * (n - 1) / 2
        max_density = max_edges / n
        # TODO: Make this configurable
        for i in range(10):
            graph = random_graph(n, (i + 1) * max_density / 10)
            print("n={}, d={}".format(n, (i + 1) * max_density / 10))
            print(convert_to_dot_syntax(graph))

            print("Kruskal's Minimum Spanning Tree")
            mst = kruskals_algorithm(graph)
            print(convert_to_dot_syntax(mst))

            print("Prim's Minimum Spanning Tree")
            mst = prims_algorithm(graph, randrange(n))
            print(convert_to_dot_syntax(mst, True))

            print("Generating digraph")
            graph = random_graph(n, (i + 1) * max_density / 10, False)
            print("n={}, d={}".format(n, (i + 1) * max_density / 10))
            print(convert_to_dot_syntax(graph, True))

            print("Dijkstra's one-to-all shortest path")
            dijkstras = dijkstras_algorithm(graph, randrange(n))

            print("Floyd-Warshall all-pairs shortest path")
            floyd_warshalls = floyd_warshall(graph)


def floyd_warshall(graph):
    # Create the weight matrix, with special condition of inf if there isn't an edge connecting two nodes
    adj_matrix = [[inf if i != j else 0 for j in range(len(graph))] for i in range(len(graph))]

    for i in range(len(graph)):
        for j, val in graph[i].items():
            adj_matrix[i][j] = val

    for k in range(len(graph)):
        for i in range(len(graph)):
            for j in range(len(graph)):
                adj_matrix[i][j] = min(adj_matrix[i][j], adj_matrix[i][k] + adj_matrix[k][j])

    return adj_matrix


def kruskals_algorithm(graph):
    # Create an empty adjacency-dict
    mst = [{} for i in range(len(graph))]

    # Create a list of edges and their weights
    edges = []
    seen_edges = set()
    for u in range(len(graph)):
        for v in graph[u]:
            if (u, v) not in seen_edges:
                edges.append((graph[u][v], (u, v)))
                seen_edges.add((u, v))
                seen_edges.add((v, u))

    edges.sort(key=lambda edge: edge[0])

    # Keep a list of sets to keep track of the trees
    trees = [{node} for node in range(len(graph))]

    # Iterate over each edge
    for edge in edges:
        weight = edge[0]
        u, v = edge[1]

        if trees[u].isdisjoint(trees[v]):
            # Add the edge to the MST
            mst[u][v] = weight
            mst[v][u] = weight

            # Union the two sets
            trees[u].update(trees[v])

            # Update all other sets
            for node in trees[u] - {u}:
                trees[node] = trees[u]

    return mst


def prims_algorithm(graph, start_node):
    # Create an empty adjacency-dict
    mst = [{} for i in range(len(graph))]

    # Create a visited set
    visited = set()

    # Create a new PriorityQueue (Heap)
    frontier = PriorityQueue()

    # Maintain a parent dictionary
    pi = {i: None for i in range(len(graph))}

    # Maintain a key dictionary
    key = {i: inf for i in range(len(graph))}

    key[start_node] = 0

    # Put the start node inside
    frontier.put((0, start_node))

    # Count the number of nodes added so far
    nodes_added = 1
    while len(visited) != len(graph):
        node = frontier.get()[1]
        visited.add(node)

        # Add the edge to the graph
        if pi[node] is not None:
            mst[pi[node]][node] = key[node]
            nodes_added += 1

        for neighbor, weight in graph[node].items():
            if neighbor not in visited and weight < key[neighbor]:
                pi[neighbor] = node
                key[neighbor] = weight
                frontier.put((weight, neighbor))

    return mst


def random_graph(num_nodes, density, undirected=False):
    # Generate an empty adjacency-dict
    # An adjacency-dict looks similar to and adjacency list, except has constant-time edge lookups
    # Example:
    # 1 -> {2: 3, 4: 1}
    # 2 -> {1: 3}
    # 3 -> {5: 6}
    # 4 -> {1: 1, 5: 8}
    # 5 -> {3: 6, 4: 8}

    # Create an empty graph
    graph = [{} for i in range(num_nodes)]

    # Make it minimally connected
    for i in range(num_nodes - 1):
        # Generate a random weight for this edge
        weight = randint(1, 100)

        # Connect the nodes forward
        graph[i][i + 1] = weight

        # Connect the nodes backward
        graph[i + 1][i] = weight

    # We're allowed to create density * num_nodes edges overall
    num_edges = int(density * num_nodes)

    # Since the graph has to be connected, we have to add n-1 edges off the bat
    current_edges = num_nodes - 1

    # Loop until we fill the requisite number of edges
    while current_edges < num_edges:
        # Choose two random nodes
        start, end = randrange(num_nodes), randrange(num_nodes)

        # If they're not the same node and there isn't already an edge between them
        if start != end and end not in graph[start]:
            # Add this edge with a random weight in [1, 100]
            # TODO: Make this configurable
            weight = randint(1, 100)
            graph[start][end] = weight

            if undirected:
                # Add the edge the other way
                graph[end][start] = weight

            # Increase edge count
            current_edges += 1

    return graph


def create_adjacency_matrix_from_adjacency_list(adj_list):
    n = len(adj_list)

    # Create empty nxn matrix
    matrix = [[0 for j in range(n)] for i in range(n)]

    for i in range(n):
        for j, val in adj_list[i].items():
            matrix[i][j] = val

    return matrix


def convert_to_dot_syntax(graph, directed=False):
    # The arrows are different depending on whether or not the graph is directed
    text = "strict "
    if directed:
        text += "digraph "
        arrow = "->"
    else:
        text += "graph "
        arrow = "--"

    # Start the file off with the graph name and an opening curly brace
    text += "G\n{\n"

    # Grab the number of nodes
    n = len(graph)

    # Loop over the edges
    for u in range(n):
        for v in graph[u]:
            text += "  {} {} {} [label=\"{}\"];\n".format(u, arrow, v, graph[u][v])

    # Add in the closing curly brace
    text += "}\n"

    return text


def dijkstras_algorithm(graph, start_node):
    # TODO: Implement this
    return 0


def print_adjacency_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            print(matrix[i][j], end=" ")
        print()

if __name__ == '__main__':
    main()
