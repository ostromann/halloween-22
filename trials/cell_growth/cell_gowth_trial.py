import pygame
import math
# from settings import *

from gameplay.sound import SoundSource

pygame.init()


GAME_W, GAME_H = 300, 300
WIDTH, HEIGHT = 300, 300


class Game():
    def __init__(self):
        pygame.init()
        self.GAME_W, self.GAME_H = GAME_W, GAME_H
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = WIDTH, HEIGHT
        self.game_canvas = pygame.Surface((self.GAME_W, self.GAME_H))
        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.visible_sprites = pygame.sprite.Sprite()

    def create_boundaries(self):
        rects = [
            [0, 0, 20, self.GAME_H],
            [0, 0, self.GAME_W, 20],
            [self.GAME_W-20, 0, 20, self.GAME_H],
            [0, self.GAME_H-20, self.GAME_W, 20]
        ]

        for l, t, w, h in rects:
            Boundary([visible_sprites, obstacle_sprites], l, t, w, h)


def draw(space, window, draw_options, ):
    window.fill("white")
    # bg_rect = pygame.rect.Rect(0, 0, WIDTH, HEIGHT)
    # pygame.draw.rect(window, (0, 0, 0, 255), bg_rect)
    space.debug_draw(draw_options)
    pygame.display.update()


class Boundary(pygame.sprite.Sprite):
    def __init__(self, groups, l, t, w, h):
        super().__init__(groups)
        self.rect = pygame.rect.Rect(l, t, w, h)


def create_pixel_cells(space, width, height):
    for col in range(100, width-100):
        for row in range(100, height-100):
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = (col, row)
            shape = pymunk.Poly.create_box(body, (0.5, 0.5))
            shape.elasticity = 0
            shape.friction = 0
            space.add(body, shape)


# def create_pendulum(space):
#     rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
#     rotation_center_body.position = (500, 270)

#     body = pymunk.Body()
#     body.position = (300, 300)
#     line = pymunk.Segment(body, (0, 0), (100, 0), 5)
#     circle = pymunk.Circle(body, 40, (100, 0))
#     line.friction = 1
#     circle.friction = 1
#     line.mass = 8
#     circle.mass = 30
#     circle.elasticity = 0.95

#     rotation_center_joint = pymunk.PinJoint(
#         body, rotation_center_body, (0, 0), (0, 0))

#     space.add(circle, line, body, rotation_center_joint)


# def create_structure(space, width, height):
    # BROWN = (139, 69, 19, 100)
    # rects = [
    #     [(600, height-120), (40, 200), BROWN, 100],
    #     [(900, height-120), (40, 200), BROWN, 100],
    #     [(750, height-240), (340, 40), BROWN, 150],
    # ]

    # for pos, size, color, mass in rects:
    #     body = pymunk.Body()
    #     body.position = pos

    #     shape = pymunk.Poly.create_box(body, size, radius=2)
    #     shape.color = color
    #     shape.mass = mass
    #     shape.elasticity = 0.4
    #     shape.friction = 0.4
    #     space.add(body, shape)


# def create_particles(space, number, center_pos):
#     particles = []
#     radius = 30
#     for index in range(number):
#         phase_shift = index * 360 / number * math.pi/180
#         x = radius * math.sin((math.pi * 2 + phase_shift))
#         y = radius * math.cos((math.pi * 2 + phase_shift))

#         pos = pygame.math.Vector2((x + center_pos[0], y + center_pos[1]))

#         body = pymunk.Body()
#         body.position = (pos.x, pos.y)

#         shape = pymunk.Circle(body, 2)
#         shape.mass = 0.1
#         shape.elasticity = 1
#         shape.friction = 0
#         space.add(body, shape)
#         particles.append(shape)
#     return particles


def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps

    space = pymunk.Space()
    space.gravity = (0, 0)  # y increases downward in pygame

    # ball = create_ball(space, 30, 10)
    create_boundaries(space, WIDTH, HEIGHT)
    create_lines(space)
    # create_pixel_cells(space, WIDTH, HEIGHT)
    # create_structure(space, WIDTH, HEIGHT)
    # create_pendulum(space)

    draw_options = pymunk.pygame_util.DrawOptions(window)

    pressed_pos = None

    soundbeams = []

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                # spawn 'bullets' in all directions
                pressed_pos = pygame.mouse.get_pos()
                source = SoundSource([], space, pressed_pos, 20)
                for soundbeam in source.get_soundbeams():
                    soundbeams.append(soundbeam)

        if len(soundbeams) > 0:
            for soundbeam in soundbeams:
                decayed = soundbeam.decay(dt)
                if decayed:
                    space.remove(soundbeam, soundbeam.body)
                    soundbeams.remove(soundbeam)
                    soundbeam.kill()

        draw(space, window, draw_options)
        space.step(dt)
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)
