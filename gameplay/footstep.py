import pygame

from gameplay.sound import SoundSource


class Footstep():
    def __init__(self, groups, collision_sprites, pos, direction, volume, left, origin_type='player'):
        # super().__init__(groups)
        self.pos = pygame.math.Vector2(pos)
        self.direction = direction
        self.volume = volume
        self.left = left
        self.origin_type = origin_type

        SoundSource(groups, collision_sprites, self.pos,
                    self.volume, self.origin_type)
