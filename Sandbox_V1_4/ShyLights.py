from .System import *

class ShyLightManager(System):
    """

    """
    def __init__(self, light_sources, agents, shy_radius, shy_time):
        """

        """
        self.agents = agents
        self.shy_radius = shy_radius
        self.shy_time = shy_time
        self.light_sources = light_sources
        self.timers = [0] * len(light_sources)

        super().__init__()

    def step(self, dt):
        """

        """
        for i, light in enumerate(self.light_sources):
            if light.is_on:
                for agent in self.agents:
                    if np.linalg.norm([agent.x-light.x, agent.y-light.y]) < self.shy_radius:
                        light.is_on = False
                        self.timers[i] = 0
            else:
                self.timers[i] += dt
                if self.timers[i] > self.shy_time:
                    light.is_on = True

    def reset(self):
        """

        """
        self.timers = [0] * len(self.light_sources)


    def draw(self, ax):
        pass

    def pygame_draw(self, screen, scale, shiftx, shifty):
        pass
