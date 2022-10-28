from math import sin
import pygame
from random import randint

from gameplay.footstep import Footprint
from gameplay.utils import *
from gameplay.entity_fsm import EntityFSM, State, TimedState
from settings import *


# idle, walking, curious, roar, AttackState

class EnemyState(State):
    def __init__(self, sprite):
        super().__init__(sprite)

    def check_noise_thresholds(self):
        sound_source = self.sprite.get_loudest_source()

        if sound_source:
            if sound_source['volume'] >= enemy_data['attack_noise_threshold']:
                return 'attack'
            if sound_source['volume'] >= enemy_data['curious_noise_threshold']:
                return 'curious'


class EnemyTimedState(TimedState):
    def __init__(self, sprite, duration):
        super().__init__(sprite, duration)

    def check_noise_thresholds(self):
        sound_source = self.sprite.get_loudest_source()
        if sound_source:
            if sound_source['volume'] >= enemy_data['attack_noise_threshold']:
                return 'attack'
            if sound_source['volume'] >= enemy_data['curious_noise_threshold']:
                return 'curious'
        return ''


class DefaultState(EnemyState):
    def update(self, dt, actions):
        self.sprite.entity_fsm.register('idle', IdleState(self.sprite, randint(
            *enemy_data['idle_duration_range'])))
        self.sprite.entity_fsm.push('idle')

    def wakeup(self):
        self.sprite.entity_fsm.register('idle', IdleState(self.sprite, randint(
            *enemy_data['idle_duration_range'])))
        self.sprite.entity_fsm.push('idle')


class IdleState(EnemyTimedState):
    def startup(self):
        if ENEMY_DEBUG:
            print(f'idle startup, duration: {self.duration}')
        self.start_time = pygame.time.get_ticks()
        self.sprite.target_pos = self.sprite.pos
        self.sprite.movement = enemy_data['movement']['walk']

        self.make_noise = not randint(0, 5)
        if self.make_noise:
            self.sprite.make_noise('enemy_low_call')

    def update(self, dt, actions):
        self.check_expiration()

        if self.check_noise_thresholds() == 'curious':
            self.sprite.entity_fsm.register(
                'curious', CuriousState(self.sprite))
            self.sprite.entity_fsm.switch('curious')
        elif self.check_noise_thresholds() == 'attack':
            self.sprite.entity_fsm.register('attack', AttackState(
                self.sprite, enemy_data['max_attack_time']))
            self.sprite.entity_fsm.switch('attack')

        if self.done:
            self.sprite.entity_fsm.register('walk', WalkState(self.sprite))
            self.sprite.entity_fsm.switch('walk')


class WalkState(EnemyState):
    def startup(self):
        self.sprite.target_pos = self.sprite.get_next_waypoint()
        self.sprite.movement = enemy_data['movement']['walk']
        if ENEMY_DEBUG:
            print(f'walk to {self.sprite.target_pos}')

    def cleanup(self):
        self.sprite.spawn_footprint()

    def update(self, dt, actions):
        self.check_done()

        if self.check_noise_thresholds() == 'curious':
            self.sprite.entity_fsm.register(
                'curious', CuriousState(self.sprite))
            self.sprite.entity_fsm.switch('curious')
        elif self.check_noise_thresholds() == 'attack':
            self.sprite.entity_fsm.register('attack', AttackState(
                self.sprite, enemy_data['max_attack_time']))
            self.sprite.entity_fsm.switch('attack')

        if self.done:
            self.done = False
            self.sprite.entity_fsm.register(
                'idle', IdleState(self.sprite, randint(
                    *enemy_data['idle_duration_range'])))
            self.sprite.entity_fsm.switch('idle')

    def check_done(self):
        distance, _ = get_distance_direction_a_to_b(
            self.sprite.pos, self.sprite.target_pos)

        if distance < enemy_data['waypoint_radius']:
            self.done = True


class CuriousRealizationState(EnemyTimedState):
    def startup(self):
        if ENEMY_DEBUG:
            print('realization startup')
        self.start_time = pygame.time.get_ticks()
        self.sprite.movement = enemy_data['movement']['idle']
        self.sprite.target_pos = self.sprite.pos

    def update(self, dt, actions):
        self.check_expiration()
        if ENEMY_DEBUG:
            print('What was that?!?!?!')
            print(self.time_remaining)

        if self.check_noise_thresholds() == 'attack':
            self.sprite.entity_fsm.register('attack', AttackState(
                self.sprite, enemy_data['max_attack_time']))
            self.sprite.entity_fsm.switch('attack')

        if self.done:
            # self.done = False
            self.sprite.entity_fsm.pop()  # Curious should be below it


class InspectState(EnemyTimedState):
    def startup(self):
        if ENEMY_DEBUG:
            print('Inspecting startup')
        self.start_time = pygame.time.get_ticks()
        self.sprite.movement = enemy_data['movement']['idle']
        self.sprite.target_pos = self.sprite.pos

    def update(self, dt, actions):
        self.check_expiration()
        if ENEMY_DEBUG:
            print('What is here?!?!?!')
            print(self.time_remaining)

        if self.check_noise_thresholds() == 'attack':
            self.sprite.entity_fsm.register('attack', AttackState(
                self.sprite, enemy_data['max_attack_time']))
            self.sprite.entity_fsm.switch('attack')

        if self.done:
            self.sprite.entity_fsm.pop_all()


class CuriousState(EnemyState):
    def startup(self):
        self.sprite.entity_fsm.register(
            'realization', CuriousRealizationState(self.sprite, 300))
        self.sprite.entity_fsm.push('realization')

    def suspend(self):
        sound_source = self.sprite.get_loudest_source()  # return dict of pos, and volume
        if ENEMY_DEBUG:
            print('Need a moment to realize that')

    def wakeup(self):
        if ENEMY_DEBUG:
            print(f'Now, I will walk to {self.sprite.target_pos}')
        sound_source = self.sprite.get_loudest_source()  # return dict of pos, and volume
        self.sprite.target_pos = sound_source['pos']
        self.sprite.movement = enemy_data['movement']['walk']

    def cleanup(self):
        # TODO:
        # self.sprite.trigger_sound('sniff')
        pass

    def update(self, dt, actions):
        self.check_done()

        if self.check_noise_thresholds() == 'attack':
            self.sprite.entity_fsm.register('attack', AttackState(
                self.sprite, enemy_data['max_attack_time']))
            self.sprite.entity_fsm.switch('attack')

        if self.done:
            self.sprite.entity_fsm.register('inspect', InspectState(
                self.sprite, enemy_data['inspect_duration']))
            self.sprite.entity_fsm.push('inspect')

    def check_done(self):
        distance, _ = get_distance_direction_a_to_b(
            self.sprite.pos, self.sprite.target_pos)

        if distance < enemy_data['waypoint_radius']:
            self.done = True


class RoarState(EnemyTimedState):
    def startup(self):
        if ENEMY_DEBUG:
            print('roar startup')
        self.start_time = pygame.time.get_ticks()
        self.sprite.movement = enemy_data['movement']['idle']
        self.sprite.target_pos = self.sprite.pos
        # TODO: trigger sound roar

    def update(self, dt, actions):
        self.check_expiration()
        if ENEMY_DEBUG:
            print('ROOOOOAAAR!!!')
            print(self.time_remaining)

        if self.done:
            # self.done = False
            self.sprite.entity_fsm.pop()  # Attack should be below it


class AttackState(EnemyTimedState):
    def startup(self):
        self.start_time = pygame.time.get_ticks()
        self.sprite.entity_fsm.register('roar', RoarState(
            self.sprite, enemy_data['roar_duration']))
        self.sprite.entity_fsm.push('roar')

    def wakeup(self):
        self.sprite.target_pos = self.sprite.get_loudest_source()['pos']
        if ENEMY_DEBUG:
            print(f'walk to {self.sprite.target_pos}')
        self.sprite.movement = enemy_data['movement']['run']

    def update(self, dt, actions):
        self.check_done()
        self.check_expiration()

        # update to new attack
        # But now also be alert to curious noise threshold
        if self.check_noise_thresholds() == 'attack' or 'curious':
            sound_source = self.sprite.get_loudest_source()
            self.sprite.target_pos = self.sprite.get_loudest_source()['pos']

        if self.done:
            self.sprite.entity_fsm.pop_all()

    def check_done(self):
        distance, _ = get_distance_direction_a_to_b(
            self.sprite.pos, self.sprite.target_pos)

        if distance < enemy_data['attack_radius']:
            self.done = True


class Enemy(pygame.sprite.Sprite):
    def __init__(self, groups, collision_sprites, sound_sprites, pos, waypoints, player, trigger_spawn_footprint, trigger_spawn_soundsource, trigger_sound):

        # general setup
        super().__init__(groups)

        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.hitbox = self.rect
        self.hitbox.center = self.pos
        self.collision_sprites = collision_sprites
        self.sound_sprites = sound_sprites

        # movement
        self.waypoints = waypoints
        self.waypoint_index = 0
        self.destination = self.pos
        self.direction = pygame.math.Vector2()
        self.movement = enemy_data['movement']['idle']
        self.distance_travelled = 0
        self.target_pos = self.pos

        # Interaction functions
        self.left = True  # Player starts on left foot
        self.trigger_spawn_footprint = trigger_spawn_footprint
        self.trigger_spawn_soundsource = trigger_spawn_soundsource
        self.trigger_sound = trigger_sound

        # interaction
        self.noise_meter = {}
        self.player = player

        # FSM
        self.entity_fsm = EntityFSM()
        self.entity_fsm.register('default', DefaultState(self))
        self.entity_fsm.register('idle', IdleState(
            self, randint(*enemy_data['idle_duration_range'])))
        self.entity_fsm.register('walk', WalkState(self))
        self.entity_fsm.push('default')

    def get_next_waypoint(self):
        self.waypoint_index += 1
        self.waypoint_index %= len(self.waypoints)
        return pygame.math.Vector2(self.waypoints[self.waypoint_index])

    def move(self, dt):
        self.old_pos = pygame.math.Vector2(self.pos)
        distance, self.direction = get_distance_direction_a_to_b(
            self.pos, self.target_pos)

        if distance <= (self.direction * self.movement['speed'] * dt * 60).magnitude():
            self.pos = self.target_pos

        else:
            self.pos += self.direction * self.movement['speed'] * dt * 60

        self.distance_travelled += (self.pos - self.old_pos).magnitude()

        self.hitbox.centerx = round(self.pos.x)
        self.collision('horizontal')
        self.hitbox.centery = round(self.pos.y)
        self.collision('vertical')
        self.rect.center = self.hitbox.center

        if self.distance_travelled >= self.movement['footstep_distance']:
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

    def make_noise(self, noise):
        self.trigger_sound(self.pos, 8, f'enemy_low_call')
        self.trigger_spawn_soundsource(self.pos, 8, 'enemy')

    def spawn_footprint(self):
        offset_pos = self.direction * 20
        self.trigger_spawn_footprint(
            self.pos+offset_pos, self.direction, self.movement['footstep_volume'], self.left, 'enemy')
        self.left = not self.left
        self.distance_travelled = 0

    def update_noise_meter(self):
        for sound in self.sound_sprites:
            if sound.rect.colliderect(self.hitbox):
                if sound.origin_type in enemy_data['noise_sensitivity_list']:
                    if sound.source not in self.noise_meter.keys():
                        self.noise_meter[sound.source] = {
                            'volume': 0, 'pos': sound.source.pos}
                    self.noise_meter[sound.source] = {
                        'volume': max([
                            0,
                            self.noise_meter[sound.source]['volume'],
                            sound.volume
                        ]),
                        'pos': sound.source.pos
                    }

    def get_loudest_source(self):
        loudest_source = 0
        loudest_source_dict = {'volume': 0, 'pos': pygame.math.Vector2()}
        if self.noise_meter:
            for key, val in self.noise_meter.items():
                if val['volume'] > loudest_source:
                    loudest_source = val['volume']
                    loudest_source_dict = val
        print(loudest_source_dict)
        return loudest_source_dict

    def decay_noise_meter(self, dt):
        for key, val in self.noise_meter.items():
            self.noise_meter[key]['volume'] = max(
                [0, val['volume'] - enemy_data['noise_decay'] * dt])

    def update(self, dt, actions):
        self.entity_fsm.execute(dt, actions)
        self.move(dt)
        self.update_noise_meter()
        self.decay_noise_meter(dt)
