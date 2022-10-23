import pygame
from random import random
from gameplay.entity import Entity
from gameplay.sound import SoundSource
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, groups, collision_sprites, alpha_sprites, pos):
        super().__init__(groups)

        # movement
        # topleft because this pos comes from the 64 64 gridworld in tiled
        self.image = pygame.Surface((20, 20))
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()
        self.hitbox = self.rect
        self.hitbox.center = self.pos
        self.collision_sprites = collision_sprites
        self.alpha_sprites = alpha_sprites

        self.speed = 1

    def stomp(self):
        print('stomping')
        SoundSource(self.groups(), self.alpha_sprites,
                    self.pos, SOUNDBEAM_MAX_LOUDNESS)

    def input(self, actions):
        # Movement
        self.direction.x = actions['right'] - actions['left']
        self.direction.y = actions['down'] - actions['up']
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # Click
        if actions['space']:
            self.stomp()

    def move(self, dt):
        self.pos += self.direction * self.speed * dt * 60
        # print(self.pos)

        self.hitbox.centerx = round(self.pos.x)
        self.collision('horizontal')

        self.hitbox.centery = round(self.pos.y)
        self.collision('vertical')

        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.collision_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:    # moving right
                        self.pos.x = sprite.hitbox.left - self.hitbox.width / 2
                    elif self.direction.x < 0:    # moving left
                        self.pos.x = sprite.hitbox.right + self.hitbox.width / 2
                    self.hitbox.centerx = round(self.pos.x)
                    self.rect.centerx = round(self.pos.x)

        if direction == 'vertical':
            for sprite in self.collision_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:    # moving down
                        self.pos.y = sprite.hitbox.top - self.hitbox.height / 2
                    elif self.direction.y < 0:    # moving up
                        self.pos.y = sprite.hitbox.bottom + self.hitbox.height / 2
                    self.hitbox.centery = round(self.pos.y)
                    self.rect.centery = round(self.pos.y)

    def update(self, dt, actions):
        self.input(actions)
        self.move(dt)
