import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.Surface((32,32))
        self.image.fill('blue')
        self.rect = self.image.get_rect(topleft = pos)
        
        #player movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 4
        self.gravity = 0.4
        self.jump_height = 12
        self.jumping = False
        self.falling = False
        self.on_ground = True
        
    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        if keys[pygame.K_SPACE]:
            self.jump()
            

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        if self.direction.y > 0:
            self.falling = True
        else:
            self.falling = False
            
        if self.direction.y < 0:
            self.jumping = True
        else:
            self.jumping = False
            
        if self.jumping or self.falling:
            self.on_ground = False
        else:
            self.on_ground = True
            
        if self.direction.y >= 0 and self.on_ground:
            self.direction.y -= self.jump_height
            self.on_ground = False
            
            
            
    def update(self):
        self.get_input()
        self.apply_gravity()
