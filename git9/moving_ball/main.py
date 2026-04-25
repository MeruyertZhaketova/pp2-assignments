import pygame
from ball import Ball

pygame.init()

WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")

WHITE = (255, 255, 255)

ball = Ball(WIDTH // 2, HEIGHT // 2)

clock = pygame.time.Clock()
done = False

while not done:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ball.move(0, -ball.speed, WIDTH, HEIGHT)
            if event.key == pygame.K_DOWN:
                ball.move(0, ball.speed, WIDTH, HEIGHT)
            if event.key == pygame.K_LEFT:
                ball.move(-ball.speed, 0, WIDTH, HEIGHT)
            if event.key == pygame.K_RIGHT:
                ball.move(ball.speed, 0, WIDTH, HEIGHT)

    screen.fill(WHITE)
    ball.draw(screen)
    pygame.display.flip()

pygame.quit()