import pygame
import random
import sys
import os
import time

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
immunity_url = resource_path("immunity.png")
slow_url = resource_path("slow.png")
pistol_url = resource_path("pistol.png")
shoot_pistol_url = resource_path("shoot_pistol.png")

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

class ShootPistol(pygame.sprite.Sprite):
    def __init__(self):
        super(ShootPistol, self).__init__()
        self.surf = pygame.image.load(shoot_pistol_url).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        coords = player.position()
        self.rect = self.surf.get_rect(
            center=(
                0,
                coords[1] - 25,
            )
        )

    def position(self):
        return (self.rect.top, self.rect.bottom)

    def fire(self):
        self.kill()

class Pistol(pygame.sprite.Sprite):
    def __init__(self):
        super(Pistol, self).__init__()
        self.surf = pygame.image.load(pistol_url).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = 10

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

    def collide(self):
        self.kill()

class Slow(pygame.sprite.Sprite):
    def __init__(self):
        super(Slow, self).__init__()
        self.surf = pygame.image.load(slow_url).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = 10

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

    def collide(self):
        self.kill()

class Immunity(pygame.sprite.Sprite):
    def __init__(self):
        super(Immunity, self).__init__()
        self.surf = pygame.image.load(immunity_url).convert()
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = 8

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

    def collide(self):
        self.kill()


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

    def shot(self):
        self.kill()

    def position(self):
        return (self.rect.top, self.rect.bottom)

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

        if self.rect.top <= 0:
            self.rect.top = SCREEN_HEIGHT - 65
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = 65

    def position(self):
        return (self.rect.top, self.rect.bottom)

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 600)

ADDIMMUNITY = pygame.USEREVENT + 2
pygame.time.set_timer(ADDIMMUNITY, 5000)

ADDSLOW = pygame.USEREVENT + 3
pygame.time.set_timer(ADDSLOW, 3500)

ADDPISTOL = pygame.USEREVENT + 4
pygame.time.set_timer(ADDPISTOL, 15000)

global player
player = Player()

slowed = pygame.sprite.Group()
enemies = pygame.sprite.Group()
immunity = pygame.sprite.Group()
pistol = pygame.sprite.Group()
shoot_pistol = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

x = "Sans"

font = pygame.font.SysFont(x, 34)
font_colour = pygame.Color("dodgerblue")

immunity_font = pygame.font.SysFont(x, 34)
immune = False
immune_timer = 0

slow_font = pygame.font.SysFont(x, 34)
slow = False
slow_timer = 0

pistol_font = pygame.font.SysFont(x, 34)
pistol_status = False
pistol_timer = 0

shoot_pistol_status = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_SPACE and pistol_status == True:
                global new_shoot_pistol
                new_shoot_pistol = ShootPistol()
                shoot_pistol.add(new_shoot_pistol)
                all_sprites.add(new_shoot_pistol)
                shoot_pistol_status = True
        elif event.type == QUIT:
            running = False
        elif event.type == ADDENEMY:
            global new_enemy
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == ADDIMMUNITY:
            global new_immunity
            new_immunity = Immunity()
            immunity.add(new_immunity)
            all_sprites.add(new_immunity)
        elif event.type == ADDSLOW:
            global new_slow
            new_slow = Slow()
            slowed.add(new_slow)
            all_sprites.add(new_slow)
        elif event.type == ADDPISTOL:
            global new_pistol
            new_pistol = Pistol()
            pistol.add(new_pistol)
            all_sprites.add(new_pistol)

    ticks = pygame.time.get_ticks() - start_time
    millis = ticks % 1000
    seconds = int(ticks / 1000 % 60)
    minutes = int(ticks / 60000 % 24)
    out = '{minutes:02d}:{seconds:02d}:{millis}'.format(minutes=minutes, millis=millis, seconds=seconds)
    text = font.render(out, True, font_colour)
    screen.blit(text, (50, 50))

    for user in all_sprites:
        screen.blit(user.surf, user.rect)

    if immune == True:
        immunity_text = immunity_font.render(f"You are currently immune for {(105 - immune_timer) // 35}", True, (255,0,0))
        screen.blit(immunity_text, (300, 10))

    if slow == True:
        slow_text = slow_font.render(f"Enemies are currently slowed for {(105 - slow_timer) // 35}", True, (255,0,0))
        screen.blit(slow_text, (300, 40))

    if pistol_status == True:
        pistol_text = pistol_font.render(f"You are equipped with the pistol for {(350 - pistol_timer) // 35}", True, (255,0,0))
        screen.blit(pistol_text, (300, 70))

    clock.tick(35)

    pygame.display.flip()

    key_presses = pygame.key.get_pressed()

    player.update(key_presses)

    if seconds == 30 or seconds == 59:
        ENEMY_MIN_SPEED += 0.08
        ENEMY_MAX_SPEED += 0.08

    slowed.update()
    immunity.update()
    pistol.update()
    enemies.update()

    if pygame.sprite.spritecollideany(player, immunity) or immune == True:
        if immune == False:
            immune = True
            new_immunity.collide()

        if immune_timer == 105:
            immune = False
            immune_timer = 0
        immune_timer += 1

    if pygame.sprite.spritecollideany(player, slowed) or slow == True:
        if slow == False:
            slow = True
            new_slow.collide()
            ENEMY_MIN_SPEED -= 15
            ENEMY_MAX_SPEED -= 15

        if slow_timer == 105:
            slow = False
            slow_timer = 0
            ENEMY_MIN_SPEED += 15
            ENEMY_MAX_SPEED += 15
        slow_timer += 1

    if pygame.sprite.spritecollideany(player, pistol) or pistol_status == True:
        if pistol_status == False:
            pistol_status = True
            new_pistol.collide()

        if pistol_timer == 350:
            pistol_status = False
            pistol_timer = 0

        pistol_timer += 1

        if shoot_pistol_status == True and pygame.sprite.groupcollide(shoot_pistol, enemies, True, True):
            shoot_pistol_status = False
        elif shoot_pistol_status == True:
            new_shoot_pistol.fire()

    if pygame.sprite.spritecollideany(player, enemies) and immune == False:
        player.kill()
        running = False

    screen.blit(pygame.image.load(map_url).convert(), [0, 0])