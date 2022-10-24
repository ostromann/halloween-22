import pygame
import pymunk
from math import sin, cos, pi
from random import random

from settings import *


class Soundbeam(pygame.sprite.Sprite):
    def __init__(self, groups, collision_sprites, pos, direction, volume):
        super().__init__(groups)
        self.volume = volume
        self.pos = pygame.math.Vector2(pos)

        self.size_gain = 1
        self.speed = SOUNDBEAM_SPEED
        self.direction = direction

        self.rect = pygame.rect.Rect(
            pos.x - SOUNDBEAM_SIZE/2, pos.y - SOUNDBEAM_SIZE/2, SOUNDBEAM_SIZE, SOUNDBEAM_SIZE)
        self.orig_rect = self.rect.copy()

        self.surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        bright = int(self.volume / SOUNDBEAM_MAX_LOUDNESS * 255)
        # self.surf.fill((bright, bright, bright))
        # self.surf.set_alpha(bright)
        self.image = self.surf

        self.collision_sprites = collision_sprites

    def attenuate(self, dt):
        self.volume -= SOUNDBEAM_ATTENUATION * dt

    def propagate(self, dt):
        self.size_gain += SOUNDBEAM_SIZE_GAIN * dt
        self.rect = self.orig_rect.inflate(
            round(self.size_gain), round(self.size_gain))

    def dissolve(self):
        if self.size_gain >= 2:
            # spawn 4 new soundbeams, kill itself
            for i in range(2):
                for j in range(2):
                    x = self.rect.topleft[0] + self.rect.width / 2 * i
                    y = self.rect.topleft[1] + self.rect.height / 2 * i

                    pos = pygame.math.Vector2(x, y)
                    Soundbeam(self.groups(), self.collision_sprites,
                              pos, self.direction, self.volume)
            self.kill()

    def decay(self, dt):
        self.attenuate(dt)
        self.propagate(dt)
        # self.dissolve()

        if self.volume <= 0:
            self.kill()

    def move(self, dt):
        self.pos += self.direction * self.speed * dt * 60

        self.rect.centerx = round(self.pos.x)
        self.collision('horizontal')

        self.rect.centery = round(self.pos.y)
        self.collision('vertical')

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.collision_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:    # moving right
                        self.pos.x = sprite.rect.left - self.rect.width / 2
                        self.direction.x *= -1
                    elif self.direction.x < 0:    # moving left
                        self.pos.x = sprite.rect.right + self.rect.width / 2
                        self.direction.x *= -1
                    self.rect.centerx = round(self.pos.x)

        if direction == 'vertical':
            for sprite in self.collision_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:    # moving down
                        self.pos.y = sprite.rect.top - self.rect.height / 2
                        self.direction.y *= -1
                    elif self.direction.y < 0:    # moving up
                        self.pos.y = sprite.rect.bottom + self.rect.height / 2
                        self.direction.y *= -1
                    self.rect.centery = round(self.pos.y)

    def animate(self, dt):
        self.surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        bright = self.volume / SOUNDBEAM_MAX_LOUDNESS * 255
        self.surf.fill((bright, bright, bright, bright))
        # self.surf.set_alpha(bright)
        self.image = self.surf

    def update(self, dt, actions):
        self.animate(dt)
        self.decay(dt)
        self.move(dt)


class SoundSource():
    def __init__(self, groups, collision_sprites, pos, volume):
        # super().__init__(self, groups)
        self.groups = groups
        self.volume = volume
        self.pos = pygame.math.Vector2(pos)
        self.collision_sprites = collision_sprites
        self.emit_soundbeams()
        # play sound

    def emit_soundbeams(self):
        self.soundbeams = []
        for index in range(SOUNDBEAM_NUMBERS):
            phase_shift = index * 360 / SOUNDBEAM_NUMBERS * pi/180
            x = sin((pi * 2 + phase_shift))
            y = cos((pi * 2 + phase_shift))
            direction = pygame.math.Vector2(x, y)
            self.soundbeams.append(
                Soundbeam(self.groups, self.collision_sprites, self.pos, direction, self.volume))

    def get_soundbeams(self):
        return self.soundbeams
