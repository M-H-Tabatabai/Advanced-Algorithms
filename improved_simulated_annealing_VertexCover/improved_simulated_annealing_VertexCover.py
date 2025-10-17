# ============================
# Import Required Libraries
# ============================
import random        # For generating random numbers and random samples
import time          # For measuring execution time of algorithms
import networkx as nx  # For creating, analyzing, and processing graphs
import numpy as np     # For numerical operations and array computations

# ==========================================================
# Implements an Improved Simulated Annealing algorithm 
# for solving the Vertex Cover problem on a graph.
# ==========================================================

import random
import numpy as np

def improved_simulated_annealing_VertexCover(
    graph, 
    Max_Node, 
    initial_temp=1500, 
    cooling_rate=0.9, 
    max_iteration=1500, 
    early_stop=150
):
    """
    Performs an improved simulated annealing search to find a vertex cover.

    Args:
        graph (networkx.Graph): The input graph.
        Max_Node (int): Maximum number of nodes allowed in the vertex cover.
        initial_temp (float, optional): Initial temperature of the algorithm. Default is 1500.
        cooling_rate (float, optional): Rate at which temperature decreases per iteration. Default is 0.9.
        max_iteration (int, optional): Maximum number of iterations. Default is 1500.
        early_stop (int, optional): Max consecutive iterations without improvement before stopping. Default is 150.

    Returns:
        tuple: (best_solution_nodes, best_covered_edges)
            - best_solution_nodes (list): List of nodes in the best vertex cover found.
            - best_covered_edges (int): Number of edges covered by the best solution.
    """

    # Extract graph data
    nodes = list(graph.nodes)  # List of all nodes
    edges = set(graph.edges)   # Set of all edges

    # Create an initial random vertex cover
    current_solution = set(random.sample(nodes, Max_Node))
    best_solution = current_solution.copy()
    
    # Function to count edges covered by a given set of nodes
    def count_covered_edges(cover):
        return len([edge for edge in edges if edge[0] in cover or edge[1] in cover])

    # Track best coverage and temperature
    best_covered = count_covered_edges(best_solution)
    current_temp = initial_temp
    no_improvement_iterations = 0

    for i in range(max_iteration):
        # Stop if no improvement for early_stop iterations
        if no_improvement_iterations >= early_stop:
            break

        # Select a node to remove from current solution
        node_out = random.choice(list(current_solution))
        node_in_candidates = [node for node in nodes if node not in current_solution]
        if node_in_candidates:
            # Select a node with highest degree to maximize edge coverage
            node_in = max(node_in_candidates, key=lambda n: graph.degree[n])
        else:
            continue

        # Generate new solution
        new_solution = current_solution.copy()
        new_solution.remove(node_out)
        new_solution.add(node_in)

        # Calculate covered edges in the new solution
        new_covered = count_covered_edges(new_solution)

        # Decide whether to accept the new solution
        new_best_difference = new_covered - best_covered
        if current_temp > 0 and (
            new_best_difference > 0 or random.random() < np.exp(new_best_difference / current_temp)
        ):
            current_solution = new_solution
            if new_covered > best_covered:
                best_solution = current_solution
                best_covered = new_covered
                no_improvement_iterations = 0
            else:
                no_improvement_iterations += 1

        # Decrease temperature
        current_temp *= cooling_rate * (1 - i / max_iteration)

    return list(best_solution), best_covered

# Function to run the improved simulated annealing vertex cover algorithm on multiple graphs
def run_algorithm(graph_files, Max_Node_values):
    """
    Executes the vertex cover algorithm on a collection of graphs.

    Parameters:
    - graph_files (dict): Dictionary where keys are graph names and values are paths to GEXF files.
    - Max_Node_values (dict): Dictionary mapping graph names to their corresponding Max_Node limits.

    Returns:
    - results (dict): Dictionary containing results for each graph with keys:
        "Covered Edges" -> number of edges covered by the vertex cover
        "Runtime (s)"   -> execution time in seconds
        "Vertex Cover"  -> list of nodes included in the vertex cover
    """
    results = {}  # Initialize a dictionary to store results for each graph

    for name, path in graph_files.items():
        # Load the graph from the GEXF file
        graph = nx.read_gexf(path)
        
        # Retrieve the Max_Node value for the current graph, if specified
        Max_Node = Max_Node_values.get(name, None)
        
        if Max_Node:
            # Record start time for runtime measurement
            start_time = time.time()
            
            # Run the improved simulated annealing vertex cover algorithm
            cover, covered_edges = improved_simulated_annealing_VertexCover(graph, Max_Node)
            
            # Calculate total execution time
            runtime = time.time() - start_time
            
            # Store results in the dictionary
            results[name] = {
                "Covered Edges": covered_edges,
                "Runtime (s)": runtime,
                "Vertex Cover": cover
            }

    return results  # Return the compiled results for all graphs



# Dictionary containing file paths for each graph in GEXF format
graph_files = {
    "yeast": "datasets/yeast.gexf",
    "eurosis": "datasets/EuroSiS_Generale_Pays.gexf",
    "codeminer": "datasets/codeminer.gexf",
    "cpan-authors": "datasets/cpan-authors.gexf"
}

# Maximum number of nodes to be considered in the vertex cover for each graph
Max_Node_values = {
    "codeminer": 191,
    "cpan-authors": 116,
    "eurosis": 597,
    "yeast": 763
}

# Execute the vertex cover algorithm on all graphs
results = run_algorithm(graph_files, Max_Node_values)

# Display the results for each graph
for name, result in results.items():
    print(f"Graph: {name}")
    print(f"Covered Edges: {result['Covered Edges']} Edges")  # Number of edges covered by the computed vertex cover
    print(f"Runtime: {result['Runtime (s)']} seconds \n")     # Time taken to compute the vertex cover
