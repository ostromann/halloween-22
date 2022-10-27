import os
import time
import pygame
import json
from states.game_world import GameWorld

from settings import *
from states.menues import MainMenu, PauseMenu, DeathScreen
from states.state import FSM
from debug import debug


class Game():
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.GAME_W, self.GAME_H = WIDTH, HEIGHT
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = WIDTH*2, HEIGHT*2
        self.game_canvas = pygame.Surface(
            (self.GAME_W, self.GAME_H), pygame.SRCALPHA)
        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.running, self.playing = True, True
        self.actions = {
            'w': False,
            'a': False,
            's': False,
            'd': False,
            'q': False,
            'e': False,
            'SPACE': False,
            'LCTRL': False,
            'LSHIFT': False,
            'ENTER': False,
            'TAB': False,
        }
        self.dt, self.prev_time, self.cumulative_dt = 0, 0, 0

        # level index
        self.level = 3

        # State machine set up
        self.fsm = FSM()
        self.fsm.register('main_menu', MainMenu(self))
        self.fsm.register('run-through', GameWorld(self,
                          blocks_render=True, blocks_update=True))
        self.fsm.register('pause', PauseMenu(self, blocks_update=True))
        self.fsm.register('death', DeathScreen(self, blocks_update=True))
        self.fsm.push('main_menu')
        self.load_assets()

        # sound
        main_sound = pygame.mixer.Sound('assets/audio/music/main.ogg')
        main_sound.set_volume(0)
        main_sound.play(loops=-1)

    def game_loop(self):
        while self.playing:
            self.clock.tick(FPS)
            self.get_dt()
            self.get_events()
            self.fsm.update()
            self.render()

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
                    self.running = False
                if event.key == pygame.K_a:
                    self.actions['a'] = True
                if event.key == pygame.K_d:
                    self.actions['d'] = True
                if event.key == pygame.K_w:
                    self.actions['w'] = True
                if event.key == pygame.K_s:
                    self.actions['s'] = True
                if event.key == pygame.K_SPACE:
                    self.actions['SPACE'] = True
                if event.key == pygame.K_LCTRL:
                    self.actions['LCTRL'] = True
                if event.key == pygame.K_LSHIFT:
                    self.actions['LSHIFT'] = True
                if event.key == pygame.K_RETURN:
                    self.actions['ENTER'] = True
                if event.key == pygame.K_TAB:
                    self.actions['TAB'] = True

            # TODO: instead get keys pressed for lshift and ctrl
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.actions['a'] = False
                if event.key == pygame.K_d:
                    self.actions['d'] = False
                if event.key == pygame.K_w:
                    self.actions['w'] = False
                if event.key == pygame.K_s:
                    self.actions['s'] = False
                if event.key == pygame.K_SPACE:
                    self.actions['SPACE'] = False
                if event.key == pygame.K_LCTRL:
                    self.actions['LCTRL'] = False
                if event.key == pygame.K_LSHIFT:
                    self.actions['LSHIFT'] = False
                if event.key == pygame.K_RETURN:
                    self.actions['start'] = False
                if event.key == pygame.K_TAB:
                    self.actions['TAB'] = False

    def load_assets(self):
        # Create pointers to directories
        self.assets_dir = os.path.join("assets")
        # self.sprite_dir = os.path.join(self.assets_dir, "sprites")
        self.font_dir = os.path.join(self.assets_dir, "fonts")
        self.title_font = pygame.font.Font(os.path.join(
            self.font_dir, "BLACKOUT.TTF"), 140)
        self.main_font = pygame.font.Font(os.path.join(
            self.font_dir, "Oswald-Medium.ttf"), 30)

    def update(self):
        self.state_stack[-1].update(self.dt, self.actions)

    def render(self):
        self.fsm.render()
        # self.state_stack[-1].render()
        # TODO: Scaling the final screen
        self.screen.blit(pygame.transform.scale(
            self.game_canvas, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0, 0))
        pygame.display.flip()

    def get_dt(self):
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now

    def draw_text(self, surface, text, font_type, color, x, y):

        if font_type == 'title':
            font = self.title_font
        elif font_type == 'main':
            font = self.main_font
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)

    def reset_keys(self):
        for action in ['SPACE', 'ENTER', 'TAB']:
            self.actions[action] = False


if __name__ == "__main__":
    g = Game()
    while g.running:
        g.game_loop()
