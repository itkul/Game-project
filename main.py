import pygame as p
import sys
from random import randrange
from os import path

width = 1200
hight = 800
life = 3
restart = False

img_dir = path.join(path.dirname(__file__), 'img')

class Player(p.sprite.Sprite):
    def __init__(self):
        p.sprite.Sprite.__init__(self)
        self.image = p.image.load(path.join(img_dir, 'КорабльGame.png')).convert()
        self.image = p.transform.scale(self.image, (100, 100))
        self.image.set_colorkey((0, 0, 0))
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
        self.image = p.image.load(path.join(img_dir, 'ВрагGame.png')).convert()
        self.image = p.transform.scale(self.image, (70, 70))
        self.image.set_colorkey((0, 0, 0))
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
        self.image = p.image.load(path.join(img_dir, 'ПуляGame.png')).convert()
        self.image = p.transform.scale(self.image, (20, 20))
        self.image.set_colorkey((0, 0, 0))
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
    if p.mouse.get_pressed()[0]:
        square.fire()

def lose_window():
    global restart
    while True:
        control()
        screen.fill((0,0,0))
        lose = p.font.SysFont('arial', 80)
        restart = p.font.SysFont('arial', 40)
        lose_label = lose.render('Вы проиграли', True, (255, 255, 255))
        restart_label = restart.render('Начать заново', True, (255, 255, 255))
        restart_label_rect = restart_label.get_rect(topleft = (507, 320))
        screen.blit(lose_label,(410, 180))
        screen.blit(restart_label, restart_label_rect)
        p.display.flip()
        if restart_label_rect.collidepoint(p.mouse.get_pos()) and p.mouse.get_pressed()[0]:
            restart = True
            break
    start()
        
def start():
    global screen, All_Sprites, life, restart
    if restart:
        life = 4
    while True:
        clock.tick(30)
        control()
        motion()
        screen.fill((0, 0, 0))
        background = p.image.load(path.join(img_dir, 'космосGame.jpg')).convert()
        background_rect = background.get_rect()
        screen.blit(background, background_rect)
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
    lose_window()

def hello_window():
    while True:
        control()
        screen.fill((0,0,0))
        hello = p.font.SysFont('arial', 80)
        first_start = p.font.SysFont('arial', 40)
        hello_label = hello.render('Добро пожаловать', True, (255, 255, 255))
        start_label = first_start.render('Начать игру', True, (255, 255, 255))
        start_label_rect = start_label.get_rect(topleft = (507, 320))
        screen.blit(hello_label,(330, 180))
        screen.blit(start_label, start_label_rect)
        p.display.flip()
        if start_label_rect.collidepoint(p.mouse.get_pos()) and p.mouse.get_pressed()[0]:
            break
    start()

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
    
hello_window()
