import pygame

class Lazer(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.Surface((16,8))
        self.image.fill((100,0,0))
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, speed):
        self.rect.x += speed * 16
