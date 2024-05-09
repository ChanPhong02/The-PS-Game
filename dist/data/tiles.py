from platform import python_branch
import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,size,info,level_index):
        super().__init__()
        level_index == 0
        if info == 0:
            self.image = pygame.image.load('data/graphics/goal.png')
        if info == 1:
            self.image = pygame.image.load(f'data/graphics/dirt{level_index+1}.png')
        if info == 2:
            self.image = pygame.image.load(f'data/graphics/grass{level_index+1}.png')
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft = pos)

    def update(self,x_shift):
        self.rect.x += x_shift*2
