import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.Surface((8,8))
        self.image.fill('white')
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, speed):
        self.rect.x += speed * 16
