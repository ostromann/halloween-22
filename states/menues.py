import pygame
from states.state import State
from settings import *
# from states.game_world_states_minimal import GameWorld


class MainMenu(State):
    def __init__(self, game, blocks_update=None, blocks_render=None):
        super().__init__(game, blocks_update, blocks_render)

    def startup(self):
        # get the items from the MainMenu
        pass

    def suspense(self):
        # basically do nothing
        pass

    def wakeup(self):
        # set back pointer to first item
        pass

    def cleanup(self):
        # basically do nothing
        pass

    def update(self):
        if self.game.actions['ENTER']:
            self.game.fsm.switch('run-through')
        self.game.reset_keys()

    def render(self):
        self.game.game_canvas.fill((0, 0, 0))
        self.game.draw_text(self.game.game_canvas, "echo escape", 'title',
                            (255, 255, 255), self.game.GAME_W/2, self.game.GAME_H*2/5)

        self.game.draw_text(self.game.game_canvas, "Press [ENTER] to start the escape.", 'main',
                            (255, 255, 255), self.game.GAME_W/2, 3*self.game.GAME_H/4)


class PauseMenu(State):
    def __init__(self, game, blocks_update=None, blocks_render=None):
        super().__init__(game, blocks_update, blocks_render)

    def startup(self):
        print('PauseMenu startup')
        self.menu_surf = pygame.Surface(
            (self.game.GAME_W * 0.5, self.game.GAME_H * 0.5))

    def suspense(self):
        print('PauseMenu suspend')
        # basically do nothing
        pass

    def wakeup(self):
        print('PauseMenu wakeup')
        # set back pointer to first item
        pass

    def cleanup(self):
        print('PauseMenu clean up')
        # basically do nothing
        pass

    def update(self):
        if self.game.actions['ENTER']:
            self.game.fsm.pop()
        self.game.reset_keys()

    def render(self):
        self.menu_surf.fill((255, 255, 255))
        self.game.draw_text(self.menu_surf, "Menu", (0, 0, 0), self.menu_surf.get_width(
        ) // 2, self.menu_surf.get_height() // 2)
        self.display_surface.blit(
            self.menu_surf, (self.game.GAME_W * 0.25, self.game.GAME_H * 0.25))


class DeathScreen(State):
    def __init__(self, game, blocks_update=None, blocks_render=None):
        super().__init__(game, blocks_update, blocks_render)

    def startup(self):
        print('now in  death screen')
        # get the items from the MainMenu
        pass

    def suspense(self):
        # basically do nothing
        pass

    def wakeup(self):
        # set back pointer to first item
        pass

    def cleanup(self):
        # basically do nothing
        pass

    def update(self):
        print('updating death screen')
        print(self.game.fsm.state_stack)
        if self.game.actions['ENTER']:
            self.game.fsm.switch('run-through')
        self.game.reset_keys()

    def render(self):
        self.game.game_canvas.fill((0, 0, 0))
        self.game.draw_text(self.game.game_canvas, "you died", 'title',
                            (223, 12, 0), self.game.GAME_W/2, self.game.GAME_H/5*2)

        self.game.draw_text(self.game.game_canvas, "Press [ENTER] to try again.", 'main',
                            (223, 12, 0), self.game.GAME_W/2, 3*self.game.GAME_H/4)


class LevelIntro(State):
    def __init__(self, game, blocks_update=None, blocks_render=None):
        super().__init__(game, blocks_update, blocks_render)

    def startup(self):
        self.line_start_time = pygame.time.get_ticks()
        self.print_line_index = 1
        self.all_lines_printed = False
        # get the items from the MainMenu
        pass

    def suspense(self):
        # basically do nothing
        pass

    def wakeup(self):
        # set back pointer to first item
        pass

    def cleanup(self):
        # basically do nothing
        pass

    def update(self):
        if self.all_lines_printed:
            if self.game.actions['ENTER']:
                self.game.fsm.pop()
        self.game.reset_keys()

    def render(self):
        self.game.game_canvas.fill((0, 0, 0))
        text = level_data[self.game.level]['intro_text']

        start_height = self.game.GAME_H/4
        row_offset = 40

        current_time = pygame.time.get_ticks()
        if current_time - self.line_start_time >= LINE_DURATION:
            self.line_start_time = pygame.time.get_ticks()
            self.print_line_index += 1

        if self.print_line_index < len(text):
            for i, line in enumerate(text[:self.print_line_index]):
                self.game.draw_text(self.game.game_canvas, line, 'main',
                                    (255, 255, 255), self.game.GAME_W/2, start_height + i * row_offset)
        else:
            self.all_lines_printed = True
