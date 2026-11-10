class Graph:
    def __init__(self):
        self.adjacency = {}
        self.positions = {}

    def add_node(self, node_id, x, y):
        self.adjacency[node_id] = {}
        self.positions[node_id] = (x, y)

    def add_edge(self, u, v, weight):
        self.adjacency[u][v] = weight
        self.adjacency[v][u] = weight

    def neighbors(self, node):
        return self.adjacency[node]

    def get_position(self, node):
        return self.positions[node]