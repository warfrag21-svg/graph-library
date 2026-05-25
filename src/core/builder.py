# src/core/builder.py
"""
Реализация паттерна Builder для создания графов.
Позволяет создавать сложные графы с помощью цепочек вызовов.
"""

import random
from typing import Dict, Generic, List, Optional, Tuple, TypeVar

from src.core.enums import GraphType
from src.core.graph import AdjacencyListGraph
from src.core.interfaces import IGraph

T = TypeVar("T")


class GraphBuilder(Generic[T]):
    """
    Строитель для создания графов с fluent-интерфейсом.

    Позволяет создавать графы путём последовательного добавления
    узлов и рёбер с возможностью цепочки вызовов.

    Пример:
        graph = (GraphBuilder[str]()
                .add_node("A")
                .add_node("B")
                .add_edge("A", "B", 5.0)
                .build())
    """

    def __init__(self, graph_type: GraphType = GraphType.DIRECTED):
        """
        Инициализация строителя.

        Args:
            graph_type: Тип создаваемого графа
        """
        self._graph = AdjacencyListGraph[T](graph_type)
        self._graph_type = graph_type

    def add_node(self, node: T) -> "GraphBuilder[T]":
        """
        Добавить узел в граф.

        Args:
            node: Добавляемый узел

        Returns:
            GraphBuilder: сам строитель (для цепочек)
        """
        self._graph.add_node(node)
        return self

    def add_nodes(self, *nodes: T) -> "GraphBuilder[T]":
        """
        Добавить несколько узлов.

        Args:
            *nodes: Узлы для добавления

        Returns:
            GraphBuilder: сам строитель
        """
        for node in nodes:
            self._graph.add_node(node)
        return self

    def add_edge(self, from_node: T, to_node: T, weight: float = 1.0) -> "GraphBuilder[T]":
        """
        Добавить ребро в граф.

        Args:
            from_node: Начальный узел
            to_node: Конечный узел
            weight: Вес ребра

        Returns:
            GraphBuilder: сам строитель
        """
        self._graph.add_edge(from_node, to_node, weight)
        return self

    def add_edges(self, *edges) -> "GraphBuilder[T]":
        """
        Добавить несколько рёбер.

        Args:
            *edges: Кортежи (from, to) или (from, to, weight)

        Returns:
            GraphBuilder: сам строитель
        """
        for edge in edges:
            match len(edge):
                case 2:
                    self._graph.add_edge(edge[0], edge[1])
                case 3:
                    self._graph.add_edge(edge[0], edge[1], edge[2])
                case _:
                    raise ValueError(f"Некорректный формат: {edge}")
        return self

    def remove_node(self, node: T) -> "GraphBuilder[T]":
        """
        Удалить узел из графа.

        Args:
            node: Удаляемый узел

        Returns:
            GraphBuilder: сам строитель
        """
        self._graph.remove_node(node)
        return self

    def remove_edge(self, from_node: T, to_node: T) -> "GraphBuilder[T]":
        """
        Удалить ребро из графа.

        Args:
            from_node: Начальный узел
            to_node: Конечный узел

        Returns:
            GraphBuilder: сам строитель
        """
        self._graph.remove_edge(from_node, to_node)
        return self

    def build(self) -> AdjacencyListGraph[T]:
        """
        Построить граф.

        Returns:
            AdjacencyListGraph[T]: Готовый граф
        """
        return self._graph

    def build_interface(self) -> IGraph[T]:
        """
        Построить граф и вернуть как интерфейс.

        Returns:
            IGraph[T]: Готовый граф в виде интерфейса
        """
        return self._graph

    def reset(self) -> "GraphBuilder[T]":
        """
        Сбросить строитель (очистить граф).

        Returns:
            GraphBuilder: сам строитель
        """
        self._graph = AdjacencyListGraph[T](self._graph_type)
        return self

    def copy(self) -> "GraphBuilder[T]":
        """
        Создать копию строителя.

        Returns:
            GraphBuilder: Новый строитель с копией графа
        """
        new_builder = GraphBuilder[T](self._graph_type)
        # Копируем узлы и рёбра
        for node in self._graph.get_nodes():
            new_builder.add_node(node)
        for node in self._graph.get_nodes():
            for neighbor, weight in self._graph.get_neighbors(node).items():
                new_builder.add_edge(node, neighbor, weight)
        return new_builder


class GraphFactory:
    """
    Фабрика для создания типовых графов.
    Содержит статические методы для генерации различных структур.
    """

    @staticmethod
    def create_grid(
        width: int,
        height: int,
        graph_type: GraphType = GraphType.UNDIRECTED,
        weight: float = 1.0,
        diagonal: bool = False,
    ) -> IGraph[Tuple[int, int]]:
        """
        Создать граф-сетку.

        Args:
            width: Ширина сетки
            height: Высота сетки
            graph_type: Тип графа
            weight: Вес рёбер
            diagonal: Добавлять ли диагональные связи

        Returns:
            IGraph[Tuple[int, int]]: Граф-сетка
        """
        builder = GraphBuilder[Tuple[int, int]](graph_type)

        # Добавляем узлы
        for x in range(width):
            for y in range(height):
                builder.add_node((x, y))

        # Добавляем рёбра
        for x in range(width):
            for y in range(height):
                # Вправо
                if x + 1 < width:
                    builder.add_edge((x, y), (x + 1, y), weight)
                # Вниз
                if y + 1 < height:
                    builder.add_edge((x, y), (x, y + 1), weight)
                # Диагонали
                if diagonal:
                    if x + 1 < width and y + 1 < height:
                        builder.add_edge((x, y), (x + 1, y + 1), weight * 1.5)
                    if x + 1 < width and y - 1 >= 0:
                        builder.add_edge((x, y), (x + 1, y - 1), weight * 1.5)

        return builder.build_interface()

    @staticmethod
    def create_random(
        num_nodes: int,
        edge_probability: float = 0.3,
        graph_type: GraphType = GraphType.DIRECTED,
        min_weight: float = 1.0,
        max_weight: float = 10.0,
        seed: Optional[int] = None,
    ) -> IGraph[int]:
        """
        Создать случайный граф.

        Args:
            num_nodes: Количество узлов
            edge_probability: Вероятность наличия ребра
            graph_type: Тип графа
            min_weight: Минимальный вес ребра
            max_weight: Максимальный вес ребра
            seed: Зерно для генератора (для воспроизводимости)

        Returns:
            IGraph[int]: Случайный граф
        """
        if seed is not None:
            random.seed(seed)

        builder = GraphBuilder[int](graph_type)

        # Добавляем узлы
        builder.add_nodes(*range(num_nodes))

        # Добавляем случайные рёбра
        for i in range(num_nodes):
            # Диапазон соседей зависит от типа графа
            start = i + 1 if graph_type == GraphType.UNDIRECTED else 0

            for j in range(start, num_nodes):
                if i != j and random.random() < edge_probability:
                    weight = random.uniform(min_weight, max_weight)
                    builder.add_edge(i, j, weight)

        return builder.build_interface()

    @staticmethod
    def create_complete(
        nodes: List[T], weight: float = 1.0, graph_type: GraphType = GraphType.UNDIRECTED
    ) -> IGraph[T]:
        """
        Создать полный граф (каждый с каждым).

        Args:
            nodes: Список узлов
            weight: Вес всех рёбер
            graph_type: Тип графа

        Returns:
            IGraph[T]: Полный граф
        """
        builder = GraphBuilder[T](graph_type)
        builder.add_nodes(*nodes)

        for i, node1 in enumerate(nodes):
            for node2 in nodes[i + 1 :]:
                builder.add_edge(node1, node2, weight)

        return builder.build_interface()

    @staticmethod
    def create_path(
        nodes: List[T], weight: float = 1.0, graph_type: GraphType = GraphType.UNDIRECTED
    ) -> IGraph[T]:
        """
        Создать путь (линейный граф).

        Args:
            nodes: Список узлов в порядке пути
            weight: Вес рёбер
            graph_type: Тип графа

        Returns:
            IGraph[T]: Граф-путь
        """
        builder = GraphBuilder[T](graph_type)
        builder.add_nodes(*nodes)

        for i in range(len(nodes) - 1):
            builder.add_edge(nodes[i], nodes[i + 1], weight)

        return builder.build_interface()

    @staticmethod
    def create_cycle(
        nodes: List[T], weight: float = 1.0, graph_type: GraphType = GraphType.UNDIRECTED
    ) -> IGraph[T]:
        """
        Создать цикл (кольцо).

        Args:
            nodes: Список узлов
            weight: Вес рёбер
            graph_type: Тип графа

        Returns:
            IGraph[T]: Граф-цикл
        """
        builder = GraphBuilder[T](graph_type)
        builder.add_nodes(*nodes)

        for i in range(len(nodes)):
            builder.add_edge(nodes[i], nodes[(i + 1) % len(nodes)], weight)

        return builder.build_interface()

    @staticmethod
    def create_tree(
        levels: int,
        branching_factor: int,
        node_prefix: str = "Node",
        weight: float = 1.0,
        graph_type: GraphType = GraphType.UNDIRECTED,
    ) -> IGraph[str]:
        """
        Создать дерево.

        Args:
            levels: Количество уровней
            branching_factor: Коэффициент ветвления
            node_prefix: Префикс для имён узлов
            weight: Вес рёбер
            graph_type: Тип графа

        Returns:
            IGraph[str]: Дерево
        """
        builder = GraphBuilder[str](graph_type)

        def add_level(parent: str, current_level: int, counter: List[int]) -> None:
            if current_level >= levels:
                return

            for i in range(branching_factor):
                counter[0] += 1
                child = f"{node_prefix}_{counter[0]}"
                builder.add_node(child)
                builder.add_edge(parent, child, weight)
                add_level(child, current_level + 1, counter)

        # Корень
        root = f"{node_prefix}_0"
        builder.add_node(root)
        add_level(root, 1, [0])

        return builder.build_interface()

    @staticmethod
    def create_bipartite(
        set_a: List[T],
        set_b: List[T],
        density: float = 1.0,
        weight: float = 1.0,
        graph_type: GraphType = GraphType.UNDIRECTED,
        seed: Optional[int] = None,
    ) -> IGraph[T]:
        """
        Создать двудольный граф.

        Args:
            set_a: Первая доля
            set_b: Вторая доля
            density: Плотность связей (0.0-1.0)
            weight: Вес рёбер
            graph_type: Тип графа
            seed: Зерно для генератора

        Returns:
            IGraph[T]: Двудольный граф
        """
        if seed is not None:
            random.seed(seed)

        builder = GraphBuilder[T](graph_type)
        builder.add_nodes(*set_a)
        builder.add_nodes(*set_b)

        for a in set_a:
            for b in set_b:
                if random.random() < density:
                    builder.add_edge(a, b, weight)

        return builder.build_interface()

    @staticmethod
    def from_adjacency_list(
        adj_list: Dict[T, List[Tuple[T, float]]], graph_type: GraphType = GraphType.DIRECTED
    ) -> IGraph[T]:
        """
        Создать граф из списка смежности.

        Args:
            adj_list: Словарь {узел: [(сосед, вес), ...]}
            graph_type: Тип графа

        Returns:
            IGraph[T]: Построенный граф
        """
        builder = GraphBuilder[T](graph_type)

        # Добавляем все узлы
        for node in adj_list:
            builder.add_node(node)

        # Добавляем рёбра
        for from_node, neighbors in adj_list.items():
            for to_node, weight in neighbors:
                builder.add_edge(from_node, to_node, weight)

        return builder.build_interface()


# Удобные функции для быстрого создания графов
def grid_graph(
    width: int, height: int, directed: bool = False, diagonal: bool = False
) -> IGraph[Tuple[int, int]]:
    """Быстрое создание сетки."""
    return GraphFactory.create_grid(
        width, height, GraphType.DIRECTED if directed else GraphType.UNDIRECTED, diagonal=diagonal
    )


def random_graph(
    n: int, p: float = 0.3, directed: bool = False, seed: Optional[int] = None
) -> IGraph[int]:
    """Быстрое создание случайного графа."""
    return GraphFactory.create_random(
        n, p, GraphType.DIRECTED if directed else GraphType.UNDIRECTED, seed=seed
    )


def complete_graph(nodes: List[T]) -> IGraph[T]:
    """Быстрое создание полного графа."""
    return GraphFactory.create_complete(nodes)


def path_graph(nodes: List[T]) -> IGraph[T]:
    """Быстрое создание пути."""
    return GraphFactory.create_path(nodes)
