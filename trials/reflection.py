import pygame
import random
from math import atan2, degrees, pi
pygame.init()
display = pygame.display.set_mode((1280, 720))
width, height = display.get_rect()[2], display.get_rect()[3]

vec = pygame.math.Vector2
distance = vec(0, -2000)

reflect = False
reflections = 5
objects = []  # list of rects
objects.append(pygame.Rect(0, 0, 120, 110))

rays = 10  # number of rays from source
draw = False  # flag for drawing objects
rotation = False
rot = 0

font = pygame.font.SysFont('square721cn', 40)
font2 = pygame.font.SysFont('square721cn', 24)
clock = pygame.time.Clock()


def Light(origin, direction, bounces, objects, c=False):
    origin = origin  # line start coordinates
    direction = vec(direction)  # vector specifiying the direction of ray
    end = origin  # line end coordinates(origin+direction, line 33)
    bounces = bounces
    colour = [(50, 50, 50), (50, 50, 50), (100, 100, 100),
              (150, 150, 150), (200, 200, 200), (255, 255, 255)]
    # colour of the ray depends on how many times its been reflected
    colour = colour[bounces]
    hit = False  # hit flag
    while True:
        # increment the ray little by little to detect collisions
        end += direction.normalize()*50
        for ob in objects:
            clipped_line = ob.clipline(origin, end)  # check for collision
            if clipped_line and bounces != 0:  # limit for reflections
                start1 = clipped_line[0]
                hitstart = list(start1)  # coordinates of where the ray hits
                end = hitstart  # the end of the ray is where it hits
                if hitstart[0] >= ob.right-1:  # reflection based on where the ray hit
                    direction[0] *= -1
                    end[0] += 1
                elif hitstart[0] <= ob.left:
                    direction[0] *= -1
                    end[0] -= 1
                elif hitstart[1] <= ob.top:
                    direction[1] *= -1
                    end[1] -= 1
                elif hitstart[1] >= ob.bottom-1:
                    direction[1] *= -1
                    end[1] += 1
                hit = True
                break
        # max length for ray, could optimize further but good enough
        if hit or (end).length() > 2000:
            break

    pygame.draw.line(display, colour, origin, end, bounces)  # draw the ray

    if hit and reflect:
        bounces -= 1
        # create a new ray starting from where parent ray hit
        Light(hitstart, direction, bounces, objects)
    else:
        return


while True:
    clock.tick(60)
    display.fill((0, 0, 0))
    fps = clock.get_fps()
    fpstext = font.render(str(int(fps)), False, (190, 190, 190))
    raystext = font2.render("RAYS= "+str(rays), False, (190, 190, 190))
    rotatetext = font2.render("ROTATE", False, (190, 190, 190))
    reflecttext = font2.render("REFLECT", False, (190, 190, 190))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                reflect = not reflect
            elif event.button == 3:
                draw = True
                # mouse position for drawing objects
                startpos = list(pygame.mouse.get_pos())
            elif event.button == 4:
                if rays > 1:
                    rays -= 1
            elif event.button == 5:
                if rays < 360:
                    rays += 1
        elif event.type == pygame.MOUSEBUTTONUP:
            if draw:
                draw = False  # stop drawing
                objects.append(pygame.Rect(
                    topleft[0], topleft[1], xdist, ydist))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                objects = [pygame.Rect(0, 0, 120, 110)]
            elif event.key == pygame.K_SPACE:
                rotation = not rotation

    if draw:
        topleft = list(startpos)  # creating and drawing objects
        curpos = list(pygame.mouse.get_pos())
        xdist = abs(curpos[0]-topleft[0])
        ydist = abs(curpos[1]-topleft[1])
        if curpos[0] < topleft[0]:
            if curpos[1] < topleft[1]:
                topleft = curpos
            else:
                topleft[0] -= xdist
        elif curpos[1] < topleft[1]:
            topleft[1] -= ydist
        pygame.draw.rect(display, (100, 30, 30),
                         (topleft[0], topleft[1], xdist, ydist), 4)

    if objects:
        for ob in objects[1:]:
            pygame.draw.rect(display, (100, 30, 30), ob,
                             4)  # displaying objects

    origin = pygame.mouse.get_pos()  # light source coordinates

    angle = 0
    for k in range(rays):
        angle += 360/rays
        nline = distance.rotate(angle+rot)  # source ray rotation
        Light(origin, nline, 5, objects, True)  # creating source rays

    if rotation:
        rot += 0.2
    else:
        pygame.draw.line(display, (190, 190, 190), (5, 95),
                         (72, 95), 5)  # rotation ui strikethrough

    display.blit(fpstext, (7, 0))
    display.blit(raystext, (7, 40))
    display.blit(reflecttext, (7, 60))
    display.blit(rotatetext, (7, 80))

    if not reflect:
        pygame.draw.line(display, (190, 190, 190), (5, 75),
                         (80, 75), 5)  # reflection ui strikethrough

    pygame.display.update()
