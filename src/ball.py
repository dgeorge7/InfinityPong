import pygame
import math
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/ball.png')
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = pygame.math.Vector2(0, 0)
      
    def vec(self, pos, speed):
           '''
           A vector is created based on the position of the ball compared to the position of any object.
           args: (obj, tuple, int/float) Takes in the object itself, a tuple of coordinates, and an int/float representing speed.
           return (obj): Returns a vector object.
           '''
           if pos[1] < self.rect.centery and pos[0] > self.rect.centerx: 
                self.vel = pygame.math.Vector2(-speed*2, speed)
           elif pos[1] < self.rect.centery and pos[0] < self.rect.centerx: 
                  self.vel = pygame.math.Vector2(speed*2, speed)
           elif pos[1] > self.rect.centery and pos[0] < self.rect.centerx: 
                  self.vel = pygame.math.Vector2(speed*2, -speed)
           elif pos[1] > self.rect.centery and pos[0] > self.rect.centerx: 
                  self.vel = pygame.math.Vector2(-speed*2, -speed)
           elif pos[1] == self.rect.centery and pos[0] < self.rect.centerx: 
                  self.vel = pygame.math.Vector2(speed, 0)
           elif pos[1] == self.rect.centery and pos[0] < self.rect.centerx:  
                  self.vel = pygame.math.Vector2(-speed, 0)
           elif pos[1] < self.rect.centery and pos[0] == self.rect.centerx: 
                  self.vel = pygame.math.Vector2(0, speed)
           elif pos[1] > self.rect.centery and pos[0] == self.rect.centerx:
                  self.vel = pygame.math.Vector2(0, -speed)
           return self.vel
               
   
    def bounce(self, vel):
           '''
           The given vector is added to the ball's center coordinates.
           args: (obj) Takes in the object itself and a vector object as parameters.
           return (bool): Returns True
           '''
           self.rect.center +=  self.vel 
           return True   
           

       