import pygame
from color_palette import *
import random

pygame.init()

WIDTH = 600
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont(None, 36)

image_game_over = font.render("Game Over", True, colorRED)
image_game_over_rect = image_game_over.get_rect(center=(WIDTH // 2, HEIGHT // 2))

CELL = 30


def draw_grid():
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            if j != 0:
                pygame.draw.rect(screen, colorGRAY, (i * CELL, j * CELL, CELL, CELL), 1)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0
        self.score = 0
        self.level = 1
        self.alive = True

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy

        head = self.body[0]

        if head.x < 0 or head.x >= WIDTH // CELL or head.y < 0 or head.y >= HEIGHT // CELL:
            self.alive = False

    def draw(self):
        pygame.draw.rect(screen, colorRED,
                         (self.body[0].x * CELL, self.body[0].y * CELL, CELL, CELL))

        for s in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW,
                             (s.x * CELL, s.y * CELL, CELL, CELL))

    def check_collision(self, food):
        head = self.body[0]

        if head.x == food.pos.x and head.y == food.pos.y:
            self.score += food.weight
            self.body.append(Point(head.x, head.y))
            food.generate_random_pos(self.body)
            self.level = 1 + self.score // 3


class Food:
    def __init__(self):
        self.pos = Point(5, 5)
        self.weight = 1
        self.spawn_time = pygame.time.get_ticks()

    def draw(self):
        pygame.draw.rect(screen, colorGREEN,
                         (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

        text = font.render(str(self.weight), True, colorBLACK)
        screen.blit(text, (self.pos.x * CELL + 8, self.pos.y * CELL + 5))

    def generate_random_pos(self, snake_body):
        self.weight = random.choice([1, 2, 3])
        self.spawn_time = pygame.time.get_ticks()

        while True:
            self.pos.x = random.randint(0, WIDTH // CELL - 1)
            self.pos.y = random.randint(1, HEIGHT // CELL - 1)

            if not any(self.pos.x == s.x and self.pos.y == s.y for s in snake_body):
                break


# ---------------- RESET FUNCTION ----------------
def reset_game():
    snake = Snake()
    food = Food()
    food.generate_random_pos(snake.body)
    return snake, food


snake, food = reset_game()

clock = pygame.time.Clock()
FPS = 5

running = True

while running:

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RIGHT:
                snake.dx, snake.dy = 1, 0
            elif event.key == pygame.K_LEFT:
                snake.dx, snake.dy = -1, 0
            elif event.key == pygame.K_DOWN:
                snake.dx, snake.dy = 0, 1
            elif event.key == pygame.K_UP:
                snake.dx, snake.dy = 0, -1

            # ---------------- RESTART ----------------
            if not snake.alive:
                if event.key == pygame.K_r:
                    snake, food = reset_game()

                if event.key == pygame.K_ESCAPE:
                    running = False

    # food timer
    if pygame.time.get_ticks() - food.spawn_time > 5000:
        food.generate_random_pos(snake.body)

    # update
    if snake.alive:
        snake.move()
        snake.check_collision(food)

    # draw
    screen.fill(colorBLACK)
    draw_grid()

    snake.draw()
    food.draw()

    # UI
    score_text = font.render(f"Score: {snake.score}", True, colorWHITE)
    level_text = font.render(f"Level: {snake.level}", True, colorWHITE)

    screen.blit(score_text, (10, 5))
    screen.blit(level_text, (150, 5))

    # GAME OVER SCREEN
    if not snake.alive:
        screen.blit(image_game_over, image_game_over_rect)

        restart_text = font.render("Press R to Restart / ESC to Quit", True, colorWHITE)
        screen.blit(restart_text, (WIDTH//2 - 180, HEIGHT//2 + 40))

    pygame.display.flip()
    clock.tick(FPS + snake.level)

pygame.quit()