import pygame

class movingTile(pygame.sprite.Sprite):
    def __init__(self,pos,size):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill('orange')
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 4

        #detect mouse
        self.drag = False

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0
            
        if keys[pygame.K_DOWN]:
            self.direction.y = 1
        elif keys[pygame.K_UP]:
            self.direction.y = -1
        else:
            self.direction.y = 0

##        self.curs = pygame.mouse.get_pos()
##        if self.rect.collidepoint(self.curs):
##            #print("Mouse over")
##            for event in pygame.event.get():
##                if event.type == pygame.MOUSEBUTTONDOWN:
##                    if event.button == 1:
##                        self.drag = True
##                        
##                if event.type == pygame.MOUSEBUTTONUP:
##                    if event.button == 1:
##                        self.drag = False
##                        
##                if event.type == pygame.MOUSEMOTION:
##                    if self.drag:
##                        self.rect
        
        
    def update (self):
        self.get_input()
