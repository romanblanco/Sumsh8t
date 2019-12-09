import math
import random
import logging
import pprint

import pyglet
from pyglet import gl
from pyglet.window import key

log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)

#načtu knihovny

WIDTH = 800
HEIGHT = 600

MIMOX = -9000
MIMOY = -9000
MIMOLX = -10000
MIMOLY = -10000

#definuju pole

window = pyglet.window.Window(WIDTH, HEIGHT)

POCET_METEORU = 1

ACCELERATION = 150
LASER_ACCELERATION = 1000
EFFECT_ACCELERATION = 100
METEORB_ACCELERATION = 20
METEORM_ACCELERATION = 40
METEORS_ACCELERATION = 80
METEORT_ACCELERATION = 100
METEOR_ROTATION_SPEED = 20
ROTATION_SPEED = 100
#vlastnosti objektů

batch = pyglet.graphics.Batch()

stisknute_klavesy = set()

meteory_b = []; meteory_m = []; meteory_s = []; meteory_t = []
meteory_b2 = []; meteory_m2 = []; meteory_s2 = []; meteory_t2 = []
meteory_b3 = []; meteory_m3 = []; meteory_s3 = []; meteory_t3 = []
meteory_big = []; meteory_med = []; meteory_small = []; meteory_tiny = []

#definuju skupiny důležité pro meteory. Bez nich by se velký nerozdělil na 2 malé, kdyby to fungovalo..

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

#obrázky





pozice = [20, HEIGHT-20]
#pozice pro spawn velkého meteoru

class Object:

    def __init__(self, imgpng, acc, rot, ziv):

        vec = pyglet.image.load(imgpng)
        vec.anchor_x = vec.width // 2
        vec.anchor_y = vec.height // 2

        self.sprite = pyglet.sprite.Sprite(vec, batch=batch)
        self.sprite.x = MIMOX
        self.sprite.y = MIMOY
        self.sprite.acc = acc
        self.sprite.rot = rot
        self.sprite.ziv = ziv

        #nadefinuju všechny objekty, protože nevím jak je vykreslit postupně tak je všechny vytvořím hned a jen vykreslím tam, kde nejdou vidět, pozice MIMOX,y,


class Meteor(Object):

    def pohyb_meteoru(self, t, player, laser, skup, predskup, cilskup):

        Las2metx = abs(laser.sprite.x - self.sprite.x)
        Las2mety = abs(laser.sprite.y - self.sprite.y)
        Ship2metx = abs(player.sprite.x - self.sprite.x)
        Ship2mety = abs(player.sprite.y - self.sprite.y)

        #konstanty pro zásah nebo kolizi

        init_metheor_spawn = self.sprite.acc == METEORB_ACCELERATION and self not in skup and self not in cilskup
        meteor_hit = self.sprite.acc != METEORB_ACCELERATION and self not in skup and self not in cilskup and len(predskup) != 0
        rocket_hit = Ship2metx < 60 and Ship2mety < 60
        laser_hit = Las2metx < 50 and Las2mety < 50

        if init_metheor_spawn:
            log.error('spawn main: ------------------ ')
            self.sprite.x = random.uniform(20, WIDTH-20)
            self.sprite.y = random.choice(pozice)
            self.sprite.rotn = random.uniform(0, 360)
            skup.append(self)
            log.error('puvodni: %s', len(skup))
            log.error('ponicene: %s', len(predskup))
            log.error('znicene: %s', len(cilskup))

            #spawn velkého meteoru

        if meteor_hit:
            log.error('meteor hit: ------------------ ')
            met = predskup.pop()
            self.sprite.x = met.sprite.x
            self.sprite.y = met.sprite.y
            if len(predskup) == 0:
                met.sprite.x = MIMOX
                met.sprite.y = MIMOY
            self.sprite.rotn = random.uniform(0, 360)
            skup.append(self)
            log.error('puvodni: %s', len(skup))
            log.error('ponicene: %s', len(predskup))
            log.error('znicene: %s', len(cilskup))

            #spawn zbylých meteorů

        if self.sprite.x != MIMOX:
            if self.sprite.x > WIDTH:
                self.sprite.x = 0
            elif self.sprite.y < 0 :
                self.sprite.y = HEIGHT
            elif self.sprite.x < 0:
                self.sprite.x = WIDTH
            elif self.sprite.y > HEIGHT :
                self.sprite.y = 0
            else:
                self.sprite.x = self.sprite.x + t * self.sprite.acc * math.cos(math.radians(self.sprite.rotn))
                self.sprite.y = self.sprite.y + t * self.sprite.acc * math.sin(math.radians(self.sprite.rotn))
                self.sprite.rotation += t*self.sprite.rot

                #pohyb meteorů

        if laser_hit:
            log.error('laser shoot: ------------------ ')
            laser.sprite.x = MIMOLX
            laser.sprite.y = MIMOLY
            cilskup.append(self)
            cilskup.append(self)
            if self.sprite.acc == METEORT_ACCELERATION:
                self.sprite.x = MIMOX
                self.sprite.y = MIMOY
                if len(cilskup) == 16:
                    skup.clear()
                    cilskup.clear()
                    meteory_b3.clear()
                    meteory_m3.clear()
                    meteory_s3.clear()
            log.error('puvodni: %s', len(skup))
            log.error('ponicene: %s', len(predskup))
            log.error('znicene: %s', len(cilskup))

            #zásah laserem

        if rocket_hit:

            log.error('rocket hit: ------------------ ')
            player.sprite.x = WIDTH//2
            player.sprite.y = HEIGHT//2
            cilskup.append(self)
            cilskup.append(self)
            if self.sprite.acc == METEORT_ACCELERATION:
                self.sprite.x = MIMOX
                self.sprite.y = MIMOY
            player.sprite.ziv -= 1
            if player.sprite.ziv == 1:
                player.sprite.x = MIMOLX
                player.sprite.y = MIMOLY

                #kolize s hracem
            log.error('puvodni: %s', len(skup))
            log.error('ponicene: %s', len(predskup))
            log.error('znicene: %s', len(cilskup))

class Spaceship(Object):

    def pohyb_lodi(self, t, laser):

        if self.sprite.x != MIMOX:
            if self.sprite.x > WIDTH:
                self.sprite.x = 0
            elif self.sprite.y < 0 :
                self.sprite.y = HEIGHT
            elif self.sprite.x < 0:
                self.sprite.x = WIDTH
            elif self.sprite.y > HEIGHT :
                self.sprite.y = 0

        if 'w' in stisknute_klavesy:

            if self.sprite.acc < 250:
                self.sprite.acc += 10
            self.sprite.x = self.sprite.x + t * self.sprite.acc * math.cos(math.radians(90-self.sprite.rotation))
            self.sprite.y = self.sprite.y + t * self.sprite.acc * math.sin(math.radians(90-self.sprite.rotation))
            self.sprite.v = 'w'

        if 'w' not in stisknute_klavesy and 's' not in stisknute_klavesy:

            if self.sprite.acc != 0:
                self.sprite.acc -= 10
            if self.sprite.v == 'w':
                self.sprite.x = self.sprite.x + t * self.sprite.acc * math.cos(math.radians(90-self.sprite.rotation))
                self.sprite.y = self.sprite.y + t * self.sprite.acc * math.sin(math.radians(90-self.sprite.rotation))
            else:
                self.sprite.x = self.sprite.x - t * self.sprite.acc * math.cos(math.radians(90-self.sprite.rotation))
                self.sprite.y = self.sprite.y - t * self.sprite.acc * math.sin(math.radians(90-self.sprite.rotation))

        if 's' in stisknute_klavesy:

            if self.sprite.acc < 250:
                self.sprite.acc += 10
            self.sprite.x = self.sprite.x - t * self.sprite.acc * math.cos(math.radians(90-self.sprite.rotation))
            self.sprite.y = self.sprite.y - t * self.sprite.acc * math.sin(math.radians(90-self.sprite.rotation))
            self.sprite.v = 's'

        if 'd' in stisknute_klavesy:

            self.sprite.rotation = self.sprite.rotation + t * self.sprite.rot

        if 'a' in stisknute_klavesy:

            self.sprite.rotation = self.sprite.rotation - t * self.sprite.rot

            #ovládání lodi

        if 'r' in stisknute_klavesy and 'l' not in stisknute_klavesy:

            if self.sprite.canon == 1:
                laser.sprite.x = self.sprite.x - 30 * math.sin(math.radians(90-self.sprite.rotation))
                laser.sprite.y = self.sprite.y + 30 * math.cos(math.radians(90-self.sprite.rotation))
                self.sprite.canon = 2
            else:
                laser.sprite.x = self.sprite.x + 30 * math.sin(math.radians(90-self.sprite.rotation))
                laser.sprite.y = self.sprite.y - 30 * math.cos(math.radians(90-self.sprite.rotation))
                self.sprite.canon = 1
            laser.sprite.rotation = self.sprite.rotation
            for lef in effects['blast']:
                lef.sprite.rotation = self.sprite.rotation + random.uniform(-10, 10)
                lef.sprite.acc = random.uniform(200,600)
                lef.sprite.scale = random.uniform(0.2, 0.4)
                lef.sprite.x = laser.sprite.x
                lef.sprite.y = laser.sprite.y
                lef.sprite.ttl = 16
            stisknute_klavesy.add('l')
            stisknute_klavesy.discard('r')

        if 'l' in stisknute_klavesy:

            rx = t * LASER_ACCELERATION * math.cos(math.radians(90-player_laser.sprite.rotation))
            ry = t * LASER_ACCELERATION * math.sin(math.radians(90-player_laser.sprite.rotation))


            if laser.sprite.x > WIDTH or laser.sprite.x < 0 or laser.sprite.y > HEIGHT or laser.sprite.y < 0:

                laser.sprite.x = MIMOLX
                laser.sprite.y = MIMOLY
                stisknute_klavesy.discard('l')

            else:

                laser.sprite.x += rx
                laser.sprite.y += ry

        for lef in effects['blast']:

            if lef.sprite.x != MIMOLX:

                if lef.sprite.ttl == 0:
                    lef.sprite.x = MIMOLX
                    lef.sprite.y = MIMOLY
                else:
                    lef.sprite.ttl = lef.sprite.ttl - 1
                    lef.sprite.x += t * lef.sprite.acc * math.cos(math.radians(90-lef.sprite.rotation))
                    lef.sprite.y += t * lef.sprite.acc * math.sin(math.radians(90-lef.sprite.rotation))
                    lef.sprite.opacity -= 20

                #výstřel laseru a jeho zmizení když nic netrefí
class Wazer:

    def __init__(self):

        Las = pyglet.image.load('laserBlue01.png')
        Las.anchor_x = Las.width // 2
        Las.anchor_y = Las.height // 2
        self.sprite = pyglet.sprite.Sprite(Las, batch=batch)
        self.sprite.x = MIMOLX
        self.sprite.y = MIMOLY

class Effect:

    def __init__(self,img,cas):

        ef = pyglet.image.load(img)
        ef.height = ef.height // 2
        ef.anchor_x = ef.width // 2
        ef.anchor_y = ef.height
        self.sprite = pyglet.sprite.Sprite(ef, batch=batch)

        self.sprite.x = MIMOLX
        self.sprite.y = MIMOLY
        self.sprite.ttl = cas

player_ship = Spaceship('playerShip1_red.png', 0 , ROTATION_SPEED, 5)
player_ship.sprite.x = WIDTH//2
player_ship.sprite.y = HEIGHT//2
player_ship.sprite.canon = 0
player_ship.sprite.v = 'q'

player_laser = Wazer()

effects = {'blast': [
        Effect('laserBlue01.png', 30),
        Effect('laserBlue01.png', 30),
        Effect('laserBlue01.png', 30),
        Effect('laserBlue01.png', 30),
        Effect('laserBlue01.png', 30),
        Effect('laserBlue01.png', 30),
        Effect('laserBlue01.png', 30),
        Effect('laserBlue01.png', 30),
        Effect('laserBlue01.png', 30),
        Effect('laserBlue01.png', 30),

    ]



    }

meteors = {
  'big': [
      Meteor(random.choice(meteory_big), METEORB_ACCELERATION, METEOR_ROTATION_SPEED, 1),
  ],
  'medium': [
      Meteor(random.choice(meteory_med), METEORM_ACCELERATION, METEOR_ROTATION_SPEED, 1),
      Meteor(random.choice(meteory_med), METEORM_ACCELERATION, METEOR_ROTATION_SPEED, 1),
  ],
  'small': [
      Meteor(random.choice(meteory_small), METEORS_ACCELERATION, METEOR_ROTATION_SPEED, 1),
      Meteor(random.choice(meteory_small), METEORS_ACCELERATION, METEOR_ROTATION_SPEED, 1),
      Meteor(random.choice(meteory_small), METEORS_ACCELERATION, METEOR_ROTATION_SPEED, 1),
      Meteor(random.choice(meteory_small), METEORS_ACCELERATION, METEOR_ROTATION_SPEED, 1),
  ],
  'tiny': [
      Meteor(random.choice(meteory_tiny), METEORT_ACCELERATION, METEOR_ROTATION_SPEED, 1),
      Meteor(random.choice(meteory_tiny), METEORT_ACCELERATION, METEOR_ROTATION_SPEED, 1),
      Meteor(random.choice(meteory_tiny), METEORT_ACCELERATION, METEOR_ROTATION_SPEED, 1),
      Meteor(random.choice(meteory_tiny), METEORT_ACCELERATION, METEOR_ROTATION_SPEED, 1),
      Meteor(random.choice(meteory_tiny), METEORT_ACCELERATION, METEOR_ROTATION_SPEED, 1),
      Meteor(random.choice(meteory_tiny), METEORT_ACCELERATION, METEOR_ROTATION_SPEED, 1),
      Meteor(random.choice(meteory_tiny), METEORT_ACCELERATION, METEOR_ROTATION_SPEED, 1),
      Meteor(random.choice(meteory_tiny), METEORT_ACCELERATION, METEOR_ROTATION_SPEED, 1),
  ],
}

#vytvorím laser, meteory a lod

def cas(t):
    player_ship.pohyb_lodi(t, player_laser)
    for big_meteor in meteors['big']:
        big_meteor.pohyb_meteoru(t, player_ship, player_laser, meteory_b3, meteory_t2, meteory_b2)
    for medium_meteor in meteors['medium']:
        medium_meteor.pohyb_meteoru(t, player_ship, player_laser, meteory_m3, meteory_b2, meteory_m2)
    for small_meteor in meteors['small']:
        small_meteor.pohyb_meteoru(t, player_ship, player_laser, meteory_s3, meteory_m2, meteory_s2)
    for small_meteor in meteors['tiny']:
        small_meteor.pohyb_meteoru(t, player_ship, player_laser, meteory_t3, meteory_s2, meteory_t2)

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

    # funkce spojená s ovládáním lodi


def pusteni_klavesy(symbol,m):

    if symbol == key.W:
        stisknute_klavesy.discard('w')
    if symbol == key.S:
        stisknute_klavesy.discard('s')
    if symbol == key.A:
        stisknute_klavesy.discard('a')
    if symbol == key.D:
        stisknute_klavesy.discard('d')

    #viz předchozí koment

def vykresli():
    window.clear()
    batch.draw()


window.push_handlers(
    on_draw=vykresli,
    on_key_press=stisk_klavesy,
    on_key_release=pusteni_klavesy,
    )
pyglet.clock.schedule_interval(cas,1/30)

# no tak tu je ten zbytek

#

pyglet.app.run()
