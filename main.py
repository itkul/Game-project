import pygame as p
import sys
from random import randrange
from os import path

img_dir = path.join(path.dirname(__file__), 'img')

class Game:
    def __init__(self):
        self.width = 1200
        self.hight = 800
        self.kill_counter = 0
        self.restart = False
        self.screen = p.display.set_mode((self.width, self.hight))
        self.life = 3
        self.clock = p.time.Clock()
        self.All_Sprites = p.sprite.Group()
        self.Bullets = p.sprite.Group()
        self.Mobs = p.sprite.Group()

    def lose_window(self):
        while True:
            self.control()
            background = p.image.load(path.join(img_dir, 'ПроигрышGame.jpg')).convert()
            background_rect = background.get_rect()
            self.screen.blit(background, background_rect)
            lose = p.font.SysFont('arial', 80)
            restart = p.font.SysFont('arial', 40)
            lose_label = lose.render('Вы проиграли', True, (255, 255, 255))
            restart_label = restart.render('Начать заново', True, (255, 255, 255))
            restart_label_rect = restart_label.get_rect(topleft = (507, 320))
            quet_label =restart.render('Выйти', True, (255, 0, 0))
            quet_label_rect = quet_label.get_rect(topleft = (550, 400))
            self.screen.blit(lose_label,(410, 180))
            self.screen.blit(restart_label, restart_label_rect)
            self.screen.blit(quet_label, quet_label_rect)
            p.display.flip()
            if restart_label_rect.collidepoint(p.mouse.get_pos()) and p.mouse.get_pressed()[0]:
                self.restart = True
                break
            elif quet_label_rect.collidepoint(p.mouse.get_pos()) and p.mouse.get_pressed()[0]:
                sys.exit()
        self.start()
        
    def start(self):
        if self.restart:
            self.life = 3
            self.kill_counter = 0
            for mob in self.Mobs:
                mob.restart()
            player.rect.centerx = self.width/2
            player.rect.bottom = self.hight - 30
        self.All_Sprites.add(player)
        while True:
            self.clock.tick(30)
            self.control()
            self.motion()
            background = p.image.load(path.join(img_dir, 'космосGame.jpg')).convert()
            background_rect = background.get_rect()
            self.screen.blit(background, background_rect)
            self.All_Sprites.update()
            hits = p.sprite.spritecollide(player, self.Mobs, False)
            if hits:
                self.life -= 1
                if self.life == 0:
                    break
                else:
                    player.rect.centerx = self.width/2
                    player.rect.bottom = self.hight - 30
            kills = p.sprite.groupcollide(self.Mobs, self.Bullets, True, True)
            for mob in kills:
                mob = Mob()
                self.All_Sprites.add(mob)
                self.Mobs.add(mob)
                self.kill_counter += 1

            self.lives(50, 5)
            self.count_mob()
            self.All_Sprites.draw(self.screen)
            p.display.flip()
        self.lose_window()

    def hello_window(self):
        while True:
            self.control()
            background = p.image.load(path.join(img_dir, 'ДобропожаловатьGame.jpg')).convert()
            background_rect = background.get_rect()
            self.screen.blit(background, background_rect)
            hello = p.font.SysFont('arial', 80)
            first_start = p.font.SysFont('arial', 40)
            hello_label = hello.render('Добро пожаловать', True, (255, 255, 255))
            start_label = first_start.render('Начать игру', True, (255, 255, 255))
            start_label_rect = start_label.get_rect(topleft = (507, 320))
            self.screen.blit(hello_label,(330, 180))
            self.screen.blit(start_label, start_label_rect)
            p.display.flip()
            if start_label_rect.collidepoint(p.mouse.get_pos()) and p.mouse.get_pressed()[0]:
                break
        self.start()
        
    def control(self):
        for event in p.event.get():
            if event.type == p.QUIT:
                sys.exit()

    def motion(self):
        if p.key.get_pressed()[p.K_d]:
            player.right()
        elif p.key.get_pressed()[p.K_a]:
            player.left()
        elif p.key.get_pressed()[p.K_s]:
            player.down()
        elif p.key.get_pressed()[p.K_w]:
            player.up()
        if p.mouse.get_pressed()[0]:
            player.fire()

    def lives(self, x, y):
        img = p.image.load(path.join(img_dir, 'ЖизниGame.png')).convert_alpha()
        for i in range(self.life):
            img_rect = img.get_rect()
            img_rect.x = x + 30 * i
            img_rect.y = y
            self.screen.blit(img, img_rect)

    def count_mob(self):
        img_counter = p.image.load(path.join(img_dir, 'ВрагGame.png')).convert_alpha()
        img_counter = p.transform.scale(img_counter, (70, 70))
        img_counter_rect = img_counter.get_rect()
        img_counter_rect.x = 50
        img_counter_rect.y = 70
        counter = p.font.SysFont('arial', 30)
        counter_label = counter.render(f': {self.kill_counter}', True, (255, 255, 255))
        self.screen.blit(img_counter, img_counter_rect)
        self.screen.blit(counter_label, (120, 90))

class Player(p.sprite.Sprite):
    def __init__(self):
        p.sprite.Sprite.__init__(self)
        self.image = p.image.load(path.join(img_dir, 'КорабльGame.png')).convert_alpha()
        self.image = p.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.centerx = game.width/2
        self.rect.bottom = game.hight - 30
        
    def right(self):
        self.rect.x += 15
        if self.rect.left > game.width:
            self.rect.right = 0
    
    def left(self):
        self.rect.x -= 15
        if self.rect.right < 0:
            self.rect.left = game.width
    
    def down(self):
        self.rect.y += 15
        if self.rect.bottom > game.hight:
            self.rect.top = 0

    def up(self):
        self.rect.y -= 15
        if self.rect.top < 0:
            self.rect.bottom = game.hight
    
    def fire(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        game.All_Sprites.add(bullet)
        game.Bullets.add(bullet)

class Mob(p.sprite.Sprite):
    def __init__(self):
        p.sprite.Sprite.__init__(self)
        self.image = p.image.load(path.join(img_dir, 'ВрагGame.png')).convert_alpha()
        self.image = p.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.x = randrange(game.width - self.rect.width)
        self.rect.y = randrange(-100, -30)
        self.speedx = randrange(-2, 3)
        self.speedy = randrange(3, 10)
        
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > game.hight or self.rect.right < 0:
            self.rect.x = randrange(game.width - self.rect.width)
            self.rect.y = randrange(-100, -30)
            self.speedy = randrange(1, 10)
    
    def restart(self):
        self.rect.x = randrange(game.width - self.rect.width)
        self.rect.y = randrange(-100, -30)
        self.speedy = randrange(1, 10)

class Bullet(p.sprite.Sprite):
    def __init__(self, x, y):
        p.sprite.Sprite.__init__(self)
        self.image = p.image.load(path.join(img_dir, 'ПуляGame.png')).convert_alpha()
        self.image = p.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        self.rect.y -= 10
        if self.rect.bottom < 0:
            self.kill()

p.init()
game = Game()
player = Player()

for i in range(10):
    mob = Mob()
    game.All_Sprites.add(mob)
    game.Mobs.add(mob)
    
game.hello_window()
