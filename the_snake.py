from random import randint
from typing import List, Optional, Tuple

import pygame


# Константы для размеров поля и сетки:
SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP: Tuple[int, int] = (0, -1)
DOWN: Tuple[int, int] = (0, 1)
LEFT: Tuple[int, int] = (-1, 0)
RIGHT: Tuple[int, int] = (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR: Tuple[int, int, int] = (0, 0, 0)
BORDER_COLOR: Tuple[int, int, int] = (93, 216, 228)
APPLE_COLOR: Tuple[int, int, int] = (255, 0, 0)
SNAKE_COLOR: Tuple[int, int, int] = (0, 255, 0)
TEXT_COLOR: Tuple[int, int, int] = (255, 255, 255)

# Скорость движения змейки:
SPEED: int = 20

# Настройка игрового окна:
screen: pygame.Surface = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32
)
pygame.display.set_caption('Змейка')
clock: pygame.time.Clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self) -> None:
        """Инициализирует игровой объект."""
        self.position: Tuple[int, int] = (
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        )
        self.body_color: Optional[Tuple[int, int, int]] = None

    def draw_cell(
        self, position: Tuple[int, int], color: Tuple[int, int, int]
    ) -> None:
        """Отрисовывает одну ячейку на экране."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self) -> None:
        """Абстрактный метод для отрисовки объекта."""
        raise NotImplementedError(
            'Метод draw() должен быть переопределен в дочерних классах'
        )


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self) -> None:
        """Инициализирует яблоко."""
        super().__init__()
        self.body_color: Tuple[int, int, int] = APPLE_COLOR
        self.randomize_position()

    def randomize_position(
        self, occupied_positions: List[Tuple[int, int]] = None
    ) -> None:
        """Устанавливает случайное положение яблока."""
        if occupied_positions is None:
            occupied_positions = []

        while True:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if new_position not in occupied_positions:
                self.position = new_position
                break

    def draw(self) -> None:
        """Отрисовывает яблоко на экране."""
        self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self) -> None:
        """Инициализирует змейку."""
        super().__init__()
        self.body_color: Tuple[int, int, int] = SNAKE_COLOR
        self.reset()

    def update_direction(self) -> None:
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self) -> Tuple[int, int]:
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def move(self) -> None:
        """Двигает змейку вперед."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self) -> None:
        """Отрисовывает змейку на экране."""
        for position in self.positions[:-1]:
            self.draw_cell(position, self.body_color)

        head_position = self.get_head_position()
        self.draw_cell(head_position, self.body_color)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние."""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1
        self.last = None


def handle_keys(game_object: Snake) -> None:
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main() -> None:
    """Основная функция игры."""
    pygame.init()

    snake: Snake = Snake()
    apple: Apple = Apple()
    score: int = 0
    font: pygame.font.Font = pygame.font.Font(None, 36)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
            score += 1

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            score = 0

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()

        score_text = font.render(f'Очки: {score}', True, TEXT_COLOR)
        screen.blit(score_text, (10, 10))

        pygame.display.update()


if __name__ == '__main__':
    main()
    