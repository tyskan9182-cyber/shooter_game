from pygame import *
from random import randint 
from time import time as timer
from time import sleep
window_size_one = 900
window_size_two = 700

game = True
finish = False

clock = time.Clock()

fps = 60

mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.1)
mixer.music.play()
#? 
fire = mixer.Sound('fire.ogg')
fire.set_volume(0.1)
font.init()
font1 = font.Font(None, 36)
font3 = font.Font(None, 100)
window = display.set_mode((window_size_one, window_size_two))
display.set_caption('SpaceGame')
background = transform.scale(image.load('galaxy.jpg') , (window_size_one, window_size_two))

score = 0
lost = 0
num_fire = 0
rel_time = False
healts = 3
bullets = sprite.Group()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, width, height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < window_size_one - 95:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx - 7, self.rect.top, 15, 25, 9)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= window_size_two:
            self.rect.y = 0
            self.rect.x = randint(0, window_size_one - 80)
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y == 0:
            bullet.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= window_size_two:
            self.rect.y = 0
            self.rect.x = randint(0, window_size_one - 80)

sprite_1 = Player('rocket.png', 0, window_size_two - 110, 90, 100, 7)
monsters = sprite.Group()
asterrss = sprite.Group()

for i in range(5):
    sprite_enemy = Enemy('ufo.png', randint(0, window_size_one - 80), 0, 100, 80, randint(1, 3))
    monsters.add(sprite_enemy)
for i in range(3):
    asterr = Asteroid('asteroid.png', randint(0, window_size_one - 80), 0, 90, 70, randint(1, 3))
    asterrss.add(asterr) 
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <= 6 and rel_time == False:
                    sprite_1.fire() 
                    fire.play()
                    num_fire += 1
                if num_fire >= 6 and rel_time == False:
                    start = timer()
                    rel_time = True             
    if finish != True:
        window.blit(background, (0,0))
        sprite_1.reset()
        sprite_1.update()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        asterrss.update()
        asterrss.draw(window)
        text_lose = font1.render('Пропущенно: ' + str(lost), 1, (255, 255, 255))
        text_win = font1.render('Cчёт: ' + str(score), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        window.blit(text_win, (10, 80))
        helt = font1.render('Счётчик HP: ', 1, (255, 255, 255))
        heltHP = font1.render(str(healts), 1, (255, 0, 0))
        window.blit(helt, (10, 130))
        window.blit(heltHP, (160, 130))
        if sprite.spritecollide(sprite_1, monsters, True):
            sprite_enemy = Enemy('ufo.png', randint(0, window_size_one - 80), 0, 100, 80, randint(1, 5))
            healts -= 1
        if sprite.spritecollide(sprite_1, asterrss, True):
            asterr = Asteroid('asteroid.png', randint(0, window_size_one - 80), 0, 90, 70, randint(1, 3))
            healts -= 1
        if score >= 13:
            text_winner = font3.render('YOU WIN', 1, (0, 255, 0))
            window.blit(text_winner, (250, 350))
            finish = True
        elif lost >= 5 or healts <= 0:
            text_looser = font3.render('YOU LOSE', 1, (255, 0, 0))
            window.blit(text_looser, (250, 350))
            finish = True 
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        asterrss_list = sprite.groupcollide(asterrss, bullets, True, True)
        for count in sprites_list:
            score += 1
            sprite_enemy = Enemy('ufo.png', randint(0, window_size_one - 80), 0, 100, 80, randint(1, 5))
            monsters.add(sprite_enemy)
        if rel_time == True:  
            end = timer()
            if end - start <= 1.5:
                reloadd = font1.render('Wait...reload...', 1, (255, 0, 0))
                window.blit(reloadd, (350, 550))
            else:
                num_fire = 0
                rel_time = False
        display.update()
    else:
        finish = False
        healts = 3
        score = 0
        lost = 0
        num_fire = 0
        rel_time = False
        for i in bullets:
            i.kill()
        for i in monsters:
            i.kill()
        for i in asterrss:
            i.kill()
        sleep(3)
        for i in range(5):
            sprite_enemy = Enemy('ufo.png', randint(0, window_size_one - 80), 0, 100, 80, randint(1, 3))
            monsters.add(sprite_enemy)
        for i in range(3):
            asterr = Asteroid('asteroid.png', randint(0, window_size_one - 80), 0, 90, 70, randint(1, 3))
            asterrss.add(asterr)
    clock.tick(fps)
    
