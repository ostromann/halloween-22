import pygame
from settings import *


class Boundary(pygame.sprite.Sprite):
    def __init__(self, groups, pos, size, surface=None):
        # self.sprite_type = sprite_type
        super().__init__(groups)
        if surface == None:
            surface = pygame.Surface(size)
        self.image = surface

        self.rect = self.image.get_rect(topleft=(pos))
        self.hitbox = self.rect
        self.hitbox.topleft = pos
