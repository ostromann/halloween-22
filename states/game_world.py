
import os
import pygame
from random import choice, randint
from debug import debug

from states.state import State, FSM
from gameplay.camera import YSortCameraGroup
from gameplay.boundary import Boundary
from gameplay.sound import SoundSource, Soundbeam
from gameplay.player import Player

from settings import *


class PreLevel(State):
    def __init__(self, game, blocks_update=None, blocks_render=None):
        super().__init__(game, blocks_update, blocks_render)

    def startup(self):
        print('PreLevel startup')
        Boundary((50, 50), [self.game.visible_sprites,
                 self.game.collision_sprites])
        # Call when state is pushed to the stack
        self.game.fsm.switch('level')
        pass

    def cleanup(self):
        print('PreLevel cleanup')
        # Call when state is pop from the stack
        pass

    def suspend(self):
        print('PreLevel suspend')
        # Call when a new state is pushed on top of the current one
        pass

    def wakeup(self):
        print('PreLevel wakeup')
        # Call when the state ontop of this one is popped
        pass

    def update(self):
        pass

    def render(self):
        pass


class Level(State):
    def __init__(self, game, blocks_update=None, blocks_render=None):
        super().__init__(game, blocks_update, blocks_render)

    def startup(self):
        print('Level startup')
        # Call when state is pushed to the stack
        pass

    def cleanup(self):
        print('Level cleanup')
        # Call when state is pop from the stack
        pass

    def suspend(self):
        print('Level suspend')
        # Call when a new state is pushed on top of the current one
        pass

    def wakeup(self):
        print('Level wakeup')
        # Call when the state ontop of this one is popped
        pass

    def update(self):
        dt = self.game.game.dt
        actions = self.game.game.actions
        print(actions)

        if actions['left']:
            print('spawn sound source')
            SoundSource([self.game.visible_sprites],
                        self.game.collision_sprites, (100, 100), 20)

        self.game.visible_sprites.update(dt, actions)

    def render(self):
        self.game.visible_sprites.custom_draw()


class GameWorld(State):
    def __init__(self, game, blocks_update=None, blocks_render=None):
        super().__init__(game, blocks_update, blocks_render)
        self.display_surface = pygame.display.get_surface()

    def startup(self):
        print('GameWorld startup')
        self.color = choice([(200, 50, 0), (0, 200, 50), (50, 0, 200)])
        self.orig_color = self.color

        # sprite group setup
        # self.visible_sprites = YSortCameraGroup()
        self.visible_sprites = pygame.sprite.Group()
        self.alpha_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.collectible_sprites = pygame.sprite.Group()

        # FSM for run-through
        self.fsm = FSM()
        self.fsm.register('prelevel', PreLevel(self))
        self.fsm.register('level', Level(self))
        self.fsm.push('prelevel')

        # Level set up
        # OuterWalls

        Boundary([self.visible_sprites, self.collision_sprites],
                 (0, 0), (300, WALL_WIDTH))
        Boundary([self.visible_sprites, self.collision_sprites],
                 (0, 0), (WALL_WIDTH, 300))
        Boundary([self.visible_sprites, self.collision_sprites],
                 (0, 300-WALL_WIDTH), (300, WALL_WIDTH))
        Boundary([self.visible_sprites, self.collision_sprites],
                 (300-WALL_WIDTH, 0), (WALL_WIDTH, 300))

        # Additional Walls
        Boundary([self.visible_sprites, self.collision_sprites],
                 (0, 150), (150, WALL_WIDTH))
        Boundary([self.visible_sprites, self.collision_sprites],
                 (150, 150), (WALL_WIDTH, 80))

        # Player
        self.player = Player(
            [self.visible_sprites], self.collision_sprites, self.alpha_sprites, (20, 20))

    def suspend(self):
        print('GameWorld suspend')
        # Call when a new state is pushed on top of the current one
        pass

    def wakeup(self):
        print('GameWorld wakeup')
        # Call when the state ontop of this one is popped
        pass

    def cleanup(self):
        print('GameWorld cleanup')
        # Call when state is pop from the stack
        pass

    def update(self):
        # print(self.game.actions)
        if self.game.actions['start']:
            print('push pause')
            self.game.fsm.push('pause')
        if self.game.actions['LCTRL']:
            print('spawn sound source')
            SoundSource([self.alpha_sprites],
                        self.collision_sprites, (randint(10, 290), randint(10, 290)), 20)

        # print(self.game.dt, self.game.actions)
        self.visible_sprites.update(self.game.dt, self.game.actions)
        self.alpha_sprites.update(self.game.dt, self.game.actions)
        # self.game.reset_keys()
        # self.fsm.update()

    def render(self):
        self.display_surface.fill((0, 0, 0))

        # for sprite in self.visible_sprites:
        #     self.display_surface.blit(sprite.image, sprite.rect.topleft)

        self.alpha_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.alpha_surf.blit(pygame.image.load(os.path.join(
            'assets', 'graphics', 'background.png')).convert_alpha(), (0, 0))
        # self.alpha_surf.set_alpha(0)
        for sprite in self.alpha_sprites:
            print('blitting alpha sprite')
            self.alpha_surf.blit(
                sprite.image, sprite.rect.topleft, special_flags=pygame.BLEND_RGBA_MAX)

        self.display_surface.blit(self.alpha_surf, (0, 0))

        # debug(self.player.direction)
        # debug(self.game.actions['analog']['L'], 30)

        if self.game.dt == 0:
            debug('inf')
        else:
            debug(int(1/self.game.dt))
        self.fsm.render()
