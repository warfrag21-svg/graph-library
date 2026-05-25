# tests/conftest.py
"""
Конфигурация pytest и общие фикстуры для тестов.
"""

import os
import random

# tests/conftest.py
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import pytest

# Добавляем корневую папку проекта в путь
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.builder import GraphBuilder, GraphFactory
from src.core.enums import GraphType

# Теперь можно импортировать
from src.core.graph import AdjacencyListGraph

# ... остальные импорты


@pytest.fixture
def empty_graph():
    """Пустой граф."""
    return AdjacencyListGraph()


@pytest.fixture
def simple_directed_graph():
    """Простой направленный граф."""
    graph = AdjacencyListGraph[str](GraphType.DIRECTED)
    graph.add_edge("A", "B", 5)
    graph.add_edge("B", "C", 3)
    graph.add_edge("A", "C", 7)
    graph.add_edge("C", "D", 2)
    return graph


@pytest.fixture
def simple_undirected_graph():
    """Простой ненаправленный граф."""
    graph = AdjacencyListGraph[str](GraphType.UNDIRECTED)
    graph.add_edge("A", "B", 5)
    graph.add_edge("B", "C", 3)
    graph.add_edge("A", "C", 7)
    graph.add_edge("C", "D", 2)
    return graph


@pytest.fixture
def grid_graph_3x3():
    """Сетка 3x3."""
    return GraphFactory.create_grid(3, 3, diagonal=False)


@pytest.fixture
def grid_graph_5x5():
    """Сетка 5x5."""
    return GraphFactory.create_grid(5, 5, diagonal=False)


@pytest.fixture
def dag_graph():
    """Направленный ациклический граф."""
    graph = AdjacencyListGraph[str](GraphType.DIRECTED)
    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")
    graph.add_edge("C", "D")
    graph.add_edge("D", "E")
    return graph


@pytest.fixture
def cyclic_graph():
    """Граф с циклом."""
    graph = AdjacencyListGraph[str](GraphType.DIRECTED)
    graph.add_edge("A", "B")
    graph.add_edge("B", "C")
    graph.add_edge("C", "A")  # Цикл
    graph.add_edge("C", "D")
    return graph


@pytest.fixture
def tree_graph():
    """Дерево."""
    return GraphFactory.create_tree(3, 2, "Node", weight=1.0)


@pytest.fixture
def complete_graph_k5():
    """Полный граф K5."""
    return GraphFactory.create_complete([1, 2, 3, 4, 5], weight=1.0)


@pytest.fixture
def path_graph_p5():
    """Путь P5."""
    return GraphFactory.create_path(["A", "B", "C", "D", "E"], weight=1.0)


@pytest.fixture
def cycle_graph_c5():
    """Цикл C5."""
    return GraphFactory.create_cycle([1, 2, 3, 4, 5], weight=1.0)


@pytest.fixture
def weighted_graph():
    """Граф с разными весами."""
    graph = AdjacencyListGraph[str](GraphType.UNDIRECTED)
    graph.add_edge("A", "B", 5.5)
    graph.add_edge("B", "C", 3.2)
    graph.add_edge("C", "D", 7.8)
    graph.add_edge("D", "E", 1.1)
    graph.add_edge("A", "E", 10.0)
    graph.add_edge("B", "D", 4.4)
    return graph


@pytest.fixture
def large_graph_100():
    """Граф со 100 узлами для тестов производительности."""
    random.seed(42)  # Для воспроизводимости
    return GraphFactory.create_random(100, 0.05, seed=42)


@pytest.fixture
def large_graph_1000():
    """Граф с 1000 узлами для тестов производительности."""
    random.seed(42)
    return GraphFactory.create_random(1000, 0.01, seed=42)


@pytest.fixture
def graph_with_isolated_nodes():
    """Граф с изолированными узлами."""
    graph = AdjacencyListGraph[str]()
    graph.add_nodes("A", "B", "C", "D", "E")
    graph.add_edge("A", "B")
    graph.add_edge("C", "D")
    # E изолирован
    return graph


@pytest.fixture
def graph_with_self_loop():
    """Граф с петлёй."""
    graph = AdjacencyListGraph[str](GraphType.DIRECTED)
    graph.add_edge("A", "A", 1.0)  # Петля
    graph.add_edge("A", "B")
    return graph
