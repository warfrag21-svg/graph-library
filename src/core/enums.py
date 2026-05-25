# src/core/enums.py
"""
Перечисления для библиотеки графов.
"""

from enum import Enum


class GraphType(Enum):
    """Тип графа: направленный или ненаправленный."""

    DIRECTED = "directed"
    UNDIRECTED = "undirected"

    def __str__(self):
        return self.value
