"""
Регрессионные тесты для предотвращения повторного появления исправленных ошибок.
"""

import pytest

from src.algorithms.astar import astar_search, dijkstra_search
from src.algorithms.heuristics import ManhattanHeuristic
from src.algorithms.pathfinder import bfs_path, find_all_paths
from src.core.builder import GraphBuilder, GraphFactory
from src.core.enums import GraphType
from src.core.graph import AdjacencyListGraph
from src.exceptions.exceptions import NegativeEdgeWeightException, NodeNotFoundException


class TestFixedIssues:
    """Проверка, что ранее исправленные ошибки не вернулись."""

    def test_issue_negative_weight_rejected(self):
        graph = AdjacencyListGraph()
        with pytest.raises(NegativeEdgeWeightException):
            graph.add_edge("A", "B", -1.0)

    def test_issue_zero_weight_allowed(self):
        graph = AdjacencyListGraph()
        graph.add_edge("A", "B", 0.0)
        assert graph.get_edge_weight("A", "B") == 0.0

    def test_issue_remove_node_clears_edges(self):
        graph = AdjacencyListGraph()
        graph.add_edge("A", "B")
        graph.add_edge("A", "C")
        graph.remove_node("A")
        assert not graph.has_node("A")
        assert not graph.has_edge("A", "B")
        assert not graph.has_edge("A", "C")

    def test_issue_undirected_edge_count(self):
        graph = AdjacencyListGraph(GraphType.UNDIRECTED)
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        assert graph.edge_count == 2
        graph.add_edge("A", "C")
        assert graph.edge_count == 3  #

    def test_issue_astar_with_zero_weights_chooses_shortest(self):
        graph = AdjacencyListGraph()
        graph.add_edge("A", "B", 0)
        graph.add_edge("B", "C", 0)
        graph.add_edge("A", "C", 10)
        result = astar_search(graph, "A", "C", ManhattanHeuristic())
        assert result.path == ["A", "B", "C"]
        assert result.distance == 0

    def test_issue_astar_heuristic_not_overestimate(self):
        grid = GraphFactory.create_grid(5, 5)
        start, goal = (0, 0), (4, 4)
        real = dijkstra_search(grid, start, goal)
        estimate = ManhattanHeuristic().estimate(start, goal)
        assert estimate <= real.distance + 1e-9

    def test_issue_find_all_paths_no_duplicates(self):
        graph = (
            GraphBuilder[str](GraphType.UNDIRECTED)
            .add_edges(("A", "B"), ("B", "C"), ("A", "C"))
            .build()
        )
        paths = find_all_paths(graph, "A", "C", max_depth=3)
        path_strings = [str(p) for p in paths]
        assert len(path_strings) == len(set(path_strings))

    def test_issue_bfs_path_in_directed_cycle(self):
        graph = AdjacencyListGraph(GraphType.DIRECTED)
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        graph.add_edge("C", "A")
        path = bfs_path(graph, "C", "B")
        assert path is not None
        assert path[0] == "C"
        assert path[-1] == "B"

    def test_issue_node_not_found_exception(self):
        graph = AdjacencyListGraph()
        graph.add_node("A")
        with pytest.raises(NodeNotFoundException):
            graph.get_neighbors("B")
