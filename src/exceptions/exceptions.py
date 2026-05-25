# src/exceptions/exceptions.py
"""
Пользовательские исключения для библиотеки графов.
"""


class GraphException(Exception):
    """Базовое исключение для всех ошибок графа."""

    pass


class NodeNotFoundException(GraphException):
    """Узел не найден в графе."""

    pass


class EdgeNotFoundException(GraphException):
    """Ребро не найдено в графе."""

    pass


class NegativeEdgeWeightException(GraphException):
    """Попытка добавить ребро с отрицательным весом."""

    pass


class CycleDetectedException(GraphException):
    """В графе обнаружен цикл при топологической сортировке."""

    pass


class UnsupportedGraphTypeException(GraphException):
    """Операция не поддерживается для данного типа графа."""

    pass
