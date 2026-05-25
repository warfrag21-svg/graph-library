# src/visualization/matplotlib_adapter.py (полный исправленный файл)

"""
Адаптер для визуализации графов с помощью matplotlib.
"""

import math
import warnings
from typing import Any, Dict, List, Optional, Tuple

from src.core.interfaces import IGraph
from src.visualization.interfaces import IGraphVisualizer, NullVisualizer

# Импорт matplotlib с обработкой ошибок
try:
    import matplotlib.patches as mpatches
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection
    from matplotlib.patches import FancyArrowPatch

    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    plt = mpatches = LineCollection = FancyArrowPatch = None


class MatplotlibVisualizer(IGraphVisualizer):
    """Адаптер для визуализации графов через matplotlib."""

    # Цвета
    COLORS = {"default": "lightblue", "path": "red", "start": "green", "goal": "gold"}

    # Размеры
    NODE_SIZE = 500
    NODE_SIZE_PATH = 600
    EDGE_WIDTH = 1.5
    EDGE_WIDTH_PATH = 3.0
    FONT_NODE = 10
    FONT_WEIGHT = 8

    # Геометрия
    NODE_RADIUS = 0.05
    WEIGHT_OFFSET = 0.08
    LAYOUT_MARGIN = 0.3
    LAYOUT_RADIUS = 1.0

    def __init__(self, max_nodes: int = 1000):
        self.max_nodes = max_nodes
        self._fig = None
        self._ax = None
        self._pos = None

        if not MATPLOTLIB_AVAILABLE:
            warnings.warn("Matplotlib не установлен. Установите: pip install matplotlib")

    # ==================== Вспомогательные методы ====================

    def _is_available(self) -> bool:
        """Проверить доступность matplotlib."""
        if not MATPLOTLIB_AVAILABLE:
            print("Matplotlib не установлен")
        return MATPLOTLIB_AVAILABLE

    def _is_undirected(self, graph: IGraph) -> bool:
        """Проверить, является ли граф ненаправленным."""
        return (
            hasattr(graph, "type")
            and hasattr(graph.type, "name")
            and graph.type.name == "UNDIRECTED"
        )

    def _get_node_color(self, node, path: Optional[List]) -> str:
        """Определить цвет узла."""
        if not path or node not in path:
            return self.COLORS["default"]
        if node == path[0]:
            return self.COLORS["start"]
        if node == path[-1]:
            return self.COLORS["goal"]
        return self.COLORS["path"]

    # ==================== Layout ====================

    def _compute_layout(self, graph: IGraph) -> Dict:
        """Вычислить позиции узлов (по координатам или по кругу)."""
        nodes = list(graph.get_nodes())

        if not nodes:
            return {}

        # Проверяем, являются ли узлы координатами
        is_coords = all(
            isinstance(n, (tuple, list))
            and len(n) == 2
            and all(isinstance(v, (int, float)) for v in n)
            for n in nodes
        )

        if is_coords:
            return {n: (float(n[0]), float(n[1])) for n in nodes}

        # Располагаем по кругу
        n = len(nodes)
        return {
            node: (
                self.LAYOUT_RADIUS * math.cos(2 * math.pi * i / n),
                self.LAYOUT_RADIUS * math.sin(2 * math.pi * i / n),
            )
            for i, node in enumerate(nodes)
        }

    # ==================== Сбор рёбер ====================

    def _collect_all_edges(self, graph: IGraph, pos: Dict, path: Optional[List]):
        """Собрать все рёбра для отрисовки."""
        default_edges = []
        path_edges = []
        weight_positions = []

        # Строим множество рёбер пути
        path_edge_set = set()
        if path and len(path) > 1:
            for i in range(len(path) - 1):
                path_edge_set.add((path[i], path[i + 1]))
                if self._is_undirected(graph):
                    path_edge_set.add((path[i + 1], path[i]))

        processed = set()

        for node in graph.get_nodes():
            if node not in pos:
                continue

            for neighbor, weight in graph.get_neighbors(node).items():
                if neighbor not in pos:
                    continue

                edge_key = tuple(sorted([str(node), str(neighbor)]))
                if self._is_undirected(graph) and edge_key in processed:
                    continue
                processed.add(edge_key)

                edge_coords = [pos[node], pos[neighbor]]
                is_path_edge = (node, neighbor) in path_edge_set or (
                    neighbor,
                    node,
                ) in path_edge_set

                if is_path_edge:
                    path_edges.append(edge_coords)
                else:
                    default_edges.append(edge_coords)

                weight_positions.append(
                    {
                        "node1": node,
                        "node2": neighbor,
                        "weight": weight,
                        "pos1": pos[node],
                        "pos2": pos[neighbor],
                        "is_path": is_path_edge,
                    }
                )

        return default_edges, path_edges, weight_positions

    # ==================== Отрисовка ====================

    def _draw_edges(
        self, edges: List, color: str, width: float, alpha: float = 0.7, is_directed: bool = False
    ):
        """Нарисовать рёбра (с учётом направленности)."""
        if not edges:
            return

        if is_directed:
            # Для направленных графов рисуем стрелки
            for edge in edges:
                x1, y1 = edge[0]
                x2, y2 = edge[1]

                arrow = FancyArrowPatch(
                    (x1, y1),
                    (x2, y2),
                    arrowstyle="->",
                    color=color,
                    linewidth=width,
                    alpha=alpha,
                    mutation_scale=20,
                    zorder=1,
                )
                self._ax.add_patch(arrow)
        else:
            # Для ненаправленных графов рисуем обычные линии
            lc = LineCollection(edges, colors=color, linewidths=width, alpha=alpha, zorder=1)
            self._ax.add_collection(lc)

    def _draw_nodes(self, pos: Dict, path: Optional[List]):
        """Нарисовать узлы."""
        for node, (x, y) in pos.items():
            color = self._get_node_color(node, path)

            if path and node in path:
                linewidth = 2.5
            else:
                linewidth = 1.5

            circle = mpatches.Circle(
                (x, y),
                radius=self.NODE_RADIUS,
                facecolor=color,
                edgecolor="black",
                linewidth=linewidth,
                zorder=2,
            )
            self._ax.add_patch(circle)

            self._ax.text(
                x,
                y - 0.1,
                str(node),
                ha="center",
                va="center",
                fontsize=self.FONT_NODE,
                fontweight="bold",
                zorder=3,
            )

    def _draw_weights(self, weight_positions: List[Dict]):
        """Нарисовать веса рёбер."""
        for wp in weight_positions:
            x1, y1 = wp["pos1"]
            x2, y2 = wp["pos2"]

            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2

            dx = y2 - y1
            dy = -(x2 - x1)
            length = math.hypot(dx, dy)
            if length > 0:
                mx += dx / length * self.WEIGHT_OFFSET
                my += dy / length * self.WEIGHT_OFFSET

            text_color = "darkred" if wp["is_path"] else "black"

            self._ax.text(
                mx,
                my,
                f"{wp['weight']:.1f}",
                ha="center",
                va="center",
                fontsize=self.FONT_WEIGHT,
                color=text_color,
                bbox=dict(
                    boxstyle="round,pad=0.2",
                    facecolor="white",
                    edgecolor="gray" if not wp["is_path"] else "red",
                    alpha=0.85,
                    zorder=4,
                ),
            )

    # ==================== Public API ====================

    def visualize(
        self,
        graph: IGraph,
        path: Optional[List] = None,
        title: str = "Graph",
        show_weights: bool = True,
        figsize: Tuple[int, int] = (10, 8),
    ) -> Optional[Any]:
        """Визуализировать граф."""
        if not self._is_available():
            return None

        nodes_count = len(graph.get_nodes())
        if nodes_count > self.max_nodes:
            print(f"Граф слишком большой ({nodes_count} > {self.max_nodes})")

        self.close()

        pos = self._compute_layout(graph)
        if not pos:
            print("Нет узлов для отрисовки")
            return None

        default_edges, path_edges, weight_positions = self._collect_all_edges(graph, pos, path)

        self._fig, self._ax = plt.subplots(figsize=figsize)

        is_directed = not self._is_undirected(graph)

        self._draw_edges(
            default_edges, color="gray", width=self.EDGE_WIDTH, alpha=0.5, is_directed=is_directed
        )
        self._draw_edges(
            path_edges,
            color=self.COLORS["path"],
            width=self.EDGE_WIDTH_PATH,
            alpha=0.9,
            is_directed=is_directed,
        )
        self._draw_nodes(pos, path)

        if show_weights:
            self._draw_weights(weight_positions)

        self._ax.set_aspect("equal")
        self._ax.axis("off")
        self._ax.set_title(title, fontsize=14, fontweight="bold", pad=20)

        xs = [p[0] for p in pos.values()]
        ys = [p[1] for p in pos.values()]
        self._ax.set_xlim(min(xs) - self.LAYOUT_MARGIN, max(xs) + self.LAYOUT_MARGIN)
        self._ax.set_ylim(min(ys) - self.LAYOUT_MARGIN, max(ys) + self.LAYOUT_MARGIN)

        plt.tight_layout()
        return self._fig

    def save(self, filename: str, dpi: int = 300, **kwargs) -> None:
        """Сохранить визуализацию."""
        if self._fig:
            self._fig.savefig(filename, dpi=dpi, bbox_inches="tight", **kwargs)
            print(f"Сохранено в {filename}")

    def close(self) -> None:
        """Закрыть окно."""
        if self._fig:
            plt.close(self._fig)
            self._fig = self._ax = self._pos = None

    def show(self) -> None:
        """Показать окно."""
        if self._fig:
            plt.show()


def create_visualizer(backend: str = "matplotlib", **kwargs) -> IGraphVisualizer:
    """Фабрика визуализаторов."""
    if backend == "matplotlib":
        return MatplotlibVisualizer(**kwargs)
    if backend == "null":
        return NullVisualizer()
    raise ValueError(f"Неизвестный бэкенд: {backend}")
