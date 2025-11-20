from .stimuli import *
from .Sensor import *

# a class to define a sensor which detects instances of the LightSource class
class LightSensor(Sensor, FOV_thing):
    """
        A class which represents a light sensor. :class:`LightSensor` inherits both from :class:`Sensor` and :class:`FOV_thing`.
    """
    def __init__(self, light_sources: List[LightSource], x: float, y: float, theta: float=0, FOV: float=2*math.pi, noisemaker: NoiseSource=None, label: str=None, enabled: bool=True, name_str: str='LightSensor', colour: str='red', delay_steps: int=0):
        """
            __init__(self, light_sources: List[LightSource], x: float, y: float, theta: float=0, FOV: float=2*math.pi, noisemaker: NoiseSource=None, label: str=None, enabled: bool=True, name_str: str='LightSensor', colour: str='red', delay_steps: int=0)

            :param light_sources: The list of instances of :class:`LightSource` which this sensor can potentially detect.
            :type light_sources: list[:class:`Light_Source`]

            :param x: The initial x-coordinate of the :class:`LightSensor`, defaults to ``None``.
            :type x: float

            :param y: The initial y-coordinate of the :class:`LightSensor`, defaults to ``None``.
            :type y: float

            :param theta: The initial angular orientation of the :class:`LightSensor`, defaults to ``None``.
            :type theta: float

            :param FOV: The sensor's angular field of view. Defaults to ``2pi``.
            :type FOV: float

            :param noisemaker: The sensor's source of noise.
            :type noisemaker: :class:`NoiseSource`

            :param label: A :class:`LightSensor`'s label determines which of the :class:`LightSource` s in its list it can actually detect. Defaults to ``None``, in which case the sensor will detect all light sources in its list. If a sensor's ``label`` attribute is set to some string, then it will only detect light sources which have their ``label`` attributes set to the same value.
            :type label: str

            :param enabled: A flag for specifying whether or not a light sensor is enabled. Defaults to ``True``. If set to ``False``, then the sensor will not detect anything.
            :type enabled: bool

            :param name_str: The name of the sensor, used in plotting simulation data.
            :type name_str: str

            :param delay_steps: The number of simulation steps a sensor signal will be delayed for.
            :type delay_steps: int
        """
        super().__init__(x=x, y=y, theta=theta, enabled=enabled, name_str=name_str, colour=colour, noisemaker=noisemaker, delay_steps=delay_steps)
        self.light_sources = light_sources
        # self.initial_light_sources = light_sources  # a list of LightSource instances which this sensor can detect
        self.activation: float = 0.0  # sensor activation. this variable is updated in and returned from the step method. it is stored separately in case you want to access it multiple times between simulation steps, although that is unlikely to be necessary
        self.activations = [self.activation]  # for plotting and analysis, a sensor keeps a complete record of its activation over time
        self.noisemaker = noisemaker  # noise source
        self.FOV = FOV  # sensor angular field of view

        self.label = label
        # self.initial_label = label
        # self.initial_enabled = enabled # Perhaps should be moved to Sensor!?
        # self.initial_FOV = FOV

        self.initial_state = LightSensor.get_data(self)

    def step(self, dt: float) -> float:
        """
            A method to step a light sensor forwards in time. A :class:`LightSensor` has no dynamics, apart from a potential delay from a :class:`DelayBlock`, so technically is not integrated, but ``dt`` is passed to this method for consistency with the step methods of other classes.

            :param dt: Integration interval - not used here.
            :type dt: float

            :return: The activation (level of stimulation) of the sensor. When the sensor detects multiple light sources, their effects are summed linearly.
            :rtype: float
        """
        super().step(dt)  # call System step method, to store xy-coordinates and theta
        self.activation = 0.0  # begin with zero activation, and add to it for every detected light source
        # only detect anything if enabled
        if self.enabled:
            for source in self.light_sources:  # for every light source the sensor can detect
                # if this sensor has a label set, then it will only detect sensors with the same label
                if not self.label or self.label == source.label:
                    angle_to_source = math.atan2(source.y - self.y, source.x - self.x)  # find angle of vector from light source to sensor
                    if abs(angle_difference(angle_to_source, self.theta)) <= (self.FOV/2):  # if angle is within field fo view, the sensor detects the light
                        self.activation += source.get_brightness_at(self.x, self.y, self.theta)  # stimuli from multiple lights are added linearly

        return self.update(dt)

        # replacing the above call to update() with the lines below seems to improve performance significantly, although it leads to duplicated code

        # if self.noisemaker != None:
        #     self.activation += self.noisemaker.step(dt)
		#
        # if self.delay_block != None:
        #     self.activation = self.delay_block.step(self.activation)
		#
        # # record activation
        # self.activations.append(self.activation)  # store activation
		#
        # # return activation
        # return self.activation  # return activation

    def get_data(self) -> dict:
        """
            A function to get the data from a :class:`LightSensor`, in the form of a string-keyed dict.

            These data, as and when they are included in the returned dict, can be accessed with the following keys:

            * data inherited from :class:`Sensor`: see :class:`Sensor`
            * current sensor output (activation): ``data["activation"]``
            * history of sensor outputs (activations): ``data["activations"]``
            * sensor's field of view: ``data["FOV"]``
            * label of light sources which this sensor will detect, if they are also in its list of light sources: ``data["label"]``. If this value is ``None``, then the sensor will detect lights with any label.
            * list of light sources that the sensor will detect, if they have the same label as it, or its label is ``None``: ``data["light_sources"]``
            * data of sensor's noise source, if it has one: ``data["noises"]``

            :return: The sensors's data.
            :rtype: dict
        """
        data = super().get_data()
        data["activation"] = self.activation
        data["activations"] = cp.copy(self.activations)
        data["FOV"] = self.FOV
        data["label"] = self.label
        data["light_sources"] = self.light_sources  # only here for reset() - no use for plotting/analysis
        data["noises"] =  None
        if self.noisemaker:
            # print(self.noisemaker.get_data())
            # print()
            data["noises"] = self.noisemaker.get_data()["noises"][:]
        return data

    def reset(self) -> None:
        '''
            A method to reset a sensor to its initial state, by resetting its ``x``, ``y``, ``theta``, ``light_sources``, ``activation``, ``activations``, ``label``, ``enabled``, and ``FOV`` attributes to their values at time of construction. If the sensor has a ``noisemaker``, then the reset method of that object will also be called.

            Note: this method will not reset any attributes which have been added outside of the :meth:`Sandbox.LightSensor.__init__` method.
        '''
        super().reset()

        self.activation = self.initial_state["activations"][0]
        self.activations = [self.activation]
        self.label = self.initial_state["label"]
        self.enabled = self.initial_state["enabled"]
        self.FOV = self.initial_state["FOV"]
        self.light_sources = self.initial_state["light_sources"]

        if self.noisemaker:
            self.noisemaker.reset()

    def clone(self):
        """
            A method to clone a LightSensor. I'm not sure why I wrote this method - it is not used anywhere.

            :return: A copy of the sensor.
            :rtype: :class:`LightSensor`
        """
        c = cp.deepcopy(self)
        c.light_sources = cp.copy(self.light_sources)
        return c

    def pygame_draw(self, screen, scale: float, shiftx: float, shifty: float) -> None:
        """
            A method for drawing the sensor, as a small circle with lines radiating out from its centre to inidicate the sensor's FOV.

            :param screen: The PyGame display to draw on.
            :type screen: PyGame display

            :param scale: The scale to draw at.
            :type scale: float

            :param shiftx: The offset from centre in the x-axis for drawing.
            :type shiftx: float

            :param shifty: The offset from centre in the y-axis for drawing.
            :type shifty: float
        """
        super().pygame_draw(screen, scale, shiftx, shifty)

        self.pygame_draw_FOV(screen, scale, shiftx, shifty)
