from re import S
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        player_walk1 = pygame.image.load('data/graphics/player_walk_1.png').convert_alpha()
        player_walk1_1 = pygame.transform.flip(player_walk1, True, False)
        player_walk2 = pygame.image.load('data/graphics/player_walk_2.png').convert_alpha()
        player_walk1_2 = pygame.transform.flip(player_walk2, True, False)
        self.player_jump = pygame.image.load('data/graphics/jump.png').convert_alpha()
        self.player_jump_back = pygame.transform.flip(self.player_jump, True, False)
        self.image_list = [self.player_jump, player_walk1, player_walk2, player_walk1_1, player_walk1_2]
        self.facing = 1
        self.image = self.player_jump
        self.rect = self.image.get_rect(topleft = pos)
 
        #player movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 3
        self.gravity = 0.8
        self.jump_speed = -16
        self.jump_sound = pygame.mixer.Sound('data/audio/jump.wav')

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.facing = 1

        elif keys[pygame.K_LEFT]  or keys[pygame.K_a]:
            self.direction.x = -1
            self.facing = -1

        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            self.jump()
        

    def jump(self):
        if self.direction.y == 0:
            self.direction.y = self.jump_speed
            self.jump_sound.play()
            if self.facing == 1:
                self.image = self.player_jump
            else:
                self.image = self.player_jump_back

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        if self.direction.y > 1.6:
            if self.facing == 1:
                self.image = self.player_jump
            else:
                self.image = self.player_jump_back


    def player_animation_right(self):
        if pygame.time.get_ticks() % 200 < 100:
            self.image = self.image_list[1]
        else:
            self.image = self.image_list[2]

    def player_animation_left(self):
        if pygame.time.get_ticks() % 200 < 100:
            self.image = self.image_list[3]
        else:
            self.image = self.image_list[4]

    def setIMG(self,a):
        if self.direction.x < 0:
           self.player_animation_left()
        elif self.direction.x > 0:
           self.player_animation_right()
        else:
           self.image = a

    def update(self):
        self.get_input()
        self.rect.x += self.direction.x * self.speed