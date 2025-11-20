from .base import *
from .noise import *
from .DelayBlock import *

import math

# base sensor class. in the current implementation, only contains methods for drawing
class Sensor(System):
    """
        An abstract class for representing sensors. The output from a :class:`Sensor` can be both noisy and delayed, due to the incorporation of a :class:`NoiseSource` and a :class:`DelayBlock`.
    """
    # by default, a Sensor has no position, but one can be specified (and for most sensors will)
    def __init__(self, x: float=None, y: float=None, theta: float=None, colour: str='red', radius: float=0.2, enabled: bool=True, name_str: str='Sensor', delay_steps: int=0, noisemaker=None):
        """
            __init__(self, x: float=None, y: float=None, theta: float=None, colour: str='red', radius: float=0.2, enabled: bool=True, name_str: str='Sensor', delay_steps: int=0, noisemaker=None)

            :param x: The initial x-coordinate of the :class:`Sensor`, defaults to ``None``.
            :type x: float

            :param y: The initial y-coordinate of the :class:`Sensor`, defaults to ``None``.
            :type y: float

            :param theta: The initial angular orientation of the :class:`Sensor`, defaults to ``None``.
            :type theta: float

            :param colour: The colour of the sensor, for drawing.
            :type colour: str

            :param radius: The radius of the sensor, for drawing.
            :type radius: float

            :param enabled: A flag for specifying whether or not a sensor is enabled. Only the attribute is implemented here - how to use it is a decision for subclasses, e.g. in :class:`LightSensor`.
            :type enabled: bool

            :param name_str: The name of the sensor, used in plotting simulation data.
            :type name_str: str

            :param delay_steps: The number of simulation steps a sensor signal will be delayed for.
            :type delay_steps: int

            :param noisemaker: The source of noise for this sensor. Defaults to ``None``.
            :type noisemaker: :class:`NoiseSource`
        """
        super().__init__(x, y, theta)
        self.colour = colour
        self.radius = radius
        self.enabled = enabled
        self.name_str = name_str

        self.delay_block = None
        delay_steps = int(delay_steps)
        if delay_steps > 0:
            self.delay_block = DelayBlock(delay_steps)

        self.noisemaker = noisemaker  # noise source

        self.initial_state = Sensor.get_data(self)

    # draw sensor in the specified matplotlib axes
    def draw(self, ax) -> None:
        """
            A method to draw the sensor in the specified matplotlib axes, as a small coloured circle.

            :param ax: The Matplotlib axes to draw the sensor on.
            :type ax: Matplotlib axes
        """
        if self.has_position:
            ax.add_artist(mpatches.Circle((self.x, self.y), self.radius, color=self.colour))
            ax.plot(self.x, self.y, 'k.')

    # draw sensor in a pygame display
    def pygame_draw(self, screen, scale: float, shiftx: float, shifty: float) -> None:
        """
            A method to draw the sensor in the specified PyGame display, as a small coloured circle.

            :param screen: The PyGame display to draw on.
            :type screen: PyGame display

            :param scale: The scale to draw at.
            :type scale: float

            :param shiftx: The offset from centre in the x-axis for drawing.
            :type shiftx: float

            :param shifty: The offset from centre in the y-axis for drawing.
            :type shifty: float
        """
        if self.has_position:
            pygame.draw.circle(screen, center=(scale*self.x+shiftx, scale*self.y+shifty), color=self.colour, radius=scale*self.radius)

    def get_data(self) -> Dict[str, Union[float, List[float], str]]:
        """
            A method to get the sensors data, in the form of a dict.

            :return: The sensor's data, which includes the data returned from :meth:`Sandbox.System.get_data`, as well as the sensor's colour and radius (which are both assumed to be static), and its "enabled" state and "name_str" string.
            :rtype: dict
        """
        data = super().get_data()
        data["colour"] = self.colour
        data["radius"] = self.radius
        data["enabled"] = self.enabled
        data["name_str"] = self.name_str
        noises = None
        if self.noisemaker:
            noises = self.noisemaker.get_data()["noises"]
        data["noises"] = noises

        return data

    def reset(self) -> None:
        """
            A method to reset a sensor to its initial state, so it can be reused in later simulations.
        """
        super().reset()
        self.colour = self.initial_state["colour"]
        self.radius = self.initial_state["radius"]
        self.enabled = self.initial_state["enabled"]
        self.name_str = self.initial_state["name_str"]
        if self.noisemaker:
            self.noisemaker.reset()

    def update(self, dt) -> float:
        """
            A method to implement the addition of noise and a delay to a sensor's dynamics, as well as keep a record of the sensor's output.

            All subclasses of :class:`Sensor` must call this method from the end of their ``step()`` methods (I'm not happy with this design, and it will be changed in later implementations).
        """
        if self.noisemaker != None:
            self.activation += self.noisemaker.step(dt)

        if self.delay_block != None:
            self.activation = self.delay_block.step(self.activation)

        # record activation
        self.activations.append(self.activation)  # store activation

        # return activation
        return self.activation  # return activation

class FOV_thing:
    """
        A class which is used only for drawing a sensor's field of view (FOV).
        This code is separated from :class:`Sensor`, as not all sensors will necesarily have a FOV. Sensor classes which have a FOV should have multiple inheritance of :class:`Sensor` and :class:`FOV_thing`, as in the case of :class:`LightSensor`.
    """
    def pygame_draw_FOV(self, screen, scale: float, shiftx: float, shifty: float) -> None:
        """
            A method to draw a FOV in the specified PyGame display, with two short lines which indicate its angular extent.
            NOTE: this method is in need of some improvement, in the next implementation - it should be possible to draw the lines at different lengths, and it should also somehow be made clear which line starts and which ends the FOV.

            :param screen: The PyGame display to draw on.
            :type screen: PyGame display

            :param scale: The scale to draw at.
            :type scale: float

            :param shiftx: The offset from centre in the x-axis for drawing.
            :type shiftx: float

            :param shifty: The offset from centre in the y-axis for drawing.
            :type shifty: float
        """
        left_end_x, left_end_y, right_end_x, right_end_y = self.__fov_ends()

        pygame.draw.line(screen, color='green',
                         start_pos=(scale * self.x + shiftx, scale * self.y + shifty),
                         end_pos=(scale * left_end_x + shiftx, scale * left_end_y + shifty), width=2)
        pygame.draw.line(screen, color='green',
                         start_pos=(scale * self.x + shiftx, scale * self.y + shifty),
                         end_pos=(scale * right_end_x + shiftx, scale * right_end_y + shifty), width=2)

    # calculate end coords of lines indicating field of view
    def __fov_ends(self) -> Tuple[float, float, float, float]:
        """
            A method for calculating the coordinates of the ends of the lines for drawing a FOV.
        """
        left_end_x = self.x + math.cos(self.theta + self.FOV/2)
        left_end_y = self.y + math.sin(self.theta + self.FOV/2)
        right_end_x = self.x + math.cos(self.theta - self.FOV/2)
        right_end_y = self.y + math.sin(self.theta - self.FOV/2)
        return left_end_x, left_end_y, right_end_x, right_end_y

    def draw_FOV(self, ax) -> None:
        """
            Draw lines indicating the sensor's field of view in Matplotlib axes

            :param ax: The Matplotlib axes to draw on.
            :type ax: Matplotlib axes
        """
        left_end_x, left_end_y, right_end_x, right_end_y = self.__fov_ends()
        ax.plot([self.x, left_end_x],
                 [self.y, left_end_y], 'b--', linewidth='2')
        ax.plot([self.x, right_end_x],
                 [self.y, right_end_y], 'r--', linewidth='2')
