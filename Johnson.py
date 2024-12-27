import tkinter as tk
from tkinter import messagebox
import math

# Bellman-Ford Algorithm
def bellman_ford(graph, vertices, source):
    distance = {v: float('inf') for v in vertices}
    distance[source] = 0

    for _ in range(len(vertices) - 1):
        for u in graph:
            for v, w in graph[u]:
                if distance[u] + w < distance[v]:
                    distance[v] = distance[u] + w

    # Check for negative weight cycle
    for u in graph:
        for v, w in graph[u]:
            if distance[u] + w < distance[v]:
                return None  # Negative weight cycle detected

    return distance

# Dijkstra's Algorithm
def dijkstra(graph, vertices, source):
    distance = {v: float('inf') for v in vertices}
    distance[source] = 0
    visited = set()

    while len(visited) < len(vertices):
        u = min((v for v in vertices if v not in visited), key=lambda v: distance[v], default=None)
        if u is None or distance[u] == float('inf'):
            break
        visited.add(u)

        for v, w in graph[u]:
            if v not in visited and distance[u] + w < distance[v]:
                distance[v] = distance[u] + w

    return distance

# Johnson's Algorithm
def johnson(vertices, edges):
    # Add a new vertex 'Q' connected to all vertices with weight 0
    extended_graph = {v: edges.get(v, []) for v in vertices}
    extended_graph['Q'] = [(v, 0) for v in vertices]

    # Run Bellman-Ford from 'Q'
    h = bellman_ford(extended_graph, vertices + ['Q'], 'Q')
    if h is None:
        return None  # Negative weight cycle detected

    # Reweight edges
    reweighted_graph = {}
    for u in edges:
        reweighted_graph[u] = [(v, w + h[u] - h[v]) for v, w in edges[u]]

    # Run Dijkstra for each vertex
    distances = {}
    for u in vertices:
        distances[u] = dijkstra(reweighted_graph, vertices, u)

    # Adjust distances back
    for u in distances:
        for v in distances[u]:
            distances[u][v] += h[v] - h[u]

    return distances

# Draw graph
def draw_graph(canvas, vertices, edges, shortest_paths=None):
    canvas.delete("all")
    positions = {}

    # Position vertices in a circular layout
    angle_step = 360 / len(vertices)
    radius = 150
    center_x, center_y = 300, 300
    for i, vertex in enumerate(vertices):
        angle = math.radians(i * angle_step)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        positions[vertex] = (x, y)
        canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="lightblue", outline="black")
        canvas.create_text(x, y, text=vertex, font=("Arial", 14, "bold"))

    # Draw edges
    for u, neighbors in edges.items():
        x1, y1 = positions[u]
        for v, w in neighbors:
            x2, y2 = positions[v]
            canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill="black", width=2)
            label_x, label_y = (x1 + x2) / 2, (y1 + y2) / 2
            canvas.create_text(label_x, label_y, text=str(w), font=("Arial", 10), fill="red")

    # Highlight shortest paths
    if shortest_paths:
        for u, paths in shortest_paths.items():
            for v, dist in paths.items():
                if dist < float('inf'):
                    x1, y1 = positions[u]
                    x2, y2 = positions[v]
                    canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill="green", width=3)

# Run Johnson's Algorithm
def run_johnson():
    vertices_input = entry_vertices.get().strip()
    edges_input = entry_edges.get("1.0", tk.END).strip()

    if not vertices_input or not edges_input:
        messagebox.showerror("Input Error", "Please enter vertices and edges.")
        return

    vertices = vertices_input.split()
    edges = {v: [] for v in vertices}

    try:
        for edge in edges_input.split("\n"):
            u, v, w = edge.split()
            edges[u].append((v, int(w)))
    except Exception:
        messagebox.showerror("Input Error", "Edges format is incorrect. Use: u v w")
        return

    distances = johnson(vertices, edges)
    if distances is None:
        messagebox.showerror("Negative Cycle", "Graph contains a negative weight cycle.")
        return

    result_label.config(text=f"Shortest Paths:\n{distances}")
    draw_graph(canvas, vertices, edges, distances)

# GUI
root = tk.Tk()
root.title("Johnson's Algorithm Visualization")

# Canvas
canvas = tk.Canvas(root, width=600, height=600, bg="white")
canvas.pack(pady=10)

# Input Frame
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# Vertices Input
tk.Label(input_frame, text="Vertices:").grid(row=0, column=0, sticky="w")
entry_vertices = tk.Entry(input_frame, width=50)
entry_vertices.grid(row=0, column=1)

# Edges Input
tk.Label(input_frame, text="Edges (u v w):").grid(row=1, column=0, sticky="w")
entry_edges = tk.Text(input_frame, width=50, height=10)
entry_edges.grid(row=1, column=1)

# Run Button
tk.Button(input_frame, text="Run Johnson", command=run_johnson).grid(row=2, column=0, columnspan=2, pady=10)

# Result Label
result_label = tk.Label(root, text="", font=("Arial", 10), justify="left")
result_label.pack(pady=10)

root.mainloop()
