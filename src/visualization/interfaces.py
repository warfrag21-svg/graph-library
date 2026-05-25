# src/visualization/interfaces.py
"""
Интерфейсы для визуализации графов.
Паттерн Адаптер: отделяем ядро от конкретных библиотек визуализации.
"""

from abc import ABC, abstractmethod
from typing import Any, Generic, List, Optional, Tuple, TypeVar

from src.core.interfaces import IGraph

T = TypeVar("T")


class IGraphVisualizer(ABC, Generic[T]):
    """
    Интерфейс для визуализаторов графов.

    Позволяет подменять способ визуализации без изменения ядра.
    """

    @abstractmethod
    def visualize(
        self,
        graph: IGraph[T],
        path: Optional[List[T]] = None,
        title: str = "Graph",
        show_weights: bool = True,
        figsize: Tuple[int, int] = (10, 8),
    ) -> Any:
        """
        Визуализировать граф.

        Args:
            graph: Граф для визуализации
            path: Опциональный путь для подсветки
            title: Заголовок графика
            show_weights: Показывать ли веса рёбер
            figsize: Размер фигуры (ширина, высота)

        Returns:
            Any: Объект визуализации (зависит от реализации)
        """
        pass

    @abstractmethod
    def save(self, filename: str, **kwargs) -> None:
        """
        Сохранить текущую визуализацию в файл.

        Args:
            filename: Имя файла
            **kwargs: Дополнительные параметры
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """Закрыть окно визуализации и освободить ресурсы."""
        pass

    @abstractmethod
    def show(self) -> None:
        """Показать окно визуализации."""
        pass


class NullVisualizer(IGraphVisualizer[T]):
    """
    Пустой визуализатор для тестирования.
    Ничего не делает, но реализует интерфейс.
    """

    def visualize(
        self,
        graph: IGraph[T],
        path: Optional[List[T]] = None,
        title: str = "Graph",
        show_weights: bool = True,
        figsize: Tuple[int, int] = (10, 8),
    ) -> None:
        """Ничего не делает."""
        pass

    def save(self, filename: str, **kwargs) -> None:
        """Ничего не делает."""
        pass

    def close(self) -> None:
        """Ничего не делает."""
        pass

    def show(self) -> None:
        """Ничего не делает."""
        pass
