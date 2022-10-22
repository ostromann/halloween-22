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
        pygame.display.flip()

    def execute(self):
        self.update()
        self.render()

    def update_states(self):
        # TODO: Fix this.
        # First go backwards through the stack until there is a state that is blocking
        # Then go forwards starting from the blocking state to update all remaining states
        # update_lvl = len(self.state_stack) - 1
        # for lvl, state in enumerate(reversed(self.state_stack)):
        #     if state.blocks_update:
        #         print(f'Update {state}, {state.blocks_update}, {update_lvl}')
        #         update_lvl = len(self.state_stack) - lvl
        #         break
        # for state in self.state_stack[update_lvl:]:
        #     state.update()
        self.state_stack[-1].update()

    def render_states(self):
        # render_lvl = len(self.state_stack) - 1
        # for lvl, state in enumerate(reversed(self.state_stack)):
        #     if state.blocks_render:
        #         render_lvl = len(self.state_stack)
        #         break
        for state in self.state_stack:
            # print(f'Render {state}, {state.blocks_render},{render_lvl}')
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
