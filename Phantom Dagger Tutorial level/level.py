import pygame,sys
from tiles import Tile
from setings import tile_size
from player import Player
from movingTiles import movingTile
from rails import Rail
from drone import Drone
from lazer import Lazer
from exitDoor import Door
from bullet import Bullet
from healthBar import Bar

class Level:
    def __init__(self,level_data,surface):

        # level setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.setAI = 1
        self.droneCollision = False
        self.timer_event = pygame.USEREVENT + 1
        self.counter = 1000
        self.timer = 0
        self.deadDrone = False
        self.player_health = 100

    def setup_level(self,layout):

        #names of sprite Groupes
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.movingTiles = pygame.sprite.Group()
        self.rails = pygame.sprite.Group()
        self.drone = pygame.sprite.GroupSingle()
        self.lazer = pygame.sprite.Group()
        self.door = pygame.sprite.GroupSingle()
        self.bullet = pygame.sprite.Group()
        self.bar = pygame.sprite.GroupSingle()
        

        #create temp names for each Sprite then add
        #them to their respective Groups
        for row_index,row in enumerate(layout):
            for col_index,cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                
                if cell == 'X':
                    tile = Tile((x,y),tile_size)
                    self.tiles.add(tile)
                    
                if cell == 'P':
                    player_sprite = Player((x,y))
                    self.player.add(player_sprite)

                if cell == 'M':
                    mTile = movingTile((x,y),tile_size)
                    self.movingTiles.add(mTile)

                if cell == 'R':
                    rail = Rail((x,y),tile_size)
                    self.rails.add(rail)

                if cell == 'D':
                    drone_sprite = Drone(((x + 1),y))
                    self.drone.add(drone_sprite)

                if cell == 'E':
                    door_sprite = Door(((x+64),y),tile_size)
                    self.door.add(door_sprite)

        bar_sprite = Bar()
        self.bar.add(bar_sprite)

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        door = self.door.sprite

        #player colides with wall
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.direction.x = 0
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.direction.x = 0

        #player colides with magnetic block
        for sprite in self.movingTiles.sprites():
            sprite.rect.x += sprite.direction.x * sprite.speed
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.direction.x = 0
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.direction.x = 0

        #player collides with door
        if player.rect.colliderect(door.rect):
            if self.setAI == 1:
                print("You Win")
                pygame.time.delay(2000)
                pygame.quit()
                sys.exit()

            elif self.setAI == 2:
                if player.direction.x < 0:
                    player.rect.left = door.rect.right
                    player.direction.x = 0
                elif player.direction.x > 0:
                    player.rect.right = door.rect.left
                    player.direction.x = 0

        #magnetic block collides with wall
        for sprite in self.tiles.sprites():
            for mTiles in self.movingTiles.sprites():
                if sprite.rect.colliderect(mTiles.rect):
                    if mTiles.direction.x < 0:
                        mTiles.rect.left = sprite.rect.right
                        mTiles.direction.x = 0
                    elif mTiles.direction.x > 0:
                        mTiles.rect.right = sprite.rect.left
                        mTiles.direction.x = 0

        #magnetic block collides with magnetic block
        MTiles = self.movingTiles.sprites()                
        for i, mTile1 in enumerate(MTiles):
            for mTile2 in MTiles[i+1:]:
                if pygame.sprite.collide_mask(mTile1, mTile2):
                    if mTile1.direction.x < 0:
                        mTile1.rect.left = mTile2.rect.right
                        mTile1.direction.x += 1
                    if mTile1.direction.x > 0:
                        mTile1.rect.right = mTile2.rect.left
                        mTile1.direction.x -= 1
                #added a vice versa due to collisions only working one way.
                if pygame.sprite.collide_mask(mTile2, mTile1):
                    if mTile2.direction.x < 0:
                        mTile2.rect.left = mTile1.rect.right
                        mTile2.direction.x += 1
                    if mTile2.direction.x > 0:
                        mTile2.rect.right = mTile1.rect.left
                        mTile2.direction.x -= 1

        #magnetic block collides with Rail
        for sprite in self.rails.sprites():
            for mTiles in self.movingTiles.sprites():
                if sprite.rect.colliderect(mTiles.rect):
                    if mTiles.direction.x < 0:
                        mTiles.rect.left = sprite.rect.right
                        mTiles.direction.x = 0
                    elif mTiles.direction.x > 0:
                        mTiles.rect.right = sprite.rect.left
                        mTiles.direction.x = 0

        #drone laser collides with wall and magnetic blocks
        for sprite in self.tiles.sprites():
            for beam in self.lazer.sprites():
                if beam.rect.colliderect(sprite.rect):
                    self.lazer.remove(beam)

        for sprite in self.movingTiles.sprites():
            for beam in self.lazer.sprites():
                if beam.rect.colliderect(sprite.rect):
                    self.lazer.remove(beam)

        #drone bullet collides with wall and magnetic blocks
        for sprite in self.tiles.sprites():
            for bullet in self.bullet.sprites():
                if bullet.rect.colliderect(sprite.rect):
                    self.bullet.remove(bullet)

        for sprite in self.movingTiles.sprites():
            for bullet in self.bullet.sprites():
                if bullet.rect.colliderect(sprite.rect):
                    self.bullet.remove(bullet)

        #player collides with bullet
        for sprite in self.bullet.sprites():
            if sprite.rect.colliderect(player.rect):
                if self.player_health > 0:
                    self.player_health -= 10
                    self.bullet.remove(sprite)
                    

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        drone = self.drone.sprite
        drone.rect.y += drone.direction.y * drone.speed

        #player colides with wall
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0.1

        #player colides with magnetic block
        for sprite in self.movingTiles.sprites():
            sprite.rect.y += sprite.direction.y * sprite.speed
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0.1

        #Drone collides with wall
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(drone.rect):
                if self.setAI == 1:
                    drone.speed *= -1
                    drone.rect.y += 3 * drone.speed
                    
                elif self.setAI == 2:
                    self.droneColision = True
                    drone.speed = 1
##                    if drone.direction.y < 0:
##                        drone.direction.y = 0
##                    elif drone.direction.y > 0:
##                        drone.direction.y = 0
##                    print(drone.direction.y)
                    if drone.direction.y > 0:
                        drone.rect.bottom = sprite.rect.top
                        drone.direction.y = -0.1
                    elif drone.direction.y < 0:
                        drone.rect.top = sprite.rect.bottom
                        drone.direction.y = 0.1

        #player lands on top of drone
        if player.rect.colliderect(drone.rect):
            drone.speed = 0
            drone.rect.x = -100
            self.deadDrone = True               

        #magnetic block collides with wall
        for sprite in self.tiles.sprites():
            for mTiles in self.movingTiles.sprites():
                if sprite.rect.colliderect(mTiles.rect):
                    if mTiles.direction.y < 0:
                        mTiles.rect.top = sprite.rect.bottom
                        mTiles.direction.y = 0
                    elif mTiles.direction.y > 0:
                        mTiles.rect.bottom = sprite.rect.top
                        mTiles.direction.y = 0

        #magnetic block collides with magnetic block
        MTiles = self.movingTiles.sprites()                
        for i, mTile1 in enumerate(MTiles):
            for mTile2 in MTiles[i+1:]:
                if pygame.sprite.collide_mask(mTile1, mTile2):
                    if mTile1.direction.y < 0:
                        mTile1.rect.top = mTile2.rect.bottom
                        mTile1.direction.y += 1
                    if mTile1.direction.y > 0:
                        mTile1.rect.bottom = mTile2.rect.top
                        mTile1.direction.y -= 1
                #added a vice versa due to collisions only working one way.
                if pygame.sprite.collide_mask(mTile2, mTile1):
                    if mTile2.direction.y < 0:
                        mTile2.rect.top = mTile1.rect.bottom
                        mTile2.direction.y += 1
                    if mTile2.direction.y > 0:
                        mTile2.rect.bottom = mTile1.rect.top
                        mTile2.direction.y -= 1

        #magnetic block collides with rail
        for sprite in self.rails.sprites():
            for mTiles in self.movingTiles.sprites():
                if sprite.rect.colliderect(mTiles.rect):
                    if mTiles.direction.y < 0:
                        mTiles.rect.top = sprite.rect.bottom
                        mTiles.direction.y = 0
                    elif mTiles.direction.y > 0:
                        mTiles.rect.bottom = sprite.rect.top
                        mTiles.direction.y = 0

        #player collides with wall and moving tiles
        for wall in self.tiles.sprites():
            for mTiles in self.movingTiles.sprites():
                if wall.rect.colliderect(player.rect) and mTiles.rect.colliderect(player.rect):
                    mTiles.direction.y = 0

        #player collides with lazer
        for sprite in self.lazer.sprites():
            if sprite.rect.colliderect(player.rect):
                self.setAI = 2
                self.timer = 10000

    def awareTimer(self):
        if self.timer > 0:
            self.timer -= 10
        elif self.timer == 0:
            self.setAI = 1
##        
##        pygame.time.set_timer(self.timer_event, (timer * 1000))
##        for event in pygame.event.get():
##            if event.type == self.timer_event:
##                if self.counter > 0 :
##                    self.counter -=10
##                    print(self.counter)
##                elif self.counter <= 0:
##                    self.setAI = 1
##
##                
##            while self.seconds < timer:
##                self.seconds = (pygame.time.get_ticks() - self.timerStart)/1000
##                if self.seconds == 10:
##                    self.setAI = 1
##                    lazer.image.fill((100,0,0))
        
        

    def droneLaser(self):
        drone = self.drone.sprite
        if not self.deadDrone:
            laser_sprite = Lazer((drone.rect.x,(drone.rect.y + 16)))
            self.lazer.add(laser_sprite)
            if self.setAI == 2:
                for lazer in self.lazer.sprites():
                    lazer.image.fill('black')

    def droneShoot(self):
        drone = self.drone.sprite
        if not self.deadDrone:
            if self.setAI == 2:
                self.counter -= 10
                if self.counter <= 0:
                    self.counter = 1000
                    bullet_sprite = Bullet((drone.rect.x,(drone.rect.y + 16)))
                    self.bullet.add(bullet_sprite)

    def playerTracker(self):
        player = self.player.sprite
        drone = self.drone.sprite
##        if self.droneColision == False:
        self.playerTrackerY = player.rect.y
##        elif self.droneColision == True:
##            self.playerTrakerY = drone.rect.y
        

    def run(self):
        #level tiles
        if self.setAI == 1:
            self.rails.update(self.world_shift)
            self.rails.draw(self.display_surface)
            self.lazer.update(1)
            self.lazer.draw(self.display_surface)
        if self.setAI == 2:
            self.lazer.update(1)
            self.lazer.draw(self.display_surface)
            self.rails.update(self.world_shift)
            self.rails.draw(self.display_surface)

        self.bullet.update(1)
        self.bullet.draw(self.display_surface)

        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.movingTiles.update()
        self.movingTiles.draw(self.display_surface)
        self.awareTimer()
        self.door.update(self.setAI)
        self.door.draw(self.display_surface)
        
        
        #player
        self.player.update()
        self.vertical_movement_collision()
        self.horizontal_movement_collision()
        self.player.draw(self.display_surface)
        self.playerTracker()
        self.bar.update(self.player_health)
        self.bar.draw(self.display_surface)

        #enemies
        self.drone.update(self.setAI, self.playerTrackerY, self.droneCollision)
        self.drone.draw(self.display_surface)
        self.droneLaser()
        self.droneShoot()
        
