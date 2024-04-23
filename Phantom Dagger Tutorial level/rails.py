import pygame

class Rail(pygame.sprite.Sprite):
    def __init__(self,pos,size):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill((64,64,64))
        self.rect = self.image.get_rect(topleft = pos)
        
    def update (self,x_shift):
        self.rect.x += x_shift
