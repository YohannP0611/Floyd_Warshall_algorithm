
"""
floyd_warshall.py - Floyd-Warshall algorithm implementation.

Computes all-pairs shortest paths in a directed weighted graph.
Detects negative (absorbing) cycles.
Reconstructs shortest paths from the predecessor matrix.
"""

INF = float('inf')


def run(adjacency: list[list[float]]) -> tuple[list[list[float]], list[list[int | None]]]:
    """
    Execute the Floyd-Warshall algorithm.

    Parameters
    ----------
    adjacency : n×n adjacency matrix where adjacency[i][j] is the weight of
                the edge from i to j (INF if no direct edge, 0 on diagonal).

    Returns
    -------
    L : n×n distance matrix – L[i][j] is the shortest-path weight from i to j.
    P : n×n predecessor matrix – P[i][j] is the predecessor of j on the
        shortest path from i, or None if no path exists / same vertex.
    """
    n = len(adjacency)

    # --- Initialise L and P ------------------------------------------------
    # L starts as a copy of the adjacency matrix.
    L = [[adjacency[i][j] for j in range(n)] for i in range(n)]

    # P[i][j] = i when there is a direct edge i->j (including i==j, weight 0),
    #           None otherwise.
    P: list[list[int | None]] = [[None] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if adjacency[i][j] != INF:
                # There is an edge (or the diagonal zero): i is the predecessor
                P[i][j] = i

    # --- Main loop ---------------------------------------------------------
    # For each intermediate vertex k, relax all pairs (i, j).
    for k in range(n):
        for i in range(n):
            for j in range(n):
                # Only relax when both sub-paths are reachable
                if L[i][k] != INF and L[k][j] != INF:
                    new_dist = L[i][k] + L[k][j]
                    if new_dist < L[i][j]:
                        L[i][j] = new_dist
                        # j is reached via k on the shortest path from i
                        P[i][j] = P[k][j]

    return L, P


def has_negative_cycle(L: list[list[float]]) -> bool:
    """
    Return True if the distance matrix *L* reveals a negative (absorbing) cycle.

    After Floyd-Warshall completes, L[i][i] represents the shortest round-trip
    cost from vertex i back to itself. In a graph without negative cycles this
    is always 0 (the trivial path of zero edges). If any L[i][i] < 0, the
    algorithm found a cycle through i whose total weight is negative, so a
    negative cycle exists and is reachable.

    Checking the diagonal is the standard, exact method for negative-cycle
    detection in Floyd-Warshall: every negative cycle must contain at least
    one vertex k, and that vertex will exhibit L[k][k] < 0.
    """
    n = len(L)
    return any(L[i][i] < 0 for i in range(n))


def reconstruct_path(P: list[list[int | None]], source: int, target: int) -> list[int] | None:
    """
    Reconstruct the shortest path from *source* to *target* using matrix *P*.

    Returns
    -------
    list[int] : ordered list of vertex indices from source to target, or
    None      : if no path exists between the two vertices.
    """
    if P[source][target] is None:
        return None  # no path

    path = []
    current = target

    # Walk backwards from target to source following predecessors
    while current != source:
        path.append(current)
        prev = P[source][current]
        if prev is None:
            return None  # broken chain – no path
        current = prev

    path.append(source)
    path.reverse()
    return path


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def _fmt(val: float) -> str:
    """Format a matrix cell for display."""
    if val == INF:
        return "INF"
    # Display as integer when the value is a whole number
    if isinstance(val, float) and val == int(val):
        return str(int(val))
    return str(val)


def display_matrix(matrix: list[list[float | int | None]], title: str, label: str = "v") -> None:
    """
    Print *matrix* with row/column headers.

    Parameters
    ----------
    matrix : square 2-D list (distance or predecessor).
    title  : header text printed above the matrix.
    label  : vertex label prefix (default "v").
    """
    n = len(matrix)
    col_width = 8

    print(f"\n{title}")
    print("=" * (col_width * (n + 1) + 2))

    # Column headers
    header = " " * (col_width + 2)
    for j in range(n):
        header += f"{label + str(j):>{col_width}}"
    print(header)
    print(" " * (col_width + 2) + "-" * (col_width * n))

    # Rows
    for i in range(n):
        row = f"{label + str(i):>{col_width}} |"
        for j in range(n):
            val = matrix[i][j]
            if val is None:
                cell = "-"
            else:
                cell = _fmt(val)
            row += f"{cell:>{col_width}}"
        print(row)
