from .System import *

'''
    Note: Stimulus classes are not normally
	stepped, so they don't keep histories.
'''

# this is the base class for stimuli in the environment. it could be used in other ways, but for now is only used as the
# base for the various types of light sources
class Stimulus(System):
    """
        An abstract class to represent a source of sensory stimulation.
    """
    def __init__(self, x: float=None, y: float=None, theta: float=None, is_on: bool=True):
        """
            __init__(x: float=None, y: float=None, theta: float=None, is_on: bool=True)

            :param x: The x-coordinate of the stimulus. Defaults to ``None``.
            :type x: float

            :param y: The y-coordinate of the stimulus. Defaults to ``None``.
            :type y: float

            :param theta: The angular orientation of the stimulus. Defaults to ``None``.
            :type theta: float

            :param is_on: A flag which can be use to determine whether or not a stimulus can be detected. Defaults to ``True``. This allows for the stimulus to be turned on and off, but the actual response to the state of this flag is determined elsewhere, e.g. in :class:`LightSource`. Also, a sensor implementation could choose to ignore this flag and detect a stimulus even when it is not on.
            :type is_on: bool
        """
        super().__init__(x, y, theta)
        self.is_on = is_on
        self.initial_is_on = is_on

    def __eq__(self, other):
        '''
            Overrides the == operator for instances of this class.

            :param other: The instance of System that this instance will be compared to.
            :type other: System
        '''

        if other == None:
            return False

        is_eq = super().__eq__(other)
        is_eq = is_eq and self.is_on == other.is_on
        is_eq = is_eq and self.initial_is_on == other.initial_is_on

        return is_eq

    # get distance from the given xy coordinates to the Stimulus, if the Stimulus has position
    def get_distance(self, x: float, y: float) -> float:
        """
            A method for finding the Euclidean distance from the passed in x- and y-coordinates to the position of this stimulus, assuming it has position - this method should not be invoked on an instance of :class:`Stimulus` which does not have position.

			The passed in x- and y- coordinates can be used to get the distance from any position, but they will typically be the coordinates of a sensor which will potentially detect this stimulus.

            :param x: The x-component of the position to find the distance from.
            :type x: float

            :param y: The y-component of the position to find the distance from.
            :type y: float

            :return: The distance.
            :rtype: float
        """
        if self.has_position:
            # vec = np.array([self.x - x, self.y - y])  # vector from sensor to stimulus
            # return np.linalg.norm(vec)  # length of vector, i.e. distance from sensor to stimulus
            return norm(self.x, x, self.y, y)
        else:
            return None

    def get_data(self) -> dict:
        """
            A method to return the data of the stimulus.
            Note: this is not likely to be particularly useful, as it only contains the original state, as recorded by :class:`System`, and the current state of "is_on".

            :return: A dict containing the data returned from :meth:`Sandbox.System.get_data`, plus ``is_on``.
            :rtype: dict
        """
        data = super().get_data()
        data["is_on"] = self.is_on
        return data

    def reset(self) -> None:
        """
            A method to reset the :class:`Stimulus` to its original state.
        """
		# reset System attributes
        super().reset()
		# reset Stimulus attributes
        self.is_on = self.initial_is_on

# this class implements a static and noiseless light source. it has two models for decay of brightness over distance,
# inverse square and linear. you should use whichever you find easiest, but that will depend on what kind of controllers
# you are working on
#   in the linear case, brightness decays from the maximum to zero, according to the specified
#   gradient.
#       - the downside to this is that there will be a maximum detection distance, beyond which a sensor will not detect
#       the light, but this is only likely to be a problem if a large decay gradient is used (not that problems are
#       necessarily bad - they can make things more interesting).
#       - the upside to the linear decay model is that it may make it easier to program certain kinds of controller.
#   in the inverse square case, brightness decays in a way which is closer to reality.
#       - the upside to the inverse square model is that there is no hard limit to detection range (although there will
#       be a distance at which a sensor is barely stimulated by it)
#       - the downside is that the inverse square model can make it more difficult to program certain kinds of
#       controller, due to its nonlinearity.
class LightSource(Stimulus):
    """
        A subclass of :class:`Stimulus`, :class:`LightSource` is a class which represents a light source. It is possible to set the "model" of intensity of a :class:`LightSource` to be either an inverse square law of decay with distance, or a linear one, or for the light to be detected with constant brightness at all distances.

        .. image:: images/LinearLightSource.svg
          :width: 600
          :align: center
          :alt: Linear light decay model

        .. image:: images/InvSqLightSource.svg
          :width: 600
          :align: center
          :alt: Inverse square light decay model

    """
    # construct light source
    def __init__(self, x: float, y: float, theta: float=0, spread=2*math.pi, brightness: float=1, gradient: float=0.01, model: str='inv_sq', is_on: bool=True, colour: str='yellow', label: str=None):
        """
            __init__(x: float=None, y: float=None, theta: float=None, is_on: bool=True)

            :param x: The x-coordinate of the light.
            :type x: float

            :param y: The y-coordinate of the light.
            :type y: float

            :param theta: The orientation of the light.
            :type theta: float

            :param spread: The angular spread of light around ``theta``. Can be used to create lights which are only detectable from certain angles. WARNING: this feature has not been used or tested in a long while, and is not guaranteed to work with this new *Sandbox* version.

            :param brightness: The brightness of the light, at its own coordinate.
            :type brightness: float

            :param gradient: The gradient of brightness decay with distance, when the linear model is used.
            :type gradient: float

            :param model: The light decay model. ``inv_sq``, ``linear``, and ``binary`` are valid models.
            :type model: str

            :param is_on: A flag which can be use to determine whether or not a light can be detected. Defaults to ``True``. This allows for the light to be turned on and off.
            :type is_on: bool

            :param colour: The colour of the light. Note: this is for drawing only - no system currently implemented in *Sandbox* can detect a light's RGB colour.
            :type colour: str

            :param label: A light source's label defines a group. Any :class:`LightSensor` with the same label attribute will detect all, and only, light sources which are in its list and also in that group. A :class:`LightSensor` with no label will detect any :class:`LightSource` in its list, regardless of label.
            :type label: str
        """
        super().__init__(x, y, theta, is_on)  # call Stimulus constructor
        self.brightness = brightness  # this is the brightness of the light at the source
        self.initial_brightness = brightness

        self.gradient = gradient  # this determines how quickly the brightness decays when the linear model is used
        self.initial_gradient = gradient

        self.model = model  # model can be inv_sq, which is realistic, or linear, which is not physically realistic but is easier to work with
        self.initial_model = model

        self.colour = colour # colour of light, for animation and plots
        self.initial_colour = colour

        self.label = label # group label of light
        self.initial_label = label

        self.half_spread = spread / 2 # angular spread of light cone
        self.initial_half_spread = spread / 2

    def get_brightness_at(self, x: float, y: float, sensor_angle=None) -> float:
        """
            A method to get the brightness of the light (as it is perceived) at the given xy coordinates, according to the light source's ``model``, and which angles it can be perceived from (determined by the light's ``spread`` attribute).

            :param x: The x-component of the position to find the brightness at.
            :type x: float

            :param y: The y-component of the position to find the brightness at.
            :type y: float

            :param sensor_angle: The orientation of the sensor at the position to find the brightness at. For lights which are not omni-directional, this will affect whether the sensor can detect the light.
            :type sensor_angle: float

            :return: The perceived brightness at the given coordinates.
            :rtype: float
        """

        # print(sensor_angle)

        if not self.is_on:
            return 0

        # angle_diff = -np.Inf
#
        # if sensor_angle is not None:
		#
        #     self.theta = self.theta % (2*math.pi)
		#
        #     # for computing the next step, constrain the angle of the sensor to be in the interval [0, 2*np.pi]
        #     sensor_angle += math.pi # rotate this angle, to be from point of view of light
        #     angle = sensor_angle % (2*math.pi)
        #     if angle < 0:
        #         angle += 2 * math.pi
		#
        #     # find the difference between the direction the sensor points in and the direction the light source points in
        #     angle_diff = min([np.abs(self.theta - angle), np.abs(self.theta - (angle-2*math.pi))])
		#
        # print(sensor_angle, angle_diff)

        self.theta = self.theta % (2*math.pi)

        brightness = 0
        # if sensor can "see" light from its current position and orientation, then return brightness at sensor's coordinate, else return 0

        angle_to_light = math.atan2(y-self.y, x-self.x)  # find angle of vector from light source to sensor

        # if angle_diff > self.half_spread:
        if abs(angle_difference(angle_to_light, self.theta)) >= (self.half_spread):
            return 0
        else:
            dist = self.get_distance(x, y)
            if self.model == 'inv_sq':
                brightness = self.inv_sq_model(dist)
            elif self.model == 'linear':
                brightness = self.linear_model(dist)
            elif self.model == 'binary':
                brightness = self.brightness

        return brightness

    # for some controllers, it is much easier to work with a linear light decay model. it is not physically realistic as a model of light, but we can think of this as being preprocessed to linearise raw sensor data
    def linear_model(self, dist: float) -> float:
        """
            A method to find the perceived brightness of the light source at the given distance, when the linear decay model is used.

            :param dist: The distance from the light source.
            :type dist: float

            :return: The perceived brightness.
            :rtype: float
        """
        return max(self.brightness - self.gradient * dist, 0)

    # this is a more realistic model of light decay. for simple Braitenberg vehicle style robots the nonlinearity of
    # light decay can lead to interesting behaviours
    def inv_sq_model(self, dist: float) -> float:
        """
            A method to find the perceived brightness of the light source at the given distance, when the inverse square decay model is used.

            :param dist: The distance from the light source.
            :type dist: float

            :return: The perceived brightness.
            :rtype: float
        """
        return self.brightness / np.power(dist+1, 2)  # 1 is added to fix brightness at dist=0

    def get_data(self) -> dict:
        """
            Get the :class:`LightSource`'s data. This method, if used, relies on the assumption that the :class:`LightSource` and its properties are static.

            :return: The :class:`LightSource`'s data in dict form.
            :rtype: dict
        """
        data = super().get_data()
        data["brightness"] = self.brightness
        data["gradient"] = self.gradient
        data["model"] = self.model
        data["colour"] = self.colour
        data["label"] = self.label
        data["half_spread"] = self.half_spread
        return data

    def reset(self) -> None:
        """
            A method to reset the :class:`LightSource` to its original state.
        """
        super().reset()
        self.brightness = self.initial_brightness
        self.gradient = self.initial_gradient
        self.model = self.initial_model
        self.colour = self.initial_colour
        self.label = self.initial_label
        self.half_spread = self.initial_half_spread

    def __eq__(self, other):
        '''
            Overrides the == operator for instances of this class.

            :param other: The instance of :class:`LightSource` that this instance will be compared to.
            :type other: System
        '''

        if other == None:
            return False

        is_eq = super().__eq__(other)

        is_eq = is_eq and self.brightness == other.brightness
        is_eq = is_eq and self.initial_brightness == other.initial_brightness
        is_eq = is_eq and self.gradient == other.gradient
        is_eq = is_eq and self.initial_gradient == other.initial_gradient
        is_eq = is_eq and self.model == other.model
        is_eq = is_eq and self.initial_model == other.initial_model
        is_eq = is_eq and self.colour == other.colour
        is_eq = is_eq and self.initial_colour == other.initial_colour
        is_eq = is_eq and self.label == other.label
        is_eq = is_eq and self.initial_label == other.initial_label
        is_eq = is_eq and self.half_spread == other.half_spread
        is_eq = is_eq and self.initial_half_spread == other.initial_half_spread

        return is_eq

    # calculate coords of line ends for indicating angular spread of light
    # lines are drawn from light source position, and are 1 unit long
    def calculate_ends(self):
        right_end_x = self.x + np.cos(self.theta - self.half_spread)
        right_end_y = self.y + np.sin(self.theta - self.half_spread)
        left_end_x = self.x + np.cos(self.theta + self.half_spread)
        left_end_y = self.y + np.sin(self.theta + self.half_spread)
        return left_end_x, left_end_y, right_end_x, right_end_y

    def draw(self, ax) -> None:
        """
            A method to draw the light source in the specified matplotlib axes.
            A :class:`LightSource` which is switched on is drawn as a circle with colour specified by the light source's ``colour`` attribute, with a smaller circle in its center which is orange coloured.  A :class:`LightSource` which is not on will have its outer circle coloured in grey.

            :param ax: The Matplotlib axes to draw the light on.
            :type ax: Matplotlib axes.
        """
        if not self.is_on:
            colour = 'gray'
        else:
            colour = self.colour
        ax.add_artist(mpatches.Circle((self.x, self.y), 0.7, color=colour))
        ax.add_artist(mpatches.Circle((self.x, self.y), 0.2, color='orange'))
        ax.plot(self.x, self.y, 'r.')

        # get coords of line ends for indicating angular spread of light
        left_end_x, left_end_y, right_end_x, right_end_y = self.calculate_ends()

        if self.half_spread < math.pi:
            # draw lines to indicate angular spread of light
            plt.plot([self.x, left_end_x],
                     [self.y, left_end_y], 'r--', linewidth='2')
            plt.plot([self.x, right_end_x],
                     [self.y, right_end_y], 'r--', linewidth='2')

    # draw light source in a pygame display
    def pygame_draw(self, screen, scale: float, shiftx: float, shifty: float) -> None:
        """
            A method to draw the light source in the specified PyGame display.
            A :class:`LightSource` which is switched on is drawn as a circle with colour specified by the light source's ``colour`` attribute, with a smaller circle in its center which is orange coloured.  A :class:`LightSource` which is not on will have its outer circle coloured in grey.

            :param screen: The PyGame display to draw on.
            :type screen: PyGame display

            :param scale: The scale to draw at.
            :type scale: float

            :param shiftx: The offset from centre in the x-axis for drawing.
            :type shiftx: float

            :param shifty: The offset from centre in the y-axis for drawing.
            :type shifty: float
        """
        if not self.is_on:
            colour = 'gray'
        else:
            colour = self.colour
        pygame.draw.circle(screen, center=(scale*self.x+shiftx, scale*self.y+shifty), color=colour, radius=scale*0.7)
        pygame.draw.circle(screen, center=(scale*self.x+shiftx, scale*self.y+shifty), color='orange', radius=scale*0.2)

        # get coords of line ends for indicating angular spread of light
        left_end_x, left_end_y, right_end_x, right_end_y = self.calculate_ends()

        if self.half_spread < math.pi:
            # draw lines to indicate angular spread of light
            pygame.draw.line(screen, color='red',
                         start_pos=(scale * self.x + shiftx, scale * self.y + shifty),
                         end_pos=(scale * left_end_x + shiftx, scale * left_end_y + shifty), width=2)
            pygame.draw.line(screen, color='red',
                         start_pos=(scale * self.x + shiftx, scale * self.y + shifty),
                         end_pos=(scale * right_end_x + shiftx, scale * right_end_y + shifty), width=2)
