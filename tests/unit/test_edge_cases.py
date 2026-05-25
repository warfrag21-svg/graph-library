"""
Тесты граничных случаев.
"""

import math

import pytest

from src.algorithms.astar import astar_search
from src.algorithms.heuristics import (
    EuclideanHeuristic,
    ManhattanHeuristic,
    ZeroHeuristic,
)
from src.algorithms.pathfinder import bfs_path, find_all_paths
from src.algorithms.topological import TopologicalSort, topological_sort
from src.core.builder import GraphFactory
from src.core.enums import GraphType
from src.core.graph import AdjacencyListGraph
from src.exceptions.exceptions import (
    CycleDetectedException,
    EdgeNotFoundException,
    NegativeEdgeWeightException,
    NodeNotFoundException,
    UnsupportedGraphTypeException,
)


class TestEdgeCases:
    """Тесты граничных случаев."""

    def test_empty_graph_operations(self):
        graph = AdjacencyListGraph()
        assert graph.size == 0
        assert graph.edge_count == 0

        with pytest.raises(NodeNotFoundException):
            graph.get_neighbors("A")

        graph.remove_node("A")
        graph.remove_edge("A", "B")

    def test_single_node_graph(self):
        graph = AdjacencyListGraph()
        graph.add_node("A")
        assert graph.size == 1

        result = astar_search(graph, "A", "A", ZeroHeuristic())
        assert result.path == ["A"]
        assert result.distance == 0

    def test_negative_weight(self):
        graph = AdjacencyListGraph()
        with pytest.raises(NegativeEdgeWeightException):
            graph.add_edge("A", "B", -5.0)

    def test_zero_weight(self):
        graph = AdjacencyListGraph()
        graph.add_edge("A", "B", 0.0)
        assert graph.get_edge_weight("A", "B") == 0.0

    def test_nonexistent_nodes(self):
        graph = AdjacencyListGraph()
        graph.add_node("A")

        with pytest.raises(NodeNotFoundException):
            graph.get_neighbors("B")

        with pytest.raises(EdgeNotFoundException):
            graph.get_edge_weight("A", "B")

    def test_start_equals_goal(self):
        graph = AdjacencyListGraph()
        graph.add_node("A")

        result = astar_search(graph, "A", "A", ZeroHeuristic())
        assert result.path == ["A"]

        path = bfs_path(graph, "A", "A")
        assert path == ["A"]

    def test_max_depth_limit(self):
        graph = GraphFactory.create_path([1, 2, 3, 4, 5])

        paths = find_all_paths(graph, 1, 5, max_depth=3)
        assert len(paths) == 0

        paths = find_all_paths(graph, 1, 5, max_depth=4)
        assert len(paths) == 1


class TestExceptions:
    """Тесты исключений."""

    def test_node_not_found(self):
        graph = AdjacencyListGraph()
        with pytest.raises(NodeNotFoundException):
            graph.get_neighbors("A")

    def test_edge_not_found(self):
        graph = AdjacencyListGraph()
        graph.add_nodes("A", "B")
        with pytest.raises(EdgeNotFoundException):
            graph.get_edge_weight("A", "B")

    def test_cycle_detection(self, cyclic_graph):
        with pytest.raises(CycleDetectedException):
            topological_sort(cyclic_graph)

    def test_unsupported_graph_type(self):
        undirected = AdjacencyListGraph(GraphType.UNDIRECTED)
        with pytest.raises(UnsupportedGraphTypeException):
            TopologicalSort(undirected)


class TestHeuristicEdgeCases:
    """Граничные случаи эвристик."""

    def test_heuristic_with_wrong_types(self):
        euclidean = EuclideanHeuristic()
        manhattan = ManhattanHeuristic()

        assert euclidean.estimate("A", "B") == 0.0
        assert euclidean.estimate((1,), (2, 3)) == 0.0

        assert manhattan.estimate("A", "B") == 0.0
        assert manhattan.estimate((1,), (2, 3)) == 0.0
