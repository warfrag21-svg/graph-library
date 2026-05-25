"""
Тесты для эвристических функций.
"""

import math

import pytest

from src.algorithms.heuristics import (
    ChebyshevHeuristic,
    EuclideanHeuristic,
    HeuristicFactory,
    HeuristicFunction,
    ManhattanHeuristic,
    OctileHeuristic,
    ZeroHeuristic,
)


class TestHeuristicInterface:
    """Тестирование базового интерфейса."""

    def test_heuristic_is_abstract(self):
        with pytest.raises(TypeError):
            HeuristicFunction()  # type: ignore

    def test_str_representation(self):
        assert str(ZeroHeuristic()) == "ZeroHeuristic"
        assert str(EuclideanHeuristic()) == "EuclideanHeuristic"
        assert str(ChebyshevHeuristic()) == "ChebyshevHeuristic"
        assert str(OctileHeuristic()) == "OctileHeuristic"


class TestZeroHeuristic:
    """Тестирование нулевой эвристики."""

    def test_always_zero(self):
        h = ZeroHeuristic()
        assert h.estimate("A", "B") == 0.0
        assert h.estimate(1, 2) == 0.0
        assert h.estimate((1, 2), (3, 4)) == 0.0


class TestEuclideanHeuristic:
    """Тестирование евклидовой эвристики."""

    def test_euclidean_distance(self):
        h = EuclideanHeuristic()
        assert h.estimate((0, 0), (5, 0)) == 5.0
        assert h.estimate((0, 0), (3, 4)) == 5.0
        assert h.estimate((1, 1), (1, 1)) == 0.0
        assert h.estimate((-3, -4), (0, 0)) == 5.0

    def test_float_coordinates(self):
        h = EuclideanHeuristic()
        result = h.estimate((1.5, 2.5), (4.5, 6.5))
        expected = math.sqrt(3.0**2 + 4.0**2)
        assert math.isclose(result, expected)

    def test_invalid_input(self):
        h = EuclideanHeuristic()
        assert h.estimate("A", "B") == 0.0
        assert h.estimate((1,), (2, 3)) == 0.0
        assert h.estimate(123, 456) == 0.0


class TestManhattanHeuristic:
    """Тестирование манхэттенской эвристики."""

    def test_manhattan_distance(self):
        h = ManhattanHeuristic()
        assert h.estimate((0, 0), (5, 0)) == 5.0
        assert h.estimate((0, 0), (3, 4)) == 7.0
        assert h.estimate((-2, -3), (1, 2)) == 8.0
        assert h.estimate((1, 1), (1, 1)) == 0

    def test_float_coordinates(self):
        h = ManhattanHeuristic()
        result = h.estimate((1.5, 2.5), (4.5, 6.5))
        assert math.isclose(result, 3.0 + 4.0)

    def test_invalid_input(self):
        h = ManhattanHeuristic()
        assert h.estimate("A", "B") == 0.0
        assert h.estimate((1,), (2, 3)) == 0.0
        assert h.estimate(123, 456) == 0.0


class TestChebyshevHeuristic:
    """Тестирование эвристики Чебышёва."""

    def test_chebyshev_distance(self):
        h = ChebyshevHeuristic()
        assert h.estimate((0, 0), (5, 0)) == 5.0
        assert h.estimate((0, 0), (0, 4)) == 4.0
        assert h.estimate((0, 0), (3, 4)) == 4.0
        assert h.estimate((0, 0), (7, 2)) == 7.0
        assert h.estimate((-2, -3), (1, 2)) == 5.0
        assert h.estimate((1, 1), (1, 1)) == 0

    def test_invalid_input(self):
        h = ChebyshevHeuristic()
        assert h.estimate("A", "B") == 0.0
        assert h.estimate((1,), (2, 3)) == 0.0
        assert h.estimate(123, 456) == 0.0


class TestOctileHeuristic:
    """Тестирование октаиловой эвристики."""

    def test_octile_distance_default_cost(self):
        h = OctileHeuristic()
        assert h.estimate((0, 0), (5, 0)) == 5.0
        assert h.estimate((0, 0), (0, 5)) == 5.0
        assert h.estimate((0, 0), (3, 3)) == 3 * math.sqrt(2)
        assert math.isclose(h.estimate((0, 0), (3, 4)), 3 * math.sqrt(2) + 1)
        assert math.isclose(h.estimate((0, 0), (4, 3)), 3 * math.sqrt(2) + 1)

    def test_octile_distance_custom_cost(self):
        h = OctileHeuristic(diagonal_cost=1.5)
        assert h.estimate((0, 0), (3, 3)) == 4.5
        assert math.isclose(h.estimate((0, 0), (3, 4)), 4.5 + 1)

    def test_invalid_input(self):
        h = OctileHeuristic()
        assert h.estimate("A", "B") == 0.0
        assert h.estimate((1,), (2, 3)) == 0.0
        assert h.estimate(123, 456) == 0.0


class TestHeuristicFactory:
    """Тестирование фабрики эвристик."""

    def test_create_zero(self):
        h = HeuristicFactory.create("zero")
        assert isinstance(h, ZeroHeuristic)

    def test_create_euclidean(self):
        h = HeuristicFactory.create("euclidean")
        assert isinstance(h, EuclideanHeuristic)
        assert h.estimate((0, 0), (3, 4)) == 5.0

    def test_create_manhattan(self):
        h = HeuristicFactory.create("manhattan")
        assert isinstance(h, ManhattanHeuristic)
        assert h.estimate((0, 0), (3, 4)) == 7.0

    def test_create_chebyshev(self):
        h = HeuristicFactory.create("chebyshev")
        assert isinstance(h, ChebyshevHeuristic)
        assert h.estimate((0, 0), (3, 4)) == 4.0

    def test_create_octile(self):
        h = HeuristicFactory.create("octile")
        assert isinstance(h, OctileHeuristic)
        assert math.isclose(h.estimate((0, 0), (3, 4)), 3 * math.sqrt(2) + 1)

    def test_create_octile_custom_cost(self):
        h = HeuristicFactory.create("octile", diagonal_cost=1.5)
        assert isinstance(h, OctileHeuristic)
        assert h.diagonal_cost == 1.5

    def test_create_unknown(self):
        with pytest.raises(ValueError):
            HeuristicFactory.create("unknown")

    def test_list_available(self):
        available = HeuristicFactory.list_available()
        assert "zero" in available
        assert "euclidean" in available
        assert "manhattan" in available
        assert "chebyshev" in available
        assert "octile" in available
        assert len(available) == 5
