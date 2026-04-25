import pygame
from clock import Clock

pygame.init()

screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Mickey Clock")

clock_obj = Clock(screen)
fps = pygame.time.Clock()

running = True
while running:
    screen.fill((255, 255, 255))  # белый фон

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock_obj.draw()  # рисуем часы

    pygame.display.flip()
    fps.tick(60)

pygame.quit()