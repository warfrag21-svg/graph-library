"""
Тесты для алгоритма A*.
"""

import math

import pytest

from src.algorithms.astar import AStar, astar_search, dijkstra_search
from src.algorithms.heuristics import (
    EuclideanHeuristic,
    ManhattanHeuristic,
    ZeroHeuristic,
)
from src.core.enums import GraphType
from src.core.graph import AdjacencyListGraph
from src.exceptions.exceptions import GraphException, NodeNotFoundException


class TestAStarInitialization:
    """Тестирование инициализации A*."""

    def test_init_with_default_heuristic(self):
        graph = AdjacencyListGraph()
        astar = AStar(graph)
        assert isinstance(astar.heuristic, ZeroHeuristic)

    def test_init_with_custom_heuristic(self):
        graph = AdjacencyListGraph()
        heuristic = ManhattanHeuristic()
        astar = AStar(graph, heuristic)
        assert astar.heuristic is heuristic


class TestAStarBasic:
    """Базовые тесты алгоритма A*."""

    def setup_method(self):
        self.graph = AdjacencyListGraph(GraphType.DIRECTED)
        self.graph.add_edge("A", "B", 5)
        self.graph.add_edge("A", "C", 7)
        self.graph.add_edge("B", "D", 2)
        self.graph.add_edge("C", "E", 1)
        self.graph.add_edge("E", "B", 3)
        self.astar = AStar(self.graph, ZeroHeuristic())

    def test_simple_path_exists(self):
        result = self.astar.find_path("A", "D")
        assert result.path == ["A", "B", "D"]
        assert result.distance == 7.0
        assert result.is_valid()

    def test_path_to_self(self):
        result = self.astar.find_path("A", "A")
        assert result.path == ["A"]
        assert result.distance == 0.0

    def test_path_not_found(self):
        self.graph.add_node("X")
        with pytest.raises(GraphException):
            self.astar.find_path("A", "X")

    def test_start_node_not_found(self):
        with pytest.raises(NodeNotFoundException):
            self.astar.find_path("X", "A")

    def test_goal_node_not_found(self):
        with pytest.raises(NodeNotFoundException):
            self.astar.find_path("A", "X")

    def test_find_shortest_path(self):
        path = self.astar.find_shortest_path("A", "D")
        assert path == ["A", "B", "D"]


class TestAStarWithHeuristics:
    """Тестирование A* с разными эвристиками."""

    def setup_method(self):
        self.grid = AdjacencyListGraph(GraphType.UNDIRECTED)
        for x in range(3):
            for y in range(3):
                node = (x, y)
                if x > 0:
                    self.grid.add_edge(node, (x - 1, y), 1.0)
                if y > 0:
                    self.grid.add_edge(node, (x, y - 1), 1.0)
        self.start = (0, 0)
        self.goal = (2, 2)

    def test_astar_with_manhattan(self):
        astar = AStar(self.grid, ManhattanHeuristic())
        result = astar.find_path(self.start, self.goal)
        assert len(result.path) == 5
        assert math.isclose(result.distance, 4.0)

    def test_astar_with_euclidean(self):
        astar = AStar(self.grid, EuclideanHeuristic())
        result = astar.find_path(self.start, self.goal)
        assert len(result.path) == 5
        assert math.isclose(result.distance, 4.0)


class TestDijkstra:
    """Тесты алгоритма Дейкстры."""

    def setup_method(self):
        self.graph = AdjacencyListGraph(GraphType.DIRECTED)
        self.graph.add_edge("A", "B", 4)
        self.graph.add_edge("A", "C", 2)
        self.graph.add_edge("B", "C", 1)
        self.graph.add_edge("B", "D", 5)
        self.graph.add_edge("C", "D", 8)
        self.graph.add_edge("C", "E", 10)
        self.graph.add_edge("D", "E", 2)

    def test_dijkstra_search(self):
        result = dijkstra_search(self.graph, "A", "E")
        assert result.distance == 11.0
        assert result.path == ["A", "B", "D", "E"]

    def test_dijkstra_vs_astar(self):
        dijkstra_result = dijkstra_search(self.graph, "A", "E")
        astar_result = astar_search(self.graph, "A", "E", ZeroHeuristic())
        assert dijkstra_result.path == astar_result.path
        assert dijkstra_result.distance == astar_result.distance


class TestAStarEdgeCases:
    """Граничные случаи A*."""

    def test_empty_graph(self):
        graph = AdjacencyListGraph()
        astar = AStar(graph)
        with pytest.raises(NodeNotFoundException):
            astar.find_path("A", "B")

    def test_single_node_graph(self):
        graph = AdjacencyListGraph()
        graph.add_node("A")
        astar = AStar(graph)
        result = astar.find_path("A", "A")
        assert result.path == ["A"]
        assert result.distance == 0.0

    def test_zero_weight_edges(self):
        graph = AdjacencyListGraph()
        graph.add_edge("A", "B", 0)
        graph.add_edge("B", "C", 0)
        astar = AStar(graph)
        result = astar.find_path("A", "C")
        assert result.distance == 0.0
        assert result.path == ["A", "B", "C"]
