from .System import *

class MerryGoRound(System):
    """
        A class to simulate a single light which "moves" along a predefined path. Actually, this class operates on a list of light sources, and emulates the movement of one of them by changing which single light is on at any given time.
        This class could be used in other ways, but only works as intended if the list of lights is organised correctly, e.g. when the list of lights creates a circular path.
    """
    def __init__(self, light_sources, period, is_on_ind=0):
        """
            __init__(self, light_sources, period, is_on_ind=0)

            :param light_sources: The list of light sources used by the ``MerryGoRound``.
            :type light_sources: list(LightSource)

            :param period: The time taken for the light which is switched on to change.
            :type period: float

            :param is_on_ind: The index in the list of light sources of the light which is initially switched on. Defaults to ``0``.
            :type is_on_ind: int
        """
        self.light_sources = light_sources
        self.timer = 0
        self.period = period
        self.is_on_ind = is_on_ind
        self.initial_is_on_ind = is_on_ind

        for l in light_sources:
            l.is_on = False
            l.initial_is_on = False
        self.light_sources[self.is_on_ind].is_on = True
        self.light_sources[self.is_on_ind].initial_is_on = True

        super().__init__()

    def step(self, dt):
        """
            Step ``MerryGoRound`` forward in time.

            :param dt: The interval of time to integrate the controller over.
            :type dt: float
        """
        self.timer += dt
        if self.timer > self.period:
            self.light_sources[self.is_on_ind].is_on = False
            self.is_on_ind += 1
            if self.is_on_ind >= len(self.light_sources):
                self.is_on_ind = 0
            self.light_sources[self.is_on_ind].is_on = True
            self.timer = 0

    # an only minimal reset method
    def reset(self):
        """
            Reset merry go round, so it can be reused in later simulation runs.
        """
        self.is_on_ind = self.initial_is_on_ind
        self.timer = 0

    def draw(self, ax):
        # a dummy draw method - light sources have their own draw methods
        pass

    def pygame_draw(self, screen, scale, shiftx, shifty):
        # a dummy draw method - light sources have their own draw methods
        pass
