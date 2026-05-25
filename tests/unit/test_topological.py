"""
Тесты для топологической сортировки.
"""

import pytest

from src.algorithms.topological import (
    TopologicalSort,
    find_cycles,
    is_dag,
    topological_sort,
)
from src.core.enums import GraphType
from src.core.graph import AdjacencyListGraph
from src.exceptions.exceptions import (
    CycleDetectedException,
    UnsupportedGraphTypeException,
)


class TestTopologicalSort:
    """Тесты топологической сортировки."""

    def setup_method(self):
        self.linear = AdjacencyListGraph(GraphType.DIRECTED)
        self.linear.add_edge("A", "B")
        self.linear.add_edge("B", "C")
        self.linear.add_edge("C", "D")

        self.dag = AdjacencyListGraph(GraphType.DIRECTED)
        self.dag.add_edge("A", "B")
        self.dag.add_edge("A", "C")
        self.dag.add_edge("B", "D")
        self.dag.add_edge("C", "D")
        self.dag.add_edge("D", "E")

        self.cyclic = AdjacencyListGraph(GraphType.DIRECTED)
        self.cyclic.add_edge("A", "B")
        self.cyclic.add_edge("B", "C")
        self.cyclic.add_edge("C", "A")
        self.cyclic.add_edge("C", "D")

        self.undirected = AdjacencyListGraph(GraphType.UNDIRECTED)
        self.undirected.add_edge("A", "B")
        self.undirected.add_edge("B", "C")

    def test_validate_graph_type(self):
        with pytest.raises(UnsupportedGraphTypeException):
            TopologicalSort(self.undirected)

    def test_sort_linear(self):
        result = topological_sort(self.linear)
        assert result == ["A", "B", "C", "D"]

    def test_sort_dag(self):
        result = topological_sort(self.dag)
        assert result[0] == "A"
        assert result[-1] == "E"
        assert set(result) == {"A", "B", "C", "D", "E"}

    def test_sort_empty_graph(self):
        empty = AdjacencyListGraph(GraphType.DIRECTED)
        result = topological_sort(empty)
        assert result == []

    def test_sort_single_node(self):
        single = AdjacencyListGraph(GraphType.DIRECTED)
        single.add_node("A")
        result = topological_sort(single)
        assert result == ["A"]

    def test_cyclic_graph(self):
        with pytest.raises(CycleDetectedException):
            topological_sort(self.cyclic)

    def test_is_dag(self):
        assert is_dag(self.dag) is True
        assert is_dag(self.linear) is True
        assert is_dag(self.cyclic) is False

    def test_is_dag_undirected(self):
        with pytest.raises(UnsupportedGraphTypeException):
            is_dag(self.undirected)

    def test_find_cycles_simple(self):
        cycles = find_cycles(self.cyclic)
        assert len(cycles) > 0

    def test_find_cycles_no_cycles(self):
        cycles = find_cycles(self.dag)
        assert cycles == []

    def test_dag_with_unconnected(self):
        graph = AdjacencyListGraph(GraphType.DIRECTED)
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        graph.add_edge("X", "Y")
        graph.add_edge("Y", "Z")

        result = topological_sort(graph)
        assert len(result) == 6
        assert set(result) == {"A", "B", "C", "X", "Y", "Z"}


class TestTopologicalEdgeCases:
    """Граничные случаи топологической сортировки."""

    def test_self_loop(self):
        graph = AdjacencyListGraph(GraphType.DIRECTED)
        graph.add_edge("A", "A")

        with pytest.raises(CycleDetectedException):
            topological_sort(graph)
        assert is_dag(graph) is False

    def test_two_node_cycle(self):
        graph = AdjacencyListGraph(GraphType.DIRECTED)
        graph.add_edge("A", "B")
        graph.add_edge("B", "A")

        with pytest.raises(CycleDetectedException):
            topological_sort(graph)

    def test_graph_with_multiple_roots(self):
        graph = AdjacencyListGraph(GraphType.DIRECTED)
        graph.add_edge("A", "C")
        graph.add_edge("B", "C")
        graph.add_edge("C", "D")
        graph.add_edge("E", "F")

        result = topological_sort(graph)
        assert set(result) == {"A", "B", "C", "D", "E", "F"}
        assert result.index("A") < result.index("C")
        assert result.index("B") < result.index("C")
        assert result.index("C") < result.index("D")


def test_functional_interface():
    graph = AdjacencyListGraph(GraphType.DIRECTED)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)

    assert topological_sort(graph) == [1, 2, 3]
    assert is_dag(graph) is True

    graph.add_edge(3, 1)
    assert is_dag(graph) is False
