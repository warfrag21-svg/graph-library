"""
Тесты для строителя графов.
"""

import pytest

from src.core.builder import GraphBuilder, GraphFactory
from src.core.enums import GraphType
from src.exceptions.exceptions import NegativeEdgeWeightException


class TestGraphBuilder:
    """Тесты для строителя графов."""

    def test_builder_initialization(self):
        builder = GraphBuilder[str]()
        assert builder._graph_type == GraphType.DIRECTED

        builder = GraphBuilder[int](GraphType.UNDIRECTED)
        assert builder._graph_type == GraphType.UNDIRECTED

    def test_builder_add_node(self):
        builder = GraphBuilder[str]()
        result = builder.add_node("A")
        assert result is builder

        graph = builder.build()
        assert graph.has_node("A")
        assert graph.size == 1

    def test_builder_add_nodes(self):
        builder = GraphBuilder[str]()
        builder.add_nodes("A", "B", "C")
        graph = builder.build()
        assert graph.size == 3

    def test_builder_add_edge(self):
        builder = GraphBuilder[str]()
        builder.add_edge("A", "B", 5.0)
        graph = builder.build()
        assert graph.has_edge("A", "B")
        assert graph.get_edge_weight("A", "B") == 5.0

    def test_builder_add_edges(self):
        builder = GraphBuilder[str]()
        builder.add_edges(("A", "B", 1.0), ("B", "C", 2.0))
        graph = builder.build()
        assert graph.has_edge("A", "B")
        assert graph.has_edge("B", "C")

    def test_builder_chain(self):
        graph = GraphBuilder[str]().add_node("A").add_node("B").add_edge("A", "B", 2.0).build()
        assert graph.has_edge("A", "B")
        assert graph.size == 2

    def test_builder_reset(self):
        builder = GraphBuilder[str]()
        builder.add_nodes("A", "B", "C")
        assert builder.build().size == 3
        builder.reset()
        assert builder.build().size == 0

    def test_builder_copy(self):
        builder = GraphBuilder[str]()
        builder.add_nodes("A", "B")
        builder.add_edge("A", "B")

        copy = builder.copy()
        copy.add_node("C")

        assert builder.build().size == 2
        assert copy.build().size == 3

    def test_builder_with_directed_graph(self):
        graph = GraphBuilder[str](GraphType.DIRECTED).add_edge("A", "B").build()
        assert graph.has_edge("A", "B")
        assert not graph.has_edge("B", "A")

    def test_builder_with_undirected_graph(self):
        graph = GraphBuilder[str](GraphType.UNDIRECTED).add_edge("A", "B").build()
        assert graph.has_edge("A", "B")
        assert graph.has_edge("B", "A")

    def test_builder_negative_weight(self):
        builder = GraphBuilder[str]()
        with pytest.raises(NegativeEdgeWeightException):
            builder.add_edge("A", "B", -1.0)


class TestGraphFactory:
    """Тесты для фабрики графов."""

    def test_create_grid(self):
        grid = GraphFactory.create_grid(3, 3)
        assert grid.size == 9
        assert grid.has_edge((0, 0), (1, 0))
        assert grid.has_edge((0, 0), (0, 1))

    def test_create_random(self):
        graph = GraphFactory.create_random(10, 0.5, seed=42)
        assert graph.size == 10
        assert 0 <= graph.edge_count <= 45

    def test_create_complete(self):
        nodes = ["A", "B", "C", "D"]
        graph = GraphFactory.create_complete(nodes)
        assert graph.edge_count == 6
        assert graph.has_edge("A", "B")
        assert graph.has_edge("A", "C")
        assert graph.has_edge("A", "D")

    def test_create_path(self):
        nodes = ["A", "B", "C", "D"]
        graph = GraphFactory.create_path(nodes)
        assert graph.edge_count == 3
        assert graph.has_edge("A", "B")
        assert graph.has_edge("C", "D")
        assert not graph.has_edge("A", "C")

    def test_create_cycle(self):
        nodes = ["A", "B", "C"]
        graph = GraphFactory.create_cycle(nodes)
        assert graph.edge_count == 3
        assert graph.has_edge("A", "B")
        assert graph.has_edge("B", "C")
        assert graph.has_edge("C", "A")

    def test_create_tree(self):
        tree = GraphFactory.create_tree(3, 2, "Node")
        assert tree.size == 7
        assert tree.edge_count == 6
        assert tree.has_node("Node_0")

    def test_from_adjacency_list(self):
        adj_list = {"A": [("B", 2.0), ("C", 3.0)], "B": [("C", 1.0)], "C": []}
        graph = GraphFactory.from_adjacency_list(adj_list)
        assert graph.size == 3
        assert graph.has_edge("A", "B")
        assert graph.get_edge_weight("A", "B") == 2.0
