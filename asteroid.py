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

window = pyglet.window.Window(WIDTH, HEIGHT)


ACCELERATION = 150
LASER_ACCELERATION = 2000
METEORB_ACCELERATION = 20
METEORM_ACCELERATION = 40
METEORS_ACCELERATION = 60
METEORT_ACCELERATION = 80
rotation_speed = 100

batch = pyglet.graphics.Batch()

Metb1 = pyglet.image.load('meteorGrey_big4.png')
Metb1.anchor_x = Metb1.width // 2
Metb1.anchor_y = Metb1.height // 2

Metm1 = pyglet.image.load('meteorGrey_med1.png')
Metm1.anchor_x = Metm1.width // 2
Metm1.anchor_y = Metm1.height // 2

Metm2 = pyglet.image.load('meteorGrey_med2.png')
Metm2.anchor_x = Metm2.width // 2
Metm2.anchor_y = Metm2.height // 2

Mets1 = pyglet.image.load('meteorGrey_small1.png')
Mets1.anchor_x = Mets1.width // 2
Mets1.anchor_y = Mets1.height // 2

Mets2 = pyglet.image.load('meteorGrey_small2.png')
Mets2.anchor_x = Mets2.width // 2
Mets2.anchor_y = Mets2.height // 2

Mett1 = pyglet.image.load('meteorGrey_tiny1.png')
Mett1.anchor_x = Mett1.width // 2
Mett1.anchor_y = Mett1.height // 2

Mett2 = pyglet.image.load('meteorGrey_tiny2.png')
Mett2.anchor_x = Mett2.width // 2
Mett2.anchor_y = Mett2.height // 2

stisknute_klavesy = set()
meteory = set()
meteory_2 = set()
meteory_3 = set()
meteory_4 = set()
zivoty = set()
pozice = [20, HEIGHT-20]

class Meteor:

    def __init__(self,met):

        self.sprite = pyglet.sprite.Sprite(met, batch=batch)
        self.sprite.x = mimox
        self.sprite.y = mimoy


    def pohyb_meteoru(self,t):

        if len(meteory_2)==6:

            self.sprite.x = mimox
            self.sprite.y = mimoy

        if len(meteory_4)==6:

            meteory.discard(self)
            meteory_3.discard(self)
            meteory_2.clear()
            meteory_4.clear()

        if self not in meteory and self not in meteory_3:

            self.sprite.x = random.uniform(20, WIDTH-20)
            self.sprite.y = random.choice(pozice)
            self.sprite.rotation = random.uniform(0, 360)
            meteory.add(self)

        if self in meteory and self not in meteory_3:
            if self.sprite.x > WIDTH:
                self.sprite.x = 0
            elif self.sprite.y < 0 :
                self.sprite.y = HEIGHT
            elif self.sprite.x < 0:
                self.sprite.x = WIDTH
            elif self.sprite.y > HEIGHT :
                self.sprite.y = 0
            else:
                self.sprite.x = self.sprite.x + t * METEORM_ACCELERATION * math.cos(math.radians(self.sprite.rotation))
                self.sprite.y = self.sprite.y + t * METEORM_ACCELERATION * math.sin(math.radians(self.sprite.rotation))
        if abs(Player_laser.sprite.x - self.sprite.x) < 50 and abs(Player_laser.sprite.y - self.sprite.y) < 50:

            Player_laser.sprite.x = mimolx
            Player_laser.sprite.y = mimoly
            meteory_3.add(self)

        if abs(Player_ship.sprite.x - self.sprite.x) < 60 and abs(Player_ship.sprite.y - self.sprite.y) < 60:

            Player_ship.sprite.x = WIDTH//2
            Player_ship.sprite.y = HEIGHT//2
            zivoty.add(self)

            if len(zivoty) > 2:
                Player_ship.sprite.x = mimolx
                Player_ship.sprite.y = mimoly

            self.sprite.x = mimox
            self.sprite.y = mimoy

            meteory_3.add(self)

    def zbytek_meteoru(self,t,met):

        if met in meteory_3 and self not in meteory_2:

            self.sprite.x = met.sprite.x
            self.sprite.y = met.sprite.y
            self.sprite.rotation = random.uniform(0, 360)
            meteory_2.add(self)

        if self in meteory_2 and self not in meteory_4:
            if self.sprite.x > WIDTH:
                self.sprite.x = 0
            elif self.sprite.y < 0 :
                self.sprite.y = HEIGHT
            elif self.sprite.x < 0:
                self.sprite.x = WIDTH
            elif self.sprite.y > HEIGHT :
                self.sprite.y = 0
            else:
                self.sprite.x = self.sprite.x + t * METEORT_ACCELERATION * math.cos(math.radians(self.sprite.rotation))
                self.sprite.y = self.sprite.y + t * METEORT_ACCELERATION * math.sin(math.radians(self.sprite.rotation))

        if abs(Player_laser.sprite.x - self.sprite.x) < 30 and abs(Player_laser.sprite.y - self.sprite.y) < 30:

            Player_laser.sprite.x = mimolx
            Player_laser.sprite.y = mimoly

            self.sprite.x = mimox
            self.sprite.y = mimoy

            meteory_4.add(self)

        if abs(Player_ship.sprite.x - self.sprite.x) < 30 and abs(Player_ship.sprite.y - self.sprite.y) < 30:

            Player_ship.sprite.x = WIDTH//2
            Player_ship.sprite.y = HEIGHT//2
            zivoty.add(self)

            if len(zivoty) > 2:
                Player_ship.sprite.x = mimolx
                Player_ship.sprite.y = mimoly

            self.sprite.x = mimox
            self.sprite.y = mimoy

            meteory_4.add(self)

class Spaceship:

    def __init__(self):

        Ship = pyglet.image.load('playerShip1_red.png')
        Ship.anchor_x = Ship.width // 2
        Ship.anchor_y = Ship.height // 2
        self.sprite = pyglet.sprite.Sprite(Ship, batch=batch)
        self.sprite.x = WIDTH//2
        self.sprite.y = HEIGHT//2
        self.lives = zivoty

    def zivoty(self):
        self.lives = zivoty
    def pohyb_lodi(self,t):

        la = 1

        if 'w' in stisknute_klavesy:

            self.sprite.x = self.sprite.x + t * ACCELERATION * math.cos(math.radians(90-self.sprite.rotation))
            self.sprite.y = self.sprite.y + t * ACCELERATION * math.sin(math.radians(90-self.sprite.rotation))

        if 's' in stisknute_klavesy:

            self.sprite.x = self.sprite.x - t * ACCELERATION * math.cos(math.radians(90-self.sprite.rotation))
            self.sprite.y = self.sprite.y - t * ACCELERATION * math.sin(math.radians(90-self.sprite.rotation))

        if 'd' in stisknute_klavesy:

            self.sprite.rotation = self.sprite.rotation + t * rotation_speed

        if 'a' in stisknute_klavesy:

            self.sprite.rotation = self.sprite.rotation - t * rotation_speed

        if 'r' in stisknute_klavesy and 'l' not in stisknute_klavesy:


                Player_laser.sprite.x = self.sprite.x
                Player_laser.sprite.y = self.sprite.y
                Player_laser.sprite.rotation = self.sprite.rotation
                stisknute_klavesy.add('l')
                stisknute_klavesy.discard('r')

        if 'l' in stisknute_klavesy:

                rx = t * LASER_ACCELERATION * math.cos(math.radians(90-Player_laser.sprite.rotation))
                ry = t * LASER_ACCELERATION * math.sin(math.radians(90-Player_laser.sprite.rotation))

                if Player_laser.sprite.x > WIDTH or Player_laser.sprite.x < 0 or Player_laser.sprite.y > HEIGHT or Player_laser.sprite.y < 0:

                    Player_laser.sprite.x = mimox
                    Player_laser.sprite.y = mimoy
                    stisknute_klavesy.discard('l')

                else:

                    Player_laser.sprite.x = Player_laser.sprite.x + rx
                    Player_laser.sprite.y = Player_laser.sprite.y + ry

class Wazer:

    def __init__(self):

        Las = pyglet.image.load('laserBlue01.png')
        Las.anchor_x = Las.width // 2
        Las.anchor_y = Las.height // 2
        self.sprite = pyglet.sprite.Sprite(Las, batch=batch)
        self.sprite.x = mimolx
        self.sprite.y = mimoly


Player_ship = Spaceship()
Player_laser = Wazer()

metb1 = Meteor(Metb1)
metb1.sprite.x = mimox
metb1.sprite.y = mimoy
metm1 = Meteor(Metm1)

metm2 = Meteor(Metm2)
mets1 = Meteor(Mets1)
mets2 = Meteor(Mets2)
mett1 = Meteor(Mett1)
mett2 = Meteor(Mett2)

def cas(t):
    Player_ship.pohyb_lodi(t)
    metb1.pohyb_meteoru(t)
    metm1.zbytek_meteoru(t, metb1)
    metm2.zbytek_meteoru(t, metb1)
    mets1.zbytek_meteoru(t, metb1)
    mets2.zbytek_meteoru(t, metb1)
    mett1.zbytek_meteoru(t, metb1)
    mett2.zbytek_meteoru(t, metb1)

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
