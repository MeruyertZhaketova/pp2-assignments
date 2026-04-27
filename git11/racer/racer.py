import pygame
import random
import time

pygame.init()

WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# ---------------- IMAGES ----------------
image_background = pygame.image.load('resources/AnimatedStreet.png')
image_player = pygame.image.load('resources/Player.png')
image_enemy = pygame.image.load('resources/Enemy.png')
coin_image = pygame.image.load('resources/dollar.png').convert_alpha()

# ---------------- SOUND ----------------
pygame.mixer.music.load('resources/background.wav')
pygame.mixer.music.play(-1)

sound_crash = pygame.mixer.Sound('resources/crash.wav')

# ---------------- FONT ----------------
font = pygame.font.SysFont("Verdana", 60)
fontt = pygame.font.SysFont("Verdana", 20)

image_game_over = font.render("Game Over", True, "black")
image_game_over_rect = image_game_over.get_rect(center=(WIDTH // 2, HEIGHT // 2))

collected = 0

clock = pygame.time.Clock()
FPS = 60


# ---------------- PLAYER ----------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_player
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT
        self.speed = 5

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH


# ---------------- ENEMY ----------------
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_enemy
        self.rect = self.image.get_rect()
        self.speed = 5
        self.reset()

    def reset(self):
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        self.rect.top = -100

    def move(self):
        self.rect.move_ip(0, self.speed)

        if self.rect.top > HEIGHT:
            self.reset()


# ---------------- COIN ----------------
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(coin_image, (40, 40))
        self.rect = self.image.get_rect()
        self.speed = 4
        self.value = 1
        self.reset()

    def reset(self):
        self.value = random.choice([1, 2, 3])
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        self.rect.top = random.randint(-300, -50)

    def move(self):
        self.rect.move_ip(0, self.speed)

        if self.rect.top > HEIGHT:
            self.reset()


# ---------------- INIT ----------------
player = Player()
enemy = Enemy()
coin = Coin()

all_sprites = pygame.sprite.Group(player, enemy, coin)
enemy_sprites = pygame.sprite.Group(enemy)
coin_sprites = pygame.sprite.Group(coin)

running = True

# ---------------- GAME LOOP ----------------
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # background
    screen.blit(image_background, (0, 0))

    # player move
    player.move()

    # score
    score_text = fontt.render(f"Score: {collected}", True, "black")
    screen.blit(score_text, (10, 10))

    # ---------------- MOVE + DRAW ----------------
    enemy.move()
    coin.move()

    screen.blit(enemy.image, enemy.rect)
    screen.blit(coin.image, coin.rect)
    screen.blit(player.image, player.rect)

    # ---------------- COIN COLLISION ----------------
    if pygame.sprite.collide_rect(player, coin):
        collected += coin.value
        coin.reset()

        if collected % 5 == 0:
            enemy.speed += 1
            coin.speed += 0.5

    # ---------------- ENEMY COLLISION ----------------
    if pygame.sprite.collide_rect(player, enemy):
        sound_crash.play()

        screen.fill("red")
        screen.blit(image_game_over, image_game_over_rect)
        pygame.display.flip()

        time.sleep(2)
        running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()