# src/algorithms/astar.py

import heapq
import time
from collections import defaultdict
from typing import Dict, List, Optional, Set, TypeVar

from src.algorithms.heuristics import HeuristicFunction, ZeroHeuristic
from src.core.interfaces import IGraph
from src.core.models import PathResult
from src.exceptions.exceptions import GraphException, NodeNotFoundException

T = TypeVar("T")


class AStar:
    """
    Реализация алгоритма A* для поиска кратчайшего пути.

    Использует эвристическую функцию для ускорения поиска.
    Если эвристика не указана, используется ZeroHeuristic (Дейкстра).

    Attributes:
        graph: Граф для поиска
        heuristic: Эвристическая функция оценки расстояния
    """

    def __init__(self, graph: IGraph[T], heuristic: Optional[HeuristicFunction] = None):
        """
        Инициализация поиска A*.
        """
        self.graph = graph
        self.heuristic = heuristic or ZeroHeuristic()

    def find_path(self, start: T, goal: T) -> PathResult[T]:
        """
        Найти кратчайший путь от start до goal.
        """
        self._validate_nodes(start, goal)

        if start == goal:
            return PathResult(path=[start], distance=0.0, nodes_explored=1, execution_time_ms=0.0)

        start_time = time.time()

        open_set = []
        heapq.heappush(open_set, (0.0, start))

        came_from: Dict[T, Optional[T]] = {start: None}

        g_score: Dict[T, float] = defaultdict(lambda: float("inf"))
        g_score[start] = 0.0

        f_score: Dict[T, float] = defaultdict(lambda: float("inf"))
        f_score[start] = self.heuristic.estimate(start, goal)

        closed_set: Set[T] = set()
        nodes_explored = 0

        while open_set:
            current_f, current = heapq.heappop(open_set)
            nodes_explored += 1

            if current == goal:
                return self._reconstruct_path(
                    came_from, current, g_score[current], nodes_explored, start_time
                )

            if current_f > f_score[current]:
                continue

            closed_set.add(current)

            for neighbor, weight in self.graph.get_neighbors(current).items():
                if neighbor in closed_set:
                    continue

                tentative_g = g_score[current] + weight

                if tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + self.heuristic.estimate(neighbor, goal)
                    f_score[neighbor] = f

                    heapq.heappush(open_set, (f, neighbor))

        execution_time = (time.time() - start_time) * 1000
        raise GraphException(
            f"Путь от {start} до {goal} не найден. "
            f"Исследовано узлов: {nodes_explored}, "
            f"Время: {execution_time:.2f}ms"
        )

    def find_shortest_path(self, start: T, goal: T) -> Optional[List[T]]:
        """Упрощённый метод: только путь (без метрик)."""
        try:
            result = self.find_path(start, goal)
            return result.path
        except GraphException:
            return None

    def _validate_nodes(self, start: T, goal: T) -> None:
        """Проверить существование узлов."""
        if not self.graph.has_node(start):
            raise NodeNotFoundException(f"Стартовый узел {start} не найден")
        if not self.graph.has_node(goal):
            raise NodeNotFoundException(f"Целевой узел {goal} не найден")

    def _reconstruct_path(
        self,
        came_from: Dict[T, Optional[T]],
        current: T,
        distance: float,
        nodes_explored: int,
        start_time: float,
    ) -> PathResult[T]:
        """Восстановить путь из словаря came_from."""
        path = []
        node = current
        while node is not None:
            path.append(node)
            node = came_from.get(node)

        path.reverse()
        execution_time = (time.time() - start_time) * 1000

        return PathResult(
            path=path,
            distance=distance,
            nodes_explored=nodes_explored,
            execution_time_ms=execution_time,
        )


# Функциональный интерфейс
def astar_search(
    graph: IGraph[T], start: T, goal: T, heuristic: Optional[HeuristicFunction] = None
) -> PathResult[T]:
    """Функция-обёртка для поиска A*."""
    return AStar(graph, heuristic).find_path(start, goal)


def dijkstra_search(graph: IGraph[T], start: T, goal: T) -> PathResult[T]:
    """Алгоритм Дейкстры (частный случай A* с нулевой эвристикой)."""
    return astar_search(graph, start, goal, ZeroHeuristic())
