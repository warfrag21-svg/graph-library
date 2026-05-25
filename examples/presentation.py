from src.algorithms.astar import astar_search, dijkstra_search
from src.algorithms.heuristics import (
    ChebyshevHeuristic,
    EuclideanHeuristic,
    ManhattanHeuristic,
    OctileHeuristic,
    ZeroHeuristic,
)
from src.algorithms.pathfinder import bfs_path, bfs_traverse, dfs_traverse
from src.algorithms.topological import topological_sort
from src.core.builder import GraphBuilder, GraphFactory
from src.core.enums import GraphType
from src.core.graph import AdjacencyListGraph
from src.visualization.matplotlib_adapter import MatplotlibVisualizer

graph = AdjacencyListGraph(GraphType.UNDIRECTED)
graph.add_node("A")
graph.add_edge("A", "B", 5)


graph = (
    GraphBuilder[str](GraphType.UNDIRECTED)
    .add_nodes("A", "B", "C", "D")
    .add_edges(("A", "B", 5), ("A", "C", 3))
    .build()
)

grid = GraphFactory.create_grid(5, 5)
random_graph = GraphFactory.create_random(100, 0.3)
complete = GraphFactory.create_complete(["A", "B", "C"])

grid = GraphFactory.create_grid(11, 11)
result1 = astar_search(grid, (0, 0), (10, 4), ManhattanHeuristic())
result2 = astar_search(grid, (0, 0), (4, 10), EuclideanHeuristic())
result3 = astar_search(grid, (2, 1), (4, 4), ChebyshevHeuristic())
print("Манхеттенская евристика")
print(f"Путь: {result1.path}")
print(f"Расстояние: {result1.distance}")
print("\nЕвристика Евклида")
print(f"Путь: {result2.path}")
print(f"Расстояние: {result2.distance}")
print("\nЕвристика Чебышева")
print(f"Путь: {result3.path}")
print(f"Расстояние: {result3.distance}")

dag = AdjacencyListGraph[str](GraphType.DIRECTED)
dag.add_edge("A", "B")
dag.add_edge("A", "C")
dag.add_edge("B", "D")
dag.add_edge("B", "E")
dag.add_edge("C", "E")
dag.add_edge("C", "F")
dag.add_edge("D", "G")
dag.add_edge("E", "G")
dag.add_edge("F", "G")
order = topological_sort(dag)
print(f"Порядок: {' → '.join(order)}")

graph = (
    GraphBuilder[str](GraphType.UNDIRECTED)
    .add_nodes("A", "B", "C", "D", "E", "F", "G", "H")
    .add_edges(
        ("A", "B", 1),
        ("A", "C", 1),
        ("B", "D", 1),
        ("B", "E", 1),
        ("C", "F", 1),
        ("C", "G", 1),
        ("D", "H", 1),
    )
    .build()
)

bfs_order = bfs_traverse(graph, "A")
dfs_order = dfs_traverse(graph, "A")
print()
print(f"Поиск в ширину (BFS): {' →' .join(bfs_order)}")
print(f"Поиск в глубину (DFS): {' → '.join(dfs_order)}")


from src.core.builder import GraphFactory
from src.core.enums import GraphType

grid = GraphFactory.create_grid(5, 5, diagonal=False)
grid_diag = GraphFactory.create_grid(5, 5, diagonal=True)
random_g = GraphFactory.create_random(10, 0.3, seed=42)
complete = GraphFactory.create_complete(["A", "B", "C", "D", "E"])
path = GraphFactory.create_path([1, 2, 3, 4, 5])
cycle = GraphFactory.create_cycle(["A", "B", "C", "D", "E"])
tree = GraphFactory.create_tree(3, 2, "Node")
bipartite = GraphFactory.create_bipartite(["A1", "A2", "A3"], ["B1", "B2"], density=1.0)
adj_list = {"A": [("B", 2.0), ("C", 3.0)], "B": [("C", 1.0)]}
from_adj = GraphFactory.from_adjacency_list(adj_list)
