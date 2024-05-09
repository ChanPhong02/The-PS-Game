from asyncio import wait_for
from email.mime import image
from operator import index
from re import X
from turtle import back
import pygame
from .tiles import Tile
from .settings import *
from .player import * 

class Level:
    def __init__(self,level_data,surface,game,max_level):

        #tao level
        self.display_surface = surface
        self.world_shift = 0
        self.game = game
        self.game_active = True
        self.index_level = 0
        self.max_level = max_level
        self.text_font = pygame.font.Font('data/font/Pixeltype.ttf', 30)
        self.text_font2 = pygame.font.Font('data/font/Pixeltype.ttf', 70)
        self.setup_level(level_data)
        

    def setup_level(self,layout):
        self.background = pygame.image.load(f'data/graphics/background{self.index_level+1}.png')
        self.tiles = pygame.sprite.Group()
        self.goal = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for row_index,row, in enumerate(layout):
            for col_index,cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                row_above = layout[row_index-1]
                cell_above = row_above[col_index]
                if cell == 'X':
                    if cell == cell_above or row_index == 0:
                        tile = Tile((x,y),tile_size,1,self.index_level)
                        self.tiles.add(tile)
                    else:
                        tile = Tile((x,y),tile_size,2,self.index_level)
                        self.tiles.add(tile)
                if cell == 'G':
                    tile = Tile((x,y),tile_size,0,self.index_level)
                    self.goal.add(tile)
                if cell == 'P':
                    player_sprite = Player((x,y))
                    self.player.add(player_sprite)
   
    def scroll_x(self):
        player = self.player.sprite
        self.player_x = player.rect.centerx
        self.direction_x = player.direction.x

        if self.player_x < screen_width/4 and self.direction_x < 0:
            player.speed = 0
            self.world_shift = 3
        elif self.player_x > screen_width - (screen_width/4) and self.direction_x > 0:
            player.speed = 0
            self.world_shift = -3
        else:
            player.speed = 3
            self.world_shift = 0
            
    def check_gameover(self):
        keys = pygame.key.get_pressed()
        if self.player.sprite.rect.top > screen_height:
            self.background_gameover = pygame.image.load('data/graphics/background_gameover.png')
            self.background_gameover = pygame.transform.scale(self.background_gameover, (1280, 720))
            self.game_active = False
            self.display_surface.blit(self.background_gameover, (0,0))
            #self.text = self.text_font.render('Game over',False,'Red')
            #self.display_surface.blit(self.text,(500,200))
            self.text = self.text_font.render('Press <Enter> to try again',False,'White')
            self.display_surface.blit(self.text,(502,590))
            self.text = self.text_font.render('Press <ESC> to back to main menu',False,'White')
            self.display_surface.blit(self.text,(480,620))
            if keys[pygame.K_ESCAPE]:
                self.game.playing = False
                self.game_active = True
                self.index_level = 0
                self.setup_level(level_map[self.index_level])
            elif keys[pygame.K_RETURN]:
                self.setup_level(level_map[self.index_level])
                self.game_active = True

    def check_win(self):
        keys = pygame.key.get_pressed()
        if pygame.sprite.spritecollide(self.player.sprite,self.goal,False):
            background_gamewin1 = pygame.image.load('data/graphics/YouWin1.png')
            background_gamewin2 = pygame.image.load('data/graphics/YouWinAll.png')
            self.background_gamewin1 = pygame.transform.scale(background_gamewin1, (1280, 720))
            self.background_gamewin2 = pygame.transform.scale(background_gamewin2, (1280, 720))
            self.game_active = False
            if self.index_level == self.max_level:
                self.display_surface.blit(self.background_gamewin2, (0,0))
                self.text = self.text_font.render('You Win All Levels!!',False,'White')
                self.display_surface.blit(self.text,(550,660))
                self.text = self.text_font.render('Press <Enter> or <ESC> to back to main menu',False,'White')
                self.display_surface.blit(self.text,(450,690))
            else:
                #self.text = self.text_font.render('You Win !!',False,'Black')
                self.display_surface.blit(self.background_gamewin1, (0,0))
                self.text = self.text_font.render('Press <Enter> to next level',False,'White')
                self.display_surface.blit(self.text,(502,590))
                self.text = self.text_font.render('Press <ESC> to back to main menu',False,'White')
                self.display_surface.blit(self.text,(480,620))
            if keys[pygame.K_ESCAPE]:
                self.game.playing = False
                self.game_active = True
                self.index_level = 0
                self.setup_level(level_map[self.index_level])
            elif keys[pygame.K_RETURN]:
                if self.index_level == self.max_level:
                    self.index_level = 0
                    self.game.playing = False
                else:
                    self.index_level += 1 
                self.setup_level(level_map[self.index_level])
                self.game_active = True
    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0 or self.world_shift > 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0 or self.world_shift < 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player_stand = pygame.image.load('data/graphics/player_stand.png').convert_alpha()
        player = self.player.sprite
        if self.game_active:
            player.apply_gravity()
        else:
            player.direction.x = 0
            player.direction.y = 0

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.setIMG(player_stand)
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                elif player.direction.y < 0:
                        player.rect.top = sprite.rect.bottom
                        player.direction.y = 1
    def create_background(self):
        self.game.background = self.background
        self.game.background = pygame.transform.scale(self.game.background, (1280, 720))
        self.game.display.blit(self.game.background, (0,0))


    def run(self):
        #map
        self.tiles.draw(self.display_surface)
        self.goal.draw(self.display_surface)
        self.check_gameover()
        self.check_win()
        if self.game_active:
            #map
            self.tiles.update(self.world_shift)
            self.goal.update(self.world_shift)
            #background
            self.create_background()
            #player
            self.horizontal_movement_collision()
            self.vertical_movement_collision()
            self.scroll_x()            
            self.player.update()
            self.player.draw(self.display_surface)
            #level info
            self.text = self.text_font2.render(f'Level: {self.index_level + 1}',False,'White')  
            self.display_surface.blit(self.text,(screen_width-180,screen_height - 50))


