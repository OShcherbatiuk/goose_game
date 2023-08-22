import random
from os import listdir

import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT

pygame.init()

FPS = pygame.time.Clock()

screen = width, heigth = 1024, 768

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0

font = pygame.font.SysFont('Verdana', 20)

main_surface = pygame.display.set_mode(screen)

IMGS_PATH = 'goose'

player_imgs = [pygame.transform.scale(pygame.image.load(IMGS_PATH + '/' + file).convert_alpha(), (120, 60)) for file in
               listdir(IMGS_PATH)]
player = player_imgs[0]
player_rect = player.get_rect()
player_speed = 5


def creat_enemy():
    enemy = pygame.transform.scale(pygame.image.load('enemy.png').convert_alpha(), (80, 30))
    enemy_rect = pygame.Rect(width, random.randint(30, heigth - 30), *enemy.get_size())
    enemy_speed = random.randint(2, 5)
    return [enemy, enemy_rect, enemy_speed]


def creat_bonus():
    bonus = pygame.transform.scale(pygame.image.load('bonus.png').convert_alpha(), (100, 160))
    bonus_rect = pygame.Rect(random.randint(100, width - 100), -bonus.get_height(), *bonus.get_size())
    bonus_speed = random.randint(3, 6)
    return [bonus, bonus_rect, bonus_speed]


def creat_weapon_bonus():
    weapon_bonus = pygame.transform.scale(pygame.image.load('weapon_bonus.png').convert_alpha(), (70, 70))
    weapon_bonus_rect = pygame.Rect(random.randint(70, width - 70), -weapon_bonus.get_height(), *weapon_bonus.get_size())
    weapon_bonus_speed = 4
    return [weapon_bonus, weapon_bonus_rect, weapon_bonus_speed]


def create_weapon():
    weapon = pygame.transform.scale(pygame.image.load('weapon.png').convert_alpha(), (30, 80))
    weapon_rect = pygame.Rect(random.randint(30, width - 30), heigth, *weapon.get_size())
    weapon_speed = 10
    return [weapon, weapon_rect, weapon_speed]


bg = pygame.transform.scale(pygame.image.load('background.png').convert(), screen)
bgX = 0
bgX2 = bg.get_width()
bg_speed = 1

CREAT_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREAT_ENEMY, 1500)

CREAT_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREAT_BONUS, 1500)

CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 125)

CRATE_WEAPON_BONUS = pygame.USEREVENT + 4
pygame.time.set_timer(CRATE_WEAPON_BONUS, 5500)

img_index = 0

scores = 0

enemies = []
bonuses = []
weapons = []
weapons_bonuses = []

is_working = True

while is_working:

    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False

        if event.type == CREAT_ENEMY:
            enemies.append(creat_enemy())

        if event.type == CREAT_BONUS:
            bonuses.append(creat_bonus())

        if event.type == CRATE_WEAPON_BONUS:
            weapons_bonuses.append(creat_weapon_bonus())

        if event.type == CHANGE_IMG:
            img_index += 1
            if img_index == len(player_imgs):
                img_index = 0
            player = player_imgs[img_index]

    pressed_keys = pygame.key.get_pressed()

    bgX -= bg_speed
    bgX2 -= bg_speed

    if bgX < -bg.get_width():
        bgX = bg.get_width()

    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()

    main_surface.blit(bg, (bgX, 0))
    main_surface.blit(bg, (bgX2, 0))

    main_surface.blit(player, player_rect)

    main_surface.blit(font.render(str(scores), True, BLACK), (width - 30, 0))

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])

        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

        if player_rect.colliderect(enemy[1]):
            is_working = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])

        if bonus[1].bottom > heigth:
            bonuses.pop(bonuses.index(bonus))

        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            scores += 1

    for weapon_bonus in weapons_bonuses:
        weapon_bonus[1] = weapon_bonus[1].move(0, weapon_bonus[2])
        main_surface.blit(weapon_bonus[0], weapon_bonus[1])

        if weapon_bonus[1].bottom > heigth:
            weapons_bonuses.pop(weapons_bonuses.index(weapon_bonus))

        if player_rect.colliderect(weapon_bonus[1]):
            weapons_bonuses.pop(weapons_bonuses.index(weapon_bonus))
            scores += 2
            for _ in range(7):
                weapons.append(create_weapon())

    for weapon in weapons:
        weapon[1] = weapon[1].move(0, -weapon[2])
        main_surface.blit(weapon[0], weapon[1])

        if weapon[1].top < 0:
            weapons.pop(weapons.index(weapon))

        for enemy in enemies:
            if enemy[1].colliderect(weapon[1]):
                enemies.pop(enemies.index(enemy))
                weapons.pop(weapons.index(weapon))
                scores += 1

    if pressed_keys[K_DOWN] and not player_rect.bottom >= heigth:
        player_rect = player_rect.move(0, player_speed)

    if pressed_keys[K_UP] and not player_rect.top <= 0:
        player_rect = player_rect.move(0, -player_speed)

    if pressed_keys[K_RIGHT] and not player_rect.right >= width:
        player_rect = player_rect.move(player_speed, 0)

    if pressed_keys[K_LEFT] and not player_rect.left <= 0:
        player_rect = player_rect.move(-player_speed, 0)

    pygame.display.flip()
