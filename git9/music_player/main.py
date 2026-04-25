import pygame
import os
from player import MusicPlayer

pygame.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont("Arial", 24)

BASE_DIR = os.path.dirname(__file__)

playlist = [
    os.path.join(BASE_DIR, "sample_tracks", "track1.mp3"),
    os.path.join(BASE_DIR, "sample_tracks", "track2.mp3")
]

player = MusicPlayer(playlist)

running = True
while running:
    screen.fill((30, 30, 30))

    text = font.render(
        f"Now playing: {player.get_current_track()}",
        True,
        (255, 255, 255)
    )
    screen.blit(text, (20, 50))

    help_text = font.render(
        "P=Play S=Stop N=Next B=Prev Q=Quit",
        True,
        (180, 180, 180)
    )
    screen.blit(help_text, (20, 150))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_p:
                player.play()

            if event.key == pygame.K_s:
                player.stop()

            if event.key == pygame.K_n:
                player.next_track()

            if event.key == pygame.K_b:
                player.prev_track()

            if event.key == pygame.K_q:
                running = False

    pygame.display.flip()

pygame.quit()