# src/core/graph.py
"""
Реализация графа на основе списка смежности.
"""

from typing import Dict, Generic, Set, TypeVar

from src.core.enums import GraphType
from src.core.interfaces import IGraph
from src.exceptions.exceptions import (
    EdgeNotFoundException,
    NegativeEdgeWeightException,
    NodeNotFoundException,
)

T = TypeVar("T")


class AdjacencyListGraph(IGraph[T], Generic[T]):
    """
    Реализация графа на основе списка смежности.

    Хранит граф как словарь: узел -> {сосед: вес}
    Поддерживает направленные и ненаправленные графы.
    """

    def __init__(self, graph_type: GraphType = GraphType.DIRECTED):
        """
        Инициализация пустого графа.

        Args:
            graph_type: Тип графа (направленный/ненаправленный)
        """
        self._adjacency: Dict[T, Dict[T, float]] = {}
        self._type = graph_type

    def add_node(self, node: T) -> None:
        """Добавить узел, если его нет."""
        if node not in self._adjacency:
            self._adjacency[node] = {}

    def add_nodes(self, *nodes: T) -> None:
        """
        Добавить несколько узлов.

        Args:
            *nodes: Узлы для добавления
        """
        for node in nodes:
            self.add_node(node)

    def add_edge(self, from_node: T, to_node: T, weight: float = 1.0) -> None:
        """
        Добавить ребро с проверкой веса.

        Raises:
            NegativeEdgeWeightException: если weight < 0
        """
        if weight < 0:
            raise NegativeEdgeWeightException(f"Вес ребра не может быть отрицательным: {weight}")

        # Добавляем узлы при необходимости
        self.add_node(from_node)
        self.add_node(to_node)

        # Добавляем прямое ребро
        self._adjacency[from_node][to_node] = weight

        # Для ненаправленного графа добавляем обратное ребро
        if self._type == GraphType.UNDIRECTED:
            self._adjacency[to_node][from_node] = weight

    def get_nodes(self) -> Set[T]:
        """Вернуть множество всех узлов."""
        return set(self._adjacency.keys())

    def get_neighbors(self, node: T) -> Dict[T, float]:
        """
        Вернуть соседей узла.

        Raises:
            NodeNotFoundException: если узел не существует
        """
        self._validate_node_exists(node)
        return self._adjacency[node].copy()  # Защитная копия

    def has_node(self, node: T) -> bool:
        """Проверить существование узла."""
        return node in self._adjacency

    def has_edge(self, from_node: T, to_node: T) -> bool:
        """Проверить существование ребра."""
        return self.has_node(from_node) and to_node in self._adjacency[from_node]

    def get_edge_weight(self, from_node: T, to_node: T) -> float:
        """
        Получить вес ребра.

        Raises:
            EdgeNotFoundException: если ребро не существует
        """
        if not self.has_edge(from_node, to_node):
            raise EdgeNotFoundException(f"Ребро {from_node} -> {to_node} не найдено")
        return self._adjacency[from_node][to_node]

    def remove_node(self, node: T) -> None:
        """Удалить узел и все связанные рёбра."""
        if not self.has_node(node):
            return

        # Удаляем узел
        del self._adjacency[node]

        # Удаляем все ссылки на этот узел
        for other_node in self._adjacency:
            if node in self._adjacency[other_node]:
                del self._adjacency[other_node][node]

    def remove_edge(self, from_node: T, to_node: T) -> None:
        """Удалить ребро, если оно существует."""
        if not self.has_edge(from_node, to_node):
            return

        del self._adjacency[from_node][to_node]

        # Для ненаправленного графа удаляем обратное ребро
        if self._type == GraphType.UNDIRECTED and self.has_edge(to_node, from_node):
            del self._adjacency[to_node][from_node]

    def __str__(self) -> str:
        """Строковое представление графа."""
        if not self._adjacency:
            return "Empty graph"

        lines = [f"Graph type: {self._type}"]
        for node in sorted(self._adjacency.keys(), key=str):
            neighbors = self._adjacency[node]
            if neighbors:
                neighbors_str = ", ".join(
                    f"{n}({w})" for n, w in sorted(neighbors.items(), key=str)
                )
                lines.append(f"  {node} -> {neighbors_str}")
            else:
                lines.append(f"  {node} -> (no neighbors)")
        return "\n".join(lines)

    # Приватные методы валидации
    def _validate_node_exists(self, node: T) -> None:
        """Проверить существование узла, иначе исключение."""
        if not self.has_node(node):
            raise NodeNotFoundException(f"Узел {node} не найден")

    # Свойства для доступа к состоянию
    @property
    def type(self) -> GraphType:
        """Тип графа."""
        return self._type

    @property
    def size(self) -> int:
        """Количество узлов в графе."""
        return len(self._adjacency)

    @property
    def edge_count(self) -> int:
        """Количество рёбер в графе."""
        count = 0
        for node in self._adjacency:
            count += len(self._adjacency[node])

        # Для ненаправленного графа каждое ребро посчитано дважды
        if self._type == GraphType.UNDIRECTED:
            count //= 2
        return count
