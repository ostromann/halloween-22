import pygame

from gameplay.footstep import Footstep
from gameplay.utils import *
from settings import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, groups, collision_sprites, sound_sprites, pos, destination_points, player, trigger_spawn_footprint, trigger_spawn_soundsource):

        # general setup
        super().__init__(groups)

        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.image.fill((255, 0, 0, 0))
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.hitbox = self.rect
        self.hitbox.center = self.pos
        self.collision_sprites = collision_sprites
        self.sound_sprites = sound_sprites

        # movement
        self.destination_points = destination_points
        self.destination_point_index = 0
        self.destination = self.pos
        self.direction = pygame.math.Vector2()
        self.speed = ENEMY_MOVEMENT_SPEED
        self.distance_travelled = 0

        # Interaction functions
        self.left = True  # Player starts on left foot
        self.trigger_spawn_footprint = trigger_spawn_footprint
        self.trigger_spawn_soundsource = trigger_spawn_soundsource

        # interaction
        self.noise_meter = {}
        self.noise_meter_threshold = SOUNDBEAM_MAX_LOUDNESS * 0.3
        self.notice_volume_decay = ENEMY_VOLUME_DECAY
        self.player = player

    def move_to_point(self, dt):
        _, direction = get_distance_direction_a_to_b(
            self.pos, self.destination)
        self.direction = direction

        self.move(dt)

    def move(self, dt):
        self.pos += self.direction * self.speed * dt * 60
        self.hitbox.centerx = round(self.pos.x)
        self.hitbox.centery = round(self.pos.y)
        self.rect.center = self.hitbox.center

        self.distance_travelled += (self.direction *
                                    self.speed * dt * 60).magnitude()

        if self.distance_travelled >= ENEMY_FOOTSTEP_DISTANCE:
            offset_pos = self.direction * 20
            self.trigger_spawn_footprint(
                self.pos+offset_pos, self.direction, ENEMY_FOOTSTEP_VOLUME, self.left, 'enemy')
            self.left = not self.left
            self.distance_travelled = 0

    def update_noise_meter(self):
        for sprite in self.sound_sprites:
            if sprite.rect.colliderect(self.hitbox):
                origin = sprite.origin_type
                if origin not in self.noise_meter.keys():
                    self.noise_meter[origin] = 0
                self.noise_meter[origin] = max(
                    [0, self.noise_meter[origin], sprite.volume])

                # TODO: identify the source from which the sound came.
        # print(f'noise-meter: {self.noise_meter}')

    def check_noise_meter(self):
        aggro = None
        for key, val in self.noise_meter.items():
            if val >= self.noise_meter_threshold:
                aggro = key

        # if aggro:
        #     print(f"ROAR! I'm so angry at {key}.")
        # else:
        #     print('Okay! I have calmed down!')

    def decay_noise_meter(self, dt):
        for key, val in self.noise_meter.items():
            self.noise_meter[key] = max(
                [0, val - ENEMY_VOLUME_DECAY * dt])

    def check_destination_reached(self):
        distance, _ = get_distance_direction_a_to_b(self.pos, self.destination)
        old_destination = self.destination

        if distance <= ENEMY_DESTINATION_RADIUS:
            self.destination_point_index += 1
            self.destination_point_index %= len(self.destination_points)
            self.destination = self.destination_points[self.destination_point_index]
            # print(
            #     f'destination {old_destination} reached by {distance}: next destination point {self.destination}')

    def update(self, dt, actions):
        self.update_noise_meter()
        self.check_noise_meter()
        self.decay_noise_meter(dt)
        self.check_destination_reached()
        self.move_to_point(dt)
