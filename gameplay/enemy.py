import pygame

from gameplay.footstep import Footstep
from gameplay.utils import *
from settings import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, groups, collision_sprites, alpha_sprites, sound_sprites, pos, destination_points, player):

        # general setup
        super().__init__(groups)

        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.hitbox = self.rect
        self.hitbox.center = self.pos
        self.collision_sprites = collision_sprites
        self.alpha_sprites = alpha_sprites
        self.sound_sprites = sound_sprites

        # movement
        self.destination_points = destination_points
        self.destination_point_index = 0
        self.destination = self.pos
        self.direction = pygame.math.Vector2()
        self.speed = ENEMY_MOVEMENT_SPEED
        self.last_footstep = None

        # interaction
        self.noise_meter = {}
        self.noise_meter_threshold = SOUNDBEAM_MAX_LOUDNESS * 0.3
        self.notice_volume_decay = ENEMY_VOLUME_DECAY
        self.player = player

    def render(self):
        new_surf = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(new_surf, (255, 0, 0, 255), (10, 10), 10)
        # radius = self.notice_volume_meter / self.notice_volume_threshold * 10
        # if radius >= 9:
        #     radius = 9
        # pygame.draw.circle(new_surf, (0, 0, 0, 255), (10, 10), radius)
        self.image.blit(new_surf, (0, 0))

    def move_to_point(self, dt):
        # self.destination = self.destination_points[self.destination_point_index]
        _, direction = get_distance_direction_a_to_b(
            self.pos, self.destination)
        self.direction = direction

        self.move(dt)

    def move(self, dt):
        self.pos += self.direction * self.speed * dt * 60
        self.hitbox.centerx = round(self.pos.x)
        self.hitbox.centery = round(self.pos.y)
        self.rect.center = self.hitbox.center

        if self.last_footstep:
            distance, _ = get_distance_direction_a_to_b(
                self.last_footstep.pos, self.pos)
            if distance >= ENEMY_FOOTSTEP_DISTANCE:
                self.spawn_footprint()
        else:
            self.spawn_footprint()

    def spawn_footprint(self):
        if not self.last_footstep:
            self.last_footstep = Footstep(
                [self.alpha_sprites], self.collision_sprites, self.pos, self.direction, volume=ENEMY_FOOTSTEP_VOLUME, left=True, origin_type='enemy')
        else:
            self.last_footstep = Footstep([self.alpha_sprites], self.collision_sprites, self.pos,
                                          self.direction, volume=ENEMY_FOOTSTEP_VOLUME, left=not self.last_footstep.left, origin_type='enemy')

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

        if aggro:
            print(f"ROAR! I'm so angry at {key}.")
        else:
            print('Okay! I have calmed down!')

            # if self.notice_volume_meter >= self.notice_volume_threshold:
            #     # TODO: The largest contributor to the sound wave
            #     self.destination = self.player.pos
            #     self.notice_volume_meter = 0

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
        self.render()
        self.update_noise_meter()
        self.check_noise_meter()
        self.decay_noise_meter(dt)
        self.check_destination_reached()
        self.move_to_point(dt)
