import pygame
import pymunk
import math

from settings import *


'''
body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        body.position = pos

        super().__init__(body, radius, offset=(0, 0))
        self.mass = mass
        self.elasticity = 0.4
        self.friction = 0.4
        self.color = (255, 0, 0, 0)
        self.collision_type = config.collision_types['asteroid']
        self.filter = pymunk.ShapeFilter(
            categories=config.object_categories['asteroid'], mask=config.category_masks['asteroid'])
'''


class Soundbeam(pygame.sprite.Sprite, pymunk.Circle):
    def __init__(self, groups, space, pos, direction, volume):
        pygame.sprite.Sprite.__init__(self, groups)
        self.volume = volume
        body = self.get_body(*pos)
        pymunk.Circle.__init__(self, body, SOUNDBEAM_RADIUS)
        self.mass = 0.1
        self.elasticity = 1
        self.friction = 0
        self.collision_type = COLLISION_TYPES['soundbeam']
        self.filter = pymunk.ShapeFilter(
            categories=OBJECT_CATEGORIES['soundbeam'], mask=CATEGORY_MASKS['soundbeam'])
        space.add(body, self)

        self.body.apply_impulse_at_local_point(direction, (0, 0))

    def get_body(self, x, y):
        body = pymunk.Body()
        body.position = (x, y)
        return body

    def decay(self, dt):
        self.volume -= SOUNDBEAM_ATTENUATION * dt
        self.unsafe_set_radius(self.radius + SOUNDBEAM_RADIUS_GAIN * dt)
        print(self.volume)
        if self.volume <= 0:
            # self.space.remove(self, self.body)
            return True
        return False


class SoundSource():
    def __init__(self, groups, space, pos, volume):
        # super().__init__(self, groups)
        self.groups = groups
        self.volume = volume
        self.pos = pygame.math.Vector2(pos)
        self.space = space
        self.emit_soundbeams()

    def emit_soundbeams(self):
        self.soundbeams = []
        radius = 1
        for index in range(SOUNDBEAM_NUMBERS):
            phase_shift = index * 360 / SOUNDBEAM_NUMBERS * math.pi/180
            x = radius * math.sin((math.pi * 2 + phase_shift))
            y = radius * math.cos((math.pi * 2 + phase_shift))

            pos = (x + self.pos.x, y + self.pos.y)
            direction = (x*30, y*30)
            self.soundbeams.append(
                Soundbeam(self.groups, self.space, pos, direction, self.volume))

    def get_soundbeams(self):
        return self.soundbeams
