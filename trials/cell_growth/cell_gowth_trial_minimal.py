from re import A
import pygame
from scipy.signal import convolve2d
import numpy as np
# from settings import *

from gameplay.sound import SoundSource

pygame.init()


WIDTH, HEIGHT = 300, 300

KERNEL = [
    [0.7,   1.0,  0.7],
    [1.0,   0.0,  1.0],
    [0.7,   1.0,  0.7]]


def draw(space, window, draw_options, ):
    window.fill("white")
    # bg_rect = pygame.rect.Rect(0, 0, WIDTH, HEIGHT)
    # pygame.draw.rect(window, (0, 0, 0, 255), bg_rect)
    pygame.display.update()


def run():
    run = True
    clock = pygame.time.Clock()
    fps = 60
    attenuation = [0, 0.05, 0.01, 0.2, 0.3,  0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    attenuation_index = 0
    dt = 1 / fps
    pressed_pos = None

    game_canvas = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    kernel = KERNEL

    # pixel_array = pygame.PixelArray()

    def diffuse_pixels(surf, kernel):
        # pixel_array = pygame.PixelArray(surf)
        pixel_array = pygame.surfarray.array2d(surf)

        pixel_array = convolve2d(
            pixel_array, kernel, boundary='symm', mode='same')
        pixel_array = pixel_array * attenuation[attenuation_index]
        return pixel_array

    def diffuse_pixel_naive(surf):
        pixel_array = pygame.surfarray.array2d(surf)
        print(type(pixel_array))

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                # spawn 'bullets' in all directions
                pressed_pos = pygame.mouse.get_pos()
                pygame.draw.circle(
                    game_canvas, (255, 255, 255, 255), pressed_pos, radius=10)

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_a:
            #         attenuation_index -= 1
            #         attenuation_index %= len(attenuation)
            #         print('Attenuation', attenuation[attenuation_index])
            #         kernel = np.array([np.array(i)
            #                           for i in KERNEL])  # make to array
            #         # normalize sum to 1
            #         # kernel = kernel/kernel.sum(axis=0, keepdims=1)
            #         kernel *= attenuation[attenuation_index]
            #         print(kernel)
            #     if event.key == pygame.K_d:
            #         attenuation_index += 1
            #         attenuation_index %= len(attenuation)
            #         print('Attenuation', attenuation[attenuation_index])
            #         kernel = np.array([np.array(i)
            #                           for i in KERNEL])  # make to array
            #         # normalize sum to 1
            #         # kernel = kernel/kernel.sum(axis=0, keepdims=1)
            #         kernel *= attenuation[attenuation_index]
            #         print(kernel)

        window.fill((0, 0, 0))
        diffused_pixels = diffuse_pixel_naive(game_canvas)
        pygame.surfarray.blit_array(game_canvas, diffused_pixels)
        window.blit(game_canvas, (0, 0))
        # print('next frame')
        pygame.display.update()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    run()
