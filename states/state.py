import pygame


class FSM():
    def __init__(self):
        self.state_stack = []
        self.state_dict = {}
        self.state_transition_queue = []

    def register(self, name, state):
        self.state_dict[name] = state

    def push(self, state):
        self.state_transition_queue.append((self._push, state))

    def pop(self):
        self.state_transition_queue.append((self._pop, ''))

    def switch(self, state):
        self.state_transition_queue.append((self._switch, state))

    def process_state_transition_queue(self):
        # FIFO Queue
        for transition, state in self.state_transition_queue:
            transition(state)
        self.state_transition_queue = []

    def _push(self, state):
        if len(self.state_stack) > 0:
            self.state_stack[-1].suspend()
        self.state_stack.append(self.state_dict[state])
        self.state_stack[-1].startup()

    def _pop(self, _):
        self.state_stack[-1].cleanup()
        self.state_stack.pop()
        self.state_stack[-1].wakeup()

    def _switch(self, state):
        self.state_stack[-1].cleanup()
        self.state_stack.pop()
        self.state_stack.append(self.state_dict[state])
        self.state_stack[-1].startup()

    def update(self):
        self.process_state_transition_queue()
        self.update_states()

    def render(self):
        self.render_states()

    def execute(self):
        self.update()
        self.render()

    def update_states(self):
        self.state_stack[-1].update()

    def render_states(self):
        for state in self.state_stack:
            state.render()


class State():
    def __init__(self, game, blocks_update=False, blocks_render=False):
        '''
        Base state for the game FSM.
        '''
        self.game = game
        self.prev_state = None
        self.display_surface = pygame.display.get_surface()
        self.blocks_update = blocks_update
        self.blocks_render = blocks_render

    def startup(self):
        # Call when state is pushed to the stack
        pass

    def cleanup(self):
        # Call when state is pop from the stack
        pass

    def suspend(self):
        # Call when a new state is pushed on top of the current one
        pass

    def wakeup(self):
        # Call when the state ontop of this one is popped
        pass

    def update(self):
        pass

    def render(self):
        pass
