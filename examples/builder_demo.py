"""
Демонстрация использования строителя графов.
"""

from src.algorithms.astar import astar_search
from src.algorithms.heuristics import ManhattanHeuristic
from src.algorithms.pathfinder import bfs_path, dfs_traverse
from src.core.builder import GraphBuilder, GraphFactory
from src.core.enums import GraphType


def demo_builder_pattern():
    """Демонстрация паттерна Builder."""
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ ПАТТЕРНА BUILDER")
    print("=" * 60)

    print("\nПростой граф:")
    graph = (
        GraphBuilder[str]()
        .add_node("Москва")
        .add_node("Питер")
        .add_node("Новгород")
        .add_edge("Москва", "Питер", 650)
        .add_edge("Москва", "Новгород", 500)
        .add_edge("Питер", "Новгород", 200)
        .build()
    )
    print(graph)

    print("\nГраф с множеством рёбер:")
    graph2 = (
        GraphBuilder[str](GraphType.UNDIRECTED)
        .add_nodes("A", "B", "C", "D", "E")
        .add_edges(("A", "B", 5), ("A", "C", 3), ("B", "D", 2), ("C", "D", 4), ("D", "E", 1))
        .build()
    )
    print(graph2)
    print(f"Узлов: {graph2.size}, Рёбер: {graph2.edge_count}")

    print("\nКопирование строителя:")
    builder = GraphBuilder[int]().add_nodes(1, 2, 3).add_edge(1, 2)
    builder_copy = builder.copy()
    builder_copy.add_node(4).add_edge(2, 3)
    print(f"Оригинал: {sorted(builder.build().get_nodes())}")
    print(f"Копия:    {sorted(builder_copy.build().get_nodes())}")

    print("\nСброс строителя:")
    builder = GraphBuilder[str]().add_nodes("X", "Y", "Z")
    print(f"До сброса: {builder.build().size} узлов")
    builder.reset()
    print(f"После сброса: {builder.build().size} узлов")

    print("\n" + "=" * 60)


def demo_factory_methods():
    """Демонстрация фабричных методов."""
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ ФАБРИЧНЫХ МЕТОДОВ")
    print("=" * 60)

    print("\nСетка 3x3:")
    grid = GraphFactory.create_grid(3, 3)
    print(f"Узлов: {grid.size}, Рёбер: {grid.edge_count}")

    print("\nСетка 2x2 с диагоналями:")
    grid_diag = GraphFactory.create_grid(2, 2, diagonal=True)
    print(f"Узлов: {grid_diag.size}, Рёбер: {grid_diag.edge_count}")

    print("\nСлучайный граф (10 узлов, p=0.3):")
    random_g = GraphFactory.create_random(10, 0.3, seed=42)
    print(f"Узлов: {random_g.size}, Рёбер: {random_g.edge_count}")

    print("\nПолный граф K5:")
    complete = GraphFactory.create_complete([1, 2, 3, 4, 5])
    print(f"Узлов: {complete.size}, Рёбер: {complete.edge_count}")

    print("\nПуть из 5 узлов:")
    path = GraphFactory.create_path(["A", "B", "C", "D", "E"])
    print(f"Рёбер: {path.edge_count}")

    print("\nЦикл из 4 узлов:")
    cycle = GraphFactory.create_cycle([1, 2, 3, 4])
    print(f"Рёбер: {cycle.edge_count}")

    print("\nДерево (3 уровня, ветвление 2):")
    tree = GraphFactory.create_tree(3, 2, "N")
    print(f"Узлов: {tree.size}, Рёбер: {tree.edge_count}")

    print("\nДвудольный граф K3,2:")
    bipartite = GraphFactory.create_bipartite(["A1", "A2", "A3"], ["B1", "B2"], density=1.0)
    print(f"Узлов: {bipartite.size}, Рёбер: {bipartite.edge_count}")

    print("\n" + "=" * 60)


def demo_practical_usage():
    """Практическое применение: поиск пути на сгенерированных графах."""
    print("=" * 60)
    print("ПРАКТИЧЕСКОЕ ПРИМЕНЕНИЕ")
    print("=" * 60)

    print("\nПоиск пути в городской сетке 5x5:")
    city = GraphFactory.create_grid(5, 5, diagonal=False)
    start, goal = (0, 0), (4, 4)
    result = astar_search(city, start, goal, ManhattanHeuristic())
    print(f"Маршрут: {start} -> {goal}")
    print(f"Длина пути: {len(result.path)-1} шагов")
    print(f"Расстояние: {result.distance:.1f}")
    print(f"Исследовано узлов: {result.nodes_explored}")

    print("\nПоиск пути в случайном графе:")
    random_g = GraphFactory.create_random(20, 0.1, seed=123)
    path = bfs_path(random_g, 0, 19)
    if path:
        print(f"Путь 0 -> 19: {' -> '.join(map(str, path[:5]))} ...")
    else:
        print("Путь не найден")

    print("\nДерево решений (обход в глубину):")
    tree = GraphFactory.create_tree(4, 2, "Decision")
    traversal = dfs_traverse(tree, "Decision_0")
    print(f"DFS обход: {' -> '.join(traversal[:8])} ...")

    print("\n" + "=" * 60)


def demo_fluent_interface():
    """Демонстрация выразительности fluent-интерфейса."""
    print("=" * 60)
    print("ВЫРАЗИТЕЛЬНОСТЬ FLUENT-ИНТЕРФЕЙСА")
    print("=" * 60)

    print("\nТранспортная сеть:")
    transport = (
        GraphBuilder[str](GraphType.UNDIRECTED)
        .add_nodes("Москва", "Питер", "НН", "Казань", "Екб")
        .add_edges(
            ("Москва", "Питер", 650),
            ("Москва", "НН", 400),
            ("Москва", "Казань", 800),
            ("Питер", "НН", 900),
            ("НН", "Казань", 350),
            ("Казань", "Екб", 900),
            ("НН", "Екб", 1200),
        )
        .build()
    )
    print(f"Городов: {transport.size}, Маршрутов: {transport.edge_count}")

    print("\nСоциальная сеть:")
    social = (
        GraphBuilder[str](GraphType.UNDIRECTED)
        .add_nodes("Анна", "Борис", "Виктор", "Глеб", "Дарья")
        .add_edges(
            ("Анна", "Борис"),
            ("Анна", "Виктор"),
            ("Борис", "Глеб"),
            ("Виктор", "Дарья"),
            ("Глеб", "Дарья"),
        )
        .build()
    )
    anna_friends = list(social.get_neighbors("Анна").keys())
    print(f"Друзья Анны: {', '.join(anna_friends)}")

    print("\nЛабиринт 4x4 со стенами:")
    maze = GraphFactory.create_grid(4, 4)
    maze.remove_edge((1, 1), (2, 1))
    maze.remove_edge((1, 2), (1, 3))
    print(f"Клеток: {maze.size}, Проходов: {maze.edge_count}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    demo_builder_pattern()
    demo_factory_methods()
    demo_practical_usage()
    demo_fluent_interface()
