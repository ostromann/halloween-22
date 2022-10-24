import pygame

from gameplay.footstep import Footstep
from gameplay.utils import *
from settings import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, groups, collision_sprites, alpha_sprites, sound_sprites, pos, destination_points, player):

        # general setup
        super().__init__(groups)

        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 0))
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
        self.notice_volume_meter = 0
        self.notice_volume_threshold = ENEMY_VOLUME_THRESHOLD
        self.notice_volume_decay = ENEMY_VOLUME_DECAY
        self.player = player

        # FSM setup
        # TODO: Later
        # self.fsm = EntityFSM(self)
        # self.fsm.states['spawn'] = SpawnState('spawn',MONSTER_SPAWN_DURATION,next_state='move')
        # self.fsm.states['move'] = MoveState('move', next_state='precharge')
        # self.fsm.states['precharge'] = SpawnState('spawn',self.stats['precharge_duration'],next_state='precharge')
        # self.fsm.states['charge'] = ChargeState('charge', next_state='move')
        # self.fsm.current_state = self.fsm.states['spawn']

    def move_to_point(self, dt):
        # self.destination = self.destination_points[self.destination_point_index]
        _, direction = get_distance_direction_a_to_b(
            self.pos, self.destination)
        self.direction = direction

        self.move(dt)

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
            if distance >= ENEMY_FOOTSTEP_DISTANCE:
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

    def spawn_footprint(self):
        if not self.last_footstep:
            self.last_footstep = Footstep(
                [self.alpha_sprites], self.collision_sprites, self.pos, self.direction, volume=ENEMY_FOOTSTEP_VOLUME, left=True, origin_type='enemy')
        else:
            self.last_footstep = Footstep([self.alpha_sprites], self.collision_sprites, self.pos,
                                          self.direction, volume=ENEMY_FOOTSTEP_VOLUME, left=not self.last_footstep.left, origin_type='enemy')

    def fill_notice_meter(self):
        for sprite in self.sound_sprites:
            if sprite.rect.colliderect(self.hitbox):
                if sprite.origin_type == 'player':
                    self.notice_volume_meter += sprite.volume
                    # TODO: identify the source from which the sound came.
        print(f'noise-meter: {self.notice_volume_meter}')

    def check_notice_meter(self):
        if self.notice_volume_meter >= self.notice_volume_threshold:
            # TODO: The largest contributor to the sound wave
            self.destination = self.player.pos
            self.notice_volume_meter = 0

    def decay_noise_meter(self, dt):
        if self.notice_volume_meter > 0:
            self.notice_volume_meter -= ENEMY_VOLUME_THRESHOLD * dt
        else:
            self.notice_volume_meter = 0

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
        self.fill_notice_meter()
        self.check_notice_meter()
        self.decay_noise_meter(dt)
        self.check_destination_reached()
        self.move_to_point(dt)
