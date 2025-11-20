# # import packages
# import sys
# import yaml
#
# # import Sandbox
# sys.path.insert(1, '../../') # relative path to folder which contains the Sandbox module
# from Sandbox_V1_4 import *

from .System import *

class FadingLight:
    """

    """
    def __init__(self, agents, light, fade_rate=0.001):
        """

        """
        self.fade_rate = fade_rate
        self.light = light
        self.r = 255
        self.g = 255
        self.b = 0
        self.initial_brightness = light.brightness
        self.agents = agents

    def step(self, dt):
        """

        """
        for agent in self.agents:
            last_brightness = self.light.brightness

            self.light.brightness -= dt * self.fade_rate * self.light.get_brightness_at(agent.x, agent.y, agent.theta)

            if self.light.brightness > 0:
                ratio = self.light.brightness / self.initial_brightness
                r = int(self.r * ratio)
                g = int(self.g * ratio)
                b = int(self.b * ratio)
                self.light.colour = pygame.Color(r, g, b)

            self.light.brightness = max(0, self.light.brightness)
            if self.light.brightness < 0.01:
                self.light.is_on = False

class FadingLightManager(System):
    """

    """
    def __init__(self, agents, light_sources, fade_rate=0.001):
        """

        """
        self.fading_lights = []
        for light in light_sources:
            self.fading_lights.append(FadingLight(agents, light, fade_rate))

        super().__init__()

    def step(self, dt):
        """

        """
        for light in self.fading_lights:
            light.step(dt)

    def draw(self, ax):
        pass

    def pygame_draw(self, screen, scale, shiftx, shifty):
        pass
