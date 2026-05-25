"""
Интеграционные тесты для проверки взаимодействия всех модулей библиотеки.
"""

import pytest

from src.algorithms.astar import astar_search, dijkstra_search
from src.algorithms.heuristics import EuclideanHeuristic, ManhattanHeuristic
from src.algorithms.pathfinder import bfs_path, bfs_traverse, dfs_traverse, has_cycle
from src.algorithms.topological import topological_sort
from src.core.builder import GraphBuilder, GraphFactory
from src.core.enums import GraphType
from src.visualization.matplotlib_adapter import MatplotlibVisualizer


class TestFullWorkflow:
    """Сквозные сценарии использования библиотеки."""

    def test_create_graph_and_find_path(self):
        """Создание графа через Builder, поиск пути A*, визуализация."""
        graph = (
            GraphBuilder[str](GraphType.UNDIRECTED)
            .add_nodes("A", "B", "C", "D", "E")
            .add_edges(("A", "B", 5), ("A", "C", 3), ("B", "D", 2), ("C", "D", 4), ("D", "E", 1))
            .build()
        )

        result = astar_search(graph, "A", "E", ManhattanHeuristic())
        assert result.path in (["A", "C", "D", "E"], ["A", "B", "D", "E"])
        assert result.distance == 8.0

        viz = MatplotlibVisualizer()
        viz.visualize(graph, path=result.path, title="Integration Test")
        viz.close()

    def test_factory_and_topological_sort(self):
        """Фабрика + топологическая сортировка."""
        dag = GraphFactory.from_adjacency_list(
            {"A": [("B", 1), ("C", 1)], "B": [("D", 1)], "C": [("D", 1)], "D": [("E", 1)], "E": []}
        )
        order = topological_sort(dag)
        assert order[0] == "A"
        assert order[-1] == "E"
        assert order.index("B") < order.index("D")
        assert order.index("C") < order.index("D")

    def test_random_graph_astar_bfs_consistency(self):
        """Случайный граф: проверка, что A* и BFS возвращают пути."""
        graph = GraphFactory.create_random(50, 0.1, seed=42)
        nodes = list(graph.get_nodes())
        start, goal = nodes[0], nodes[-1]

        try:
            astar_result = astar_search(graph, start, goal, ManhattanHeuristic())
            astar_path = astar_result.path
        except Exception:
            astar_path = None

        bfs_path_result = bfs_path(graph, start, goal)
        if bfs_path_result is not None:
            assert astar_path is not None
        else:
            assert astar_path is None

    def test_builder_copy_and_dijkstra(self):
        """Копирование строителя и алгоритм Дейкстры."""
        builder = GraphBuilder[int]().add_nodes(1, 2, 3).add_edge(1, 2, 10)
        copy_builder = builder.copy()
        copy_builder.add_edge(2, 3, 5)

        orig_graph = builder.build()
        copy_graph = copy_builder.build()

        with pytest.raises(Exception):
            dijkstra_search(orig_graph, 1, 3)

        result_copy = dijkstra_search(copy_graph, 1, 3)
        assert result_copy.path == [1, 2, 3]
        assert result_copy.distance == 15

    def test_cycle_detection_and_traversal(self):
        """Обнаружение цикла и BFS/DFS обход."""
        graph = GraphFactory.create_cycle(["A", "B", "C", "D"])
        assert has_cycle(graph) is True

        bfs_order = bfs_traverse(graph, "A")
        dfs_order = dfs_traverse(graph, "A")
        assert len(bfs_order) == 4
        assert len(dfs_order) == 4
        assert set(bfs_order) == {"A", "B", "C", "D"}
