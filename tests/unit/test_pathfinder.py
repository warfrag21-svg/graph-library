"""
Тесты для алгоритмов поиска путей.
"""

import pytest

from src.algorithms.pathfinder import (
    BFS,
    DFS,
    bfs_path,
    bfs_traverse,
    dfs_traverse,
    has_cycle,
)
from src.core.enums import GraphType
from src.core.graph import AdjacencyListGraph
from src.exceptions.exceptions import NodeNotFoundException


class TestBFS:
    """Тесты поиска в ширину."""

    def setup_method(self):
        self.graph = AdjacencyListGraph(GraphType.UNDIRECTED)
        self.graph.add_edge("A", "B")
        self.graph.add_edge("A", "C")
        self.graph.add_edge("B", "D")
        self.graph.add_edge("B", "E")
        self.graph.add_edge("C", "F")
        self.graph.add_edge("C", "G")
        self.graph.add_edge("E", "H")
        self.bfs = BFS(self.graph)

    def test_bfs_path_exists(self):
        path = self.bfs.find_path("A", "H")
        assert path == ["A", "B", "E", "H"]

    def test_bfs_path_self(self):
        path = self.bfs.find_path("A", "A")
        assert path == ["A"]

    def test_bfs_path_not_found(self):
        self.graph.add_node("X")
        path = self.bfs.find_path("A", "X")
        assert path is None

    def test_bfs_start_not_found(self):
        with pytest.raises(NodeNotFoundException):
            self.bfs.find_path("X", "A")

    def test_bfs_traverse(self):
        order = self.bfs.traverse("A")
        assert order[0] == "A"
        assert set(order) == {"A", "B", "C", "D", "E", "F", "G", "H"}

    def test_bfs_disconnected(self):
        self.graph.add_node("X")
        order = self.bfs.traverse("A")
        assert "X" not in order


class TestDFS:
    """Тесты поиска в глубину."""

    def setup_method(self):
        self.graph = AdjacencyListGraph(GraphType.UNDIRECTED)
        self.graph.add_edge("A", "B")
        self.graph.add_edge("A", "C")
        self.graph.add_edge("B", "D")
        self.graph.add_edge("B", "E")
        self.graph.add_edge("C", "F")
        self.graph.add_edge("C", "G")
        self.graph.add_edge("E", "H")
        self.dfs = DFS(self.graph)

    def test_dfs_traverse(self):
        order = self.dfs.traverse("A")
        assert order[0] == "A"
        assert set(order) == {"A", "B", "C", "D", "E", "F", "G", "H"}

    def test_dfs_path_exists(self):
        path = self.dfs.find_path("A", "H")
        assert path[0] == "A"
        assert path[-1] == "H"

    def test_dfs_path_self(self):
        path = self.dfs.find_path("A", "A")
        assert path == ["A"]

    def test_dfs_has_cycle_self_loop(self):
        graph = AdjacencyListGraph(GraphType.DIRECTED)
        graph.add_edge("A", "A")
        assert DFS(graph).has_cycle() is True


class TestPathfinderEdgeCases:
    """Граничные случаи поиска путей."""

    def test_empty_graph(self):
        graph = AdjacencyListGraph()
        with pytest.raises(NodeNotFoundException):
            BFS(graph).traverse("A")

    def test_single_node(self):
        graph = AdjacencyListGraph()
        graph.add_node("A")
        bfs = BFS(graph)
        assert bfs.find_path("A", "A") == ["A"]

    def test_directed_graph(self):
        graph = AdjacencyListGraph(GraphType.DIRECTED)
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        graph.add_edge("C", "A")

        bfs = BFS(graph)
        assert bfs.find_path("A", "C") == ["A", "B", "C"]
        assert bfs.find_path("C", "B") is not None


class TestFunctionalInterface:
    """Тестирование функционального интерфейса."""

    def setup_method(self):
        self.graph = AdjacencyListGraph()
        self.graph.add_edge("A", "B")
        self.graph.add_edge("B", "C")
        self.graph.add_edge("A", "C")

    def test_bfs_path_function(self):
        path = bfs_path(self.graph, "A", "C")
        assert path in (["A", "B", "C"], ["A", "C"])

    def test_bfs_traverse_function(self):
        order = bfs_traverse(self.graph, "A")
        assert order[0] == "A"
        assert set(order) == {"A", "B", "C"}

    def test_dfs_traverse_function(self):
        order = dfs_traverse(self.graph, "A")
        assert order[0] == "A"
        assert set(order) == {"A", "B", "C"}

    def test_has_cycle_function(self):
        assert has_cycle(self.graph) is False
        self.graph.add_edge("C", "A")
        assert has_cycle(self.graph) is True
