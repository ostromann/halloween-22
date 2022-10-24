import pygame
from random import random
from gameplay.entity import Entity
from gameplay.sound import SoundSource
from gameplay.footstep import Footstep
from gameplay.utils import *
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
        self.last_footstep = None

        # Timer
        self.stomping = False
        self.stomp_time = None
        self.stomp_cooldown = 300

    def stomp(self):
        print('stomping')
        SoundSource([self.alpha_sprites], self.collision_sprites,
                    self.pos, SOUNDBEAM_MAX_LOUDNESS)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.stomping:
            if current_time - self.stomp_time >= self.stomp_cooldown:
                self.stomping = False

    def input(self, actions):
        # Movement
        self.direction.x = actions['right'] - actions['left']
        self.direction.y = actions['down'] - actions['up']
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # Click
        if actions['space']:
            if not self.stomping:
                self.stomp()
                self.stomping = True
                self.stomp_time = pygame.time.get_ticks()

    def spawn_footprint(self):
        if not self.last_footstep:
            self.last_footstep = Footstep(
                [self.alpha_sprites], self.collision_sprites, self.pos, self.direction, volume=FOOTSTEP_VOLUME, left=True)
        else:
            self.last_footstep = Footstep([self.alpha_sprites], self.collision_sprites, self.pos,
                                          self.direction, volume=FOOTSTEP_VOLUME, left=not self.last_footstep.left)

    def move(self, dt):
        self.pos += self.direction * self.speed * dt * 60

        self.hitbox.centerx = round(self.pos.x)
        self.collision('horizontal')
        self.hitbox.centery = round(self.pos.y)
        self.collision('vertical')

        self.rect.center = self.hitbox.center

        if self.last_footstep:
            distance, _ = get_distance_direction_a_to_b(
                self.last_footstep.pos, self.pos)
            print(
                f'last footstep {self.last_footstep.pos} self {self.pos} distance {distance}')
            if distance >= FOOTSTEP_DISTANCE:
                self.spawn_footprint()
        else:
            self.spawn_footprint()

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
        self.cooldowns()
        self.input(actions)
        self.move(dt)
