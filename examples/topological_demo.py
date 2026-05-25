"""
Демонстрация топологической сортировки.
"""

from src.algorithms.topological import is_dag, topological_sort
from src.core.enums import GraphType
from src.core.graph import AdjacencyListGraph


def demo_course_prerequisites():
    """Планирование курсов с пререквизитами."""
    print("\n" + "=" * 50)
    print("ПЛАНИРОВАНИЕ КУРСОВ")
    print("=" * 50)

    courses = AdjacencyListGraph(GraphType.DIRECTED)

    courses.add_edge("MATH101", "MATH102")
    courses.add_edge("MATH101", "PHYS101")
    courses.add_edge("MATH101", "CS101")
    courses.add_edge("CS101", "CS201")
    courses.add_edge("MATH102", "CS201")
    courses.add_edge("CS201", "CS301")
    courses.add_edge("PHYS101", "CS301")
    courses.add_edge("PHYS101", "PHYS201")

    print(f"Курсов: {courses.size}, зависимостей: {courses.edge_count}")

    if is_dag(courses):
        order = topological_sort(courses)
        print(f"Порядок: {' -> '.join(order)}")
    else:
        print("Граф содержит циклы")


def demo_project_tasks():
    """Планирование задач проекта."""
    print("\n" + "=" * 50)
    print("ПЛАНИРОВАНИЕ ЗАДАЧ")
    print("=" * 50)

    tasks = AdjacencyListGraph(GraphType.DIRECTED)

    tasks.add_edge("A", "B")
    tasks.add_edge("A", "C")
    tasks.add_edge("B", "D")
    tasks.add_edge("C", "E")
    tasks.add_edge("D", "F")
    tasks.add_edge("E", "F")
    tasks.add_edge("F", "G")
    tasks.add_edge("D", "H")
    tasks.add_edge("E", "H")

    print(f"Задач: {tasks.size}, зависимостей: {tasks.edge_count}")

    order = topological_sort(tasks)
    print(f"Порядок: {' -> '.join(order)}")
    print(f"Минимальное время (при 1 дне на задачу): {len(order)} дней")


def demo_cycle_detection():
    """Обнаружение циклов."""
    print("\n" + "=" * 50)
    print("ОБНАРУЖЕНИЕ ЦИКЛОВ")
    print("=" * 50)

    cyclic = AdjacencyListGraph(GraphType.DIRECTED)
    cyclic.add_edge("Config", "Build")
    cyclic.add_edge("Build", "Test")
    cyclic.add_edge("Test", "Deploy")
    cyclic.add_edge("Deploy", "Config")
    cyclic.add_edge("Deploy", "Monitor")

    print(f"Узлов: {cyclic.size}, рёбер: {cyclic.edge_count}")

    if is_dag(cyclic):
        print("Граф ациклический")
        order = topological_sort(cyclic)
        print(f"Порядок: {' -> '.join(order)}")
    else:
        print("Граф содержит циклы")

        from src.algorithms.topological import find_cycles

        cycles = find_cycles(cyclic)
        for cycle in cycles:
            print(f"Цикл: {' -> '.join(cycle)}")


def main():
    """Запуск всех демонстраций."""
    demo_course_prerequisites()
    demo_project_tasks()
    demo_cycle_detection()


if __name__ == "__main__":
    main()
