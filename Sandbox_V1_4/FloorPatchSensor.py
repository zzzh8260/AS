from .Sensor import *
from .noise import *
from .FloorPatch import *

class FloorPatchSensor(Sensor):
    """
        A class which represents a sensor for detecting coloured patches on the floor. Can detect both :class:`FloorPatch` and :class:`CircularFloorPatch` objects.
    """
    def __init__(self, floor_patches: List[FloorPatch], x: float, y: float, noisemaker: NoiseSource=None, label: str=None, enabled: bool=True, name_str: str='FloorPatchSensor', delay_steps: float=0):
        '''
            __init__(self, floor_patches: List[FloorPatch], x: float, y: float, noisemaker: NoiseSource=None, label: str=None, enabled: bool=True, name_str: str='FloorPatchSensor', delay_steps: float=0)

            :param floor_patches: The list of instances of :class:`FloorPatch` which the sensor can potentially detect.
            :type floor_patches: list[:class:`FloorPatch`]

            :param label: A :class:`FloorPatchSensor`'s label determines which of the :class:`FloorPatch` s in its list it can actually detect. Defaults to ``None``, in which case the sensor will detect all floor patches in its list. If a sensor's ``label`` attribute is set to some string, then it will only detect floor patches which have their ``label`` attributes set to the same value.
            :type label: str

            :param x: The initial x-coordinate of the :class:`FloorPatchSensor`.
            :type x: float

            :param y: The initial y-coordinate of the :class:`FloorPatchSensor`.
            :type y: float

            :param noisemaker: The sensor's source of noise.
            :type noisemaker: :class:`NoiseSource`

            :param name_str: The name of the sensor, used in plotting simulation data.
            :type name_str: str

            :param delay_steps: The number of simulation steps a sensor signal will be delayed for.
            :type delay_steps: int

            :param enabled: A flag for specifying whether or not a floor patch is enabled. Defaults to ``True``. If set to ``False``, then the sensor will not detect anything.
            :type enabled: bool
        '''
        super().__init__(x=x, y=y, enabled=enabled, name_str=name_str, noisemaker=noisemaker, delay_steps=delay_steps)

        self.floor_patches = floor_patches

        self.activation: float = 0.0  # sensor activation. this variable is updated in and returned from the step method. it is stored separately in case you want to access it multiple times between simulation steps, although that is unlikely to be necessary
        self.activations = [self.activation]  # for plotting and analysis, a sensor keeps a complete record of its activation over time
        self.noisemaker = noisemaker  # noise source

        self.label = label

        self.initial_state = FloorPatchSensor.get_data(self)

    def step(self, dt: float) -> float:
        """
            A method to step a floor patch sensor forwards in time. A :class:`FloorPatchSensor` has no dynamics, so technically is not stepped in time, but 'step' is used for consistency.

            :param dt: Integration interval - not used here.
            :type dt: float

            :return: The activation (level of stimulation) of the sensor, which will be ``0`` when no patches are detected. When the sensor detects multiple floor patches, their effects are not summed - the output will only be ``1``.
            :rtype: float
        """
        super().step(dt)  # call System step method, to store xy-coordinates and theta
        self.activation = 0.0  # begin with zero activation, and
        # only detect anything if enabled
        if self.enabled:
            for patch in self.floor_patches:  # for every floor patch the sensor can detect
                # if this sensor has a label set, then it will only detect sensors with the same label
                if not self.label or self.label == patch.label:

                    if patch.is_in(self.x, self.y):
                        self.activation = 1

        return self.update(dt)

    def get_data(self) -> dict:
        """
            A function to get the data from an :class:`FloorPatchSensor`, in the form of a string-keyed dict.

            These data, as and when they are included in the returned dict, can be accessed with the following keys:

            * data inherited from :class:`Sensor`: see :class:`Sensor`
            * current sensor output (activation): ``data["activation"]``
            * history of sensor outputs (activations): ``data["activations"]``
            * label of floor patches which this sensor will detect, if they are also in its list of patches: ``data["label"]``. If this value is ``None``, then the sensor will detect patches with any label.
            * list of floor patches that the sensor will detect, if they have the same label as it, or its label is ``None``: ``data["light_sources"]``
            * data of sensor's noise source, if it has one: ``data["noises"]``

            :return: The sensors's data.
            :rtype: dict
        """
        data = super().get_data()
        data["activation"] = self.activation
        data["activations"] = self.activations[:]
        data["label"] = self.label
        data["floor_patches"] = self.floor_patches # only here for reset() - no use for plotting/analysis
        data["noises"] =  None
        if self.noisemaker:
            data["noises"] = self.noisemaker.get_data()["noises"][:]
        return data

    def reset(self) -> None:
        """
            A method to reset the sensor to its initial state, so that it can be reused in a later simulation.
        """
        super().reset()
        self.activation = self.initial_state["activations"][0]
        self.activations = [self.activation]
        self.label = self.initial_state["label"]
        self.enabled = self.initial_state["enabled"]
        self.floor_patches = self.initial_state["floor_patches"]

        if self.noisemaker:
            self.noisemaker.reset()

    def pygame_draw(self, screen, scale: float, shiftx: float, shifty: float) -> None:
        """
            A method for drawing the sensor, as a small circle.

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
