import pygame
import datetime

class Clock:
    def __init__(self, screen):
        self.screen = screen
        self.hand_img = pygame.image.load("images/mickey_hand.png")
        self.center = (300, 300)

    def draw(self):
        now = datetime.datetime.now()

        seconds = now.second
        minutes = now.minute

        # угол (360 / 60 = 6 градусов за единицу)
        sec_angle = -seconds * 6
        min_angle = -minutes * 6

        # вращение
        sec_hand = pygame.transform.rotate(self.hand_img, sec_angle)
        min_hand = pygame.transform.rotate(self.hand_img, min_angle)

        # центрирование
        rect1 = sec_hand.get_rect(center=self.center)
        rect2 = min_hand.get_rect(center=self.center)

        self.screen.blit(sec_hand, rect1)
        self.screen.blit(min_hand, rect2)