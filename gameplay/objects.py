import os
import pygame
from gameplay.boundary import Boundary
from gameplay.sound import SoundSource, Soundbeam

from gameplay.utils import *
from settings import *


class Key(pygame.sprite.Sprite):
    def __init__(self, groups, collision_groups, pos, player, color):
        super().__init__(groups)

        self.color = color

        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 204, 204))
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
            if distance >= 1.5 * OBJECT_PULLING_RADIUS or actions['LCTRL']:
                self.is_pulled = False

        else:
            distance, _ = get_distance_direction_a_to_b(
                self.pos, self.pulling_entity.pos)
            if distance <= OBJECT_PULLING_RADIUS and actions['LCTRL']:
                self.is_pulled = True

    def move(self, dt):
        if self.is_pulled:
            distance, direction = get_distance_direction_a_to_b(
                self.pos, self.pulling_entity.pos)

            # TODO: Get the players current speed
            self.pos += direction * \
                self.pulling_entity.movement_stats['sneak']['speed'] * dt * 60

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
    def __init__(self, groups, key_sprites, door_sprites, pos, color):
        super().__init__(groups)

        self.color = color

        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 128, 128))
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
    def __init__(self, groups, visible_sprites, collision_sprites, pos, size, closed, color):
        # self.sprite_type = sprite_type
        super().__init__(groups)
        self.visible_sprites = visible_sprites
        self.collision_sprites = collision_sprites
        self.color = color
        self.pos = pos
        self.original_pos = pos

        self.image = pygame.image.load(os.path.join(
            'assets', 'graphics', 'objects', f'door_{color}', f'door_{color}_0.png'))
        self.rect = self.image.get_rect(topleft=(self.pos))

        if size[0] > size[1]:
            inflate = (0, -9)
        else:
            inflate = (-9, 0)

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
        self.closed = not self.closed
        if self.closed:
            self.add([self.visible_sprites, self.collision_sprites])
        else:
            self.remove([self.visible_sprites, self.collision_sprites])

    def update(self, dt, actions):
        pass
        # if actions['TAB']:
        #     self.toggle_state()
