import pygame
import sys
import random
import math
from src import paddle
from src import button
from src import ball
from src import net
from src import flag
import json

class Controller:
    def __init__(self, width =1090, height=790):
        pygame.init()
        self.screen = pygame.display.set_mode((width,height)) 
        pygame.display.set_caption("Infinity Pong")
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
        self.icon = pygame.image.load('assets/paddle.png')
        pygame.display.set_icon(self.icon)
        self.gif = [pygame.image.load("assets/menu/f"+str(i)+".png").convert() for i in range(1,524)] 
        self.timage = self.gif[0]
        self.bgimage = pygame.image.load("assets/gamebg.png").convert()
        self.bgimage = pygame.transform.scale(self.bgimage, (width, height))
        self.limage =pygame.image.load("assets/losing.png").convert()
        self.limage = pygame.transform.scale(self.limage, (width, height))
        self.wimage =pygame.image.load("assets/winning.png").convert()
        self.wimage = pygame.transform.scale(self.wimage, (width, height+100))
        self.himage =pygame.image.load("assets/directions.png").convert()
        self.himage = pygame.transform.scale(self.himage, (width, height))
        self.simage =pygame.image.load("assets/levelselection.png").convert()
        self.simage = pygame.transform.scale(self.simage, (width, height))
        self.ping = pygame.mixer.Sound("assets/ping.wav")
        self.background = pygame.Surface(self.screen.get_size())
        self.background.blit(self.bgimage, (0, 3))
        self.width = width
        self.height = height
        self.levelList = []
        self.flags = pygame.sprite.Group()
        self.usa = flag.Flag("assets/flags/uflag.png", "assets/flags/sflag.png", "USA")
        self.usa.image = pygame.transform.scale(self.usa.image, (100, 50))
        self.usa.rect = self.usa.image.get_rect()
        self.hitCount = 0
        self.ballSpeed = 5
        self.bol = False
        self.opbol = False
        self.netbol = False
        self.wallbol = False
        self.helpbol = False
        self.aibol = True
        self.difficulty = 0
        self.maxDiff = 0
        self.play = button.Button((self.width/2.8, self.height/1.4),"assets/playbutton.png", "assets/playbutton0.png")
        self.help = button.Button((self.width/1.89, self.height/1.4),"assets/helpbutton.png", "assets/helpbutton0.png")
        self.net = net.Net(0, self.height/2, self.width)
        self.userPad = paddle.Paddle("User", "assets/player.png", (width/2, height))
        self.opPad = paddle.Paddle("Opp", "assets/cpu.png", (width/2, 0))
        self.ball = ball.Ball(530, 600)
        self.balls = pygame.sprite.GroupSingle(self.ball) 
        self.STATE = "INTRO"
    
    def mainloop(self):
        '''
        The state of the game is checked and the appropriate loop is run.
        args: (obj) Takes in the object itself.
        return: None
        '''
        while True:
            if(self.STATE == "INTRO"):
                self.intro()
            if(self.STATE == "GAME"):
                self.gameloop()
            if(self.STATE == "LOSE"):
                self.endloop()
            if(self.STATE == "WIN"):
                self.winloop()
            if(self.STATE == "SELECT"):
                self.select()
    
    def intro(self):
            '''
            The title screen is set up along with clickable buttons that change the game state.
            args: (obj) Takes in the object itself.
            return: None
            '''
            if not self.flags:
               pygame.mixer.music.load('assets/Infinity Pong Theme.mp3')
               pygame.mixer.music.play(-1)  
            else:
                self.flags.empty()
            count = 0
            while self.STATE == "INTRO":
                        self.mospos = pygame.mouse.get_pos()      
                        if self.help.rect.collidepoint(self.mospos):
                            self.help.image = self.help.images[1]
                        else:
                            self.help.image = self.help.images[0]
                        if self.play.rect.collidepoint(self.mospos):
                            self.play.image = self.play.images[1]
                        else:
                            self.play.image = self.play.images[0]
                        
                        for event in pygame.event.get():
                              if event.type == pygame.QUIT: 
                                pygame.quit()
                                sys.exit()
                              elif event.type == pygame.MOUSEBUTTONUP:
                                    self.mospos = pygame.mouse.get_pos()      
                                    if self.help.rect.collidepoint(self.mospos):
                                        self.screen.blit(self.himage, (0, 0))
                                        self.help.image = self.help.images[1]
                                        self.helpbol = True
                                    elif self.play.rect.collidepoint(self.mospos):
                                        self.play.image = self.play.images[1]
                                        self.STATE = "SELECT"
                              elif event.type == pygame.KEYDOWN:
                                     if(event.key == pygame.K_ESCAPE):
                                         self.helpbol = False
                        if count >= 0 and count <= len(self.gif)-1:
                           self.timage = self.gif[count]
                           self.timage = pygame.transform.scale(self.timage, (self.width, self.height+100))
                           count+=1
                        else:
                            self.timage = self.gif[0]
                            self.timage = pygame.transform.scale(self.timage, (self.width, self.height+100))
                            count = 1
                        if not self.helpbol:
                           self.screen.blit(self.timage, (0, 0))
                           self.screen.blit(self.play.image, (self.play.rect.x, self.play.rect.y))
                           self.screen.blit(self.help.image, (self.help.rect.x, self.help.rect.y))
                        pygame.display.flip()

    def  select(self):
            '''
            The level select screen is set up with clickable flags that change states from being locked to unlocked based on progress. The specific flag that is clicked determines the level. A JSON file is read to store attributes for each level in lists.
            args: (obj) Takes in the object itself.
            return: None
            '''
            if self.play.image == self.play.images[0] :
               pygame.mixer.music.load('assets/Infinity Pong Theme.mp3')
               pygame.mixer.music.play(-1)  
            self.play.image = self.play.images[0]
            self.netSpeeds = []
            self.gameSongs = []
            self.increments = []
            with open('src/levels.json', 'r') as levels:
                     self.levelList = json.load(levels)
                     for i in self.levelList:
                           self.flags.add(flag.Flag("assets/flags/sflag.png", i["flag"], i["netSpeed"], i["increment"], i["song"], i["country"]))
                     self.flagList = self.flags.sprites()
                     if self.difficulty > self.maxDiff:
                        self.maxDiff = self.difficulty
                     if self.maxDiff == 5:
                         for i in range(self.maxDiff):
                               self.flagList[i].image = self.flagList[i].images[1]
                     else:
                         for i in range(self.maxDiff+1):
                               self.flagList[i].image = self.flagList[i].images[1]

                     for i in self.flagList:
                           i.image = pygame.transform.scale(i.image, (300, 175))
                           i.rect = i.image.get_rect()
                     self.flagList[0].rect.x = 50
                     self.flagList[0].rect.y = 250
                     self.flagList[1].rect.x = 400
                     self.flagList[1].rect.y = 250
                     self.flagList[2].rect.x = 750
                     self.flagList[2].rect.y = 250
                     self.flagList[3].rect.x = 200
                     self.flagList[3].rect.y = 500
                     self.flagList[4].rect.x = 600
                     self.flagList[4].rect.y = 500

            while self.STATE == "SELECT":
                        for event in pygame.event.get():
                              if event.type == pygame.QUIT: 
                                pygame.quit()
                                sys.exit()
                              elif event.type == pygame.MOUSEBUTTONUP:
                                    self.mospos = pygame.mouse.get_pos()     
                                    if self.maxDiff == 5: 
                                       for i in range(self.maxDiff):
                                          if self.flagList[i].rect.collidepoint(self.mospos):
                                              self.flags.empty()
                                              self.STATE = "GAME"
                                              self.difficulty = i
                                    else:
                                        for i in range(self.maxDiff+1):
                                          if self.flagList[i].rect.collidepoint(self.mospos):
                                              self.flags.empty()
                                              self.STATE = "GAME"
                                              self.difficulty = i
                              elif event.type == pygame.KEYDOWN:
                                     if(event.key == pygame.K_ESCAPE):
                                         self.STATE = "INTRO"
                        self.screen.blit(self.simage, (0, 0))
                        self.flags.draw(self.screen)
                        pygame.display.flip()
                       
    
                       
    
    def gameloop(self):
        '''
        The gameplay screen is set up with paddles, a ball and a net. Ball collisions are continuously sensed, resulting in ball vectors. The points for each player is visible on top corners of the screen. Once either paddle object reaches 11 points, the game state changes and score attributes are reset.
        args: (obj) Takes in the object itself.
        return: None
        '''
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.flagList[self.difficulty].song)
        pygame.mixer.music.play(-1)  
        pygame.key.set_repeat(1,50) 
        while self.STATE == "GAME":
            self.mospos = pygame.mouse.get_pos()
            if self.mospos[1] > (self.height/2)+60 :
               self.userPad.rect.center = self.mospos
            if self.ball.rect.centery > self.height/2 and self.ball.rect.centery <= self.height/2+self.ballSpeed:
                self.aibol = True 
            if self.aibol:
               self.aibol = self.opPad.ai(1)
            self.opPad.rect.centerx = random.randrange(self.ball.rect.centerx-1,self.ball.rect.centerx+2)
         
            self.userPad.sync(self.width)
            self.opPad.sync(self.width)
            self.net.move(self.flagList[self.difficulty].nspeed) 
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                       self.STATE = "INTRO"
                       self.opbol = False
                       self.netbol = False
                       self.wallbol = False
                       self.bol = False
                       self.ball.rect.x = 530
                       self.ball.rect.y = 600
                       self.userPad.points = 0
                       self.opPad.points = 0
                       self.ballSpeed = 1
                       self.hitCount = 0

            self.hits = pygame.sprite.collide_mask(self.userPad, self.ball)
            if self.hits:
                self.opbol = False
                self.netbol = False
                self.wallbol = False
                self.hitpoint = self.userPad.rect.center
                self.ping.play(0, 350)
                self.vec = self.ball.vec(self.hitpoint,self.ballSpeed)
                self.bol = self.ball.bounce(self.vec)
                if self.ball.rect.centery < self.height/2 and self.ball.rect.centery >= self.height/2-self.ballSpeed:
                   self.hitCount += 1
                   if self.hitCount%5 == 0:
                      self.ballSpeed+= self.flagList[self.difficulty].incr
                      self.vec = self.ball.vec(self.hitpoint, self.ballSpeed)
            elif self.bol:
                self.bol = self.ball.bounce(self.vec)
                if self.ball.rect.centery < self.height/2 and self.ball.rect.centery >= self.height/2-self.ballSpeed: 
                   self.hitCount += 1
                   if self.hitCount%5 == 0:
                      self.ballSpeed+= self.flagList[self.difficulty].incr
                      self.vec = self.ball.vec(self.hitpoint, self.ballSpeed)
            
            self.opHits = pygame.sprite.collide_mask(self.opPad, self.ball)
            if self.opHits:
                self.bol = False
                self.netbol = False
                self.wallbol = False
                self.ping.play(0, 350)
                self.vec = self.ball.vec(self.opPad.rect.center,self.ballSpeed)
                self.opbol = self.ball.bounce(self.vec)
            elif self.opbol:
                self.opbol = self.ball.bounce(self.vec)
            
            self.netHits = pygame.sprite.spritecollide(self.net, self.balls, False) 
            if self.netHits:
                  if self.ball.rect.centery > self.net.rect.centery+10: 
                      self.opPad.points += 1
                  elif self.ball.rect.centery < self.net.rect.centery-10:
                      self.userPad.points += 1
                  self.bol = False
                  self.opbol = False
                  self.wallbol = False
                  self.ping.play(0, 350)
                  self.vec = self.ball.vec(self.net.rect.center,self.ballSpeed)
                  self.netbol = self.ball.bounce(self.vec)
            elif self.netbol:
                  self.netbol = self.ball.bounce(self.vec)
            
            while self.ball.rect.midright[0]>self.width:
                      self.ball.rect.centerx -= 1
             
            while self.ball.rect.midleft[0]<0:
                       self.ball.rect.centerx += 1
                  
            if self.ball.rect.midright[0] == self.width or self.ball.rect.midleft[0]== 0:
                self.opbol = False
                self.netbol = False
                self.bol = False
                self.ping.play(0, 350)
                self.vec.update(-self.vec.x, self.vec.y)
                self.wallbol = self.ball.bounce(self.vec)
                if self.vec.x > 0 and self.vec.y <0 or self.vec.x < 0 and self.vec.y <0:
                    if self.ball.rect.centery < self.height/2 and self.ball.rect.centery >= self.height/2-self.ballSpeed: 
                       self.hitCount += 1
                       if self.hitCount%5 == 0:
                          self.ballSpeed+= self.flagList[self.difficulty].incr
            elif self.wallbol:
                self.wallbol = self.ball.bounce(self.vec)
                if self.vec.x > 0 and self.vec.y <0 or self.vec.x < 0 and self.vec.y <0:
                    if self.ball.rect.centery < self.height/2 and self.ball.rect.centery >= self.height/2-self.ballSpeed: 
                       self.hitCount += 1
                       if self.hitCount%5 == 0:
                          self.ballSpeed+= self.flagList[self.difficulty].incr

            if self.ball.rect.y >= self.height:
                self.opPad.points += 1
                self.ball.rect.center = (self.width/2, self.opPad.rect.centery+100)
            elif self.ball.rect.y <= 0:
                self.userPad.points += 1
                self.ball.rect.center = (self.width/2, self.userPad.rect.centery -100)

            self.screen.blit(self.background, (0,0)) 
            self.screen.blit(self.ball.image, (self.ball.rect.x, self.ball.rect.y))
            self.screen.blit(self.net.image, (self.net.rect.x, self.net.rect.y) )
            self.screen.blit(self.userPad.image, (self.userPad.rect.x, self.userPad.rect.y))
            self.screen.blit(self.opPad.image, (self.opPad.rect.x, self.opPad.rect.y))
            self.screen.blit(self.usa.image, (30, 20))
            self.flagList[self.difficulty].image = pygame.transform.scale(self.flagList[self.difficulty].image, (100, 50))
            self.flagList[self.difficulty].rect = self.flagList[self.difficulty].image.get_rect()
            self.screen.blit(self.flagList[self.difficulty].image, (960,20))
    
            if  self.opPad.points == 11:
                self.STATE = "LOSE"
                self.opPad.points = 0
                self.userPad.points = 0
                self.ballSpeed = 1
                if self.difficulty == self.maxDiff :
                   self.difficulty = 0
                   self.maxDiff= 0
                self.hitCount = 0
                self.opbol = False
                self.netbol = False
                self.wallbol = False
                self.bol = False
                self.ball.rect.x = 530
                self.ball.rect.y = 600
            elif self.userPad.points == 11:
                if self.difficulty == self.maxDiff and self.difficulty < 4:
                   self.difficulty +=1 
                   self.STATE = "SELECT"
                elif self.difficulty == self.maxDiff and self.maxDiff == 4:
                   self.STATE = "WIN"
                   self.maxDiff = 5
                else:
                   self.STATE = "SELECT"
                self.userPad.points = 0
                self.opPad.points = 0
                self.ballSpeed = 1
                self.hitCount = 0
                self.opbol = False
                self.netbol = False
                self.wallbol = False
                self.bol = False
                self.ball.rect.x = 530
                self.ball.rect.y = 600
            myfont = pygame.font.SysFont(None, 90)
            self.score = myfont.render(str(self.userPad.points), False, (255,255,255))
            self.screen.blit(self.score, (150, 17))
            self.score = myfont.render(str(self.opPad.points), False, (255,255,255))
            if self.opPad.points >= 10:
               self.screen.blit(self.score, (880, 17))
            else:
               self.screen.blit(self.score, (903, 17))
            pygame.display.flip() 
            

    def endloop(self):
        '''
        The loss screen is set up.
        args: (obj) Takes in the object itself.
        return: None
        '''
        pygame.mixer.music.stop()
        pygame.mixer.music.load('assets/Infinity Pong Loss Theme.mp3')
        self.screen.blit(self.limage, (0, 0))
        pygame.display.flip()
        pygame.mixer.music.play()
        while self.STATE == "LOSE":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                       self.STATE = "INTRO"
     
    def winloop(self):
        '''
        The victory screen is set up. This state is only achieved when the last level is completed.
        args: (obj) Takes in the object itself.
        return: None
        '''
        pygame.mixer.music.stop()
        pygame.mixer.music.load('assets/Funky Metal.mp3')
        self.screen.blit(self.wimage, (0, 0))
        pygame.display.flip()
        pygame.mixer.music.play()
        while self.STATE == "WIN":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                       self.STATE = "INTRO"
