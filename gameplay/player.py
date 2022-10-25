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
        self.image = pygame.Surface((18, 18))
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()
        self.hitbox = self.rect
        self.hitbox.center = self.pos
        self.collision_sprites = collision_sprites

        self.movement_stats = player_data['movement']
        self.status = 'idle'
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
        self.status = 'idle'
        self.direction.x = actions['right'] - actions['left']
        self.direction.y = actions['down'] - actions['up']
        if self.direction.magnitude() != 0:
            self.status = 'walk'
            self.direction = self.direction.normalize()

        if actions['LCTRL']:
            self.status = 'sneak'
        elif actions['LSHIFT']:
            self.status = 'run'

        if actions['space']:
            if not self.stomping:
                self.status = 'idle'
                self.stomp()
                self.stomping = True
                self.stomp_time = pygame.time.get_ticks()
        print(self.status)

    def move(self, dt):
        self.pos += self.direction * \
            self.movement_stats[self.status]['speed'] * dt * 60

        self.hitbox.centerx = round(self.pos.x)
        self.collision('horizontal')
        self.hitbox.centery = round(self.pos.y)
        self.collision('vertical')

        self.rect.center = self.hitbox.center

        self.distance_travelled += (self.direction *
                                    self.movement_stats[self.status]['speed'] * dt * 60).magnitude()

        if self.distance_travelled >= self.movement_stats[self.status]['footstep_distance']:
            pos_offset = self.direction * 5

            self.trigger_spawn_footprint(
                self.pos+pos_offset, self.direction, self.movement_stats[self.status]['footstep_volume'], self.left, 'player')
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
