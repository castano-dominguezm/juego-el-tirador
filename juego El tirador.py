from pygame import *
from random import randint
from time import time as timer 

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.Font(None, 80)
win = font1.render('GANASTE!', True, (255, 255, 255))
lose = font1.render('PERDISTE!', True, (180, 0, 0))
font2 = font.Font(None, 36)

score = 0 
goal = 10
lost = 0
max_lost = 3
life = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
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
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Object(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = randint(80, win_width - 80)
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
display.set_caption("El tirador")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

ship = Player("rocket.png", 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()

for i in range(1, 6):
    monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()

for i in range (1, 4):
    asteriod = Object("asteroid.png", randint (30, win_width -30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteriod)

bullets = sprite.Group()

finish = False
run = True

rel_time = False
num_fire = 0

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and not rel_time:
                    num_fire += 1
                    ship.fire()
                    fire_sound.play()
                if num_fire >= 3 and not rel_time:
                    last_time = timer()
                    rel_time = True

    if not finish:
        window.blit(background,(0,0))

        text = font2.render("Puntaje:" + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Fallos: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        lives_text = font2.render("Vidas: " + str(life), 1, (255, 255, 255))
        window.blit(lives_text, (win_width - 120, 20))

        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        sprite.collide_rect(ship, monster )

        collides = sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, True) or sprite.spritecollide(ship, asteroids, True):
            life -= 1
            if life <= 0:
                finish = True
                window.blit(lose, (200, 200))

        if sprite.spritecollide(ship, asteroids, False):
            finish = True
            window.blit(lose, (200, 200))

        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload_text = font2.render("Espere un momento, recargando...", 1, (255, 0, 0))
                window.blit(reload_text, (250, 450))
            else:
                num_fire = 0
                rel_time = False

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        display.update()
        
    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        time.delay(3000)
        
time.delay(50)