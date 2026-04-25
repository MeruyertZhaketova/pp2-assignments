import pygame

WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Ball:
    def __init__(self, x, y, radius=25):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = 20

    def move(self, dx, dy, screen_width, screen_height):
        # проверка границ
        new_x = self.x + dx
        new_y = self.y + dy

        if self.radius <= new_x <= screen_width - self.radius:
            self.x = new_x
        if self.radius <= new_y <= screen_height - self.radius:
            self.y = new_y

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.x, self.y), self.radius)