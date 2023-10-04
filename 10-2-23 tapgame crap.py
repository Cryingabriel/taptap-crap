import pygame
from pygame.math import Vector2
import random
import math
import time
pygame.init()
pygame.display.set_caption("Spin Hunter")
screen = pygame.display.set_mode ((800, 800))
attackupgrade = "Attack Upgrade"




Bye = False
xpos = 0
ypos = 0
coins = 0
mousePos = (xpos, ypos)
playerPos = Vector2(380,390)
enemyPos = Vector2(random.randint(0,800),random.randint(0, 800))
playerDamage = 20
enemy = list()
xchoice = [0,800]
aenemies = 1000



#TICKS
time = pygame.time.Clock()
ticks = 0
#PLAYER --------------------------------------------------------------------------------
class Player:
    def __init__(self,xpos,ypos, damage):
        self.pos = Vector2(xpos,ypos)
        self.damage = damage
        self.angle = 0
        self.angle2 = 180
        self.sword = pygame.image.load("epic.png")
        self.sword2 = pygame.transform.smoothscale(self.sword,(30,120))
        self.sword4 = pygame.image.load("epic.png")
        self.sword5 = pygame.transform.smoothscale(self.sword4,(30,120))

    #draws the player/ swords in the middle
    def draw(self):
        
        sword3 = pygame.transform.rotate(self.sword2, self.angle)
        offset = Vector2(sword3.get_rect().topleft) - Vector2(sword3.get_rect().center)
        screen.blit(sword3, self.pos + offset)
        # test
        sword6 = pygame.transform.rotate(self.sword5, self.angle2)
        offset2 = Vector2(sword6.get_rect().topleft) - Vector2(sword6.get_rect().center)
        screen.blit(sword6, self.pos + offset2)
        
        self.angle2 += 70
        if self.angle2 >= 540:
            self.angle2 = 180
        #test
        self.angle += 70
        if self.angle >= 360:
            self.angle = 0

    #upgrades the damage when you press the button
    def upgrade(self):
        if mousePos[0] >= 0 and mousePos[0] <= 300 and mousePos[1] >= 650 and mousePos[1] <= 800:
            self.damage += 1
         
            
    #Update
    def update(self):
        return self.damage
         

player = Player(playerPos.x, playerPos.y, playerDamage)
#ENEMY ----------------------------------------------------------------------------------
class Enemy:
    
    #INIT -------------------------------
    def __init__(self, xpos, ypos, playerdamage):
        self.pos = Vector2(xpos, ypos)
        self.healthOPTIONS = [200,300,400,500,1000] # list of all of the health the enemies
        self.health = random.choice(self.healthOPTIONS) #going into the list of health and randomly assigning health to each enemy
        self.maxHealth = int(f"{self.health}")
        self.playerDamage = playerdamage
        self.speed = 1.02
        self.vel = (player.pos - self.pos).normalize()
        self.radius = 10
        self.dead = False
        self.coins = 0
        self.clicked = False

    #COINS ------------------------------
    def getcoins(self):
        if self.health <= 0:
            if self.dead == False:
                if self.maxHealth == self.healthOPTIONS[0]:
                    self.coins = 10
                elif self.maxHealth == self.healthOPTIONS[1]:
                    self.coins = 20
                elif self.maxHealth == self.healthOPTIONS[2]:
                    self.coins = 30
                elif self.maxHealth == self.healthOPTIONS[3]:
                    self.coins = 40
                elif self.maxHealth == self.healthOPTIONS[4]:
                    self.coins = 50
            else:
                self.coins = 0
            self.dead = True
        return self.coins
    
    #UPDATE -------------------------------
    def update(self,playerDam):
        self.playerDamage = playerDam
        self.pos += self.vel*self.speed
        if self.pos.x >= 320 and self.pos.x <= 440 and self.pos.y >= 330 and self.pos.y <= 450:
            self.health -= (self.playerDamage*10)/60
            if self.speed > 0.63:
                self.speed -= 0.03
        elif self.speed < 1.03:
            self.speed += 0.03
        #print(f"Health: {self.health}")
            
        if self.dead == True:
                self.pos.x = random.randint(0,800)
                self.pos.y = random.randint(0,800)
                self.vel = (player.pos - self.pos).normalize()
                self.health = random.choice(self.healthOPTIONS)
                self.maxHealth = int(f"{self.health}")
                self.dead = False

        
    def S(self):
        self.coins = 0
    #DRAW ---------------------------------
    def draw(self):
        #if self.health > 0:
            if self.maxHealth == self.healthOPTIONS[0]:
                pygame.draw.circle(screen, (0,244,0), (self.pos.x,self.pos.y), self.radius)

            elif self.maxHealth == self.healthOPTIONS[1]:
                pygame.draw.circle(screen, (0,0,244), (self.pos.x,self.pos.y), self.radius)

            elif self.maxHealth == self.healthOPTIONS[2]:
                pygame.draw.circle(screen, (244,244,0), (self.pos.x,self.pos.y), self.radius)
            
            elif self.maxHealth == self.healthOPTIONS[3]:
                pygame.draw.circle(screen, (211,0,244), (self.pos.x,self.pos.y), self.radius)

            elif self.maxHealth == self.healthOPTIONS[4]:
                pygame.draw.circle(screen, (244,0,0), (self.pos.x,self.pos.y), self.radius)



    #COLLIDE -----------------------------
    def collide(self):
        if math.sqrt((mousePos[0]-self.pos.x)**2 + (mousePos[1]-self.pos.y)**2)<self.radius:
            self.clicked = True
            if self.clicked == True:
                self.health -= self.playerDamage
                print(f"Health: {self.health}")
            
            else:
                self.clicked = False
            
        return self.health
    
class Background:
    #boom backround very cool
    def __init__(self):
        self.pos = Vector2(399,399)
        self.baseImage = pygame.image.load("bg4.jpg")
        self.scaled = pygame.transform.smoothscale(self.baseImage,(60,60))
        self.step1 = pygame.transform.scale2x(self.scaled)
        self.step2 = pygame.transform.scale2x(self.step1)
        self.step3 = pygame.transform.scale2x(self.step2)
        self.angle = 0

    #rotates very cool backround picture
    def draw(self):
        step4 = pygame.transform.scale(self.step3,(1000,1000))
        rotation = pygame.transform.rotate(step4, self.angle)
        offset = Vector2(rotation.get_rect().topleft) - Vector2(rotation.get_rect().center)
        screen.blit(rotation, self.pos + offset)

        self.angle += 0.5
        if self.angle >= 360:
            self.angle = 0

epicBG = Background()






for i in range(aenemies):
    enemy.append(Enemy(random.choice(xchoice), random.randint(0,800), playerDamage))


    
#Main loop ------------------------------------------------------------------------------------
while Bye == False:
    time.tick(60)
    #print(pygame.time.get_ticks())
    r = random.randrange(0,1)
    g = random.randrange(0,1)
    b = random.randrange(0,1)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Bye = True
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(enemy)):
                enemy[i].collide()
            player.upgrade()

            

        if event.type == pygame.MOUSEMOTION: #check if mouse moved
            mousePos = event.pos #refreshes mouse position
            
    
    
    #RENDER SECTION----------------------------------------------------------------------------
    screen.fill((r,g,b,100))
    time.get_fps()
    epicBG.draw()
    player.draw()

    #UPDATE SECTION-------------------------------------------------------------------------
    for i in range(len(enemy)):
        enemy[i].draw()
        enemy[i].update(player.update())
        
        coins += enemy[i].getcoins()
    for i in range(len(enemy)):
        enemy[i].S()
    #-------------------------------------------------------------------------------------------------  

    pygame.draw.rect(screen, (0,0,0), (100, 700, 150, 150))
    #this is the coins
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    text_label3 = my_font.render(str("Coins: "),1,(255,0,0))
    text_surface = my_font.render(str(coins), 1 ,(255, 0, 0))
    #click damage
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    text_surface2 = my_font.render(str(player.update()), 1 ,(255, 0, 0))
    text_label2 = my_font.render(str("Click Damage"),1,(255,0,0))
    #spin damage
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    text_surface3 = my_font.render(str(player.update()*10), 1 ,(255, 0, 0))
    text_label2 = my_font.render(str("Sword Damage"),1,(255,0,0))
    #attack upgrade
    my_font = pygame.font.SysFont('Comic Sans MS', 20)
    text_surface1 = my_font.render(str(attackupgrade), 1 ,(random.randrange(0,155), random.randrange(0,155),random.randrange(0,155)))
    
    screen.blit(text_surface1, (100,700))
    screen.blit(text_surface, (90,0))
    screen.blit(text_label3, (0,0))
    
    screen.blit(text_surface2,(700,0))
    screen.blit(text_surface3,(600,0))
    pygame.display.flip()

pygame.quit()