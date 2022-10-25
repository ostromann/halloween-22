import pygame
from random import random
from gameplay.entity import Entity
from gameplay.sound import SoundSource
from gameplay.footstep import Footstep
from gameplay.utils import *
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, groups, collision_sprites, pos, trigger_spawn_footprint, trigger_spawn_soundsource):
        super().__init__(groups)

        # movement
        # topleft because this pos comes from the 64 64 gridworld in tiled
        self.image = pygame.Surface((25, 25))
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()
        self.hitbox = self.rect
        self.hitbox.center = self.pos
        self.collision_sprites = collision_sprites

        self.speed = 1
        self.distance_travelled = 0

        # Interaction functions
        self.left = True  # Player starts on left foot
        self.trigger_spawn_footprint = trigger_spawn_footprint
        self.trigger_spawn_soundsource = trigger_spawn_soundsource

        # Timer
        self.stomping = False
        self.stomp_time = None
        self.stomp_cooldown = 300

    def stomp(self):
        self.trigger_spawn_soundsource(
            self.pos, SOUNDBEAM_MAX_LOUDNESS, 'player')

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

    def move(self, dt):
        self.pos += self.direction * self.speed * dt * 60

        self.hitbox.centerx = round(self.pos.x)
        self.collision('horizontal')
        self.hitbox.centery = round(self.pos.y)
        self.collision('vertical')

        self.rect.center = self.hitbox.center

        self.distance_travelled += (self.direction *
                                    self.speed * dt * 60).magnitude()

        if self.distance_travelled >= FOOTSTEP_DISTANCE:
            self.trigger_spawn_footprint(
                self.pos, self.direction, FOOTSTEP_VOLUME, self.left, 'player')
            self.left = not self.left
            self.distance_travelled = 0

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
