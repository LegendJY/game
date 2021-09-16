#git test 중입니다.
import pygame
import sys
import math
from pygame.locals import *
import random

img_galaxy = pygame.image.load("img/galaxy.png")
img_ship = [ pygame.image.load("img/starship.png"),
             pygame.image.load("img/starship_l.png"),
             pygame.image.load("img/starship_r.png"),
             pygame.image.load("img/starship_burner.png") ]
img_weapon = pygame.image.load("img/bullet.png")

img_enemy = [ pygame.image.load("img/enemy0.png"),
              pygame.image.load("img/enemy1.png") ]

ENEMY_MAX = 100
emy_no = 0
emy_f = [False] * ENEMY_MAX
emy_x = [0] * ENEMY_MAX
emy_y = [0] * ENEMY_MAX
emy_a = [0] * ENEMY_MAX
emy_type = [0] * ENEMY_MAX
emy_speed = [0] * ENEMY_MAX

LINE_T = -80
LINE_B = 800
LINE_L = -80
LINE_R = 1040

tmr = 0
missile_move = 0

bg_y = 0
ship_x = 480
ship_y = 360
ship_d = 0

key_spc = 0
key_spc2 = 0
key_spc3 = 0
key_spc4 = 0
key_spc5 = 0

key_i = 0
key_j = 0
key_k = 0
key_l = 0
MISSILE_MAX = 200
msl_no = 0
msl_no2 = 0
msl_no3 = 0
msl_no4 = 0

msl_a = [0] * MISSILE_MAX
msl_a2 = [0] * MISSILE_MAX
msl_a3 = [0] * MISSILE_MAX
msl_a4 = [0] * MISSILE_MAX
typ = 0

msl_f = [False] * MISSILE_MAX
msl_x = [0] * MISSILE_MAX
msl_y = [0] * MISSILE_MAX

msl_f2 = [False] * MISSILE_MAX
msl_x2 = [0] * MISSILE_MAX
msl_y2 = [0] * MISSILE_MAX

msl_f3 = [False] * MISSILE_MAX
msl_x3 = [0] * MISSILE_MAX
msl_y3 = [0] * MISSILE_MAX

msl_f4 = [False] * MISSILE_MAX
msl_x4 = [0] * MISSILE_MAX
msl_y4 = [0] * MISSILE_MAX

def move_starship(scrn,key):
    global ship_x,ship_y,ship_d,missile_move,key_spc,key_spc2,key_spc3,key_spc4,key_spc5,key_i,key_j,key_k,key_l
    ship_d= 0
    if key[K_UP] == 1:
        ship_y = ship_y - 20
    if key[K_DOWN] == 1:
        ship_y = ship_y + 20
    if key[K_LEFT] == 1:
        ship_x = ship_x - 20
        ship_d = 1
    if key[K_RIGHT] == 1:
        ship_x = ship_x + 20
        ship_d = 2

    key_spc = (key_spc + 1) * key[K_w]
    if key_spc % 5 == 1:
        set_missile(0)
    key_spc2 = (key_spc2 + 1) * key[K_s]
    if key_spc2 % 5 == 1:
        set_missile2(0)
    key_spc3 = (key_spc3 + 1) * key[K_a]
    if key_spc3 % 5 == 1:
        set_missile3(0)
    key_spc4 = (key_spc4 + 1) * key[K_d]
    if key_spc4 % 5 == 1:
        set_missile4(0)
    key_spc5 = (key_spc5 + 1) * key[K_SPACE]
    if key_spc5 % 5 == 1:
        set_missile(0)
        set_missile2(0)
        set_missile3(0)
        set_missile4(0)

    key_i = (key_i+1) * key[K_i]
    key_j = (key_j + 1) * key[K_j]
    key_k = (key_k + 1) * key[K_k]
    key_l = (key_l + 1) * key[K_l]
    if key_i == 1:
        set_missile(10)
    if key_j == 1:
        set_missile2(10)
    if key_k == 1:
        set_missile3(10)
    if key_l == 1:
        set_missile4(10)

    if ship_y < 80:
        ship_y = 80
    if ship_y > 640:
        ship_y = 640
    if ship_x < 40:
        ship_x = 40
    if ship_x > 920:
        ship_x = 920
    img_rz = pygame.transform.rotozoom(img_ship[ship_d],0,1)
    scrn.blit(img_ship[3],[ship_x-9,ship_y + 40+(tmr % 3)*2])
    scrn.blit(img_rz, [ship_x-37, ship_y-52])

def set_missile(typ):
    global msl_no
    if typ == 0:
        msl_f[msl_no] = True
        msl_x[msl_no] = ship_x
        msl_y[msl_no] = ship_y
        msl_a[msl_no] = 270
        msl_no = (msl_no + 1) % MISSILE_MAX
    if typ == 10:
        for a in range(160,390,10):
            msl_f[msl_no] = True
            msl_x[msl_no] = ship_x
            msl_y[msl_no] = ship_y
            msl_a[msl_no] = a
            msl_no = (msl_no + 1) % MISSILE_MAX

def set_missile2(typ):
    '''global msl_no2
    if typ == 0:
        msl_f2[msl_no2] = True
        msl_x2[msl_no2] = ship_x
        msl_y2[msl_no2] = ship_y
        msl_a2[msl_no2] = 270
        msl_no2 = (msl_no2 + 1) % MISSILE_MAX
    if typ == 10:
        for a in range(160, 390, 10):
            msl_f2[msl_no2] = True
            msl_x2[msl_no2] = ship_x
            msl_y2[msl_no2] = ship_y
            msl_a2[msl_no2] = a
            msl_no2 = (msl_no2 + 1) % MISSILE_MAX'''

def set_missile3(typ):
    global msl_no3
    msl_f3[msl_no3] = True
    msl_x3[msl_no3] = ship_x
    msl_y3[msl_no3] = ship_y
    msl_no3 = (msl_no3 + 1) % MISSILE_MAX

def set_missile4(typ):
    global msl_no4
    msl_f4[msl_no4] = True
    msl_x4[msl_no4] = ship_x
    msl_y4[msl_no4] = ship_y
    msl_no4 = (msl_no4 + 1) % MISSILE_MAX

def move_missile(scrn):
    global msl_f,msl_y
    for i in range(MISSILE_MAX):
        if msl_f[i] == True:
            msl_x[i] += 50 * math.cos(math.radians(msl_a[i]))
            msl_y[i] += 50 * math.sin(math.radians(msl_a[i]))
            img_rz5 = pygame.transform.rotozoom(img_weapon,-90 - msl_a[i],1.0)
            scrn.blit(img_rz5, [msl_x[i] - img_rz5.get_width() / 2, msl_y[i] - img_rz5.get_height() / 2])
            if msl_y[i] < 0 or msl_x[i] < 0 or msl_x[i] > 960:
                msl_f[i] = False

def move_missile2(scrn):
    '''global msl_f2, msl_y2
    for i in range(MISSILE_MAX):
        if msl_f2[i] == True:
            msl_x2[i] += 50 * math.cos(math.radians(msl_a2[i]))
            msl_y2[i] += 50 * math.sin(math.radians(msl_a2[i]))
            img_rz6 = pygame.transform.rotozoom(img_weapon, -90 - msl_a2[i], 1.0)
            scrn.blit(img_rz6, [msl_x2[i] - img_rz6.get_width() / 2, msl_y2[i] - img_rz6.get_height() / 2])
            if msl_y2[i] < 0 or msl_x2[i] < 0 or msl_x2[i] > 960:
                msl_f2[i] = False
'''
def move_missile3(scrn):
    global msl_f3, msl_y3
    for i in range(MISSILE_MAX):
        if msl_f3[i] == True:
            msl_x3[i] -= 50
            img_rz3 = pygame.transform.rotozoom(img_weapon, 90, 1.0)
            scrn.blit(img_rz3, [msl_x3[i] - 10, msl_y3[i] - 60])
            if msl_x3[i] < 0:
                msl_f3[i] = False


def move_missile4(scrn):
    global msl_f4, msl_y4
    for i in range(MISSILE_MAX):
        if msl_f4[i] == True:
            msl_x4[i] += 50
            img_rz4 = pygame.transform.rotozoom(img_weapon, 270, 1.0)
            scrn.blit(img_rz4, [msl_x4[i] - 10, msl_y4[i] - 60])
            if msl_y4[i] > 960:
                msl_f4[i] = False

def bring_enemy():
    if tmr % 30 == 0:
        set_enemy(random.randint(20,940),LINE_T,90,1,6)

def set_enemy(x,y,a,ty,sp):
    global emy_no
    while True:
        if emy_f[emy_no] == False:
            emy_f[emy_no] = True
            emy_x[emy_no] = x
            emy_y[emy_no] = y
            emy_a[emy_no] = a
            emy_type[emy_no] = ty
            emy_speed[emy_no] = sp

def move_enemy(scrn):
    for i in range(ENEMY_MAX):
        if emy_f[i] == True:
            ang = -90 - emy_a
            png = emy_type[i]
            emy_x = emy_x[i] + emy_speed[i] * math.cos(math.radians(emy_a[i]))
            emy_y = emy_y[i] + emy_speed[i] * math.sin(math.radians(emy_a[i]))
            if emy_type == 1 and emy_y[i] > 360:
                set_enemy(emy_x[i],emy_y[i],90,0,8)
                emy_a[i] -45
                emy_speed[i] = 16

            if emy_x[i] < LINE_L or LINE_R < emy_x[i] or emy_y[i] < LINE_T or LINE_B < emy_y[i]:
                emy_f[i] = False
            img_rz = pygame.transform.rotozoom(img_enemy[png],ang,1.0)
            scrn.blit(img_rz,[emy_x[i]-img_rz.get_width()/2,emy_y[i]-img_rz.get_height()/2])

def main():
    global bg_y,tmr
    pygame.init()
    pygame.display.set_caption("galaxy game")
    screen = pygame.display.set_mode((960,720))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    screen = pygame.display.set_mode((960,720),pygame.FULLSCREEN)
                if event.key == pygame.K_ESCAPE or pygame.K_F2:
                    screen = pygame.display.set_mode((960,720))

        bg_y = (bg_y+20) % 720
        tmr += 1

        screen.blit(img_galaxy,[0,bg_y-720])
        screen.blit(img_galaxy,[0,bg_y])

        key = pygame.key.get_pressed()
        move_starship(screen,key)
        move_missile(screen)
        move_missile2(screen)
        move_missile3(screen)
        move_missile4(screen)
        bring_enemy()
        move_enemy(screen)

        pygame.display.update()
        clock.tick(20)

if __name__ == "__main__":
    main()