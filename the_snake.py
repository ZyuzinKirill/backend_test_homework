from random import choice, randint
import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()

class GameObject:
    def __init__(self, position=None):
        self.position = position if position else (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None
        self.direction = RIGHT
        self.next_direction = None
    
    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

class Apple(GameObject):
    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()
    
    def randomize_position(self):
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )
    
    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

class Snake(GameObject):
    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.positions = [self.position]
        self.last = None
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1
    
    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
    
    def get_head_position(self):
        return self.positions[0]
    
    def move(self):
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)
        
        self.positions.insert(0, new_head)
        self.last = self.positions.pop() if len(self.positions) > self.length else None
    
    def draw(self):
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
    
    def reset(self):
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1
        self.last = None

def handle_keys(game_object):
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

def main():
    pygame.init()
    
    snake = Snake()
    apple = Apple()
    score = 0
    font = pygame.font.Font(None, 36)
    
    while True:
        clock.tick(SPEED)
        
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            score += 1
        
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position()
            score = 0
        
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        
        score_text = font.render(f'Очки: {score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        pygame.display.update()

if __name__ == '__main__':
    main()
