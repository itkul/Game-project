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

p.init()
screen = p.display.set_mode((width, hight))
clock = p.time.Clock()
square = Player()
All_Sprites = p.sprite.Group()
All_Sprites.add(square)

def control():
    for event in p.event.get():
        if event.type == p.QUIT:
            sys.exit()
    if p.key.get_pressed()[p.K_d]:
        square.right()

def start():
    global screen, All_Sprites
    while True:
        clock.tick(30)
        control()
        screen.fill((0, 0, 0))
        All_Sprites.draw(screen)
        p.display.flip()
start()