# src/algorithms/heuristics.py
"""
Эвристические функции для алгоритма A*.
Паттерн Стратегия: разные способы оценки расстояния до цели.
"""

import math
from abc import ABC, abstractmethod
from typing import Any


class HeuristicFunction(ABC):
    """
    Абстрактный базовый класс для всех эвристик.

    Определяет интерфейс для оценки расстояния между двумя узлами.
    Все конкретные эвристики должны наследоваться от этого класса.
    """

    @abstractmethod
    def estimate(self, from_node: Any, to_node: Any) -> float:
        """
        Оценить расстояние между двумя узлами.

        Args:
            from_node: Начальный узел
            to_node: Целевой узел

        Returns:
            float: Оценочное расстояние (должно быть допустимым,
                   т.е. не переоценивать реальное расстояние)
        """
        pass

    def _is_coordinate(self, node: Any) -> bool:
        """Проверить, является ли узел координатой (x, y)."""
        return (
            isinstance(node, (tuple, list))
            and len(node) == 2
            and all(isinstance(coord, (int, float)) for coord in node)
        )

    def __str__(self) -> str:
        """Имя класса эвристики."""
        return self.__class__.__name__


class ZeroHeuristic(HeuristicFunction):
    """
    Нулевая эвристика.

    Всегда возвращает 0. Превращает A* в алгоритм Дейкстры.
    Допустима для любых типов узлов.
    """

    def estimate(self, from_node: Any, to_node: Any) -> float:
        """
        Всегда возвращает 0.

        Args:
            from_node: Начальный узел (игнорируется)
            to_node: Целевой узел (игнорируется)

        Returns:
            float: Всегда 0.0
        """
        return 0.0


class EuclideanHeuristic(HeuristicFunction):
    """
    Евклидова эвристика.

    Вычисляет прямое расстояние между двумя точками.
    Требует, чтобы узлы были кортежами координат (x, y).
    Для строковых узлов возвращает 0 (эвристика не применима).
    """

    def estimate(self, from_node: Any, to_node: Any) -> float:
        """
        Евклидово расстояние: sqrt((x1-x2)² + (y1-y2)²).

        Args:
            from_node: Кортеж (x, y) начальной точки или любой другой тип
            to_node: Кортеж (x, y) целевой точки или любой другой тип

        Returns:
            float: Евклидово расстояние или 0, если узлы не координаты
        """
        # Если узлы не координаты, возвращаем 0 (эвристика не применима)
        if not self._is_coordinate(from_node) or not self._is_coordinate(to_node):
            return 0.0

        dx = from_node[0] - to_node[0]
        dy = from_node[1] - to_node[1]
        return math.sqrt(dx * dx + dy * dy)


class ManhattanHeuristic(HeuristicFunction):
    """
    Манхэттенская эвристика.

    Вычисляет расстояние городских кварталов (сумма модулей разностей).
    Требует, чтобы узлы были кортежами координат (x, y).
    Для строковых узлов возвращает 0 (эвристика не применима).
    """

    def estimate(self, from_node: Any, to_node: Any) -> float:
        """
        Манхэттенское расстояние: |x1-x2| + |y1-y2|.

        Args:
            from_node: Кортеж (x, y) начальной точки или любой другой тип
            to_node: Кортеж (x, y) целевой точки или любой другой тип

        Returns:
            float: Манхэттенское расстояние или 0, если узлы не координаты
        """
        # Если узлы не координаты, возвращаем 0 (эвристика не применима)
        if not self._is_coordinate(from_node) or not self._is_coordinate(to_node):
            return 0.0

        return abs(from_node[0] - to_node[0]) + abs(from_node[1] - to_node[1])


class ChebyshevHeuristic(HeuristicFunction):
    """
    Эвристика Чебышёва.

    Расстояние Чебышёва: max(|x1-x2|, |y1-y2|).
    Полезна для сеток с диагональными движениями.
    """

    def estimate(self, from_node: Any, to_node: Any) -> float:
        """
        Расстояние Чебышёва: max(|x1-x2|, |y1-y2|).

        Args:
            from_node: Кортеж (x, y) начальной точки или любой другой тип
            to_node: Кортеж (x, y) целевой точки или любой другой тип

        Returns:
            float: Расстояние Чебышёва или 0, если узлы не координаты
        """
        if not self._is_coordinate(from_node) or not self._is_coordinate(to_node):
            return 0.0

        dx = abs(from_node[0] - to_node[0])
        dy = abs(from_node[1] - to_node[1])
        return max(dx, dy)


class OctileHeuristic(HeuristicFunction):
    """
    Октаилова эвристика.

    Комбинация манхэттенского и диагонального расстояния.
    Полезна для сеток, где диагональные движения стоят √2.
    """

    def __init__(self, diagonal_cost: float = math.sqrt(2)):
        """
        Инициализация с указанием стоимости диагонального шага.

        Args:
            diagonal_cost: Стоимость диагонального перемещения (по умолчанию √2)
        """
        self.diagonal_cost = diagonal_cost

    def estimate(self, from_node: Any, to_node: Any) -> float:
        """
        Октаилово расстояние.

        Args:
            from_node: Кортеж (x, y) начальной точки или любой другой тип
            to_node: Кортеж (x, y) целевой точки или любой другой тип

        Returns:
            float: Октаилово расстояние или 0, если узлы не координаты
        """
        if not self._is_coordinate(from_node) or not self._is_coordinate(to_node):
            return 0.0

        dx = abs(from_node[0] - to_node[0])
        dy = abs(from_node[1] - to_node[1])

        # Количество диагональных шагов = min(dx, dy)
        # Количество прямых шагов = |dx - dy|
        return min(dx, dy) * self.diagonal_cost + abs(dx - dy) * 1.0


class HeuristicFactory:
    """
    Фабрика для создания эвристик по имени.
    Упрощает создание эвристик из конфигурации.
    """

    _heuristics = {
        "zero": ZeroHeuristic,
        "euclidean": EuclideanHeuristic,
        "manhattan": ManhattanHeuristic,
        "chebyshev": ChebyshevHeuristic,
        "octile": OctileHeuristic,
    }

    @classmethod
    def create(cls, name: str, **kwargs) -> HeuristicFunction:
        """
        Создать эвристику по имени.

        Args:
            name: Имя эвристики ('zero', 'euclidean', 'manhattan', etc.)
            **kwargs: Дополнительные параметры для конструктора

        Returns:
            HeuristicFunction: Экземпляр эвристики

        Raises:
            ValueError: Если эвристика с таким именем не найдена
        """
        name = name.lower()
        if name not in cls._heuristics:
            raise ValueError(
                f"Неизвестная эвристика: {name}. " f"Доступны: {', '.join(cls._heuristics.keys())}"
            )

        heuristic_class = cls._heuristics[name]
        return heuristic_class(**kwargs)

    @classmethod
    def list_available(cls) -> list[str]:
        """Список доступных эвристик."""
        return list(cls._heuristics.keys())


# Для обратной совместимости и удобства импорта
__all__ = [
    "HeuristicFunction",
    "ZeroHeuristic",
    "EuclideanHeuristic",
    "ManhattanHeuristic",
    "ChebyshevHeuristic",
    "OctileHeuristic",
    "HeuristicFactory",
]
