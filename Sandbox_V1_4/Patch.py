from .base import *
from .System import *
from .pygame_functions import *

from typing import List

class Patch:
    """

    """
    def __init__(self, x: float,
                 y_bottom: float,
                 y_top: float):
        """

        """
        self.x = x
        self.y_bottom = y_bottom
        self.y_top = y_top
        self.length = y_top - y_bottom

    def draw(self, ax) -> None:
        """

        """
        ax.plot([self.x, self.x], [self.y_bottom, self.y_top], linewidth=2, color='white')

    def pygame_draw(self, screen, scale: float, shiftx: float, shifty: float):
        """

        """
        pygame_drawrectangle(screen, shiftx, shifty, scale, self.x-0.5, self.x+0.5, self.y_top, self.y_bottom, colour="white", width=5)

class Wall(System):
    """

    """
    def __init__(self, x: float):
        """

        """
        # call System constructor
        super().__init__(x=0, y=0, theta=None)
        self.x = x
        self.y_bottom = 1E6
        self.y_top = -1E6
        self.patches: List[Patch] = []

    def add_patch(self, y_top: float, y_bottom: float) -> None:
        """

        """
        self.patches.append(Patch(x=self.x, y_bottom=y_bottom, y_top=y_top))
        if y_bottom < self.y_bottom:
            self.y_bottom = y_bottom
        if y_top > self.y_top:
            self.y_top = y_top

    def draw(self, ax) -> None:
        """

        """
        ax.plot([self.x, self.x], [self.y_bottom, self.y_top], linewidth=2, color='black')
        for patch in self.patches:
            patch.draw(ax)

    def pygame_draw(self, screen, scale: float, shiftx: float, shifty: float):
        """

        """
        for p in self.patches:
            p.pygame_draw(screen, scale, shiftx, shifty)

    def reset(self):
        pass

    # def perturb(self):
    #     pass
	#
    # def init_conditions(self):
    #     pass
	#
    # def step(self, dt):
    #     pass
