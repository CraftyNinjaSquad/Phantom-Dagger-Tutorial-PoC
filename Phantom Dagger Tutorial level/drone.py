import pygame

class Drone(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.Surface((64,32))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = pygame.math.Vector2(0,0)
        self.timer_event = pygame.USEREVENT + 1
        self.speed = -1
        self.facing = 1
        self.counter = 1000

##    def laserSight(self):
##        self.lazer = pygame.sprite.Group()
##        self.lazer.add(Lazer(self.facing))
        
        

    def run_AI(self,x,y,col):
        self.setAI = x
        if self.setAI == 1:
            self.direction.y = 1
        if self.setAI == 2 and not col:
            self.speed = 1
            if self.speed < 0:
                if self.rect.y > y:
                    self.direction.y = 1
                elif self.rect.y < y:
                    self.direction.y = -1
                elif self.rect.y == y:
                    self.direction.y = 0
            elif self.speed > 0:
                if self.rect.y > y:
                    self.direction.y = -1
                elif self.rect.y < y:
                    self.direction.y = 1
                elif self.rect.y == y:
                    self.direction.y = 0
            elif self.speed == 0:
                if self.rect.y < y:
                    self.speed = 1
                elif self.rect.y > y :
                    self.speed  = -1

##    def awareTimer(self, timer):

##        self.timerStart = timer * 1000

##        while self.timerStart > 0:
##            self.timerStart -= 10
##            if self.timerStart == 0:
##                self.setAI = 1
        
##        pygame.time.set_timer(self.timer_event, self.timerStart)
##        for event in pygame.event.get():
##            if event.type == self.timer_event:
##                if self.counter > 0:
##                    self.counter -=10
##                elif self.counter <= 0:
##                    self.setAI = 1

                
##            while self.seconds < timer:
##                self.seconds = (pygame.time.get_ticks() - self.timerStart)/1000
##                if self.seconds == 10:
##                    self.setAI = 1
##                    lazer.image.fill((100,0,0))

    def update(self, ai, tracker, collision):
        self.run_AI(ai, tracker, collision)
##        if self.setAI == 2:
##            self.awareTimer(1)
        
