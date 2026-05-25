# src/algorithms/pathfinder.py
"""
Реализация алгоритмов поиска путей: BFS, DFS и поиск всех путей.
"""

from collections import deque
from typing import List, Optional, TypeVar

from src.core.interfaces import IGraph
from src.exceptions.exceptions import NodeNotFoundException

T = TypeVar("T")


# ==================== Вспомогательные функции ====================


def _validate_nodes(graph: IGraph[T], start: T, goal: T) -> None:
    """Проверить существование узлов."""
    if not graph.has_node(start):
        raise NodeNotFoundException(f"Узел {start} не найден")
    if not graph.has_node(goal):
        raise NodeNotFoundException(f"Узел {goal} не найден")


def _validate_node(graph: IGraph[T], node: T) -> None:
    """Проверить существование узла."""
    if not graph.has_node(node):
        raise NodeNotFoundException(f"Узел {node} не найден")


# ==================== BFS (Поиск в ширину) ====================


class BFS:
    """
    Поиск в ширину (Breadth-First Search).

    Используется для нахождения кратчайшего пути по количеству рёбер
    и для обхода графа по уровням.
    """

    def __init__(self, graph: IGraph[T]):
        """Инициализация BFS."""
        self.graph = graph

    def find_path(self, start: T, goal: T) -> Optional[List[T]]:
        """
        Найти кратчайший путь по количеству рёбер.

        Args:
            start: Начальный узел
            goal: Целевой узел

        Returns:
            Путь или None, если путь не найден
        """
        _validate_nodes(self.graph, start, goal)

        if start == goal:
            return [start]

        queue = deque([(start, [start])])
        visited = {start}

        while queue:
            node, path = queue.popleft()

            for neighbor in self.graph.get_neighbors(node):
                if neighbor == goal:
                    return path + [neighbor]

                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None

    def traverse(self, start: T) -> List[T]:
        """
        Обойти граф в ширину.

        Args:
            start: Начальный узел

        Returns:
            Порядок обхода узлов
        """
        _validate_node(self.graph, start)

        visited = []
        queue = deque([start])
        visited_set = {start}

        while queue:
            node = queue.popleft()
            visited.append(node)

            for neighbor in self.graph.get_neighbors(node):
                if neighbor not in visited_set:
                    visited_set.add(neighbor)
                    queue.append(neighbor)

        return visited


# ==================== DFS (Поиск в глубину) ====================


class DFS:
    """
    Поиск в глубину (Depth-First Search).

    Используется для обхода графа и обнаружения циклов.
    """

    def __init__(self, graph: IGraph[T]):
        """Инициализация DFS."""
        self.graph = graph

    def traverse(self, start: T) -> List[T]:
        """
        Обойти граф в глубину.

        Args:
            start: Начальный узел

        Returns:
            Порядок обхода узлов
        """
        _validate_node(self.graph, start)

        visited = []
        stack = [start]
        visited_set = {start}

        while stack:
            node = stack.pop()
            visited.append(node)

            for neighbor in self.graph.get_neighbors(node):
                if neighbor not in visited_set:
                    visited_set.add(neighbor)
                    stack.append(neighbor)

        return visited

    def find_path(self, start: T, goal: T, max_depth: int = 100) -> Optional[List[T]]:
        """
        Найти путь с помощью DFS.

        Args:
            start: Начальный узел
            goal: Целевой узел
            max_depth: Максимальная глубина поиска

        Returns:
            Путь или None, если путь не найден
        """
        _validate_nodes(self.graph, start, goal)

        if start == goal:
            return [start]

        stack = [(start, [start], {start})]

        while stack:
            node, path, visited = stack.pop()

            if len(path) > max_depth:
                continue

            for neighbor in self.graph.get_neighbors(node):
                if neighbor == goal:
                    return path + [neighbor]

                if neighbor not in visited:
                    new_visited = visited | {neighbor}
                    stack.append((neighbor, path + [neighbor], new_visited))

        return None

    def has_cycle(self) -> bool:
        """
        Проверить наличие циклов в графе.

        Returns:
            True если есть цикл
        """
        visited = set()
        rec_stack = set()

        def dfs(node: T, parent: Optional[T] = None) -> bool:
            visited.add(node)
            rec_stack.add(node)

            for neighbor in self.graph.get_neighbors(node):
                # Для ненаправленных графов пропускаем обратное ребро к родителю
                if parent is not None and neighbor == parent:
                    continue

                if neighbor not in visited:
                    if dfs(neighbor, node):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        for node in self.graph.get_nodes():
            if node not in visited:
                if dfs(node):
                    return True

        return False


# ==================== Поиск всех путей ====================


def find_all_paths(graph: IGraph[T], start: T, goal: T, max_depth: int = 10) -> List[List[T]]:
    """
    Найти все пути от start до goal с помощью DFS.

    Args:
        graph: Граф для поиска
        start: Начальный узел
        goal: Целевой узел
        max_depth: Максимальная длина пути

    Returns:
        Список всех найденных путей
    """
    _validate_nodes(graph, start, goal)

    if start == goal:
        return [[start]]

    all_paths = []
    stack = [(start, [start], {start})]

    while stack:
        node, path, visited = stack.pop()

        if len(path) > max_depth:
            continue

        for neighbor in graph.get_neighbors(node):
            if neighbor == goal:
                all_paths.append(path + [neighbor])
                continue

            if neighbor not in visited and len(path) < max_depth:
                new_visited = visited | {neighbor}
                stack.append((neighbor, path + [neighbor], new_visited))

    return all_paths


# ==================== Функциональный интерфейс ====================


def bfs_path(graph: IGraph[T], start: T, goal: T) -> Optional[List[T]]:
    """Найти кратчайший путь BFS."""
    return BFS(graph).find_path(start, goal)


def bfs_traverse(graph: IGraph[T], start: T) -> List[T]:
    """Обойти граф BFS."""
    return BFS(graph).traverse(start)


def dfs_traverse(graph: IGraph[T], start: T) -> List[T]:
    """Обойти граф DFS."""
    return DFS(graph).traverse(start)


def has_cycle(graph: IGraph[T]) -> bool:
    """Проверить наличие циклов."""
    return DFS(graph).has_cycle()
