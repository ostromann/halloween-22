
import os
import pygame
from random import choice, randint
from debug import debug
from pytmx.util_pygame import load_pygame

from gameplay.enemy import Enemy
from gameplay.tile import Tile
from states.state import State, FSM
from gameplay.camera import YSortCameraGroup
from gameplay.boundary import Boundary
from gameplay.sound import SoundSource, Soundbeam
from gameplay.player import Player
from gameplay.objects import Key, Keyhole, Door
from gameplay.footstep import Footstep

from gameplay.utils import blitRotate2
from settings import *


class GameWorld(State):
    def __init__(self, game, blocks_update=None, blocks_render=None):
        super().__init__(game, blocks_update, blocks_render)
        # self.display_surface = pygame.display.get_surface()
        self.display_surface = self.game.game_canvas
        print(self.display_surface)

    def load_level(self, path):
        tmx_data = load_pygame(path)

        # Game logic layers first!
        layer = tmx_data.get_layer_by_name('Game_Logic')
        for obj in layer:
            if obj.name == 'player_spawn':
                self.player = Player(
                    [self.visible_sprites, self.player_sprite], self.collision_sprites, (obj.x, obj.y), self.trigger_spawn_footprint, self.trigger_spawn_soundsource)
            if obj.name == 'enemy_spawn':
                Enemy([self.visible_sprites], self.collision_sprites, (obj.x, obj.y), [
                ], self.player, self.trigger_spawn_footprint, self.trigger_spawn_soundsource)

        for layer in tmx_data.layers:
            if layer.name == 'Boundary':
                for x, y, surf in layer.tiles():
                    Tile((x*TILESIZE, y*TILESIZE), surf, [
                         self.visible_sprites, self.collision_sprites])

            if layer.name == 'Sound_Sources':
                for obj in layer:
                    print(f'Soundsource at {obj.x, obj.y}')
            if layer.name == 'Grating_Objects':
                for obj in layer:
                    for i in range(0, 4):
                        pos = (obj.x + i*4/20, obj.y+TILESIZE/2-3)
                        tmp_surf = pygame.Surface((6, 6))
                        Tile(pos, tmp_surf, [
                             self.visible_sprites, self.collision_sprites])
            if layer.name == 'Sound_Sources':
                pass
            if layer.name == 'Objects':
                for obj in layer:
                    if obj.name.split('_')[1] == 'door':
                        color, type, id, closed = obj.name.split('_')
                        print(obj.name, closed)
                        Door([self.visible_sprites, self.door_sprites], self.visible_sprites, self.collision_sprites,
                             (obj.x, obj.y), (obj.width, obj.height), closed, color=color)
                    elif obj.name.split('_')[1] == 'key':
                        color, type, id = obj.name.split('_')
                        Key([self.visible_sprites, self.key_sprites], [
                            self.collision_sprites], (obj.x, obj.y), self.player, color=color)
                    elif obj.name.split('_')[1] == 'keyhole':
                        color, type, id = obj.name.split('_')
                        Keyhole([self.visible_sprites], self.key_sprites,
                                self.door_sprites, (obj.x, obj.y), color=color)

    def startup(self):
        # Surface set up
        self.visible_surf = pygame.Surface((WIDTH, HEIGHT))
        self.alpha_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.decay_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.decay_surf.fill((0, 0, 0, 1))
        self.footprint_decay_surf = pygame.Surface(
            (WIDTH, HEIGHT), pygame.SRCALPHA)
        self.footprint_decay_surf.fill((255, 255, 255, 1))
        self.permanent_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        # Surface initialization
        self.alpha_surf.fill((0, 0, 0, 255))

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
        # self.fsm = FSM()
        # self.fsm.register('prelevel', PreLevel(self))
        # self.fsm.register('level', Level(self))
        # self.fsm.push('prelevel')

        # Level set up
        tmx_data = self.load_level(os.path.join(
            'assets', 'levels', 'template.tmx'))

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

        self.visible_surf.fill('white')
        for sprite in self.visible_sprites:
            self.visible_surf.blit(sprite.image, sprite.rect.topleft)
            # draw outline rect for debugging
            pygame.draw.rect(self.visible_surf, (133, 50, 0), sprite.rect, 1)
            pygame.draw.rect(self.visible_surf, (255, 0, 0), sprite.hitbox, 1)

        for sprite in self.permanent_sprites:
            # TODO: Add fade out to this
            blitRotate2(self.permanent_surf, sprite.image,
                        sprite.rect.topleft, sprite.angle)
            # self.permanent_surf.blit(sprite.image, sprite.rect.topleft)

        for sprite in self.alpha_sprites:
            self.alpha_surf.blit(
                sprite.image, sprite.rect.topleft, special_flags=pygame.BLEND_RGBA_SUB)

        # Fade outs
        self.decay_counter += self.game.dt
        if self.decay_counter >= FADEOUT_DECAY_TIME:
            # Fade out alpha surf to black with decay_surf
            self.decay_counter = 0
            self.alpha_surf.blit(self.decay_surf, (0, 0),
                                 special_flags=pygame.BLEND_RGBA_ADD)
            # Fade out footprints
            # print('fade out footprints')
            # self.permanent_surf.blit(self.decay_surf, (0, 0),
            #                          special_flags=pygame.BLEND_RGBA_SUB)

        self.display_surface.blit(self.visible_surf, (0, 0))
        self.display_surface.blit(self.alpha_surf, (0, 0))
        self.display_surface.blit(self.permanent_surf, (0, 0))

        # debug(
        #     f'{self.player.status}: {self.player.direction}({self.player.last_direction})')
        if self.game.dt == 0:
            debug('inf', 680, 440)
        else:
            debug(int(1/self.game.dt), 680, 440)
        # self.fsm.render()

    def trigger_spawn_footprint(self, pos, direction, volume, left, origin):
        footstep = Footstep([self.permanent_sprites], pos,
                            direction, volume, left, origin)
        self.trigger_spawn_soundsource(
            footstep.sound_source_pos, volume, 'player')

    def trigger_spawn_soundsource(self, pos, volume, origin):
        SoundSource([self.alpha_sprites], self.collision_sprites, pos,
                    volume, origin)
