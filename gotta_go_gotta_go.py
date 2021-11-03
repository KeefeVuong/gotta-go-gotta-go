import pygame
import random
import sys
import os

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT
)

enemy_url = resource_path("enemy.png")
player_url = resource_path("player.png")
map_url = resource_path("map.png")

# Initialises the game
pygame.init()
pygame.font.init()
start_time = pygame.time.get_ticks()

clock = pygame.time.Clock()

ENEMY_MIN_SPEED = 5
ENEMY_MAX_SPEED = 20

PLAYER_SPEED = 5

# Size of the game
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 550

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load(enemy_url).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(int(ENEMY_MIN_SPEED), int(ENEMY_MAX_SPEED))

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load(player_url).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                0,
                SCREEN_HEIGHT // 2,
            )
        )

    def update(self, key_presses):
        if key_presses[K_UP]:
            self.rect.move_ip(0, -5)
        if key_presses[K_DOWN]:
            self.rect.move_ip(0, 5)
        if key_presses[K_SPACE]:
            self.rect.moveip()

        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 550)

player = Player()

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

x = "Sans"

font = pygame.font.SysFont(x, 34)
font_colour = pygame.Color("dodgerblue")

running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    ticks = pygame.time.get_ticks() - start_time
    millis = ticks % 1000
    seconds = int(ticks / 1000 % 60)
    minutes = int(ticks / 60000 % 24)
    out = '{minutes:02d}:{seconds:02d}:{millis}'.format(minutes=minutes, millis=millis, seconds=seconds)
    text = font.render(out, True, font_colour)
    screen.blit(text, (50, 50))

    for user in all_sprites:
        screen.blit(user.surf, user.rect)

    clock.tick(35)

    pygame.display.flip()

    key_presses = pygame.key.get_pressed()

    player.update(key_presses)

    if seconds == 30 or seconds == 59:
        ENEMY_MIN_SPEED += 0.3
        ENEMY_MAX_SPEED += 0.3

    enemies.update()

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False

    screen.blit(pygame.image.load(map_url).convert(), [0, 0])