import os
import pygame


def run():
    run = True
    clock = pygame.time.Clock()
    pressed_pos = None

    window = pygame.display.set_mode((300, 300))
    # game_canvas = pygame.Surface((300, 300), pygame.SRCALPHA)
    visible_layer = pygame.Surface((300, 300))
    alpha_layer = pygame.Surface((300, 300), pygame.SRCALPHA)
    decay_layer = pygame.Surface((300, 300), pygame.SRCALPHA)
    bg_image = pygame.image.load(os.path.join(
        'assets', 'graphics', 'background.png')).convert_alpha()

    # prepare layers
    alpha_layer.fill((0, 0, 0, 255))
    visible_layer.blit(bg_image, (0, 0))
    while run:
        decay_layer.fill((0, 0, 0, 1))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                tmp_surf = pygame.Surface((300, 300), pygame.SRCALPHA)
                pressed_pos = pygame.mouse.get_pos()
                pygame.draw.circle(
                    tmp_surf, (0, 0, 0, 255), pressed_pos, radius=10)
                alpha_layer.blit(tmp_surf, (0, 0),
                                 special_flags=pygame.BLEND_RGBA_SUB)
        alpha_layer.blit(decay_layer, (0, 0),
                         special_flags=pygame.BLEND_RGBA_ADD)

        window.blit(visible_layer, (0, 0))
        window.blit(alpha_layer, (0, 0))
        # window.blit(game_canvas, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        pygame.display.update()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    run()
