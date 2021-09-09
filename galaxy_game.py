import pygame
import sys
import math
from pygame.locals import *

img_galaxy = pygame.image.load("img/galaxy.png")
img_ship = [ pygame.image.load("img/starship.png"),
             pygame.image.load("img/starship_l.png"),
             pygame.image.load("img/starship_r.png"),
             pygame.image.load("img/starship_burner.png") ]
img_weapon = pygame.image.load("img/bullet.png")

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

key_z = 0
MISSILE_MAX = 200
msl_no = 0
msl_no2 = 0
msl_no3 = 0
msl_no4 = 0

msl_a = [0] * MISSILE_MAX
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
    global ship_x,ship_y,ship_d,missile_move,key_spc,key_spc2,key_spc3,key_spc4,key_spc5,key_z
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
        set_missile2()
    key_spc3 = (key_spc3 + 1) * key[K_a]
    if key_spc3 % 5 == 1:
        set_missile3()
    key_spc4 = (key_spc4 + 1) * key[K_d]
    if key_spc4 % 5 == 1:
        set_missile4()
    key_spc5 = (key_spc5 + 1) * key[K_SPACE]
    if key_spc5 % 5 == 1:
        set_missile(0)
        set_missile2()
        set_missile3()
        set_missile4()

    key_z = (key_z+1) * key[K_z]
    if key_z == 1:
        set_missile(10)

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

def set_missile2():
    global msl_no2
    msl_f2[msl_no2] = True
    msl_x2[msl_no2] = ship_x
    msl_y2[msl_no2] = ship_y
    msl_no2 = (msl_no2 + 1) % MISSILE_MAX

def set_missile3():
    global msl_no3
    msl_f3[msl_no3] = True
    msl_x3[msl_no3] = ship_x
    msl_y3[msl_no3] = ship_y
    msl_no3 = (msl_no3 + 1) % MISSILE_MAX

def set_missile4():
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
            msl_y[i] += 50 * math.cos(math.radians(msl_a[i]))
            img_rz5 = pygame.transform.rotozoom(img_weapon,-90 - msl_a[i],1.0)
            scrn.blit(img_rz5, [msl_x[i] - img_rz5.get_width() / 2, msl_y[i] - img_rz5.get_height() / 2])
            if msl_y[i] < 0 or msl_x[i] < 0 or msl_x[i] > 960:
                msl_f[i] = False

def move_missile2(scrn):
    global msl_f2, msl_y2
    for i in range(MISSILE_MAX):
        if msl_f2[i] == True:
            msl_y2[i] += 50
            img_rz2 = pygame.transform.rotozoom(img_weapon,180,1.0)
            scrn.blit(img_rz2,[msl_x2[i] - 10, msl_y2[i] - 60])
            if msl_y2[i] > 720:
                msl_f2[i] = False

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

        pygame.display.update()
        clock.tick(20)

if __name__ == "__main__":
    main()