from random import randrange, randint, seed
import sys
from queue import PriorityQueue
from math import inf
from os.path import exists
from os import makedirs, chdir, listdir
from subprocess import run, PIPE


def main():
    # Create the data structure for storing a graph
    # Use a list of dictionaries, where each dict is int->int
    # Where the first int is the node id and the second is the weight of the edge

    # Create a directory for our graph output
    if not exists("graph_output"):
        makedirs("graph_output")

    # Seed the random generator
    rand_seed = randint(0, sys.maxsize)
    seed(rand_seed)

    # Create a directory for this seed value
    working_directory = "graph_output/seed_{}/".format(rand_seed)
    makedirs(working_directory)

    # Have a list hold all the graphs until we want to visualize them
    graphs = []

    # sfdp -Tpng dotExample.dot -Gsplines=true -Goverlap=scale -o dotOutput.png

    # Keep a counter for filenames
    counter = 1

    # Open up three files: one to hold output of Dijkstra's, one to hold output of Floyd-Warshall, and one for the TC
    dijkstra_out = open(working_directory + "dijkstra_output.txt", "w")
    floyd_warshall_out = open(working_directory + "floyd_warshall_output.txt", "w")
    transitive_closure_out = open(working_directory + "transitive_closure_output.txt",  "w")

    # Generate random graphs
    for n in [10, 20, 30, 40, 50]:
        # Create this directory
        folder_directory = "{}/size_{}/".format(working_directory, n)
        makedirs(folder_directory)

        # Max edges: n(n-1) -> directed
        #            (n(n-1))/2 -> undirected
        max_edges_directed = n * (n - 1)
        max_edges_undirected = max_edges_directed / 2

        max_density_directed = max_edges_directed / n
        max_density_undirected = max_edges_undirected / n

        # TODO: Make this configurable
        for i in range(10):
            d = (i + 1) * max_density_undirected / 10
            graph = random_graph(n, d)

            print("n={} e={} d={}".format(n, max(n - 1, int(d * n)), d))
            dot_syntax = convert_to_dot_syntax(graph)
            print(dot_syntax)
            print()

            filename = "undirected_graph_{}.dot".format(counter)

            # Write the file
            file = open(folder_directory + filename, "w")
            file.write(dot_syntax)

            # Add the entry to the list
            graphs.append(filename)

            print("Kruskal's Minimum Spanning Tree")
            mst = kruskals_algorithm(graph)
            dot_syntax = convert_to_dot_syntax(mst)
            print(dot_syntax)

            filename = "mst_kruskal_{}.dot".format(counter)

            # Write the file
            file = open(folder_directory + filename, "w")
            file.write(dot_syntax)

            # Add the entry to the list
            graphs.append(filename)

            print()

            print("Prim's Minimum Spanning Tree")
            mst = prims_algorithm(graph, randrange(n))
            dot_syntax = convert_to_dot_syntax(mst, True)
            print(dot_syntax)
            filename = "mst_prim_{}.dot".format(counter)

            # Write the file
            file = open(folder_directory + filename, "w")
            file.write(dot_syntax)

            # Add the entry to the list
            graphs.append(filename)
            print()

            d = (i + 1) * max_density_directed / 10

            print("Generating digraph")
            graph = random_graph(n, d, True)

            # Add the filename of the graph
            print("n={}, e={}, d={}".format(n, max(n - 1, int(d * n)), d))

            dot_syntax = convert_to_dot_syntax(graph, True)
            print(dot_syntax)
            print()

            filename = "directed_graph_{}.dot".format(counter)

            # Write the file
            file = open(folder_directory + filename, "w")
            file.write(dot_syntax)

            # Add the entry to the list
            graphs.append(filename)

            print("Dijkstra's one-to-all shortest path starting at node 0")
            dijkstras_dist, dijkstras_pi = dijkstras_algorithm(graph, 0)
            print("d: {}".format(dijkstras_dist))
            print("pi: {}\n".format(dijkstras_pi))

            # Print to file
            dijkstra_out.write("Digraph id: {}\n".format(counter))
            dijkstra_out.write("d: {}\n".format(dijkstras_dist))
            dijkstra_out.write("pi: {}\n\n".format(dijkstras_pi))

            print("Floyd-Warshall all-pairs shortest path")
            floyd_warshalls = floyd_warshall(graph)
            output = print_adjacency_matrix(floyd_warshalls)
            print(output)
            print()

            # Print to file
            floyd_warshall_out.write("Digraph id: {}\n".format(counter))
            floyd_warshall_out.write(output + "\n")

            print("Transitive closure")
            transitive_closure_matrix = transitive_closure(graph)
            output = print_adjacency_matrix(transitive_closure_matrix)
            print(output)

            # Print to file
            transitive_closure_out.write("Transitive closure matrix of id: {}\n".format(counter))
            transitive_closure_out.write(output + "\n")

            # Increment the counter
            counter += 1

    print("Generating graphs...")
    chdir(working_directory)

    for n in [10, 20, 30, 40, 50]:
        folder_directory = "size_{}/".format(n)

        print("Entering directory {}".format(folder_directory))

        # Change to that directory
        chdir(folder_directory)

        for file in listdir("./"):
            print("Generating graph based on {}".format(file))
            completed_process = \
                run("sfdp -Tpng {} -Goverlap=scale -o {}.png".format(file, file[:-4]),
                    stdout=PIPE, stderr=PIPE, shell=True)


        print()
        chdir("..")

    print("All output can be found in {}".format(working_directory))
    return 0


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


def random_graph(num_nodes, density, directed=False):
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

        if not directed:
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

            if not directed:
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
    text += "}"

    return text


def dijkstras_algorithm(graph, start_node):
    n = len(graph)

    # Need two dicts: one to hold shortest distances and one to hold predecessors
    d = {node: inf for node in range(n)}
    d[start_node] = 0
    pi = {node: None for node in range(n)}

    # Keep track of visited nodes
    visited = set()

    # Update d[source]
    d[start_node] = 0

    # Load the PQueue
    frontier = PriorityQueue()
    frontier.put((0, start_node))

    # While there are still nodes left to visit
    while len(visited) < n:
        # Grab highest priority node
        current_node = frontier.get()[1]

        # Mark this node visited
        visited.add(current_node)

        # Look at its neighbors
        for neighbor in graph[current_node]:
            new_dist = graph[current_node][neighbor] + d[current_node]

            # If going through this node is better than whatever else it was doing
            if neighbor not in visited and new_dist < d[neighbor]:
                # Update dict values
                d[neighbor] = new_dist
                pi[neighbor] = current_node

                # Add it to the frontier
                frontier.put((new_dist, neighbor))

    # Return minimum distance from start to every other node
    return d, pi


def transitive_closure(graph):
    # Copy the graph, set edge weights to 1, then pass it to floyd-warshall
    copy_graph = {}

    for i in range(len(graph)):
        neighbors = graph[i]
        copy_graph[i] = {}

        for neighbor in neighbors:
            copy_graph[i][neighbor] = 1

    return floyd_warshall(copy_graph)


def print_adjacency_matrix(matrix):
    text = ""

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            text += str(matrix[i][j]).zfill(3) + " "
        text += "\n"

    return text

if __name__ == '__main__':
    main()
