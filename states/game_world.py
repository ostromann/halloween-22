
import os
import pygame
from debug import debug
from pytmx.util_pygame import load_pygame

from gameplay.enemy import Enemy
from gameplay.soundplayer import SoundPlayer
from gameplay.tile import LevelGoal
from states.state import State
from gameplay.boundary import Boundary
from gameplay.sound import SoundSource
from gameplay.player import Player
from gameplay.objects import Key, Keyhole, Door, AmbientSound
from gameplay.footstep import FootprintPlayer
from states.menues import EscapedScreen, LevelIntro

from gameplay.utils import blitRotate2, get_closest_sprite_of_group, get_distance_direction_a_to_b
from settings import *


class GameWorld(State):
    def __init__(self, game, blocks_update=None, blocks_render=None):
        super().__init__(game, blocks_update, blocks_render)
        self.display_surface = self.game.game_canvas

    def load_level(self, level_num):
        path = os.path.join(
            'assets', 'levels', f'level_{level_num}.tmx')
        tmx_data = load_pygame(path)

        # Game logic layers first!
        layer = tmx_data.get_layer_by_name('Game_Logic')
        for obj in layer:
            if obj.name == 'player_spawn':
                self.player = Player(
                    [self.visible_sprites], self.collision_sprites, (obj.x, obj.y), self.trigger_spawn_footprint, self.trigger_spawn_soundsource, self.trigger_sound, self.pickup_item)
            if obj.name == 'enemy_spawn':
                self.enemy = Enemy([self.visible_sprites], self.collision_sprites, self.alpha_sprites, (obj.x, obj.y), [
                ], self.player, self.trigger_spawn_footprint, self.trigger_spawn_soundsource, self.trigger_sound, self.trigger_screen_shake)
            if obj.name == 'level_goal':
                self.level_goal = LevelGoal(obj, [self.visible_sprites])

        layer = tmx_data.get_layer_by_name('Enemy_WP')
        for obj in layer:
            id = obj.name.split('_')[-1]
            self.enemy.waypoints.append((obj.x, obj.y))

        for layer in tmx_data.layers:
            if layer.name == 'Sound_Sources':
                for obj in layer:
                    name, volume, interval, randomness = obj.name.split('_')
                    AmbientSound(self.sound_sprites, name, (obj.x, obj.y), interval,
                                 randomness, volume, self.trigger_sound)
            if layer.name == 'Objects':
                for obj in layer:
                    if obj.name.split('_')[1] == 'door':
                        color, type, rotate, closed = obj.name.split('_')
                        Door([self.visible_sprites, self.collision_sprites, self.door_sprites], self.visible_sprites, self.collision_sprites,
                             (obj.x, obj.y), (obj.width, obj.height), rotate, closed, color, self.trigger_sound)
                    elif obj.name.split('_')[1] == 'key':
                        color, type = obj.name.split('_')
                        surf = obj.image
                        Key([self.visible_sprites, self.key_sprites], [
                            self.collision_sprites], (obj.x, obj.y), self.player, surf, color=color)
                    elif obj.name.split('_')[1] == 'keyhole':
                        color, type = obj.name.split('_')
                        surf = obj.image
                        Keyhole([self.visible_sprites], self.key_sprites,
                                self.door_sprites, (obj.x, obj.y), surf, color=color)
            if layer.name == 'Boundary_Objects':
                for obj in layer:
                    Boundary([self.visible_sprites, self.collision_sprites],
                             (obj.x, obj.y), (obj.width, obj.height))

    def startup(self):
        # Surface set up
        self.visible_surf = pygame.Surface((WIDTH, HEIGHT))
        self.alpha_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.decay_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.decay_surf.fill((0, 0, 0, 1))
        self.footprint_decay_surf = pygame.Surface(
            (WIDTH, HEIGHT), pygame.SRCALPHA)
        self.footprint_decay_surf = pygame.Surface(
            (WIDTH, HEIGHT), pygame.SRCALPHA)
        self.footprint_decay_surf.fill((0, 0, 0, 254))
        self.footprint_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        # Surface initialization
        self.alpha_surf.fill((0, 0, 0, 255))

        # sprite group setup
        self.visible_sprites = pygame.sprite.Group()
        self.alpha_sprites = pygame.sprite.Group()
        self.footprint_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.key_sprites = pygame.sprite.Group()
        self.door_sprites = pygame.sprite.Group()
        self.sound_sprites = pygame.sprite.Group()

        self.sound_player = SoundPlayer()
        self.footprint_player = FootprintPlayer()
        self.decay_counter = 0

        # Level set up
        self.load_level(self.game.level)

        # Show Level Intro screen
        self.game.fsm.register('level_intro', LevelIntro(
            self.game))
        self.game.fsm.push('level_intro')

    def suspend(self):
        # Call when a new state is pushed on top of the current one
        pass

    def wakeup(self):
        # Call when the state ontop of this one is popped
        pass

    def cleanup(self):
        # Call when state is pop from the stack
        pass

    def update(self):
        self.visible_sprites.update(self.game.dt, self.game.actions)
        self.footprint_sprites.update(self.game.dt, self.game.actions)
        self.alpha_sprites.update(self.game.dt, self.game.actions)
        self.sound_sprites.update()
        self.game.reset_keys()
        self.check_death()
        self.check_level_goal()

    def render(self):

        self.visible_surf.fill('grey')
        for sprite in self.visible_sprites:
            self.visible_surf.blit(sprite.image, sprite.rect.topleft)
            # # draw outline rect for debugging
            # pygame.draw.rect(self.visible_surf, (133, 50, 0), sprite.rect, 1)
            # pygame.draw.rect(self.visible_surf, (255, 0, 0), sprite.hitbox, 1)

        for sprite in self.footprint_sprites:
            blitRotate2(self.footprint_surf, sprite.image,
                        sprite.rect.topleft, sprite.angle)

        for sprite in self.alpha_sprites:
            self.alpha_surf.blit(
                sprite.image, sprite.rect.topleft, special_flags=pygame.BLEND_RGBA_SUB)
            # pygame.draw.rect(self.visible_surf, (255, 0, 0), sprite.rect, 1)

        # Fade outs
        self.decay_counter += self.game.dt
        if self.decay_counter >= FADEOUT_DECAY_TIME:
            # Fade out alpha surf to black with decay_surf
            self.decay_counter = 0
            self.alpha_surf.blit(self.decay_surf, (0, 0),
                                 special_flags=pygame.BLEND_RGBA_ADD)
            # Fade out footprints
            self.footprint_surf.blit(self.decay_surf, (0, 0),
                                     special_flags=pygame.BLEND_RGBA_SUB)

        self.display_surface.blit(self.visible_surf, (0, 0))
        self.display_surface.blit(self.alpha_surf, (0, 0))
        self.display_surface.blit(self.footprint_surf, (0, 0))

        if ENEMY_DEBUG:
            if len(self.enemy.entity_fsm.state_stack) > 0:
                debug(self.display_surface,
                      f'{self.enemy.entity_fsm.state_stack[-1]}')
            debug(self.display_surface,
                  f'{len(self.enemy.entity_fsm.state_stack)}', 30)
            debug(self.display_surface,
                  f'{self.enemy.get_loudest_source()}', 60)
        if FPS_DEBUG:
            if self.game.dt == 0:
                debug(self.display_surface, 'inf', 680, 440)
            else:
                debug(self.display_surface, int(1/self.game.dt))

    # ---- SOUNDS ----
    def trigger_sound(self, pos, volume, sound_type):
        self.sound_player.play_random_sound(pos, volume, sound_type)
        self.trigger_spawn_soundsource(pos, volume, sound_type)

    def trigger_spawn_footprint(self, pos, direction, volume, left, origin):
        # TODO: Check which ground material there is and adjust sounds for that
        # default_material = 'metal'
        # if origin == 'player':
        #     self.player.rect.colliderect()

        footprint = self.footprint_player.create_footprint([self.footprint_sprites], pos,
                                                           direction, volume, left, origin)
        self.trigger_sound(footprint.sound_source_pos,
                           volume, f'{origin}_metal')

    def trigger_spawn_soundsource(self, pos, volume, origin):
        SoundSource([self.alpha_sprites], self.collision_sprites, pos,
                    volume, origin)

    def trigger_screen_shake(self, intensity):
        self.game.screen_shake = intensity

    def pickup_item(self):
        closest_item = get_closest_sprite_of_group(
            self.player, self.key_sprites)
        distance, _ = get_distance_direction_a_to_b(
            self.player.pos, closest_item.pos)
        if distance < OBJECT_PULLING_RADIUS:
            return closest_item
        else:
            return None

    def check_death(self):
        if hasattr(self, 'enemy'):
            if self.player.hitbox.colliderect(self.enemy.hitbox):
                self.game.fsm.register(
                    'run-through', GameWorld(self.game, blocks_update=True))
                self.game.fsm.switch('death')

    def check_level_goal(self):
        if self.player.hitbox.colliderect(self.level_goal.rect):
            self.game.level += 1
            if self.game.level <= 4:
                self.game.fsm.register(
                    'run-through', GameWorld(self.game, blocks_update=True))
                self.game.fsm.switch('run-through')
            else:
                self.game.fsm.register('escaped', EscapedScreen(
                    self.game, blocks_update=True))
                self.game.fsm.switch('escaped')
