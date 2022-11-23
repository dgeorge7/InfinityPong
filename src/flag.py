import pygame
class Flag(pygame.sprite.Sprite):
    def __init__(self,  sil, img, nsp = 0, inc = 0, sng = "None", name = "USA"):
        pygame.sprite.Sprite.__init__(self) 
        self.name = name
        self.images = [pygame.image.load(sil), pygame.image.load(img)]
        self.image = self.images[0] 
        self.rect = self.image.get_rect()
        self.nspeed = nsp
        self.incr = inc
        self.song = sng
    

