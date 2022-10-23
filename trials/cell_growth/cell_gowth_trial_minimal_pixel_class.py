import pygame
from scipy.signal import convolve2d
import numpy as np
from math import sqrt
# from settings import *

# from gameplay.sound import SoundSource

KERNEL = [
    [1/sqrt(2),     1.0,    1/sqrt(2)],
    [1.0,           0.0,    1.0],
    [1/sqrt(2),     1.0,    1/sqrt(2)]]


def get_modifiers():

    o = np.ones((3, 3))

    e = np.ones((3, 3))
    e[:, 0] = 0

    w = np.ones((3, 3))
    w[:, 2] = 0

    n = np.ones((3, 3))
    n[2, :] = 0

    s = np.ones((3, 3))
    s[0, :] = 0

    ne = np.ones((3, 3))
    ne = np.ones((3, 3))
    b = np.zeros(3)
    np.fill_diagonal(ne[1:], b)
    np.fill_diagonal(ne[2:], b)

    nw = np.rot90(ne)
    sw = np.rot90(nw)
    se = np.rot90(sw)

    return {
        'o': o,
        'e': e,
        'w': w,
        'n': n,
        's': s,
        'ne': ne,
        'nw': nw,
        'se': se,
        'sw': sw,
    }


MODIFIERS = get_modifiers()


basin = np.zeros(15)

source = np.ones(15)
source *= 2
source[7] = 255
direction = np.zeros(15)
direction[:7] = -1
direction[7:] = 1

# print(direction)
# print(source)

# THIS IS NOT RIGHT
# for iteration in range(30):
#     for x in range(len(source)):
#         if x == 0:
#             basin[x] = (source[x] + source[x] + source[x+1]) * 0.33
#         if x == len(source)-1:
#             basin[x] = (source[x-1] + source[x] + source[x]) * 0.33
#         else:
#             basin[x] = (source[x-1] + source[x] + source[x+1]) * 0.33

#     source = basin
#     int_basin = basin.astype(int)
#     # print(f'it{iteration}: \n{int_basin}')
#     # expand

for iteration in range(10):
    for x in range(len(source)):
        if direction[x] == -1:
            basin[x] = source[x+1]
            direction[x+1] = 0
        elif direction[x] == 1:
            print('direction 1')
            basin[x] = source[x-1]
            direction[x-1] = 0

    source = basin
    int_basin = basin.astype(int)
    print(f'it{iteration}: \n{int_basin}\n{direction}')


# class Pixel(pygame.sprite.Sprite):
#     def __init__(self, groups, pos):
#         super().__init__(groups)
#         self.image = pygame.Surface((5, 5), pygame.SRCALPHA)
#         self.rect = self.image.get_rect(topleft=pos)
#         self.alpha_val = 0
#         self.alpha_val_float = 0.0

#     def attenuate(self):
#         self.alpha_val_float *= self.alpha_val_float * 0.8
#         self.alpha_val = round(self.alpha_val)

#     def excite(self, direction, amount):


#     def update(self):
#         self.attenuate()


# pygame.init()


# WIDTH, HEIGHT = 300, 300

# KERNEL = [
#     [1/sqrt(2),   1.0,  1/sqrt(2)],
#     [1.0,   0.0,  1.0],
#     [1/sqrt(2),   1.0,  1/sqrt(2)]]


# def draw(space, window, draw_options, ):
#     window.fill("white")
#     # bg_rect = pygame.rect.Rect(0, 0, WIDTH, HEIGHT)
#     # pygame.draw.rect(window, (0, 0, 0, 255), bg_rect)
#     pygame.display.update()


# def run():
#     run = True
#     clock = pygame.time.Clock()
#     fps = 60
#     attenuation = [0, 0.05, 0.01, 0.2, 0.3,  0.4,
#                    0.5, 0.6, 1/sqrt(2), 0.8, 0.9, 1.0]
#     attenuation_index = 0
#     dt = 1 / fps
#     pressed_pos = None

#     game_canvas = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
#     window = pygame.display.set_mode((WIDTH, HEIGHT))
#     kernel = KERNEL

#     # pixel_array = pygame.PixelArray()

#     def diffuse_pixels(surf, kernel):
#         # pixel_array = pygame.PixelArray(surf)
#         pixel_array = pygame.surfarray.array2d(surf)

#         pixel_array = convolve2d(
#             pixel_array, kernel, boundary='symm', mode='same')
#         pixel_array = pixel_array * attenuation[attenuation_index]
#         return pixel_array

#     def diffuse_pixel_naive(surf):
#         pixel_array = pygame.surfarray.array2d(surf)
#         print(type(pixel_array))

#     def attenuate(surf):
#         pixel_array = pygame.surfarray.array2d(surf)
#         pixel_array = pixel_array * 0.8
#         return pygame.surfarray.make_surface(pixel_array)

#     while run:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False
#                 break

#             # if event.type == pygame.MOUSEBUTTONDOWN:
#                 # spawn 'bullets' in all directions
#             pressed_pos = pygame.mouse.get_pos()
#             pygame.draw.circle(
#                 game_canvas, (255, 255, 255, 255), pressed_pos, radius=10)

#             # if event.type == pygame.KEYDOWN:
#             #     if event.key == pygame.K_a:
#             #         attenuation_index -= 1
#             #         attenuation_index %= len(attenuation)
#             #         print('Attenuation', attenuation[attenuation_index])
#             #         kernel = np.array([np.array(i)
#             #                           for i in KERNEL])  # make to array
#             #         # normalize sum to 1
#             #         # kernel = kernel/kernel.sum(axis=0, keepdims=1)
#             #         kernel *= attenuation[attenuation_index]
#             #         print(kernel)
#             #     if event.key == pygame.K_d:
#             #         attenuation_index += 1
#             #         attenuation_index %= len(attenuation)
#             #         print('Attenuation', attenuation[attenuation_index])
#             #         kernel = np.array([np.array(i)
#             #                           for i in KERNEL])  # make to array
#             #         # normalize sum to 1
#             #         # kernel = kernel/kernel.sum(axis=0, keepdims=1)
#             #         kernel *= attenuation[attenuation_index]
#             #         print(kernel)

#         window.fill((0, 0, 0))
#         # diffused_pixels = diffuse_pixel_naive(game_canvas)
#         # pygame.surfarray.blit_array(game_canvas, diffused_pixels)
#         game_canvas = attenuate(game_canvas)
#         window.blit(game_canvas, (0, 0))
#         # print('next frame')
#         pygame.display.update()

#         clock.tick(60)

#     pygame.quit()


# if __name__ == "__main__":
#     run()
