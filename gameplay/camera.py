import pygame
import os


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self, alpha=False):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.alpha = alpha
        if self.alpha:
            self.drawing_surface = pygame.Surface(
                self.display_surface.get_size(), pygame.SRCALPHA)
        else:
            self.drawing_surface = pygame.Surface(
                self.display_surface.get_size())
        # camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # creating the floor
        if not self.alpha:
            self.floor_surf = pygame.image.load(os.path.join(
                'assets', 'graphics', 'background.png')).convert()
            self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def center_target_camera(self, target):
        # Camera following player
        self.offset.x = target.pos.x - self.half_w  # target.rect.centerx - self.half_w
        self.offset.y = target.pos.y - self.half_h  # target.rect.centery - self.half_h

    def custom_draw(self):
        # drawing the floor
        if self.alpha:
            self.drawing_surface.fill((0, 0, 0, 0))
        else:
            floor_offset_pos = self.floor_rect.topleft  # - self.offset
            self.drawing_surface.blit(self.floor_surf, floor_offset_pos)

        # active elements
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft  # - self.offset
            self.drawing_surface.blit(sprite.image, offset_pos)

        # blit to display
        if self.alpha:
            self.display_surface.blit(
                self.drawing_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        else:
            self.display_surface.blit(self.drawing_surface, (0, 0))
