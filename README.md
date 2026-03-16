# Floyd-Warshall Algorithm

School project for graph theory – a console application that computes
all-pairs shortest paths in a directed weighted graph using the
Floyd-Warshall algorithm.

---

## Project Structure

```
Floyd_Warshall_algorithm/
├── src/
│   ├── main.py            # Entry point – interactive console application
│   ├── graph.py           # Graph class (file loading, adjacency matrix, display)
│   └── floyd_warshall.py  # Floyd-Warshall algorithm, cycle detection, path reconstruction
├── graphs/
│   ├── example_graph1.txt # 4-vertex graph, no negative cycle
│   ├── example_graph2.txt # 5-vertex graph, no negative cycle
│   └── example_graph3.txt # 4-vertex graph with a negative cycle
├── output/
│   └── execution_traces.txt  # Sample program output
└── README.md
```

---

## Requirements

- Python 3.12+
- No external dependencies

---

## How to Run

From the project root directory:

```bash
python src/main.py
```

---

## Graph File Format

```
<number_of_vertices>
<number_of_edges>
<start_vertex> <end_vertex> <weight>
...
```

**Example** (`graphs/example_graph1.txt`):

```
4
5
3 1 25
1 0 12
2 0 -25
0 1 0
2 1 7
```

- Vertices are numbered from `0` to `n-1`.
- Edge weights are integers (negative values and zero are allowed).
- At most one edge between any two vertices.
- Directed edges only.

---

## Features

| Feature | Description |
|---|---|
| Multi-graph loop | Process multiple graphs without restarting |
| File loading | Graph loaded once from `.txt` file, then kept in memory |
| Adjacency matrix display | Readable matrix with row/column headers |
| Floyd-Warshall algorithm | Computes all-pairs shortest paths |
| Distance matrix **L** | Shows shortest-path weight between every pair |
| Predecessor matrix **P** | Used to reconstruct actual paths |
| Negative-cycle detection | Alerts the user if any absorbing cycle is found |
| Path reconstruction | Displays the vertex sequence for any requested path |
| Path query loop | Query multiple source/target pairs interactively |

---

## Algorithm Overview

### Initialisation
- **L[i][j]** = weight of direct edge `i→j`, `0` if `i==j`, `∞` otherwise.
- **P[i][j]** = `i` when a direct edge `i→j` exists (the immediate predecessor of `j`), `None` otherwise.

### Main Loop
For each intermediate vertex `k` from `0` to `n-1`:
```
for i in range(n):
    for j in range(n):
        if L[i][k] + L[k][j] < L[i][j]:
            L[i][j] = L[i][k] + L[k][j]
            P[i][j] = P[k][j]
```

### Negative-Cycle Detection
After the algorithm runs, if any diagonal entry `L[i][i] < 0`, the graph
contains an absorbing (negative) cycle – vertex `i` can reach itself with
negative total cost.

### Path Reconstruction
Walk backwards from the target vertex using the predecessor matrix until
reaching the source, then reverse the resulting list.

---

## Sample Output

See [`output/execution_traces.txt`](output/execution_traces.txt) for a full
execution trace covering all three example graphs.
