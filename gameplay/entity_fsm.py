import pygame


class EntityFSM():
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

    def pop_all(self):
        self.state_transition_queue.append((self._pop_all, ''))

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
        if len(self.state_stack):
            self.state_stack[-1].wakeup()

    def _pop_all(self, _):
        '''
        Pop all states but the first one which should always be DefaultState that starts a new state
        '''
        while len(self.state_stack) > 1:
            self.state_stack[-1].cleanup()
            self.state_stack.pop()
        self.state_stack[-1].wakeup()

    def _switch(self, state):
        self.state_stack[-1].cleanup()
        self.state_stack.pop()
        self._push(state)
        # self.state_stack.append(self.state_dict[state])
        # self.state_stack[-1].startup()

    def update(self, dt, actions):
        self.process_state_transition_queue()
        self.state_stack[-1].update(dt, actions)

    def animate(self, dt, actions):
        self.state_stack[-1].animate(dt, actions)

    def execute(self, dt, actions):
        self.update(dt, actions)
        self.animate(dt, actions)

# ===================================


class State():
    '''
    Base State class
    '''

    def __init__(self, sprite):
        self.sprite = sprite
        self.done = False
        pass

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

    def update(self, dt, actions):
        pass

    def animate(self, dt, actions):
        pass


class TimedState(State):
    '''
    Base TimedState class
    Automatically switches to done after duration (in miliseconds) is expired.
    '''

    def __init__(self, sprite, duration):
        super().__init__(sprite)
        self.duration = duration
        pass

    def startup(self):
        self.start_time = pygame.time.get_ticks()

    def check_expiration(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration:
            self.done = True
        self.time_remaining = self.duration - (current_time - self.start_time)

    def update(self, dt, actions):
        self.check_expiration()
        pass
