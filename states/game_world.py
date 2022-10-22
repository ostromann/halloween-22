
from states.state import State, FSM
from random import choice


class PreLevel(State):
    def __init__(self, game, blocks_update=None, blocks_render=None):
        super().__init__(game, blocks_update, blocks_render)

    def startup(self):
        # Set spawn location and time for enemies
        print('PreLevel startup')
        # Call when state is pushed to the stack
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
        pass

    def render(self):
        pass


class PostLevel(State):
    def __init__(self, game, blocks_update=None, blocks_render=None):
        super().__init__(game, blocks_update, blocks_render)

    def startup(self):
        print('PostLevel startup')
        # Call when state is pushed to the stack
        pass

    def cleanup(self):
        print('PostLevel cleanup')
        # Call when state is pop from the stack
        pass

    def suspend(self):
        print('PostLevel suspend')
        # Call when a new state is pushed on top of the current one
        pass

    def wakeup(self):
        print('Level wakeup')
        # Call when the state ontop of this one is popped
        pass

    def update(self):
        pass

    def render(self):
        pass


class Shop(State):
    def __init__(self, game, blocks_update=None, blocks_render=None):
        super().__init__(game, blocks_update, blocks_render)

    def startup(self):
        print('Shop startup')
        # Call when state is pushed to the stack
        pass

    def cleanup(self):
        print('Shop cleanup')
        # Call when state is pop from the stack
        pass

    def suspend(self):
        print('Shop suspend')
        # Call when a new state is pushed on top of the current one
        pass

    def wakeup(self):
        print('Shop wakeup')
        # Call when the state ontop of this one is popped
        pass

    def update(self):
        pass

    def render(self):
        pass


class GameWorld(State):
    def __init__(self, game, blocks_update=None, blocks_render=None):
        super().__init__(game, blocks_update, blocks_render)

    def startup(self):
        print('GameWorld startup')
        self.color = choice([(200, 50, 0), (0, 200, 50), (50, 0, 200)])
        self.orig_color = self.color

        # level settings
        self.level_start_time = 0
        self.current_time = 0
        self.level_duration = 10
        self.time_left = self.level_duration

        # FSM for run-through
        self.fsm = FSM()
        self.fsm.register('prelevel', PreLevel(self))
        self.fsm.register('level', Level(self))
        self.fsm.register('postlevel', PostLevel(self))
        self.fsm.push('prelevel')

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

    def tick_timer(self, dt):
        self.current_time += dt
        self.time_left = self.level_duration - self.current_time

    def update(self):
        # print(self.game.actions)
        if self.game.actions['start']:
            print('push pause')
            self.game.fsm.push('pause')
        if self.game.actions['left']:
            self.color = (0, 0, 0)
            self.fsm.switch('level')
        elif self.game.actions['right']:
            self.color = (255, 255, 255)
            self.fsm.switch('shop')
        else:
            self.color = self.orig_color
        self.game.reset_keys()
        self.fsm.execute()

    def render(self):
        # self.state_stack[-1].render()
        self.display_surface.fill(self.color)
