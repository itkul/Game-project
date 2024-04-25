import pygame as p
import sys
from random import randrange

width = 1200
hight = 800
life = 3 

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

class Mob(p.sprite.Sprite):
    def __init__(self):
        p.sprite.Sprite.__init__(self)
        self.image = p.Surface((30, 30))
        self.image.fill((166, 27, 27))
        self.rect = self.image.get_rect()
        self.rect.x = randrange(width - self.rect.width)
        self.rect.y = randrange(-100, -30)
        self.speedx = randrange(-2, 3)
        self.speedy = randrange(3, 10)
        
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > hight or self.rect.right < 0:
            self.rect.x = randrange(width - self.rect.width)
            self.rect.y = randrange(-100, -30)
            self.speedy = randrange(1, 10)
            
class Bullet(p.sprite.Sprite):
    def __init__(self, x, y):
        p.sprite.Sprite.__init__(self)
        self.image = p.Surface((10, 10))
        self.image.fill((230, 187, 18))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
    def update(self):
        self.rect.y -= 10
        if self.rect.bottom < 0:
            self.kill()

def control():
    for event in p.event.get():
        if event.type == p.QUIT:
            sys.exit()

def motion():
    if p.key.get_pressed()[p.K_d]:
        square.right()
    elif p.key.get_pressed()[p.K_a]:
        square.left()
    elif p.key.get_pressed()[p.K_s]:
        square.down()
    elif p.key.get_pressed()[p.K_w]:
        square.up()
    pressed = p.mouse.get_pressed()
    if pressed[0]:
        square.fire()

def window():
    while True:
        control()
        screen.fill((0,0,0))
        label = p.font.SysFont('arial', 36)
        lose_label = label.render('Вы проиграли', True, (255, 255, 255))
        screen.blit(lose_label,(width/2.5, hight/2))
        p.display.flip()
        
def start():
    global screen, All_Sprites, life
    while True:
        clock.tick(30)
        control()
        motion()
        screen.fill((0, 0, 0))
        All_Sprites.update()
        hits = p.sprite.spritecollide(square, Mobs, False)
        if hits:
            life -= 1
            if life == 0:
                break
            else:
                square.rect.centerx = width/2
                square.rect.bottom = hight - 30
        kills = p.sprite.groupcollide(Mobs, Bullets, True, True)
        for mob in kills:
            mob = Mob()
            All_Sprites.add(mob)
            Mobs.add(mob)
        All_Sprites.draw(screen)
        p.display.flip()
    window()


p.init()
screen = p.display.set_mode((width, hight))
clock = p.time.Clock()
square = Player()
All_Sprites = p.sprite.Group()
All_Sprites.add(square)
Bullets = p.sprite.Group()
Mobs = p.sprite.Group()

for i in range(10):
    mob = Mob()
    All_Sprites.add(mob)
    Mobs.add(mob)
    
start()