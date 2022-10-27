import pygame

from gameplay.sound import SoundSource
from settings import *


class Footstep(pygame.sprite.Sprite):
    def __init__(self, groups, pos, direction, volume, left, origin):
        super().__init__(groups)
        self.volume = volume
        self.left = left

        self.origin = origin
        if self.origin == 'player':
            offset_size = 5
        elif self.origin == 'enemy':
            offset_size = 10

        self.direction = pygame.math.Vector2(direction)
        self.angle = -self.direction.as_polar()[1] - 90
        self.offset = pygame.math.Vector2(self.direction.rotate(90))
        self.offset *= -offset_size if self.left else offset_size

        self.pos = pygame.math.Vector2(pos + self.offset)

        self.image = pygame.image.load(
            f'assets/graphics/footprint_{self.origin}.png').convert_alpha()
        self.brightness = 255

        if not left:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center=self.pos)
        self.sound_source_pos = self.rect.center

    def decay(self, dt):
        if self.brightness >= 20:
            self.brightness -= FOOTSTEP_FADEOUT * dt
            print(self.brightness)
        self.image = self.image.convert_alpha()
        self.image.set_alpha(self.brightness)

    def update(self, dt, actions):
        self.decay(dt)
