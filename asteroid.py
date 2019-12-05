import math
import random

import pyglet
from pyglet import gl
from pyglet.window import key

WIDTH = 1300
HEIGHT = 600

mimox = -9000
mimoy = -9000
mimolx = -10000
mimoly = -10000

Met = 0

window = pyglet.window.Window(WIDTH, HEIGHT)

pocet_meteoru = 1

ACCELERATION = 150
LASER_ACCELERATION = 2000
METEORB_ACCELERATION = 20
METEORM_ACCELERATION = 40
METEORS_ACCELERATION = 60
METEORT_ACCELERATION = 80
ROTATION_SPEED = 100

batch = pyglet.graphics.Batch()


stisknute_klavesy = set()


meteory_b = []
meteory_m = []
meteory_s = []
meteory_t = []

meteory_b2 = []
meteory_m2 = []
meteory_s2 = []
meteory_t2 = []

meteory_b3 = []
meteory_m3 = []
meteory_s3 = []
meteory_t3 = []

meteory_big = []
meteory_med = []
meteory_small = []
meteory_tiny = []

meteory_big.append('meteorGrey_big1.png')
meteory_big.append('meteorGrey_big2.png')
meteory_big.append('meteorGrey_big3.png')
meteory_big.append('meteorGrey_big4.png')

meteory_med.append('meteorGrey_med1.png')
meteory_med.append('meteorGrey_med2.png')

meteory_small.append('meteorGrey_small1.png')
meteory_small.append('meteorGrey_small2.png')

meteory_tiny.append('meteorGrey_tiny1.png')
meteory_tiny.append('meteorGrey_tiny2.png')

pozice = [20, HEIGHT-20]

class Object:

    def __init__(self, vec, imgpng, acc, rot, ziv):

        vec = pyglet.image.load(imgpng)
        vec.anchor_x = vec.width // 2
        vec.anchor_y = vec.height // 2

        self.sprite = pyglet.sprite.Sprite(vec, batch=batch)
        self.sprite.x = mimox
        self.sprite.y = mimoy
        self.sprite.acc = acc
        self.sprite.rot = rot
        self.sprite.ziv = ziv


class Meteor(Object):

    def pohyb_meteoru(self, t, player, laser, skup, predskup, cilskup, met):

        if self.sprite.acc == METEORB_ACCELERATION and self not in skup and self not in cilskup:

            self.sprite.x = random.uniform(20, WIDTH-20)
            self.sprite.y = random.choice(pozice)
            self.sprite.rotation = random.uniform(0, 360)
            skup.append(self)

        if self.sprite.acc != METEORB_ACCELERATION and self not in skup and self not in cilskup and len(predskup) != 0:

            met = predskup.pop()
            self.sprite.x = met.sprite.x
            self.sprite.y = met.sprite.y
            if len(predskup) == 0:
                met.sprite.x = mimox
                met.sprite.y = mimoy
            self.sprite.rotation = random.uniform(0, 360)
            skup.append(self)

        if self.sprite.x != mimox:
            if self.sprite.x > WIDTH:
                self.sprite.x = 0
            elif self.sprite.y < 0 :
                self.sprite.y = HEIGHT
            elif self.sprite.x < 0:
                self.sprite.x = WIDTH
            elif self.sprite.y > HEIGHT :
                self.sprite.y = 0
            else:
                self.sprite.x = self.sprite.x + t * self.sprite.acc * math.cos(math.radians(self.sprite.rotation))
                self.sprite.y = self.sprite.y + t * self.sprite.acc * math.sin(math.radians(self.sprite.rotation))

        if abs(laser.sprite.x - self.sprite.x) < 50 and abs(laser.sprite.y - self.sprite.y) < 50:

            laser.sprite.x = mimolx
            laser.sprite.y = mimoly
            cilskup.append(self)
            cilskup.append(self)

        if abs(player.sprite.x - self.sprite.x) < 60 and abs(player.sprite.y - self.sprite.y) < 60:

            player.sprite.x = WIDTH//2
            player.sprite.y = HEIGHT//2
            cilskup.append(self)
            cilskup.append(self)
            player.sprite.ziv -= 1
            if player.sprite.ziv == 1:
                player.sprite.x = mimolx
                player.sprite.y = mimoly



class Spaceship(Object):

    def pohyb_lodi(self, t, laser):

        if 'w' in stisknute_klavesy:

            self.sprite.x = self.sprite.x + t * self.sprite.acc * math.cos(math.radians(90-self.sprite.rotation))
            self.sprite.y = self.sprite.y + t * self.sprite.acc * math.sin(math.radians(90-self.sprite.rotation))

        if 's' in stisknute_klavesy:

            self.sprite.x = self.sprite.x - t * self.sprite.acc * math.cos(math.radians(90-self.sprite.rotation))
            self.sprite.y = self.sprite.y - t * self.sprite.acc * math.sin(math.radians(90-self.sprite.rotation))

        if 'd' in stisknute_klavesy:

            self.sprite.rotation = self.sprite.rotation + t * self.sprite.rot

        if 'a' in stisknute_klavesy:

            self.sprite.rotation = self.sprite.rotation - t * self.sprite.rot

        if 'r' in stisknute_klavesy and 'l' not in stisknute_klavesy:

            laser.sprite.x = self.sprite.x
            laser.sprite.y = self.sprite.y
            laser.sprite.rotation = self.sprite.rotation
            stisknute_klavesy.add('l')
            stisknute_klavesy.discard('r')

        if 'l' in stisknute_klavesy:

            rx = t * LASER_ACCELERATION * math.cos(math.radians(90-Player_laser.sprite.rotation))
            ry = t * LASER_ACCELERATION * math.sin(math.radians(90-Player_laser.sprite.rotation))

            if laser.sprite.x > WIDTH or laser.sprite.x < 0 or laser.sprite.y > HEIGHT or laser.sprite.y < 0:

                laser.sprite.x = mimox
                laser.sprite.y = mimoy
                stisknute_klavesy.discard('l')

            else:

                laser.sprite.x = laser.sprite.x + rx
                laser.sprite.y = laser.sprite.y + ry

class Wazer:

    def __init__(self):

        Las = pyglet.image.load('laserBlue01.png')
        Las.anchor_x = Las.width // 2
        Las.anchor_y = Las.height // 2
        self.sprite = pyglet.sprite.Sprite(Las, batch=batch)
        self.sprite.x = mimolx
        self.sprite.y = mimoly

def meteory_skup(met, metb, metm, mets, mett):
    for a in range(pocet_meteoru):
        met = Meteor(Met, random.choice(meteory_big), METEORB_ACCELERATION, ROTATION_SPEED, 1)
        metb.append(met)
    for a in range(pocet_meteoru*2):
        met = Meteor(Met, random.choice(meteory_med), METEORM_ACCELERATION, ROTATION_SPEED, 1)
        metm.append(met)
    for a in range(pocet_meteoru*4):
        met = Meteor(Met, random.choice(meteory_small), METEORS_ACCELERATION, ROTATION_SPEED, 1)
        mets.append(meteory_sjmena[pocet_meteoru-1])
    for a in range(pocet_meteoru*8):
        met = Meteor(Met, random.choice(meteory_tiny), METEORT_ACCELERATION, ROTATION_SPEED, 1)
        mett.append(met)

meteory_skup(Met, meteory_b, meteory_m, meteory_s, meteory_t)

#self, vec, imgpng, acc, rot, ziv
Player_ship = Spaceship(Met, 'playerShip1_red.png', ACCELERATION, ROTATION_SPEED, 5)
Player_ship.sprite.x = WIDTH//2
Player_ship.sprite.y = HEIGHT//2
Player_laser = Wazer()

def cas(t):
    Player_ship.pohyb_lodi(t, Player_laser)
    #self, t, player, laser, skup, predskup, cilskup, met
    for e in range(pocet_meteoru):
        meteory_b[pocet_meteoru-1].pohyb_meteoru(t, Player_ship, Player_laser, meteory_b3, meteory_t2, meteory_b2, Met)
    for e in range(pocet_meteoru*2):
        meteory_m[pocet_meteoru-1].pohyb_meteoru(t, Player_ship, Player_laser, meteory_m3, meteory_b2, meteory_m2, Met)
    for e in range(pocet_meteoru*4):
        meteory_s[pocet_meteoru-1].pohyb_meteoru(t, Player_ship, Player_laser, meteory_s3, meteory_m2, meteory_s2, Met)
    for e in range(pocet_meteoru*8):
        meteory_t[pocet_meteoru-1].pohyb_meteoru(t, Player_ship, Player_laser, meteory_t3, meteory_s2, meteory_t2, Met)

def stisk_klavesy(symbol,m):

    if symbol == key.W:
        stisknute_klavesy.add('w')
    if symbol == key.S:
        stisknute_klavesy.add('s')
    if symbol == key.A:
        stisknute_klavesy.add('a')
    if symbol == key.D:
        stisknute_klavesy.add('d')
    if symbol == key.R:
        stisknute_klavesy.add('r')


def pusteni_klavesy(symbol,m):

    if symbol == key.W:
        stisknute_klavesy.discard('w')
    if symbol == key.S:
        stisknute_klavesy.discard('s')
    if symbol == key.A:
        stisknute_klavesy.discard('a')
    if symbol == key.D:
        stisknute_klavesy.discard('d')

def vykresli():
    window.clear()
    batch.draw()


window.push_handlers(
    on_draw=vykresli,
    on_key_press=stisk_klavesy,
    on_key_release=pusteni_klavesy,
)
pyglet.clock.schedule_interval(cas,1/30)

pyglet.app.run()
