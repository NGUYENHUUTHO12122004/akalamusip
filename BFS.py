import tkinter as tk
import math

# BFS algorithm
def bfs(graph, start):
    visited = []
    queue = [start]

    while queue:
        current = queue.pop(0)
        if current not in visited:
            visited.append(current)
            queue.extend([node for node in graph[current] if node not in visited])
    return visited

# Function to draw graph
def draw_graph(canvas, graph, positions, path):
    canvas.delete("all")

    # Draw edges
    for node, neighbors in graph.items():
        x1, y1 = positions[node]
        for neighbor in neighbors:
            x2, y2 = positions[neighbor]
            canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

    # Highlight BFS path
    for i in range(len(path) - 1):
        x1, y1 = positions[path[i]]
        x2, y2 = positions[path[i+1]]
        canvas.create_line(x1, y1, x2, y2, fill="red", width=3)

    # Draw nodes
    for node, (x, y) in positions.items():
        color = "red" if node in path else "lightblue"
        canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=color, outline="black", width=2)
        canvas.create_text(x, y, text=node, font=("Arial", 14, "bold"))

# Run BFS and update canvas
def run_bfs():
    start = entry_start.get().strip()
    if start not in graph:
        result_label.config(text="Start node không hợp lệ!")
        return

    path = bfs(graph, start)
    result_label.config(text=f"Path: {' -> '.join(path)}")
    draw_graph(canvas, graph, positions, path)

# Update graph based on user input
def update_graph():
    global graph, positions
    edges = entry_edges.get("1.0", tk.END).strip().split("\n")
    nodes = set()

    graph = {}
    for edge in edges:
        u, v = edge.split("-")
        u, v = u.strip(), v.strip()
        nodes.update([u, v])

        if u not in graph:
            graph[u] = []
        if v not in graph[u]:
            graph[u].append(v)

        if v not in graph:
            graph[v] = []
        if u not in graph[v]:
            graph[v].append(u)

    # Assign positions for nodes (basic circular layout)
    positions = {}
    angle_step = 360 / len(nodes)
    radius = 100
    center_x, center_y = 200, 125
    for i, node in enumerate(sorted(nodes)):
        angle = math.radians(i * angle_step)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        positions[node] = (x, y)

    draw_graph(canvas, graph, positions, [])

# Initial graph and positions
graph = {}
positions = {}

# GUI
root = tk.Tk()
root.title("BFS Visualization with Custom Input")

# Canvas
canvas = tk.Canvas(root, width=400, height=250, bg="white")
canvas.pack(pady=10)

# Input for edges
frame_edges = tk.Frame(root)
frame_edges.pack(pady=5)
tk.Label(frame_edges, text="Edges (u-v, each on a new line):").pack()
entry_edges = tk.Text(frame_edges, width=30, height=5)
entry_edges.pack()

# Button to update graph
tk.Button(frame_edges, text="Update Graph", command=update_graph).pack(pady=5)

# Input and controls
control_frame = tk.Frame(root)
control_frame.pack(pady=10)

tk.Label(control_frame, text="Start Node:").pack(side=tk.LEFT)
entry_start = tk.Entry(control_frame, width=5)
entry_start.pack(side=tk.LEFT, padx=5)

tk.Button(control_frame, text="Run BFS", command=run_bfs).pack(side=tk.LEFT, padx=5)

result_label = tk.Label(root, text="Path: ", font=("Arial", 12))
result_label.pack(pady=10)

# Initial drawing
draw_graph(canvas, graph, positions, [])

root.mainloop()
