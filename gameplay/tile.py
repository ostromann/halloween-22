import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect
        self.hitbox.topleft = pos


class ObjectTile(pygame.sprite.Sprite):
    '''
    ObjectTiles of type Rectangle
    '''

    def __init__(self, obj, groups):
        if obj.name == 'Rectangle':
            super().__init__(groups)

            self.image = pygame.Surface(
                (obj.width, obj.height), pygame.SRCALPHA)
            self.rect = self.image.get_rect(topleft=(obj.x, obj.y))
        else:
            raise ValueError("'ObjTile not of name 'Rectangle'")
