import os
import pygame
import pymunk
import pymunk.pygame_util
import math

from settings import *

from gameplay.sound import SoundSource

pygame.init()


def draw(space, window, draw_options, ):
    # s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    # s.fill((255, 255, 255, 50))
    # window.blit(s, (0, 0))
    # window.fill("white")
    # bg_rect = pygame.rect.Rect(0, 0, WIDTH, HEIGHT)
    # pygame.draw.rect(window, (0, 0, 0, 255), bg_rect)
    # space.debug_draw(draw_options)
    pygame.display.update()


def create_boundaries(space, width, height):
    rects = [
        [(width/2, height - 10), (width, 20)],  # floor
        [(width/2, 10), (width, 20)],  # ceiling
        [(10, height/2), (20, height)],  # left wall
        [(width-10, height/2), (20, height)],  # right wall
    ]

    obstacles = []
    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 1
        shape.friction = 0
        shape.collision_type = COLLISION_TYPES['obstacle']
        shape.filter = pymunk.ShapeFilter(
            categories=OBJECT_CATEGORIES['obstacle'], mask=CATEGORY_MASKS['obstacle'])
        obstacles.append(shape)
        space.add(body, shape)

    return obstacles


def create_lines(space):
    # Static Segments
    segments = [
        pymunk.Segment(space.static_body, (100, 0), (100, 50), 3),
        pymunk.Segment(space.static_body, (0, 100), (100, 100), 3),
        pymunk.Segment(space.static_body, (0, 200), (100, 200), 3),
        pymunk.Segment(space.static_body, (150, 200), (150, 300), 3),
        pymunk.Segment(space.static_body, (150, 0), (150, 150), 3),
        # pymunk.Segment(space.static_body, (30, 100), (30, 200), 3),
        # pymunk.Segment(space.static_body, (50, 100), (50, 200), 5),
    ]
    space.add(*segments)


def create_pixel_cells(space, width, height):
    for col in range(100, width-100):
        for row in range(100, height-100):
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = (col, row)
            shape = pymunk.Poly.create_box(body, (0.5, 0.5))
            shape.elasticity = 0
            shape.friction = 0
            space.add(body, shape)


def spawn_sound_source_at_collision(arbiter, space, data):
    a = arbiter.shapes[0]  # Soundbeam
    b = arbiter.shapes[1]  # obstacle
    print(arbiter.contact_point_set)

    # Spawn new soundbeams
    # source = SoundSource([], space, a._get_body().position, a.volume)
    # soundbeams = source.get_soundbeams()
    # for soundbeam in source.get_soundbeams():
    #     soundbeams.append(soundbeam)
    # data['soundbeams'].append(soundbeams)


def run():
    WIDTH, HEIGHT = 300, 300
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    alpha_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    decay_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    bg_image = pygame.image.load(os.path.join(
        'assets', 'graphics', 'background.png'))
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps

    space = pymunk.Space()
    space.gravity = (0, 0)  # y increases downward in pygame

    create_lines(space)

    draw_options = pymunk.pygame_util.DrawOptions(window)
    pressed_pos = None
    soundbeams = []
    obstacles = create_boundaries(space, WIDTH, HEIGHT)

    # Collision
    # h = space.add_collision_handler(
    #     COLLISION_TYPES['soundbeam'], COLLISION_TYPES['obstacle'])
    # h.data['obstacles'] = obstacles
    # h.data['soundbeams'] = soundbeams
    # h.post_solve = spawn_sound_source_at_collision

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                # spawn 'bullets' in all directions
                pressed_pos = pygame.mouse.get_pos()
                source = SoundSource([], space, pressed_pos,
                                     SOUNDBEAM_MAX_LOUDNESS)
                for soundbeam in source.get_soundbeams():
                    soundbeams.append(soundbeam)

        if len(soundbeams) > 0:
            for soundbeam in soundbeams:
                decayed = soundbeam.decay(dt)
                if decayed:
                    space.remove(soundbeam, soundbeam.body)
                    soundbeams.remove(soundbeam)
                    soundbeam.kill()

        window.fill((0, 0, 0))

        if len(soundbeams) > 0:
            for soundbeam in soundbeams:
                l = soundbeam._get_body().position[0]-soundbeam.radius
                t = soundbeam._get_body().position[1]-soundbeam.radius
                w = soundbeam.radius*2
                h = soundbeam.radius*2
                circle_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                circle_rect = pygame.rect.Rect(l, t, w, h)
                bright = soundbeam.volume/SOUNDBEAM_MAX_LOUDNESS * 255
                pygame.draw.ellipse(
                    circle_surf, (bright, bright, bright), circle_rect)
                # alpha = soundbeam.volume/SOUNDBEAM_MAX_LOUDNESS * 255 / 20
                # print(alpha)
                circle_surf.set_alpha(bright)
                alpha_surf.blit(circle_surf, (0, 0),
                                special_flags=pygame.BLEND_RGBA_ADD)
        decay_surf.fill((10, 10, 10, 10))
        # decay_surf.blit(bg_image, (0, 0))
        alpha_surf.blit(decay_surf, (0, 0),
                        special_flags=pygame.BLEND_RGBA_SUB)
        window.blit(alpha_surf, (0, 0))

        # new_surf = pygame.Surface((50, 50), pygame.SRCALPHA)
        # new_rect = pygame.rect.Rect(20, 20, 20, 20)
        # pygame.draw.rect(new_surf, (255, 255, 255), new_rect)
        # window.blit(new_surf, (20, 20))
        pygame.display.update()

        space.step(dt)
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    run()
