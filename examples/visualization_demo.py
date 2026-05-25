"""
Минимальная демонстрация визуализации графов.
"""

import os
import random
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.algorithms.astar import astar_search
from src.algorithms.heuristics import ManhattanHeuristic
from src.core.builder import GraphBuilder
from src.core.enums import GraphType
from src.visualization.matplotlib_adapter import MatplotlibVisualizer


def show_and_wait(visualizer, title: str):
    """Показать визуализацию и ждать закрытия окна."""
    print(f"\n{title}")
    print("Закройте окно для продолжения...")
    visualizer.show()
    visualizer.close()


def demo_graph_creation():
    """1. Создание неориентированного графа."""
    print("\n" + "=" * 50)
    print("1. НЕОРИЕНТИРОВАННЫЙ ГРАФ")
    print("=" * 50)

    graph = (
        GraphBuilder[str](GraphType.UNDIRECTED)
        .add_nodes("A", "B", "C", "D", "E", "F")
        .add_edges(
            ("A", "B", 4),
            ("A", "C", 2),
            ("B", "C", 1),
            ("B", "D", 5),
            ("C", "D", 8),
            ("C", "E", 10),
            ("D", "E", 2),
            ("D", "F", 6),
            ("E", "F", 3),
        )
        .build()
    )

    print(f"Узлов: {graph.size}, рёбер: {graph.edge_count}, тип: {graph.type}")

    visualizer = MatplotlibVisualizer()
    visualizer.visualize(
        graph, title="Неориентированный взвешенный граф", show_weights=True, figsize=(10, 8)
    )
    show_and_wait(visualizer, "Неориентированный граф")


def demo_directed_graph():
    """2. Создание направленного графа."""
    print("\n" + "=" * 50)
    print("2. НАПРАВЛЕННЫЙ ГРАФ")
    print("=" * 50)

    graph = (
        GraphBuilder[str](GraphType.DIRECTED)
        .add_nodes("A", "B", "C", "D", "E")
        .add_edges(
            ("A", "B", 3),
            ("A", "C", 5),
            ("B", "C", 2),
            ("B", "D", 4),
            ("C", "E", 6),
            ("D", "E", 1),
            ("E", "A", 7),
        )
        .build()
    )

    print(f"Узлов: {graph.size}, рёбер: {graph.edge_count}, тип: {graph.type}")
    print("Стрелки показывают направление рёбер")

    visualizer = MatplotlibVisualizer()
    visualizer.visualize(
        graph, title="Направленный взвешенный граф", show_weights=True, figsize=(10, 8)
    )
    show_and_wait(visualizer, "Направленный граф")


def demo_astar_manhattan():
    """3. A* с манхэттенской эвристикой на сетке."""
    print("\n" + "=" * 50)
    print("3. A* НА СЕТКЕ")
    print("=" * 50)

    random.seed(42)

    builder = GraphBuilder[tuple](GraphType.UNDIRECTED)

    for x in range(10):
        for y in range(10):
            builder.add_node((x, y))

    for x in range(10):
        for y in range(10):
            if x + 1 < 10:
                builder.add_edge((x, y), (x + 1, y), random.randint(1, 5))
            if y + 1 < 10:
                builder.add_edge((x, y), (x, y + 1), random.randint(1, 5))

    grid = builder.build()
    start, goal = (0, 0), (9, 9)

    result = astar_search(grid, start, goal, ManhattanHeuristic())

    print(f"Старт: {start}, цель: {goal}")
    print(f"Путь: {len(result.path)} узлов, расстояние: {result.distance:.0f}")
    print(f"Исследовано: {result.nodes_explored} узлов, время: {result.execution_time_ms:.2f} ms")

    visualizer = MatplotlibVisualizer()
    visualizer.visualize(
        grid,
        path=result.path,
        title=f"A* на сетке (расстояние: {result.distance:.0f})",
        show_weights=True,
        figsize=(10, 10),
    )
    show_and_wait(visualizer, "A* на взвешенной сетке")


def main():
    """Запуск демонстрации."""
    print("\n" + "=" * 50)
    print("ДЕМОНСТРАЦИЯ БИБЛИОТЕКИ ГРАФОВ")
    print("=" * 50)

    demo_graph_creation()
    demo_directed_graph()
    demo_astar_manhattan()

    print("\n" + "=" * 50)
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("=" * 50)


if __name__ == "__main__":
    main()
