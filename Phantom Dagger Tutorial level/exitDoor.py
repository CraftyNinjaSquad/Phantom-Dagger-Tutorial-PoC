import pygame

class Door(pygame.sprite.Sprite):
    def __init__(self,pos,size):
        super().__init__()
        self.image = pygame.Surface(((size/2),size))
        self.image.fill('green')
        self.rect = self.image.get_rect(topright = pos)

    def lock (self,ai):
        if ai == 1:
            self.image.fill('green')
        elif ai == 2:
            self.image.fill('red')
        
    def update (self,ai):
        self.lock(ai)
