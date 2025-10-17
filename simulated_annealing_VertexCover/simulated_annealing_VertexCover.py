# ============================
# Import Required Libraries
# ============================

import random      # Used for generating random numbers and sampling random elements
import time        # Used to measure algorithm execution time
import networkx as nx  # NetworkX library for creating and processing graph structures
import numpy as np     # NumPy for mathematical and numerical computations


# ==========================================================
# Simulated Annealing Algorithm for the Vertex Cover Problem
# ==========================================================

def simulated_annealing_VertexCover(graph, Max_Node, initial_temp=1500, cooling_rate=0.95, max_iteration=1500):
    """
    Approximates the Vertex Cover problem using a Simulated Annealing optimization approach.

    Parameters:
        graph (networkx.Graph): The input graph.
        Max_Node (int): Maximum number of vertices allowed in the vertex cover.
        initial_temp (float): Starting temperature of the annealing process.
        cooling_rate (float): Temperature reduction rate after each iteration.
        max_iteration (int): Maximum number of iterations to perform.

    Returns:
        tuple:
            - best_solution (list): List of vertices in the best-found vertex cover.
            - best_covered (int): Number of edges covered by that solution.
    """

    # -------------------------
    # Extract graph components
    # -------------------------
    nodes_of_graph = list(graph.nodes)     # List of all graph vertices
    edges_of_graph = set(graph.edges)      # Set of all graph edges

    # -------------------------
    # Generate an initial solution
    # -------------------------
    # Start with a random set of vertices as the initial cover
    current_solution = set(random.sample(nodes_of_graph, Max_Node))
    best_solution = current_solution.copy()   # Initialize best solution as the current one

    # -------------------------
    # Helper function to count covered edges
    # -------------------------
    def count_covered_edges(cover):
        """Counts the number of edges that are covered by at least one vertex in 'cover'."""
        return len([edge for edge in edges_of_graph if edge[0] in cover or edge[1] in cover])

    # Initial evaluation
    best_covered = count_covered_edges(best_solution)
    current_temp = initial_temp

    # -------------------------
    # Main optimization loop
    # -------------------------
    for i in range(max_iteration):

        # Randomly remove one vertex and add another not in the current solution
        node_out = random.choice(list(current_solution))
        node_in = random.choice([node for node in nodes_of_graph if node not in current_solution])

        # Create a new candidate solution
        new_solution = current_solution.copy()
        new_solution.remove(node_out)
        new_solution.add(node_in)

        # Evaluate the candidate
        new_covered = count_covered_edges(new_solution)
        new_best_difference = new_covered - best_covered

        # -------------------------
        # Acceptance criterion
        # -------------------------
        # Always accept improvements; otherwise, accept with a probability based on temperature
        if new_best_difference > 0 or random.random() < np.exp(new_best_difference / current_temp):
            current_solution = new_solution
            if new_covered > best_covered:
                best_solution = current_solution
                best_covered = new_covered

        # -------------------------
        # Cooling schedule
        # -------------------------
        current_temp *= cooling_rate

    return list(best_solution), best_covered


# ==========================================================
# Function to Run Experiments on Multiple Graphs
# ==========================================================

def run_algorithm(graph_files, Max_Node_values):
    """
    Executes the Simulated Annealing Vertex Cover algorithm on multiple graphs.

    Parameters:
        graph_files (dict): A dictionary mapping graph names to their file paths (.gexf format).
        Max_Node_values (dict): A dictionary mapping graph names to their corresponding Max_Node limits.

    Returns:
        dict: A dictionary containing results for each graph, including:
              - Number of covered edges
              - Total runtime in seconds
              - The vertex cover list
    """

    results = {}

    # Iterate through each provided graph
    for name, path in graph_files.items():
        graph = nx.read_gexf(path)                     # Load the graph from file
        Max_Node = Max_Node_values.get(name, None)     # Get the max allowed vertices for this graph

        if Max_Node:
            # Record the start time of execution
            start_time = time.time()

            # Run the simulated annealing algorithm
            cover, covered_edges = simulated_annealing_VertexCover(graph, Max_Node)

            # Measure runtime
            runtime = time.time() - start_time

            # Store results in a structured format
            results[name] = {
                "Covered Edges": covered_edges,
                "Runtime (s)": runtime,
                "Vertex Cover": cover
            }

    return results


# ==========================================================
# Main Execution: Load Graphs, Run Algorithm, and Display Results
# ==========================================================

# ----------------------------------------------------------
# Define file paths to graph datasets (in .gexf format)
# ----------------------------------------------------------
# Each key represents a graph name, and each value is the file path.
graph_files = {
    "yeast": "datasets/yeast.gexf",
    "eurosis": "datasets/EuroSiS_Generale_Pays.gexf",
    "codeminer": "datasets/codeminer.gexf",
    "cpan-authors": "datasets/cpan-authors.gexf"
}

# ----------------------------------------------------------
# Define the maximum number of nodes allowed in the vertex cover
# ----------------------------------------------------------
# Each key corresponds to the same graph name in `graph_files`.
Max_Node_values = {
    "codeminer": 191,
    "cpan-authors": 116,
    "eurosis": 597,
    "yeast": 763
}

# ----------------------------------------------------------
# Execute the algorithm on all graphs and collect results
# ----------------------------------------------------------
results = run_algorithm(graph_files, Max_Node_values)

# ----------------------------------------------------------
# Display the results for each graph in a readable format
# ----------------------------------------------------------
for name, result in results.items():
    print(f"Graph: {name}")
    print(f"Covered Edges: {result['Covered Edges']} Edges")
    print(f"Runtime: {result['Runtime (s)']} seconds\n")

