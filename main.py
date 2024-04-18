import pygame as p
import sys

width = 1200
hight = 800

class Player(p.sprite.Sprite):
    def __init__(self):
        p.sprite.Sprite.__init__(self)
        self.image = p.Surface((50,50))
        self.image.fill((75,124,153))
        self.rect = self.image.get_rect()
        self.rect.centerx = width/2
        self.rect.bottom = hight - 30
    
    def right(self):
        self.rect.x += 15
        if self.rect.left > width:
            self.rect.right = 0
    
    def left(self):
        self.rect.x -= 15
        if self.rect.right < 0:
            self.rect.left = width
    
    def down(self):
        self.rect.y += 15
        if self.rect.bottom > hight:
            self.rect.top = 0

    def up(self):
        self.rect.y -= 15
        if self.rect.top < 0:
            self.rect.bottom = hight
    
    def fire(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        All_Sprites.add(bullet)
        Bullets.add(bullet)


class Bullet(p.sprite.Sprite):
    def __init__(self, x, y):
        p.sprite.Sprite.__init__(self)
        self.image = p.Surface((10,10))
        self.image.fill((230,187,18))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
    def update(self):
        self.rect.y -= 10
        if self.rect.bottom < 0:
            self.kill()

p.init()
screen = p.display.set_mode((width, hight))
clock = p.time.Clock()
square = Player()
All_Sprites = p.sprite.Group()
All_Sprites.add(square)
Bullets = p.sprite.Group()

def control():
    for event in p.event.get():
        if event.type == p.QUIT:
            sys.exit()
    if p.key.get_pressed()[p.K_d]:
        square.right()
    elif p.key.get_pressed()[p.K_a]:
        square.left()
    elif p.key.get_pressed()[p.K_s]:
        square.down()
    elif p.key.get_pressed()[p.K_w]:
        square.up()
    elif p.key.get_pressed()[p.K_e]:
        square.fire()


def start():
    global screen, All_Sprites
    while True:
        clock.tick(30)
        control()
        screen.fill((0, 0, 0))
        All_Sprites.update()
        All_Sprites.draw(screen)
        p.display.flip()
start()
