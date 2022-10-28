import os
import pygame

from gameplay.sound import SoundSource
from gameplay.utils import import_image_folder
from settings import *


class FootprintPlayer():
    def __init__(self):
        base_path = os.path.join('assets', 'graphics', 'footprints')
        pygame.mixer.init()
        self.frames = {
            # footsteps
            'player': import_image_folder(os.path.join(base_path, 'player')),
            'enemy': import_image_folder(os.path.join(base_path, 'enemy')),
        }
        print(self.frames)

    def create_footprint(self, groups, pos, direction, volume, left, origin):
        animation_frames = self.frames[origin]
        return Footprint(groups, pos, direction, volume,
                         left, origin, animation_frames)


class Footprint(pygame.sprite.Sprite):
    def __init__(self, groups, pos, direction, volume, left, origin, animation_frames):
        super().__init__(groups)
        self.volume = volume
        self.left = left

        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

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

        if not left:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center=self.pos)
        self.sound_source_pos = self.rect.center

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt * 60
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    # def decay(self, dt):
    #     if self.brightness >= 20:
    #         self.brightness -= FOOTSTEP_FADEOUT * dt
    #         print(self.brightness)
    #     self.image = self.image.convert_alpha()
    #     self.image.set_alpha(self.brightness)

    def update(self, dt, actions):
        self.animate(dt)
        # self.decay(dt)
