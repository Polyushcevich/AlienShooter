#Створи власний Шутер!

from pygame import *
from random import randint
from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys =key.get_pressed()
        if keys[K_w] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_s] and self.rect.x < w - 85:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y +=self.speed
        global score
        if self.rect.y > h:
            self.rect.y = -50
            self.rect.x = randint(20, w-100)
            score = score + 1
        

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <0:
            self.kill()

w, h = 900, 637
mw = display.set_mode((w,h))
display.set_caption("Shooter")
background = transform.scale(image.load("background.png"), (w, h))

mixer.init()
mixer.music.load("sound.mp3")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")

font.init()
text1 = font.Font(None, 36)
text2 = font.Font(None, 80)

win= text2.render("YOU WIN!", True, (125,125,255),(0, 0, 0))
lose= text2.render("YOU LOSE!", True, (125,125,255),(0,0,0))

text_name = text2.render("Alien Shooter", True, (125,125,255),(0,0,0))
text_play = text2.render("Play(a)", True, (125,125,255),(0,0,0))
text_exit = text2.render("Exit(d)", True, (125,125,255),(0,0,0))



player = Player("player.png", 200, h-100, 80,100, 5)
monsters = sprite.Group()
bullets = sprite.Group()

score = 0
killed = 0
goal = 10
max_lost = 3

life = 3
rel_time = False
num_fire = 0

def respawn_enemy():
    monster = Enemy("enemy.png", randint(20, w-100), -50,80,50,randint(1,2))
    monsters.add(monster)

def menu():
    background_menu = transform.scale(image.load("menu.gif"), (w, h))
    mw.blit(background_menu, (0,0))
    menu = True
    while menu:
        for e in event.get():
            if  e.type == QUIT:
                menu = False
            if e.type ==KEYDOWN:
                if e.key == K_a:
                    menu = False
                    game()
                if e.key == K_d:
                    menu = False
        mw.blit(text_name, ((w/2)-170,70))
        mw.blit(text_play, ((w/2)-100,150))
        mw.blit(text_exit, ((w/2)-100,200))
        display.update()




def game():
    global score, killed, goal, max_lost, rel_time, num_fire, lifea


    for i in range(1,6):
        respawn_enemy()


    clock = time.Clock()
    finish = True

    game = True
    while game:
        for e in event.get():
            if  e.type == QUIT:
                game = False
            if e.type ==KEYDOWN:
                if e.key ==K_SPACE:
                    if num_fire <5 and rel_time== False:
                        num_fire +=1
                        player.fire()
                        fire_sound.play()
                    if num_fire >=5 and rel_time== False:
                        last_time = timer()
                        rel_time = True


        if not finish:
            mw.blit(background, (0, 0))
            player.update()
            bullets.update()
            player.reset()
            monsters.draw(mw)
            bullets.draw(mw)
            monsters.update()

            if rel_time:
                now_time = timer()
                if now_time - last_time <1:
                    reload = text1.render("Reloading...",1,(135,145,240), (255,255,255))
                    mw.blit(reload,(w//2-100, h-50))
                else:
                    num_fire=0
                    rel_time=False

            text_killed = text1.render("Score:" + str(killed), 1,(135,145,240), (255,255,255))
            mw.blit(text_killed, (20,20))

            text_lost = text1.render("Skip:"+str(score),1,(135,145,240),(255,255,255))
            mw.blit(text_lost, (20,50))

            if sprite.spritecollide(player, monsters, False) or score >= max_lost:
                mw.blit(lose, (300, 200))
                display.update()
                time.delay(3000)
                finish = True
                game = False
                menu()
                


            collides = sprite.groupcollide(monsters,bullets,True,True)
            for collide in collides:
                killed += 1
                print(killed)
                respawn_enemy()

            if killed >= goal:
                finish = True
                mw.blit(win, (300, 200))
                display.update()
                time.delay(3000)

            

            

        else:
            time.delay(3000)
            finish = False
            killed = 0
            score = 0
            for bullet in bullets:
                bullet.kill()
            for monster in monsters:
                monster.kill()
            for i in range(1,6):
                respawn_enemy()

        
        display.update()
        clock.tick(45)

menu()