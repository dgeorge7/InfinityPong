import pygame
class Button(pygame.sprite.Sprite):
    def __init__(self,  pos, image, altimg):
          pygame.sprite.Sprite.__init__(self) 
          self.images = [pygame.image.load(image), pygame.image.load(altimg)]
          self.image = self.images[0] 
          self.rect = self.image.get_rect()
          self.rect.x = pos[0]
          self.rect.y = pos[1]
