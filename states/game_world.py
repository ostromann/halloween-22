
import os
import pygame
from random import choice, randint
from debug import debug
from gameplay.enemy import Enemy
from gameplay.utils import blitRotate2

from states.state import State, FSM
from gameplay.camera import YSortCameraGroup
from gameplay.boundary import Boundary
from gameplay.sound import SoundSource, Soundbeam
from gameplay.player import Player
from gameplay.item import Key, Keyhole, Door
from gameplay.footstep import Footstep

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

        # Surface set up
        self.visible_surf = pygame.Surface((WIDTH, HEIGHT))
        self.alpha_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.decay_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.decay_surf.fill((0, 0, 0, 1))
        self.permanent_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        # Surface initialization
        self.alpha_surf.fill((0, 0, 0, 255))

        self.bg_image = pygame.image.load(os.path.join(
            'assets', 'graphics', 'background_2.png'))

        # sprite group setup
        # self.visible_sprites = YSortCameraGroup()
        self.visible_sprites = pygame.sprite.Group()
        self.alpha_sprites = pygame.sprite.Group()
        self.permanent_sprites = pygame.sprite.Group()
        self.player_sprite = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.key_sprites = pygame.sprite.Group()
        self.door_sprites = pygame.sprite.Group()

        self.decay_counter = 0
        # self.collectible_sprites = pygame.sprite.Group()

        # FSM for run-through
        self.fsm = FSM()
        self.fsm.register('prelevel', PreLevel(self))
        self.fsm.register('level', Level(self))
        self.fsm.push('prelevel')

        # Level set up
        # # OuterWalls

        # Boundary([self.visible_sprites, self.collision_sprites],
        #          (0, 0), (300, WALL_WIDTH))
        # Boundary([self.visible_sprites, self.collision_sprites],
        #          (0, 0), (WALL_WIDTH, 300))
        # Boundary([self.visible_sprites, self.collision_sprites],
        #          (0, 300-WALL_WIDTH), (300, WALL_WIDTH))
        # Boundary([self.visible_sprites, self.collision_sprites],
        #          (300-WALL_WIDTH, 0), (WALL_WIDTH, 300))

        # Additional Walls
        Boundary([self.visible_sprites, self.collision_sprites],
                 (0, 140), (200, WALL_WIDTH))
        Boundary([self.visible_sprites, self.collision_sprites],
                 (140, 130), (WALL_WIDTH, 60))
        Boundary([self.visible_sprites, self.collision_sprites],
                 (140, 250), (WALL_WIDTH, 50))

        # Boundary([self.visible_sprites, self.collision_sprites],
        #          (140, 140), (50, WALL_WIDTH))
        Boundary([self.visible_sprites, self.collision_sprites],
                 (250, 140), (50, WALL_WIDTH))

        # # Door
        # Door([self.visible_sprites, self.collision_sprites, self.door_sprites],
        #      (140, 190), (WALL_WIDTH-10, 60), True, id=1)

        # Door([self.visible_sprites, self.collision_sprites, self.door_sprites],
        #      (190, 140), (60, WALL_WIDTH-10), False, id=1)

        # # Keyhole
        # Keyhole([self.visible_sprites], self.key_sprites,
        #         self.door_sprites, (170, 230), id=1)

        # Player
        self.player = Player(
            [self.visible_sprites, self.player_sprite], self.collision_sprites, (250, 250), self.trigger_spawn_footprint, self.trigger_spawn_soundsource)

        # Key
        Key([self.visible_sprites, self.key_sprites], [self.collision_sprites],
            (200, 80), self.player, id=1)
        # # Enemy
        # Enemy([self.visible_sprites], self.collision_sprites, self.alpha_sprites,
        #       self.alpha_sprites, (30, 80), [(250, 80), (30, 80)], self.player)

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

        self.visible_sprites.update(self.game.dt, self.game.actions)
        self.permanent_sprites.update(self.game.dt, self.game.actions)
        self.alpha_sprites.update(self.game.dt, self.game.actions)
        self.game.reset_keys()
        # self.fsm.update()

    def render(self):

        # self.visible_surf.blit(self.bg_image, (0, 0))
        self.visible_surf.fill((50, 50, 50))
        for sprite in self.visible_sprites:
            self.visible_surf.blit(sprite.image, sprite.rect.topleft)
            # draw outline rect for debugging
            # pygame.draw.rect(self.visible_surf, (255, 0, 0), sprite.rect, 2)

        for sprite in self.permanent_sprites:
            # TODO: Add fade out to this
            blitRotate2(self.permanent_surf, sprite.image,
                        sprite.rect.topleft, sprite.angle)
            # self.permanent_surf.blit(sprite.image, sprite.rect.topleft)

        for sprite in self.alpha_sprites:
            self.alpha_surf.blit(
                sprite.image, sprite.rect.topleft, special_flags=pygame.BLEND_RGBA_SUB)

        # Fade out to black with decay_surf
        self.decay_counter += self.game.dt
        if self.decay_counter >= FADEOUT_DECAY_TIME:
            self.decay_counter = 0
            self.alpha_surf.blit(self.decay_surf, (0, 0),
                                 special_flags=pygame.BLEND_RGBA_ADD)

        self.display_surface.blit(self.visible_surf, (0, 0))
        self.display_surface.blit(self.alpha_surf, (0, 0))
        self.display_surface.blit(self.permanent_surf, (0, 0))

        if self.game.dt == 0:
            debug('inf')
        else:
            debug(int(1/self.game.dt))
        self.fsm.render()

    def trigger_spawn_footprint(self, pos, direction, volume, left, origin):
        footstep = Footstep([self.permanent_sprites], pos,
                            direction, volume, left, origin)
        self.trigger_spawn_soundsource(
            footstep.sound_source_pos, volume, 'player')

    def trigger_spawn_soundsource(self, pos, volume, origin):
        SoundSource([self.alpha_sprites], self.collision_sprites, pos,
                    volume, origin)
