"""
Тесты для реализации графа.
"""

import pytest

from src.core.enums import GraphType
from src.core.graph import AdjacencyListGraph
from src.exceptions.exceptions import (
    EdgeNotFoundException,
    NegativeEdgeWeightException,
    NodeNotFoundException,
)


class TestAdjacencyListGraph:
    """Тестирование базовых операций графа."""

    def test_init(self):
        g = AdjacencyListGraph()
        assert g.type == GraphType.DIRECTED
        assert g.size == 0

        g = AdjacencyListGraph(GraphType.UNDIRECTED)
        assert g.type == GraphType.UNDIRECTED

    def test_add_node(self):
        g = AdjacencyListGraph()
        g.add_node("A")
        assert g.has_node("A")
        assert g.size == 1

        g.add_node("B")
        assert g.size == 2

        g.add_node("A")
        assert g.size == 2

    def test_add_edge_directed(self):
        g = AdjacencyListGraph(GraphType.DIRECTED)
        g.add_edge("A", "B", 5.0)

        assert g.has_edge("A", "B")
        assert not g.has_edge("B", "A")
        assert g.get_edge_weight("A", "B") == 5.0
        assert g.edge_count == 1

    def test_add_edge_undirected(self):
        g = AdjacencyListGraph(GraphType.UNDIRECTED)
        g.add_edge("A", "B", 5.0)

        assert g.has_edge("A", "B")
        assert g.has_edge("B", "A")
        assert g.edge_count == 1

    def test_add_edge_negative_weight(self):
        g = AdjacencyListGraph()
        with pytest.raises(NegativeEdgeWeightException):
            g.add_edge("A", "B", -1.0)

    def test_get_nodes(self):
        g = AdjacencyListGraph()
        g.add_edge("A", "B")
        g.add_node("C")
        assert g.get_nodes() == {"A", "B", "C"}

    def test_get_neighbors(self):
        g = AdjacencyListGraph()
        g.add_edge("A", "B", 2.0)
        g.add_edge("A", "C", 3.0)

        neighbors = g.get_neighbors("A")
        assert neighbors == {"B": 2.0, "C": 3.0}

    def test_get_neighbors_node_not_found(self):
        g = AdjacencyListGraph()
        with pytest.raises(NodeNotFoundException):
            g.get_neighbors("A")

    def test_has_edge(self):
        g = AdjacencyListGraph()
        g.add_edge("A", "B")

        assert g.has_edge("A", "B") is True
        assert g.has_edge("B", "A") is False
        assert g.has_edge("A", "C") is False

    def test_get_edge_weight(self):
        g = AdjacencyListGraph()
        g.add_edge("A", "B", 7.5)
        assert g.get_edge_weight("A", "B") == 7.5

    def test_get_edge_weight_not_found(self):
        g = AdjacencyListGraph()
        g.add_nodes("A", "B")
        with pytest.raises(EdgeNotFoundException):
            g.get_edge_weight("A", "B")

    def test_remove_node(self):
        g = AdjacencyListGraph()
        g.add_edge("A", "B")
        g.add_edge("A", "C")

        assert g.size == 3
        g.remove_node("A")

        assert not g.has_node("A")
        assert g.size == 2
        assert g.edge_count == 0

    def test_remove_edge_directed(self):
        g = AdjacencyListGraph(GraphType.DIRECTED)
        g.add_edge("A", "B")
        g.add_edge("B", "A")

        assert g.edge_count == 2
        g.remove_edge("A", "B")

        assert not g.has_edge("A", "B")
        assert g.has_edge("B", "A")
        assert g.edge_count == 1

    def test_remove_edge_undirected(self):
        g = AdjacencyListGraph(GraphType.UNDIRECTED)
        g.add_edge("A", "B")

        assert g.edge_count == 1
        g.remove_edge("A", "B")

        assert not g.has_edge("A", "B")
        assert g.edge_count == 0

    def test_str_empty(self):
        g = AdjacencyListGraph()
        assert str(g) == "Empty graph"

    def test_edge_count_directed(self):
        g = AdjacencyListGraph(GraphType.DIRECTED)
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        g.add_edge("B", "C")
        assert g.edge_count == 3

    def test_edge_count_undirected(self):
        g = AdjacencyListGraph(GraphType.UNDIRECTED)
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        assert g.edge_count == 2
        g.add_edge("B", "C")
        assert g.edge_count == 3
