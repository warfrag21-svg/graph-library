"""
Демонстрационный скрипт для проверки работы библиотеки графов.
Создаёт граф из 10+ узлов и сравнивает работу всех эвристик A*.
"""

from src.algorithms.astar import astar_search, dijkstra_search
from src.algorithms.heuristics import (
    ChebyshevHeuristic,
    EuclideanHeuristic,
    ManhattanHeuristic,
    OctileHeuristic,
    ZeroHeuristic,
)
from src.core.enums import GraphType
from src.core.graph import AdjacencyListGraph


def create_test_graph():
    """
    Создаёт граф для демонстрации.

    Структура графа:
    A(0,0) -5- B(1,0) -3- C(2,0)
    |         |         |
    4         1         6
    |         |         |
    D(0,1) -2- E(1,1) -4- F(2,1)
    |         |         |
    3         7         2
    |         |         |
    G(0,2) -5- H(1,2) -1- I(2,2)
              |
              8
              |
              J(1,3)
    """
    graph = AdjacencyListGraph(GraphType.UNDIRECTED)

    nodes = {
        "A": (0, 0),
        "B": (1, 0),
        "C": (2, 0),
        "D": (0, 1),
        "E": (1, 1),
        "F": (2, 1),
        "G": (0, 2),
        "H": (1, 2),
        "I": (2, 2),
        "J": (1, 3),
    }

    for node in nodes:
        graph.add_node(node)

    edges = [
        ("A", "B", 5),
        ("B", "C", 3),
        ("A", "D", 4),
        ("B", "E", 1),
        ("C", "F", 6),
        ("D", "E", 2),
        ("E", "F", 4),
        ("D", "G", 3),
        ("E", "H", 7),
        ("F", "I", 2),
        ("G", "H", 5),
        ("H", "I", 1),
        ("H", "J", 8),
    ]

    for from_node, to_node, weight in edges:
        graph.add_edge(from_node, to_node, weight)

    return graph, nodes


def compare_algorithms(graph, nodes, start: str, goal: str):
    """Сравнивает Дейкстру и все эвристики A* на одном маршруте."""
    heuristics = [
        ("Дейкстра", ZeroHeuristic()),
        ("Манхэттен", ManhattanHeuristic()),
        ("Евклид", EuclideanHeuristic()),
        ("Чебышёв", ChebyshevHeuristic()),
        ("Октаил", OctileHeuristic()),
    ]

    print(f"\n{start} -> {goal}")
    print("-" * 60)
    print(f"{'Алгоритм':<12} {'Путь':<35} {'Расстояние':<10} {'Узлов':<6} {'Время(ms)':<10}")
    print("-" * 60)

    results = []
    for name, heuristic in heuristics:
        if name == "Дейкстра":
            result = dijkstra_search(graph, start, goal)
        else:
            result = astar_search(graph, start, goal, heuristic)

        path_str = "->".join(result.path)
        if len(path_str) > 32:
            path_str = path_str[:29] + "..."

        print(
            f"{name:<12} {path_str:<35} {result.distance:<10.1f} {result.nodes_explored:<6} {result.execution_time_ms:<10.3f}"
        )
        results.append((name, result))

    print("-" * 60)

    optimal = min(results, key=lambda x: x[1].distance)
    print(f"Оптимальный путь: {optimal[0]} (расстояние: {optimal[1].distance:.1f})")

    if optimal[0] != "Дейкстра":
        dijkstra = next(r for r in results if r[0] == "Дейкстра")
        print(
            f"Сравнение с Дейкстрой: {optimal[0]} исследовал на {dijkstra[1].nodes_explored - optimal[1].nodes_explored} узлов меньше"
        )


def main():
    """Основная демонстрационная функция."""
    print("=" * 70)
    print("СРАВНЕНИЕ АЛГОРИТМОВ ПОИСКА ПУТИ")
    print("=" * 70)

    graph, nodes = create_test_graph()

    print(f"\nГраф: {graph.size} узлов, {graph.edge_count} рёбер")

    compare_algorithms(graph, nodes, "A", "I")
    compare_algorithms(graph, nodes, "A", "J")
    compare_algorithms(graph, nodes, "C", "G")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
