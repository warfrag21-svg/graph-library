# src/core/models.py
"""
Модели данных для библиотеки графов.
"""

from dataclasses import dataclass
from typing import Generic, List, TypeVar

T = TypeVar("T")


@dataclass
class PathResult(Generic[T]):
    """
    Результат поиска пути.

    Attributes:
        path: Список узлов в порядке обхода
        distance: Суммарный вес пути
        nodes_explored: Количество исследованных узлов
        execution_time_ms: Время выполнения в миллисекундах
    """

    path: List[T]
    distance: float
    nodes_explored: int
    execution_time_ms: float

    def __str__(self) -> str:
        """Краткое строковое представление."""
        path_str = " -> ".join(str(node) for node in self.path[:5])
        if len(self.path) > 5:
            path_str += f" ... ({len(self.path)} nodes)"

        return (
            f"Path: {path_str} | "
            f"Distance: {self.distance:.2f} | "
            f"Explored: {self.nodes_explored} | "
            f"Time: {self.execution_time_ms:.2f}ms"
        )

    def is_valid(self) -> bool:
        """Проверка валидности пути (не пустой и расстояние конечно)."""
        return bool(self.path) and self.distance != float("inf")
