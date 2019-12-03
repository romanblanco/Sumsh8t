import math
import random

import pyglet
from pyglet import gl
from pyglet.window import key

window = pyglet.window.Window(width=800, height=400)

obrl = pyglet.image.load('playerShip1_red.png')
spaceship = pyglet.sprite.Sprite(obrl)
spaceship.anchor_x = spaceship.width // 2
spaceship.anchor_y = spaceship.height // 2
#nefunguje pak spravím

#obr2 = pyglet.image.load('laserBlue15.png')
#laser_good = pyglet.sprite.Sprite(obr2)

#obr3 = pyglet.image.load('meteorGrey_big4.png')
#meteor.anchor_x = meteor.width // 2
#meteor.anchor_y = meteor.height // 2

#meteory pak

ACCELERATION = 100
rotation_speed = 40


#spaceship_x_speed = 5
#spaceship_y_speed = 5

#nic už to jaksi funguje

stisknute_klavesy = set()



def pohyb_lod(dt):
    if 'w' in stisknute_klavesy:
        #spaceship_x_speed += dt * ACCELERATION * math.cos(spaceship.rotation)
        #spaceship_y_speed += dt * ACCELERATION * math.sin(spaceship.rotation)
        spaceship.x = spaceship.x + dt * ACCELERATION * math.cos(math.radians(90-spaceship.rotation))
        spaceship.y = spaceship.y + dt * ACCELERATION * math.sin(math.radians(90-spaceship.rotation))
    if 's' in stisknute_klavesy:
        #spaceship_x_speed -= dt * ACCELERATION * math.cos(spaceship.rotation)
        #spaceship_y_speed -= dt * ACCELERATION * math.sin(spaceship.rotation)
        spaceship.x = spaceship.x - dt * ACCELERATION * math.cos(math.radians(90-spaceship.rotation))
        spaceship.y = spaceship.y - dt * ACCELERATION * math.sin(math.radians(90-spaceship.rotation))
    if 'd' in stisknute_klavesy:
        spaceship.rotation = spaceship.rotation + dt * rotation_speed
    if 'a' in stisknute_klavesy:
        spaceship.rotation = spaceship.rotation - dt * rotation_speed

def stisk_klavesy(symbol,m):

    if symbol == key.W:
        stisknute_klavesy.add('w')
    if symbol == key.S:
        stisknute_klavesy.add('s')
    if symbol == key.A:
        stisknute_klavesy.add('a')
    if symbol == key.D:
        stisknute_klavesy.add('d')
    if symbol == key.G:
        stisknute_klavesy.add('g')


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
    spaceship.draw()


window.push_handlers(
    on_draw=vykresli,
    on_key_press=stisk_klavesy,
    on_key_release=pusteni_klavesy,
)
pyglet.clock.schedule(pohyb_lod)

pyglet.app.run()
