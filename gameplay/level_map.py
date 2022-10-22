import pymunk
import pygame


class level_map():
    def __init__():
        rects = [
            [(width/2, height - 10), (width, 20)],  # floor
            [(width/2, 10), (width, 20)],  # ceiling
            [(10, height/2), (20, height)],  # left wall
            [(width-10, height/2), (20, height)],  # right wall
        ]

        for pos, size in rects:
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = pos
            shape = pymunk.Poly.create_box(body, size)
            shape.elasticity = 0.4
            shape.friction = 0.5
            space.add(body, shape)
        pass
