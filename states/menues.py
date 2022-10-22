import pygame
from states.state import State
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
        if self.game.actions["start"] or self.game.actions['x']:
            self.game.fsm.push('run-through')
        self.game.reset_keys()

    def render(self):
        self.display_surface.fill((0, 0, 0))
        self.game.draw_text(self.display_surface, "echo escape",
                            (255, 255, 255), self.game.SCREEN_WIDTH/2, self.game.SCREEN_HEIGHT/4)


class PauseMenu(State):
    def __init__(self, game, blocks_update=None, blocks_render=None):
        super().__init__(game, blocks_update, blocks_render)

    def startup(self):
        print('PauseMenu startup')
        self.menu_surf = pygame.Surface(
            (self.game.SCREEN_WIDTH * 0.5, self.game.SCREEN_HEIGHT * 0.5))

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
        if self.game.actions['start'] or self.game.actions['circle']:
            self.game.fsm.pop()
        self.game.reset_keys()
        # new_state.enter_state()
        # self.update_cursor(actions)
        # if actions["action1"]:
        #     self.transition_state()
        # if actions["action2"]:
        #     self.exit_state()
        # self.game.reset_keys()

    def render(self):
        # self.prev_state.render()
        self.menu_surf.fill((255, 255, 255))
        self.game.draw_text(self.menu_surf, "Menu", (0, 0, 0), self.menu_surf.get_width(
        ) // 2, self.menu_surf.get_height() // 2)
        self.display_surface.blit(
            self.menu_surf, (self.game.SCREEN_WIDTH * 0.25, self.game.SCREEN_HEIGHT * 0.25))
