import os
import time
import pygame
import json
from states.game_world import GameWorld

from joysticks import initialize_joysticks
from settings import *
from states.menues import MainMenu, PauseMenu
from states.state import FSM
from debug import debug


class Game():
    def __init__(self, joysticks):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.GAME_W, self.GAME_H = WIDTH, HEIGHT
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = WIDTH, HEIGHT
        self.game_canvas = pygame.Surface((self.GAME_W, self.GAME_H))
        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.running, self.playing = True, True
        self.actions = {
            'left': False,
            'right': False,
            'up': False,
            'down': False,
            'space': False,
            'action1': False,
            'LCTRL': False,
            'LSHIFT': False,
            'start': False,
            'TAB': False,
            # 'x': False,
            # 'square': False,
            # 'circle': False,
            # 'triangle': False
        }
        self.joysticks = joysticks
        if len(self.joysticks) > 0:
            self.joystick_detected = True
            self.initialize_joysticks()

        self.dt, self.prev_time, self.cumulative_dt = 0, 0, 0

        self.fsm = FSM()
        self.fsm.register('main_menu', MainMenu(self))
        self.fsm.register('run-through', GameWorld(self,
                          blocks_render=True, blocks_update=True))
        self.fsm.register('pause', PauseMenu(self, blocks_update=True))
        self.fsm.push('main_menu')
        self.load_assets()

    def initialize_joysticks(self):
        print('initializing joysticks:', self.joysticks)
        self.joysticks_dict = {}
        for i, joystick in enumerate(self.joysticks):
            joystick_dict = {}
            joystick_dict = {
                'name': joystick.get_name(),
                'analog_keys': {0: 0, 1: 0, 2: 0, 3: 0, 4: -1, 5: -1},
                'button_keys': self.get_joystick_button_keys(joystick.get_name()),
            }
            self.joysticks_dict[i] = joystick_dict
        print(self.joysticks_dict)

        # TODO: Handle multiple gamepads others than PS4 Controller
        self.joystick = self.joysticks_dict[0]
        self.button_keys = self.joystick['button_keys']
        self.analog_keys = self.joystick['analog_keys']

    def get_joystick_button_keys(self, name):
        if name == 'PS4 Controller':
            with open(os.path.join("ps4_keys.json"), 'r+') as file:
                button_keys = json.load(file)
        else:
            button_keys = {}
        return button_keys

    def game_loop(self):
        while self.playing:
            self.clock.tick(FPS)
            self.get_dt()
            self.get_events()
            self.fsm.execute()
            # self.update()
            # self.render()

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
                    self.actions['left'] = True
                if event.key == pygame.K_d:
                    self.actions['right'] = True
                if event.key == pygame.K_w:
                    self.actions['up'] = True
                if event.key == pygame.K_s:
                    self.actions['down'] = True
                if event.key == pygame.K_SPACE:
                    self.actions['space'] = True
                if event.key == pygame.K_LCTRL:
                    self.actions['LCTRL'] = True
                if event.key == pygame.K_LSHIFT:
                    self.actions['LSHIFT'] = True
                if event.key == pygame.K_RETURN:
                    self.actions['start'] = True
                if event.key == pygame.K_TAB:
                    self.actions['TAB'] = True

            # TODO: instead get keys pressed for lshift and ctrl
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.actions['left'] = False
                if event.key == pygame.K_d:
                    self.actions['right'] = False
                if event.key == pygame.K_w:
                    self.actions['up'] = False
                if event.key == pygame.K_s:
                    self.actions['down'] = False
                if event.key == pygame.K_SPACE:
                    self.actions['space'] = False
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
            self.font_dir, "BLACKOUT.TTF"), 60)
        self.main_font = pygame.font.Font(os.path.join(
            self.font_dir, "BLACKOUT.TTF"), 12)

    def update(self):
        self.state_stack[-1].update(self.dt, self.actions)

    def render(self):
        self.state_stack[-1].render()
        # Render current state to the screen
        # self.screen.blit(pygame.transform.scale(self.game_canvas,(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0,0))
        if self.dt == 0:
            debug('inf')
        else:
            debug(int(1/self.dt))

    def get_dt(self):
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now

    def draw_text(self, surface, text, color, x, y):
        text_surface = self.title_font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)

    def reset_keys(self):
        for action in ['LCTRL', 'LSHIFT', 'space', 'start', 'TAB']:
            self.actions[action] = False


if __name__ == "__main__":
    joysticks = initialize_joysticks()
    g = Game(joysticks)
    while g.running:
        g.game_loop()
