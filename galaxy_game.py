#git test 중입니다.
import pygame
import sys
import math
from pygame.locals import *
import random

BLACK = (0,0,0)
SILVER = (192,208,224)
RED = (255,0,0)
CYAN = (0,255,255)

img_galaxy = pygame.image.load("img/galaxy.png")
img_ship = [ pygame.image.load("img/starship.png"),
             pygame.image.load("img/starship_l.png"),
             pygame.image.load("img/starship_r.png"),
             pygame.image.load("img/starship_burner.png") ]

img_weapon = pygame.image.load("img/bullet.png")
img_shield = pygame.image.load("img/shield.png")

img_enemy = [ pygame.image.load("img/enemy0.png"),
              pygame.image.load("img/enemy1.png"),
              pygame.image.load("img/enemy2.png"),
              pygame.image.load("img/enemy3.png"),
              pygame.image.load("img/enemy4.png") ]

img_explode = [None,
               pygame.image.load("img/explosion1.png"),
               pygame.image.load("img/explosion2.png"),
               pygame.image.load("img/explosion3.png"),
               pygame.image.load("img/explosion4.png"),
               pygame.image.load("img/explosion5.png") ]

img_title = [ pygame.image.load("img/nebula.png"),
              pygame.image.load("img/logo.png") ]

se_barrage = None
se_damage = None
se_explosion = None
se_shot = None

idx = 0
score = 0

ENEMY_MAX = 100
emy_no = 0
emy_f = [False] * ENEMY_MAX
emy_x = [0] * ENEMY_MAX
emy_y = [0] * ENEMY_MAX
emy_a = [0] * ENEMY_MAX
emy_type = [0] * ENEMY_MAX
emy_speed = [0] * ENEMY_MAX

ENEMY_BULLET = 0

LINE_T = -80
LINE_B = 800
LINE_L = -80
LINE_R = 1040

tmr = 0
missile_move = 0

bg_y = 0
ship_x = 0#480
ship_y = 0#360
ship_d = 0
ship_shield = 0#100
ship_muteki = 0

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

EFFECT_MAX = 100
eff_no = 0
eff_p = [0] * EFFECT_MAX
eff_x = [0] * EFFECT_MAX
eff_y = [0] * EFFECT_MAX

def get_dis(x1,y1,x2,y2):
    return (x1-x2)**2 + (y1-y2)**2

def draw_text(scrn,txt,x,y,size,col):
    fnt = pygame.font.Font(None,size)
    sur = fnt.render(txt,True,col)
    x = x - sur.get_width() / 2
    y = y - sur.get_height() / 2
    scrn.blit(sur,[x,y])

def move_starship(scrn,key):
    global ship_x,ship_y,ship_d,missile_move,key_spc,key_spc2,key_spc3,key_spc4,key_spc5,key_z,ship_shield,ship_muteki,idx,tmr
    ship_d = 0
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
        se_shot.play()

    key_spc2 = (key_spc2 + 1) * key[K_s]
    if key_spc2 % 5 == 1:
        set_missile2(0)
        se_shot.play()

    key_spc3 = (key_spc3 + 1) * key[K_a]
    if key_spc3 % 5 == 1:
        set_missile3(0)
        se_shot.play()

    key_spc4 = (key_spc4 + 1) * key[K_d]
    if key_spc4 % 5 == 1:
        set_missile4(0)
        se_shot.play()

    key_spc5 = (key_spc5 + 1) * key[K_SPACE]
    if key_spc5 % 5 == 1:
        set_missile(0)
        set_missile2(0)
        set_missile3(0)
        set_missile4(0)
        se_shot.play()

    key_z = (key_z+1) * key[K_z]
    if key_z == 1 and ship_shield > 10:
        set_missile(10)
        ship_shield -= 10
        se_barrage.play()
    if ship_muteki % 2 == 0:
        scrn.blit(img_ship[3], [ship_x - 8, ship_y + 40 + (tmr % 3) * 2])
        scrn.blit(img_ship[ship_d], [ship_x - 37, ship_y - 48])
        if ship_y < 80:
            ship_y = 80
        if ship_y > 640:
            ship_y = 640
        if ship_x < 40:
            ship_x = 40
        if ship_x > 920:
            ship_x = 920
    if ship_muteki > 0:
        ship_muteki -= 1
        return
    elif idx == 1:
        for i in range(ENEMY_MAX):
            if emy_f[i] == True:
                w = img_enemy[emy_type[i]].get_width()
                h = img_enemy[emy_type[i]].get_height()
                r = ((w+h)/4 + (74 + 96)/4)
                if get_dis(emy_x[i],emy_y[i],ship_x,ship_y) < r * r:
                    set_effect(ship_x,ship_y)
                    ship_shield = ship_shield - 10
                    if ship_shield <= 0:
                        ship_shield = 0
                        idx = 2
                        tmr = 0
                    if ship_muteki == 0:
                        ship_muteki = 60
                        se_damage.play()
                    emy_f[i] = False

    if ship_y < 80:
        ship_y = 80
    if ship_y > 640:
        ship_y = 640
    if ship_x < 40:
        ship_x = 40
    if ship_x > 920:
        ship_x = 920
    scrn.blit(img_ship[3], [ship_x - 8, ship_y + 40 + (tmr % 3) * 2])
    scrn.blit(img_ship[ship_d], [ship_x - 37, ship_y - 48])

def set_missile(typ):
    global msl_no
    if typ == 0:
        msl_f[msl_no] = True
        msl_x[msl_no] = ship_x
        msl_y[msl_no] = ship_y
        msl_a[msl_no] = 270
        msl_no = (msl_no + 1) % MISSILE_MAX
    if typ == 10:
        for a in range(160,550,10):
            msl_f[msl_no] = True
            msl_x[msl_no] = ship_x
            msl_y[msl_no] = ship_y
            msl_a[msl_no] = a
            msl_no = (msl_no + 1) % MISSILE_MAX

def set_missile2(typ):
    global msl_no2
    msl_f2[msl_no2] = True
    msl_x2[msl_no2] = ship_x
    msl_y2[msl_no2] = ship_y
    msl_no2 = (msl_no2 + 1) % MISSILE_MAX

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
    global msl_f2, msl_y2
    for i in range(MISSILE_MAX):
        if msl_f2[i] == True:
            msl_y2[i] += 50
            img_rz2 = pygame.transform.rotozoom(img_weapon, 180, 1.0)
            scrn.blit(img_rz2, [msl_x2[i] - 10, msl_y2[i] - 60])
            if msl_x2[i] < 0:
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

def bring_enemy():
    if tmr % 30 == 0:
        set_enemy(random.randint(20,940),LINE_T,90,1,6)

def set_enemy(x, y, a, ty, sp): # 적 기체 설정
    global emy_no
    while True:
        if emy_f[emy_no] == False :
            emy_f[emy_no] = True
            emy_x[emy_no] = x
            emy_y[emy_no] = y
            emy_a[emy_no] = a
            emy_type[emy_no] = ty
            emy_speed[emy_no] = sp
            break
        emy_no = (emy_no+1) % ENEMY_MAX

def move_enemy(scrn):
    global ship_shield,idx,score,tmr
    for i in range(ENEMY_MAX):
        if emy_f[i] == True :
            ang = -90 - emy_a[i]
            png =  emy_type[i]
            emy_x[i] = emy_x[i] + emy_speed[i] * math.cos(math.radians(emy_a[i]))
            emy_y[i] = emy_y[i] + emy_speed[i] * math.sin(math.radians(emy_a[i]))
            if emy_type[i] == 1 and emy_y[i] > 360:
                set_enemy(emy_x[i], emy_y[i], 90, 0, 8)
                emy_a[i] = -10
                emy_speed[i] = 100

            if emy_x[i] < LINE_L or LINE_R < emy_x[i] or emy_y[i] < LINE_T or LINE_B < emy_y[i] :
                emy_f[i] = False

            if emy_type[i] != ENEMY_BULLET:
                w = img_enemy[emy_type[i]].get_width()
                h = img_enemy[emy_type[i]].get_height()
                r = int(w+h / 4) + 12
                for n in range(MISSILE_MAX):
                    if msl_f[n] == True and get_dis(emy_x[i],emy_y[i],msl_x[n],msl_y[n]) < r*r:
                        msl_f[n] = False
                        set_effect(emy_x[i],emy_y[i])
                        emy_f[i] = False
                        score += 100
                        se_explosion.play()
                        if ship_shield < 100:
                            ship_shield += 1
                    if msl_f2[n] == True and get_dis(emy_x[i],emy_y[i],msl_x2[n],msl_y2[n]) < r*r:
                        msl_f2[n] = False
                        set_effect(emy_x[i],emy_y[i])
                        emy_f[i] = False
                        score += 100
                        se_explosion.play()
                        if ship_shield < 100:
                            ship_shield += 1
                    if msl_f3[n] == True and get_dis(emy_x[i],emy_y[i],msl_x3[n],msl_y3[n]) < r*r:
                        msl_f3[n] = False
                        set_effect(emy_x[i],emy_y[i])
                        emy_f[i] = False
                        score += 100
                        se_explosion.play()
                        if ship_shield < 100:
                            ship_shield += 1
                    if msl_f4[n] == True and get_dis(emy_x[i],emy_y[i],msl_x4[n],msl_y4[n]) < r*r:
                        msl_f4[n] = False
                        set_effect(emy_x[i],emy_y[i])
                        emy_f[i] = False
                        score += 100
                        se_explosion.play()
                        if ship_shield < 100:
                            ship_shield += 1

            img_rz = pygame.transform.rotozoom(img_enemy[png], ang, 1.0)
            scrn.blit(img_rz, [emy_x[i] - img_rz.get_width() / 2, emy_y[i] - img_rz.get_height() /2] )

def set_effect(x,y):
    global eff_no
    eff_p[eff_no] = 1
    eff_x[eff_no] = x
    eff_y[eff_no] = y
    eff_no = (eff_no + 1) % EFFECT_MAX

def draw_effect(scrn):
    for i in range(EFFECT_MAX):
        if eff_p[i] > 0:
            scrn.blit(img_explode[eff_p[i]],[eff_x[i]-48,eff_y[i]-48])
            eff_p[i] += 1
            if eff_p[i] == 6:
                eff_p[i] = 0

def main():
    global bg_y,tmr,idx,score,ship_x,ship_y,ship_d,ship_shield,ship_muteki
    global se_barrage,se_damage,se_shot,se_explosion
    pygame.init()
    pygame.display.set_caption("galaxy game")
    screen = pygame.display.set_mode((960,720))
    clock = pygame.time.Clock()
    se_barrage = pygame.mixer.Sound("sound_gl/sound_gl_barrage.ogg")
    se_damage = pygame.mixer.Sound("sound_gl/sound_gl_damage.ogg")
    se_explosion = pygame.mixer.Sound("sound_gl/sound_gl_explosion.ogg")
    se_shot = pygame.mixer.Sound("sound_gl/sound_gl_shot.ogg")

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

        if idx == 0:
            img_rz = pygame.transform.rotozoom(img_title[0],-tmr % 360,1.0)
            screen.blit(img_rz,[480-img_rz.get_width()/2,280-img_rz.get_height()/2])
            screen.blit(img_title[1],[70,160])
            draw_text(screen,"Press [SPACE] to start",480,600,50,SILVER)
            if key[K_SPACE] == 1:
                idx = 1
                tmr = 0
                score = 0
                ship_x = 480
                ship_y = 600
                ship_d = 0
                ship_shield = 100
                ship_muteki = 0
                for i in range(ENEMY_MAX):
                    emy_f[i] = False
                for i in range(MISSILE_MAX):
                    msl_f[i] = False
                    msl_f2[i] = False
                    msl_f3[i] = False
                    msl_f4[i] = False
                pygame.mixer.music.load("sound_gl/sound_gl_bgm.ogg")
                pygame.mixer.music.play(-1)

        if idx == 1:
            move_starship(screen,key)
            move_missile(screen)
            move_missile2(screen)
            move_missile3(screen)
            move_missile4(screen)
            bring_enemy()
            move_enemy(screen)
            if tmr == 30 * 60:
                idx = 3
                tmr = 0

        if idx == 2:
            move_missile(screen)
            move_missile2(screen)
            move_missile3(screen)
            move_missile4(screen)
            if tmr == 1:
                pygame.mixer.music.stop()
            if tmr <= 90:
                if tmr % 5 == 0:
                    set_effect(ship_x + random.randint(-60,60),ship_y + random.randint(-60,60))
                if tmr % 10 == 0:
                    se_damage.play()
            if tmr == 120:
                pygame.mixer.music.load("sound_gl/sound_gl_gameover.ogg")
                pygame.mixer.music.play(0)

            if tmr > 120:
                draw_text(screen, "GAME OVER", 480, 300, 80, RED)

            if tmr == 400:
                idx = 0
                tmr = 0

        if idx == 3:
            move_starship(screen,key)
            move_missile(screen)
            move_missile2(screen)
            move_missile3(screen)
            move_missile4(screen)

            if tmr == 1:
                pygame.mixer.music.stop()
            if tmr == 2:
                pygame.mixer.music.load("sound_gl/sound_gl_gameclear.ogg")
                pygame.mixer.music.play(0)
            if tmr >= 20:
                draw_text(screen,"GAME OVER",480,300,80,SILVER)
            if tmr == 300:
                idx = 0
                tmr = 0

        draw_effect(screen)
        draw_text(screen,"SCORE"+str(score),200,30,50,SILVER)

        if idx != 0:
            screen.blit(img_shield,[40,680])
            pygame.draw.rect(screen,(64,32,32),[40+ship_shield * 4,680,(100 - ship_shield) * 4 ,12])

        pygame.display.update()
        clock.tick(20)

if __name__ == "__main__":
    main()