# src/core/interfaces.py
"""
Интерфейсы для библиотеки графов.
Абстрактные классы, определяющие контракты взаимодействия.
"""

from abc import ABC, abstractmethod
from typing import Dict, Generic, Set, TypeVar

T = TypeVar("T")


class IGraph(ABC, Generic[T]):
    """
    Интерфейс графа.
    Определяет базовые операции для работы с графом.
    """

    @abstractmethod
    def add_node(self, node: T) -> None:
        """
        Добавить узел в граф.

        Args:
            node: Добавляемый узел

        Если узел уже существует, операция игнорируется.
        """
        pass

    @abstractmethod
    def add_edge(self, from_node: T, to_node: T, weight: float = 1.0) -> None:
        """
        Добавить ребро в граф.

        Args:
            from_node: Начальный узел
            to_node: Конечный узел
            weight: Вес ребра (должен быть >= 0)

        Raises:
            NegativeEdgeWeightException: если weight < 0

        Если узлы не существуют, они автоматически добавляются.
        """
        pass

    @abstractmethod
    def get_nodes(self) -> Set[T]:
        """
        Получить все узлы графа.

        Returns:
            Множество всех узлов
        """
        pass

    @abstractmethod
    def get_neighbors(self, node: T) -> Dict[T, float]:
        """
        Получить соседей узла с весами рёбер.

        Args:
            node: Исходный узел

        Returns:
            Словарь {сосед: вес}

        Raises:
            NodeNotFoundException: если узел не существует
        """
        pass

    @abstractmethod
    def has_node(self, node: T) -> bool:
        """
        Проверить существование узла.

        Args:
            node: Проверяемый узел

        Returns:
            True если узел существует
        """
        pass

    @abstractmethod
    def has_edge(self, from_node: T, to_node: T) -> bool:
        """
        Проверить существование ребра.

        Args:
            from_node: Начальный узел
            to_node: Конечный узел

        Returns:
            True если ребро существует
        """
        pass

    @abstractmethod
    def get_edge_weight(self, from_node: T, to_node: T) -> float:
        """
        Получить вес ребра.

        Args:
            from_node: Начальный узел
            to_node: Конечный узел

        Returns:
            Вес ребра

        Raises:
            EdgeNotFoundException: если ребро не существует
        """
        pass

    @abstractmethod
    def remove_node(self, node: T) -> None:
        """
        Удалить узел из графа.

        Args:
            node: Удаляемый узел

        Удаляет узел и все связанные с ним рёбра.
        Если узел не существует, операция игнорируется.
        """
        pass

    @abstractmethod
    def remove_edge(self, from_node: T, to_node: T) -> None:
        """
        Удалить ребро из графа.

        Args:
            from_node: Начальный узел
            to_node: Конечный узел

        Если ребро не существует, операция игнорируется.
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Строковое представление графа."""
        pass
