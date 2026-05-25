# src/algorithms/topological.py
"""
Реализация топологической сортировки для направленных ациклических графов (DAG).
"""

from collections import defaultdict, deque
from typing import Dict, List, Set, TypeVar

from src.core.enums import GraphType
from src.core.interfaces import IGraph
from src.exceptions.exceptions import (
    CycleDetectedException,
    UnsupportedGraphTypeException,
)

T = TypeVar("T")


class TopologicalSort:
    """
    Класс для выполнения топологической сортировки графа.

    Реализует алгоритм Кана (Kahn's algorithm) с обнаружением циклов.
    Работает только с направленными графами (DAG).
    """

    def __init__(self, graph: IGraph[T]):
        """
        Инициализация топологической сортировки.

        Args:
            graph: Граф для сортировки

        Raises:
            UnsupportedGraphTypeException: если граф ненаправленный
        """
        self.graph = graph
        self._validate_graph_type()

    def _validate_graph_type(self) -> None:
        """Проверка, что граф направленный."""
        if hasattr(self.graph, "type") and self.graph.type == GraphType.UNDIRECTED:
            raise UnsupportedGraphTypeException(
                "Топологическая сортировка применима только к направленным графам. "
                f"Получен тип: {self.graph.type}"
            )

    def sort(self) -> List[T]:
        """
        Выполнить топологическую сортировку.

        Returns:
            List[T]: Узлы в топологическом порядке

        Raises:
            CycleDetectedException: если граф содержит циклы
        """
        nodes = self.graph.get_nodes()
        if not nodes:
            return []

        # Вычисляем входящие степени
        in_degree: Dict[T, int] = defaultdict(int)
        for node in nodes:
            for neighbor in self.graph.get_neighbors(node):
                in_degree[neighbor] += 1

        # Очередь узлов с нулевой входящей степенью
        queue = deque([node for node in nodes if in_degree[node] == 0])

        if not queue and nodes:
            raise CycleDetectedException(
                "Граф не содержит узлов с нулевой входящей степенью. "
                "Вероятно, граф содержит циклы."
            )

        result: List[T] = []

        while queue:
            node = queue.popleft()
            result.append(node)

            for neighbor in self.graph.get_neighbors(node):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(result) != len(nodes):
            raise CycleDetectedException(
                f"Граф содержит циклы. Отсортировано {len(result)} из {len(nodes)} узлов."
            )

        return result

    def is_dag(self) -> bool:
        """
        Проверить, является ли граф ациклическим (DAG).

        Returns:
            bool: True если граф не содержит циклов
        """
        try:
            self.sort()
            return True
        except CycleDetectedException:
            return False

    def find_cycles(self) -> List[List[T]]:
        """
        Найти все циклы в графе (упрощённая версия).

        Returns:
            List[List[T]]: Список найденных циклов
        """
        nodes = self.graph.get_nodes()
        visited: Set[T] = set()
        rec_stack: Set[T] = set()
        cycles: List[List[T]] = []

        def dfs(node: T, path: List[T]) -> None:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in self.graph.get_neighbors(node):
                if neighbor not in visited:
                    dfs(neighbor, path.copy())
                elif neighbor in rec_stack:
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    if cycle not in cycles:
                        cycles.append(cycle)

            rec_stack.remove(node)

        for node in nodes:
            if node not in visited:
                dfs(node, [])

        return cycles


# Функциональный интерфейс
def topological_sort(graph: IGraph[T]) -> List[T]:
    """Функция-обёртка для топологической сортировки."""
    return TopologicalSort(graph).sort()


def is_dag(graph: IGraph[T]) -> bool:
    """Проверить, является ли граф ациклическим."""
    return TopologicalSort(graph).is_dag()


def find_cycles(graph: IGraph[T]) -> List[List[T]]:
    """Найти циклы в графе."""
    return TopologicalSort(graph).find_cycles()
