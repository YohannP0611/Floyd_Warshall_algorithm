"""
graph.py - Graph representation and file loading for Floyd-Warshall algorithm.

The graph is loaded from a .txt file once and stored entirely in memory.
After loading, no further file access is performed.
"""

INF = float('inf')


class Graph:
    """Directed weighted graph stored as an adjacency matrix."""

    def __init__(self):
        self.num_vertices = 0
        self.num_edges = 0
        # adjacency[i][j] = weight of edge i->j, or INF if no edge
        self.adjacency = []

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------

    def load_from_file(self, filepath: str) -> None:
        """
        Load graph data from *filepath* into memory.

        File format:
            <number_of_vertices>
            <number_of_edges>
            <start> <end> <weight>   (one edge per line)

        Raises:
            FileNotFoundError: if the file does not exist.
            ValueError: if the file content is malformed.
        """
        with open(filepath, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]

        if len(lines) < 2:
            raise ValueError("File must contain at least two header lines.")

        self.num_vertices = int(lines[0])
        self.num_edges = int(lines[1])

        n = self.num_vertices

        # Initialise adjacency matrix: diagonal = 0, rest = INF
        self.adjacency = [[INF] * n for _ in range(n)]
        for i in range(n):
            self.adjacency[i][i] = 0

        # Read edges
        edge_lines = lines[2:]
        if len(edge_lines) < self.num_edges:
            raise ValueError(
                f"Expected {self.num_edges} edges but found {len(edge_lines)}."
            )

        for line in edge_lines[:self.num_edges]:
            parts = line.split()
            if len(parts) != 3:
                raise ValueError(f"Invalid edge line: '{line}'")
            u, v, w = int(parts[0]), int(parts[1]), int(parts[2])
            if not (0 <= u < n and 0 <= v < n):
                raise ValueError(
                    f"Vertex index out of range in edge: {u} -> {v}"
                )
            self.adjacency[u][v] = w

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def display(self) -> None:
        """Print the adjacency matrix with row/column headers."""
        n = self.num_vertices
        col_width = 8

        # Header row
        header = " " * (col_width + 2)
        for j in range(n):
            header += f"{'v' + str(j):>{col_width}}"
        print(header)

        # Separator
        print(" " * (col_width + 2) + "-" * (col_width * n))

        # Data rows
        for i in range(n):
            row = f"{'v' + str(i):>{col_width}} |"
            for j in range(n):
                val = self.adjacency[i][j]
                cell = "INF" if val == INF else str(val)
                row += f"{cell:>{col_width}}"
            print(row)
