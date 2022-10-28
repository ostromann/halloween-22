import os
import pygame
from gameplay.boundary import Boundary
from gameplay.sound import SoundSource, Soundbeam
from random import random, choice, randint

from gameplay.utils import *
from settings import *


class AmbientSound(pygame.sprite.Sprite):
    def __init__(self, groups, name, pos, interval, randomness, volume, trigger_sound):
        super().__init__(groups)
        self.name = name
        self.pos = pos
        self.interval = int(interval)
        self.randomness = float(randomness)
        self.volume = int(volume)
        self.start_time = pygame.time.get_ticks() - randint(-5000, 3000)
        self.last_played = pygame.time.get_ticks()
        self.play = choice([True, False, False, False])
        self.trigger_sound = trigger_sound

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        print(current_time, self.last_played, self.interval)

        if not self.play:
            if current_time - self.last_played >= self.interval * (1 + choice([-1, 1]) * random() * self.randomness):
                self.play = True

    def update(self):
        self.cooldown()
        if self.play:
            self.trigger_sound(self.pos, self.volume, self.name)
            self.last_played = pygame.time.get_ticks()
            self.play = False


class Key(pygame.sprite.Sprite):
    def __init__(self, groups, collision_groups, pos, player, surf, color):
        super().__init__(groups)

        self.color = color

        # self.image = pygame.image.load(os.path.join(
        #     'assets', 'graphics', 'objects', f'key_{color}', f'key_{color}_0.png'))
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()
        self.hitbox = self.rect
        self.hitbox.center = self.pos
        self.collision_groups = collision_groups

        self.pulling_entity = player
        self.is_pulled = False

    def check_pulling(self, actions):
        if self.is_pulled:
            distance, _ = get_distance_direction_a_to_b(
                self.pos, self.pulling_entity.pos)
            if distance >= 1.5 * OBJECT_PULLING_RADIUS or actions['e']:
                self.is_pulled = False

        else:
            distance, _ = get_distance_direction_a_to_b(
                self.pos, self.pulling_entity.pos)
            if distance <= OBJECT_PULLING_RADIUS and actions['e']:
                self.is_pulled = True

    def move(self, dt):
        if self.is_pulled:
            distance, direction = get_distance_direction_a_to_b(
                self.pos, self.pulling_entity.pos)

            # TODO: Get the players current speed
            self.pos += direction * \
                self.pulling_entity.movement_stats['walk']['speed'] * dt * 60

        self.hitbox.centerx = round(self.pos.x)
        self.collision('horizontal')
        self.hitbox.centery = round(self.pos.y)
        self.collision('vertical')

        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for group in self.collision_groups:
                for sprite in group:
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction.x > 0:    # moving right
                            self.pos.x = sprite.hitbox.left - self.hitbox.width / 2
                        elif self.direction.x < 0:    # moving left
                            self.pos.x = sprite.hitbox.right + self.hitbox.width / 2
                        self.hitbox.centerx = round(self.pos.x)
                        self.rect.centerx = round(self.pos.x)

        if direction == 'vertical':
            for group in self.collision_groups:
                for sprite in group:
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction.y > 0:    # moving down
                            self.pos.y = sprite.hitbox.top - self.hitbox.height / 2
                        elif self.direction.y < 0:    # moving up
                            self.pos.y = sprite.hitbox.bottom + self.hitbox.height / 2
                        self.hitbox.centery = round(self.pos.y)
                        self.rect.centery = round(self.pos.y)

    def update(self, dt, actions):
        # self.input(actions)
        self.check_pulling(actions)
        self.move(dt)


class Keyhole(pygame.sprite.Sprite):
    def __init__(self, groups, key_sprites, door_sprites, pos, surf, color):
        super().__init__(groups)

        self.color = color

        # self.image = pygame.image.load(os.path.join(
        #     'assets', 'graphics', 'objects', f'keyhole_{color}', f'keyhole_{color}_0.png'))
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        # pygame.draw.rect(self.image, (0,204,204), self.rect, width=)
        self.hitbox = self.rect
        self.hitbox.center = pos

        # logic
        self.key_sprites = key_sprites
        self.door_sprites = door_sprites

        self.has_key = False
        self.unlocked = False

    def check_key(self):
        for sprite in self.key_sprites:
            if sprite.color == self.color:
                if sprite.hitbox.colliderect(self.hitbox):
                    self.has_key = True
                else:
                    self.has_key = False

    def check_unlock(self):
        if self.unlocked and self.has_key:
            pass
        if not self.unlocked and self.has_key:
            self.unlocked = True
            self.toggle_doors()
        if self.unlocked and not self.has_key:
            self.unlocked = False
            self.toggle_doors()
        if not self.unlocked and not self.has_key:
            pass

    def toggle_doors(self):
        for sprite in self.door_sprites:
            if sprite.color == self.color:
                sprite.toggle_state()

    def update(self, dt, actions):
        self.check_key()
        self.check_unlock()


class Door(pygame.sprite.Sprite):
    def __init__(self, groups, visible_sprites, collision_sprites, pos, size, rotate, closed, color, trigger_toggle_sound):
        # self.sprite_type = sprite_type
        super().__init__(groups)
        self.visible_sprites = visible_sprites
        self.collision_sprites = collision_sprites
        self.color = color
        self.pos = pos
        self.trigger_toggle_sound = trigger_toggle_sound
        self.rotate = rotate

        # TODO: Fix rotation!
        if rotate == 'rotate':
            self.image = pygame.image.load(os.path.join(
                'assets', 'graphics', 'objects', f'door_{color}', f'door_{color}_0.png'))
            inflate = (-26, 0)
        else:
            self.image = pygame.image.load(os.path.join(
                'assets', 'graphics', 'objects', f'door_{color}', f'door_{color}_0_rotate.png'))
            inflate = (0, -26)
        self.rect = self.image.get_rect(topleft=(self.pos))

        # if size[0] > size[1]:
        #     inflate = (0, -9)
        # else:
        #     inflate = (-9, 0)

        self.hitbox = self.rect.inflate(inflate)
        self.hitbox.center = self.rect.center

        # state
        if closed == 'closed':
            self.closed = True
            self.add([self.visible_sprites, self.collision_sprites])

        else:
            self.closed = False
            self.remove([self.visible_sprites, self.collision_sprites])

    def toggle_state(self):
        # TODO: Fix the SoundSource. Objects outside the game world should only trigger the creation of a SoundSource in the gameworld!
        volume = 15
        sound_type = 'door'
        self.trigger_toggle_sound(self.pos, volume, sound_type)
        self.closed = not self.closed
        if self.closed:
            self.add([self.visible_sprites, self.collision_sprites])
        else:
            self.remove([self.visible_sprites, self.collision_sprites])

    def update(self, dt, actions):
        pass
        # if actions['TAB']:
        #     self.toggle_state()
