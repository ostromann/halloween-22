import pygame


def initialize_joysticks():
    """Initialise all joysticks, returning a list of pygame.joystick.Joystick"""
    joysticks = []

    # Initialise the Joystick sub-module
    pygame.joystick.init()

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        # NOTE: Some examples discard joysticks where the button-count
        #       is zero.  Maybe this is a common problem.
        joysticks.append(joystick)

    # TODO: Print all the statistics about the joysticks
    if (len(joysticks) == 0):
        print("No joysticks found")
    else:
        for i, joystk in enumerate(joysticks):
            print("Joystick %d is named [%s]" % (i, joystk.get_name()))

    return joysticks


class joystick_handler(object):
    def __init__(self, id):
        self.id = id
        self.joy = pygame.joystick.Joystick(id)
        self.name = self.joy.get_name()
        self.joy.init()
        self.numaxes = self.joy.get_numaxes()
        self.numballs = self.joy.get_numballs()
        self.numbuttons = self.joy.get_numbuttons()
        self.numhats = self.joy.get_numhats()

        self.axis = []
        for i in range(self.numaxes):
            self.axis.append(self.joy.get_axis(i))

        self.ball = []
        for i in range(self.numballs):
            self.ball.append(self.joy.get_ball(i))

        self.button = []
        for i in range(self.numbuttons):
            self.button.append(self.joy.get_button(i))

        self.hat = []
        for i in range(self.numhats):
            self.hat.append(self.joy.get_hat(i))
