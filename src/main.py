"""
main.py - Console application for the Floyd-Warshall shortest-path algorithm.

Usage:
    python main.py

The program runs in a loop, letting the user:
  1. Choose a graph file by number (graphs/example_graph<N>.txt).
  2. Load and display the graph's adjacency matrix.
  3. Run Floyd-Warshall and display the distance (L) and predecessor (P) matrices.
  4. Detect absorbing (negative) cycles.
  5. If the graph is cycle-free, query shortest paths between any two vertices.
  6. Repeat with a new graph without restarting.
"""

import os
import sys

# Ensure the src/ directory is on the path when running from the project root.
sys.path.insert(0, os.path.dirname(__file__))

from graph import Graph
import floyd_warshall as fw

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

GRAPHS_DIR = os.path.join(os.path.dirname(__file__), '..', 'graphs')
INF = float('inf')


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def clear_screen() -> None:
    """Clear the console screen (works on Windows and Unix)."""
    os.system('cls' if os.name == 'nt' else 'clear')


def separator(char: str = '-', width: int = 60) -> None:
    print(char * width)


def prompt_int(msg: str, min_val: int | None = None, max_val: int | None = None) -> int:
    """
    Prompt the user for an integer, repeating until a valid value is entered.

    Parameters
    ----------
    msg     : Prompt text displayed to the user.
    min_val : Optional lower bound (inclusive). Re-prompts if value is below this.
    max_val : Optional upper bound (inclusive). Re-prompts if value is above this.
    """
    while True:
        raw = input(msg).strip()
        try:
            value = int(raw)
        except ValueError:
            print("  Please enter a valid integer.")
            continue
        if min_val is not None and value < min_val:
            print(f"  Value must be >= {min_val}.")
            continue
        if max_val is not None and value > max_val:
            print(f"  Value must be <= {max_val}.")
            continue
        return value


def load_graph(graph_number: int) -> Graph | None:
    """
    Build the filename from *graph_number*, load the graph, and return it.
    Returns None if loading fails (file not found or malformed).
    """
    filename = f"graph {graph_number}.txt"
    filepath = os.path.normpath(os.path.join(GRAPHS_DIR, filename))

    print(f"\n  Loading graph from: {filepath}")

    graph = Graph()
    try:
        graph.load_from_file(filepath)
    except FileNotFoundError:
        print(f"  ERROR: File '{filepath}' not found.")
        return None
    except ValueError as exc:
        print(f"  ERROR: {exc}")
        return None

    print(f"  Graph loaded: {graph.num_vertices} vertices, {graph.num_edges} edges.")
    return graph


# ---------------------------------------------------------------------------
# Path-query sub-loop
# ---------------------------------------------------------------------------

def path_query_loop(graph: Graph, L: list, P: list) -> None:
    """
    Allow the user to query shortest paths interactively until they choose to stop.
    """
    n = graph.num_vertices
    while True:
        separator()
        print("\n  Shortest path query")
        source = prompt_int(f"  Enter source vertex (0-{n - 1}): ", 0, n - 1)
        target = prompt_int(f"  Enter target vertex (0-{n - 1}): ", 0, n - 1)

        dist = L[source][target]
        if dist == INF:
            print(f"\n  No path exists from v{source} to v{target}.")
        else:
            path = fw.reconstruct_path(P, source, target)
            if path is None:
                print(f"\n  No path exists from v{source} to v{target}.")
            else:
                path_str = " -> ".join(f"v{v}" for v in path)
                print(f"\n  Shortest path : {path_str}")
                print(f"  Total distance: {dist}")

        again = input("\n  Query another path? (y/n): ").strip().lower()
        if again != 'y':
            break


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def main() -> None:
    clear_screen()
    separator('=')
    print("  Floyd-Warshall Shortest Path Algorithm")
    separator('=')

    while True:
        # --- Step 1: choose a graph ----------------------------------------
        print()
        graph_number = prompt_int("Select graph number (e.g. 1 for graph1.txt): ", 1)

        graph = load_graph(graph_number)
        if graph is None:
            retry = input("  Try another graph? (y/n): ").strip().lower()
            if retry != 'y':
                break
            continue

        # --- Step 2: display adjacency matrix --------------------------------
        separator()
        print("\n  Adjacency matrix (initial graph):")
        graph.display()

        # --- Step 3: run Floyd-Warshall --------------------------------------
        separator()
        print("\n  Running Floyd-Warshall algorithm...")
        L, P = fw.run(graph.adjacency)

        # Display distance matrix
        fw.display_matrix(L, "Distance matrix L (shortest-path weights):")

        # Display predecessor matrix
        fw.display_matrix(P, "Predecessor matrix P:")

        # --- Step 4: negative-cycle detection --------------------------------
        separator()
        if fw.has_negative_cycle(L):
            print("\n  *** ABSORBING (NEGATIVE) CYCLE DETECTED ***")
            print("  The graph contains a negative cycle.")
            print("  Shortest paths are not well-defined for all vertex pairs.")
        else:
            print("\n  No absorbing cycle detected.")
            print("  All shortest-path distances are valid.")

            # --- Step 5: path queries ----------------------------------------
            want_path = input("\n  Query shortest paths? (y/n): ").strip().lower()
            if want_path == 'y':
                path_query_loop(graph, L, P)

        # --- Step 6: process another graph? ----------------------------------
        separator()
        another = input("\n  Process another graph? (y/n): ").strip().lower()
        if another != 'y':
            break

    separator('=')
    print("  Goodbye!")
    separator('=')


if __name__ == '__main__':
    main()
