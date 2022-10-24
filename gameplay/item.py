import pygame
from gameplay.boundary import Boundary
from gameplay.sound import SoundSource, Soundbeam

from gameplay.utils import *
from settings import *


class Key(pygame.sprite.Sprite):
    def __init__(self, groups, collision_groups, pos, player, id):
        super().__init__(groups)

        self.id = id

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

            self.pos += direction * self.pulling_entity.speed * dt * 60

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
    def __init__(self, groups, key_sprites, door_sprites, pos, id):
        super().__init__(groups)

        self.id = id

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
            if sprite.id == self.id:
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
            if sprite.id == self.id:
                sprite.toggle_state()

    def update(self, dt, actions):
        self.check_key()
        self.check_unlock()


class Door(pygame.sprite.Sprite):
    def __init__(self, groups, pos, size, closed, id):
        # self.sprite_type = sprite_type
        super().__init__(groups)

        self.id = id
        self.pos = pos

        # Define surface for open and closed
        # closed
        self.closed_size = size
        closed_surface = pygame.Surface(self.closed_size)
        self.closed_image = closed_surface

        # open
        self.open_size = pygame.math.Vector2(0, 0)
        open_surface = pygame.Surface(self.open_size)
        self.open_image = open_surface

        # state
        self.closed = closed
        self.set_sprite()

        # set image, rect and hitbox

    def set_sprite(self):
        if self.closed:
            self.image = self.closed_image
        else:
            self.image = self.open_image

        # rect and hitbox
        self.rect = self.image.get_rect(topleft=(self.pos))
        self.hitbox = self.rect
        self.hitbox.topleft = self.pos

    def toggle_state(self):
        # TODO: Fix the SoundSource. Objects outside the game world should only trigger the creation of a SoundSource in the gameworld!

        self.closed = not self.closed
        self.set_sprite()

    def update(self, dt, actions):
        if actions['TAB']:
            self.toggle_state()
