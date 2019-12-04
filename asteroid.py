import math
import random

import pyglet
from pyglet import gl
from pyglet.window import key

WIDTH = 800
HEIGHT = 400

mimox = -90
mimoy = -90
rx = 0
xy = 0

window = pyglet.window.Window(WIDTH, HEIGHT)

ACCELERATION = 140
LASER_ACCELERATION = 800
rotation_speed = 60

batch = pyglet.graphics.Batch()

Met = pyglet.image.load('meteorGrey_big4.png')

stisknute_klavesy = set()

class Spaceship:

    def __init__(self):

        Ship = pyglet.image.load('playerShip1_red.png')
        Ship.anchor_x = Ship.width // 2
        Ship.anchor_y = Ship.height // 2
        self.sprite = pyglet.sprite.Sprite(Ship, batch=batch)

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

        if 'r' in stisknute_klavesy:


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

        Las = pyglet.image.load('laserBlue15.png')
        Las.anchor_x = Las.width // 2
        Las.anchor_y = Las.height // 2
        self.sprite = pyglet.sprite.Sprite(Las, batch=batch)
        self.sprite.x = mimox
        self.sprite.y = mimoy


Player_ship = Spaceship()
Player_laser = Wazer()

Player_ship.sprite.x = WIDTH//2
Player_ship.sprite.y = HEIGHT//2

def cas(t):
    Player_ship.pohyb_lodi(t)



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


pyglet.app.run()
