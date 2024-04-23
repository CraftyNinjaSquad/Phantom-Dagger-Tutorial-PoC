import pygame,sys

class Bar(pygame.sprite.Sprite):
    def __init__ (self):
        super().__init__()
        self.image = pygame.Surface((100,16))
        self.image.fill('green')
        self.rect = self.image.get_rect(topleft = (10,10))

    def update(self,health):
        self.image = pygame.Surface((health,16))
        self.image.fill((0,128,0))
        if health <= 0:
            print("Game Over")
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit()
