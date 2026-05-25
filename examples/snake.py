"""
Змейка с искусственным интеллектом на основе библиотеки графов.
"""

import random
import sys
from typing import List, Optional, Set, Tuple

import pygame

from src.algorithms.astar import astar_search
from src.algorithms.heuristics import ManhattanHeuristic
from src.core.enums import GraphType
from src.core.graph import AdjacencyListGraph

# Константы
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE

# Настройки игры
WALL_COUNT = 100  # Количество стен (можно изменить)
WALL_COLOR = (128, 128, 128)
WALL_THICKNESS = 1

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (100, 100, 255)

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class GraphGrid:
    """Граф игрового поля."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.graph = AdjacencyListGraph[Tuple[int, int]](GraphType.UNDIRECTED)
        self.obstacles: Set[Tuple[int, int]] = set()
        self._build_graph()

    def _build_graph(self):
        for x in range(self.width):
            for y in range(self.height):
                self.graph.add_node((x, y))

        for x in range(self.width):
            for y in range(self.height):
                node = (x, y)
                if x + 1 < self.width:
                    self.graph.add_edge(node, (x + 1, y), 1.0)
                if y + 1 < self.height:
                    self.graph.add_edge(node, (x, y + 1), 1.0)

    def find_path(
        self, start: Tuple[int, int], goal: Tuple[int, int]
    ) -> Optional[List[Tuple[int, int]]]:
        if start not in self.graph.get_nodes() or goal not in self.graph.get_nodes():
            return None
        try:
            result = astar_search(self.graph, start, goal, ManhattanHeuristic())
            return result.path[1:] if len(result.path) > 1 else []
        except Exception:
            return None


class AISnake:
    """Змейка с ИИ."""

    def __init__(self, grid: GraphGrid):
        self.grid = grid
        self.body: List[Tuple[int, int]] = []
        self.direction = RIGHT
        self.grow_flag = False
        self.food_pos = (0, 0)
        self._init_snake()

    def _init_snake(self):
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        self.body = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
        self.direction = RIGHT
        self.grow_flag = False

    def get_head(self) -> Tuple[int, int]:
        return self.body[0]

    def get_body_set(self) -> Set[Tuple[int, int]]:
        return set(self.body)

    def move(self) -> bool:
        head = self.get_head()
        path = self._find_path_to_food()

        if path and len(path) > 0:
            return self._move_to(path[0])
        return self._move_safe()

    def _move_to(self, target: Tuple[int, int]) -> bool:
        head = self.get_head()
        dx = target[0] - head[0]
        dy = target[1] - head[1]

        if abs(dx) + abs(dy) != 1:
            return False

        new_dir = (dx, dy)
        if (new_dir[0] * -1, new_dir[1] * -1) == self.direction:
            return False

        self.direction = new_dir
        self.body.insert(0, target)
        if not self.grow_flag:
            self.body.pop()
        else:
            self.grow_flag = False
        return True

    def _find_path_to_food(self) -> List[Tuple[int, int]]:
        head = self.get_head()
        obstacles = self.grid.obstacles.copy()
        obstacles.update(self.get_body_set())

        if head in obstacles:
            obstacles.remove(head)

        temp_graph = AdjacencyListGraph[Tuple[int, int]](GraphType.UNDIRECTED)

        for x in range(self.grid.width):
            for y in range(self.grid.height):
                node = (x, y)
                if node not in obstacles:
                    temp_graph.add_node(node)

        for x in range(self.grid.width):
            for y in range(self.grid.height):
                node = (x, y)
                if node in obstacles:
                    continue
                if x + 1 < self.grid.width and (x + 1, y) not in obstacles:
                    temp_graph.add_edge(node, (x + 1, y), 1.0)
                if y + 1 < self.grid.height and (x, y + 1) not in obstacles:
                    temp_graph.add_edge(node, (x, y + 1), 1.0)

        try:
            if head in temp_graph.get_nodes() and self.food_pos in temp_graph.get_nodes():
                result = astar_search(temp_graph, head, self.food_pos, ManhattanHeuristic())
                if result and len(result.path) > 1:
                    return result.path[1:]
        except Exception:
            pass
        return []

    def _move_safe(self) -> bool:
        head = self.get_head()
        obstacles = self.grid.obstacles.copy()
        obstacles.update(self.get_body_set())

        for d in [self.direction, RIGHT, DOWN, LEFT, UP]:
            dx, dy = d
            new_head = (head[0] + dx, head[1] + dy)
            if (
                0 <= new_head[0] < self.grid.width
                and 0 <= new_head[1] < self.grid.height
                and new_head not in obstacles
            ):
                return self._move_to(new_head)
        return False

    def grow(self):
        self.grow_flag = True

    def check_collision(self) -> bool:
        head = self.body[0]
        if head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT:
            return True
        if head in self.body[1:]:
            return True
        if head in self.grid.obstacles:
            return True
        return False

    def set_food_pos(self, pos: Tuple[int, int]):
        self.food_pos = pos

    def get_current_path(self) -> List[Tuple[int, int]]:
        return self._find_path_to_food()

    def draw(self, screen):
        for i, seg in enumerate(self.body):
            color = GREEN if i == 0 else (0, 180, 0)
            pygame.draw.rect(
                screen,
                color,
                (seg[0] * CELL_SIZE, seg[1] * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1),
            )

        path = self.get_current_path()
        for i, pos in enumerate(path[:20]):
            pygame.draw.rect(
                screen,
                LIGHT_BLUE,
                (pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1),
                2,
            )


class Food:
    def __init__(self, snake: AISnake, walls: Set[Tuple[int, int]]):
        self.position = self._random_pos(snake, walls)

    def _random_pos(self, snake: AISnake, walls: Set[Tuple[int, int]]) -> Tuple[int, int]:
        for _ in range(100):
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            pos = (x, y)
            if pos not in snake.body and pos not in walls:
                return pos
        return (0, 0)

    def respawn(self, snake: AISnake, walls: Set[Tuple[int, int]]):
        self.position = self._random_pos(snake, walls)

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            RED,
            (
                self.position[0] * CELL_SIZE,
                self.position[1] * CELL_SIZE,
                CELL_SIZE - 1,
                CELL_SIZE - 1,
            ),
        )


class AIGame:
    def __init__(self, wall_count: int = WALL_COUNT):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(f"AI Snake")
        self.clock = pygame.time.Clock()

        self.wall_count = wall_count
        self.grid = GraphGrid(GRID_WIDTH, GRID_HEIGHT)
        self.snake = AISnake(self.grid)
        self.walls: Set[Tuple[int, int]] = set()
        self.food = Food(self.snake, self.walls)
        self.snake.set_food_pos(self.food.position)

        self._generate_walls()
        self._update_obstacles()

        self.score = 0
        self.game_speed = 15
        self.running = True
        self.paused = False

    def _generate_walls(self):
        """Сгенерировать стены."""
        self.walls.clear()
        for _ in range(self.wall_count):
            max_attempts = 100
            for _ in range(max_attempts):
                x = random.randint(0, GRID_WIDTH - 1)
                y = random.randint(0, GRID_HEIGHT - 1)
                pos = (x, y)
                if (
                    pos not in self.snake.body
                    and pos != self.food.position
                    and pos not in self.walls
                ):
                    self.walls.add(pos)
                    break

    def _update_obstacles(self):
        obstacles = self.walls.copy()
        obstacles.update(self.snake.get_body_set())
        self.grid.obstacles = obstacles

    def _draw_grid(self):
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, DARK_GRAY, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, DARK_GRAY, (0, y), (WINDOW_WIDTH, y))

    def _draw_walls(self):
        for wall in self.walls:
            pygame.draw.rect(
                self.screen,
                WALL_COLOR,
                (wall[0] * CELL_SIZE, wall[1] * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1),
            )

    def _show_info(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Очки: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

    def _show_game_over(self) -> bool:
        font = pygame.font.Font(None, 74)
        small_font = pygame.font.Font(None, 36)

        self.screen.fill(BLACK)
        game_over_text = font.render("ПОТРАЧЕНО", True, RED)
        score_text = small_font.render(f"Очки: {self.score}", True, WHITE)
        restart_text = small_font.render("Нажмите R для перезапуска, ESC - для выхода", True, WHITE)

        self.screen.blit(game_over_text, (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(score_text, (WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2))
        self.screen.blit(restart_text, (WINDOW_WIDTH // 2 - 260, WINDOW_HEIGHT // 2 + 50))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return True
                    if event.key == pygame.K_ESCAPE:
                        return False

    def _restart(self):
        self.snake = AISnake(self.grid)
        self.walls.clear()
        self._generate_walls()
        self.food = Food(self.snake, self.walls)
        self.snake.set_food_pos(self.food.position)
        self.score = 0
        self.game_speed = 15
        self.running = True
        self.paused = False
        self._update_obstacles()

    def demo_mode(self):
        print("\n" + "=" * 50)
        print("AI SNAKE - GRAPH LIBRARY DEMO")
        print("=" * 50)

        start = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        goal = (start[0] + 5, start[1] + 3)

        try:
            result = astar_search(self.grid.graph, start, goal, ManhattanHeuristic())
            print(f"Start: {start} -> Goal: {goal}")
            print(f"Path length: {len(result.path) - 1} steps")
            print(f"Time: {result.execution_time_ms:.2f} ms")
        except Exception as e:
            print(f"Error: {e}")

        print(f"Walls: {self.wall_count}")
        print("=" * 50)
        print("Game started. Snake follows optimal path (blue outline)")
        print("=" * 50)

    def run(self):
        while True:
            self._restart()

            while self.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.paused = not self.paused
                        if event.key == pygame.K_r:
                            self.running = False
                            break
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()

                if not self.running:
                    break

                if not self.paused:
                    self._update_obstacles()

                    if not self.snake.move():
                        self.running = False
                        break

                    if self.snake.get_head() == self.food.position:
                        self.snake.grow()
                        self.score += 1
                        self.food.respawn(self.snake, self.walls)
                        self.snake.set_food_pos(self.food.position)

                        if self.score % 5 == 0 and self.game_speed < 20:
                            self.game_speed += 1

                    if self.snake.check_collision():
                        self.running = False
                        break

                self.screen.fill(BLACK)
                self._draw_grid()
                self._draw_walls()
                self.food.draw(self.screen)
                self.snake.draw(self.screen)
                self._show_info()
                pygame.display.flip()
                self.clock.tick(self.game_speed)

            if not self._show_game_over():
                break

    def run_with_demo(self):
        self.demo_mode()
        self.run()


def main():
    """Главная функция."""
    # Измените WALL_COUNT в константах для настройки количества стен
    game = AIGame(wall_count=WALL_COUNT)
    game.run_with_demo()


if __name__ == "__main__":
    main()
