"""
Демонстрация алгоритмов поиска путей.
"""

from src.algorithms.pathfinder import (
    bfs_path,
    bfs_traverse,
    dfs_traverse,
    find_all_paths,
    has_cycle,
)
from src.core.enums import GraphType
from src.core.graph import AdjacencyListGraph


def demo_maze_pathfinding():
    """Поиск пути в лабиринте 4x4."""
    print("\n" + "=" * 50)
    print("ПОИСК В ЛАБИРИНТЕ")
    print("=" * 50)

    maze = AdjacencyListGraph(GraphType.UNDIRECTED)

    for x in range(4):
        for y in range(4):
            if x > 0:
                maze.add_edge((x, y), (x - 1, y))
            if y > 0:
                maze.add_edge((x, y), (x, y - 1))

    maze.remove_edge((1, 1), (2, 1))
    maze.remove_edge((1, 2), (1, 3))
    maze.remove_edge((2, 2), (3, 2))

    start, goal = (0, 0), (3, 3)
    path = bfs_path(maze, start, goal)

    print(f"Старт: {start}, Цель: {goal}")

    if path:
        print(f"Путь найден (шагов: {len(path)-1})")
        print(f"Маршрут: {' -> '.join(str(p) for p in path)}")
    else:
        print("Путь не найден")


def demo_social_network():
    """Поиск в социальной сети."""
    print("\n" + "=" * 50)
    print("СОЦИАЛЬНАЯ СЕТЬ")
    print("=" * 50)

    social = AdjacencyListGraph(GraphType.UNDIRECTED)

    friendships = [
        ("Анна", "Борис"),
        ("Анна", "Виктор"),
        ("Борис", "Глеб"),
        ("Виктор", "Дарья"),
        ("Глеб", "Елена"),
        ("Дарья", "Елена"),
        ("Елена", "Женя"),
        ("Женя", "Зоя"),
        ("Анна", "Игорь"),
        ("Игорь", "Кира"),
    ]

    for f1, f2 in friendships:
        social.add_edge(f1, f2)

    print(f"Пользователей: {social.size}, связей: {social.edge_count}")

    start, goal = "Анна", "Зоя"
    path = bfs_path(social, start, goal)

    if path:
        print(f"Цепочка {start} -> {goal}: {' -> '.join(path)}")

    bfs_order = bfs_traverse(social, start)
    dfs_order = dfs_traverse(social, start)

    print(f"BFS обход: {' -> '.join(bfs_order)}")
    print(f"DFS обход: {' -> '.join(dfs_order)}")


def demo_all_paths():
    """Поиск всех путей между вершинами."""
    print("\n" + "=" * 50)
    print("ВСЕ ПУТИ")
    print("=" * 50)

    graph = AdjacencyListGraph(GraphType.UNDIRECTED)
    edges = [
        ("A", "B"),
        ("A", "C"),
        ("B", "C"),
        ("B", "D"),
        ("C", "D"),
        ("C", "E"),
        ("D", "E"),
        ("D", "F"),
        ("E", "F"),
    ]

    for f, t in edges:
        graph.add_edge(f, t)

    start, goal = "A", "F"

    for depth in [3, 4, 5]:
        paths = find_all_paths(graph, start, goal, max_depth=depth)
        print(f"Глубина {depth}: {len(paths)} путей")

    print(f"Граф содержит циклы: {has_cycle(graph)}")


def main():
    """Запуск всех демонстраций."""
    demo_maze_pathfinding()
    demo_social_network()
    demo_all_paths()


if __name__ == "__main__":
    main()
