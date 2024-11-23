#Create your own shooter
from random import randint
from pygame import *

win_width = 1200
win_height = 600
window = display.set_mode((win_width, win_height))
display.set_caption('Catch')
background = transform.scale(image.load('galaxy.jpg'),(win_width, win_height))

font.init()
font1 = font.SysFont("Arial", 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.SysFont("Arial", 36)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_UP] and self.rect.y > 0 :
            self.rect.y -= self.speed
        if key_pressed[K_DOWN] and self.rect.y < win_height - 75:
            self.rect.y += self.speed
        if key_pressed[K_RIGHT] and self.rect.x < win_width - 75:
            self.rect.x += self.speed
        if key_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 20 , 20, -15)
        bullets.add(bullet)

class Player2(GameSprite):
    def __init__(self, player_image, player_x, player_y,size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y,size_x, size_y, player_speed)
        self.life = 10
        self.score = 0
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_w] and self.rect.y > 0 :
            self.rect.y -= self.speed
        if key_pressed[K_s] and self.rect.y < win_height - 75:
            self.rect.y += self.speed
        if key_pressed[K_d] and self.rect.x < win_width - 75:
            self.rect.x += self.speed
        if key_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 20 , 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
            lost = lost + 1
    
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
        
    
lost = 0

player = Player('rocket.png', 600, 500, 80, 100, 7)
player2 = Player2('player2.png', 400, 500, 80, 100, 7)
bullets = sprite.Group()
monsters = sprite.Group()
for i in range(1, 4):
    monster = Enemy('ufo.png', randint(80, win_width - 80), -3, 80, 80, randint(1, 4))
    monsters.add(monster)
    
asteroids = sprite.Group()
for i in range(1, 4):
    asteroid = Asteroid('asteroid.png', randint(80, win_width - 80), -3, 80, 80, randint(1, 4))
    asteroids.add(asteroid)

clock = time.Clock()
FPS = 60
score = 0
life = 3
finish = False
game = True
while game:


    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
            if e.key == K_r:
                player2.fire()
    if finish == False:
        window.blit(background,(0, 0))
        text = font2.render('Score:' + str(score), 1, (255, 255, 255))
        window.blit(text, (win_width /2, 20))

        text_lose = font2.render('Missed:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (win_width /2, 50))

        text_life = font2.render('Life:' + str(life), 1, (255, 255, 255))
        window.blit(text_life, (win_width -120, 20))

        text_life2 = font2.render('Life:' + str(player2.life), 1, (255, 255, 255))
        window.blit(text_life2, (10, 20))
        player.update()
        player.reset()
        player2.update()
        player2.reset()
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        bullets.update()
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1,4))
            monsters.add(monster)

        if sprite.spritecollide(player, monsters, False):
            life = life - 1
            sprite.spritecollide(player, monsters, True)
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 4))
            monsters.add(monster)

        if sprite.spritecollide(player2, monsters, False):
            player2.life = player2.life - 1
            sprite.spritecollide(player2, monsters, True)
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 4))
            monsters.add(monster)

        if sprite.spritecollide(player, asteroids, False):
            life = life - 1
            sprite.spritecollide(player, asteroids, True)
            asteroid = Asteroid('asteroid.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 4))
            asteroids.add(asteroid)

        if sprite.spritecollide(player2, asteroids, False):
            player2.life = player2.life - 1
            sprite.spritecollide(player2, asteroids, True)
            asteroid = Asteroid('asteroid.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 4))
            asteroids.add(asteroid)    

    display.update()
    clock.tick(FPS)