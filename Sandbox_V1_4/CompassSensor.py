from .Sensor import *

class CompassSensor(Sensor):
    """
        A class for implementing an orientation sensor. If a compass sensor is added to an :class:`Agent` with the same orientation (``theta``) as the agent, then thereafter the sensor can be used to detect the agent's orientation.
    """
    def __init__(self, x: float, y: float, theta: float, noisemaker=None, name_str: str='CompassSensor', delay_steps: float=0):
        """
            __init__(self, agent, noisemaker=None, name_str: str='HeadingSensor', delay_steps: float=0)

            :param x: The initial x-coordinate of the :class:`CompassSensor`, defaults to ``None``.
            :type x: float

            :param y: The initial y-coordinate of the :class:`CompassSensor`, defaults to ``None``.
            :type y: float

            :param noisemaker: The sensor's source of noise.
            :type noisemaker: :class:`NoiseSource`

            :param name_str: The name of the sensor, used in plotting simulation data.
            :type name_str: str

            :param delay_steps: The number of simulation steps a sensor signal will be delayed for.
            :type delay_steps: int
        """
        super().__init__(x=x, y=y, theta=theta, name_str=name_str, noisemaker=noisemaker, delay_steps=delay_steps)
        self.activation = 0  # sensor activation. this variable is updated in and returned from the step method. it is stored separately in case you want to access it multiple times between simulation steps, although that is unlikely to be necessary
        self.activations = [self.activation]  # for plotting and analysis, a sensor keeps a complete record of its activation over time

    # step sensor
    def step(self, dt):
        """
            A method to step a compass sensor forwards in time. A :class:`CompassSensor` has no dynamics, apart from a potential delay from a :class:`DelayBlock`, so technically is not integrated, but ``dt`` is passed to this method for consistency with the step methods of other classes.

            :param dt: Integration interval - not used here.
            :type dt: float

            :return: The activation (level of stimulation) of the sensor.
            :rtype: float
        """
        super().step(dt)
        self.activation = self.theta

        return self.update(dt)

    # A method to get the sensor's data, in the form of a dict.
    def get_data(self) -> dict:
        """
            A function to get the data from a :class:`CompassSensor`, in the form of a string-keyed dict.

            These data, as and when they are included in the returned dict, can be accessed with the following keys:

            * data inherited from :class:`Sensor`: see :class:`Sensor`
            * data of sensor's noise source, if it has one: ``data["noises"]``
            * history of sensor outputs (activations): ``data["activations"]``

            :return: The sensors's data.
            :rtype: dict
        """
        data = super().get_data()
        data["activations"] = self.activations
        data["noises"] =  None
        if self.noisemaker:
            data["noises"] = self.noisemaker.get_data()["noises"]
        return data


    def reset(self):
        """
            A method to reset the sensor to its initial state, so that it can be reused in a later simulation.
        """
        super().reset()
        self.activation = self.activations[0]
        self.activations = [self.activation]
        if self.noisemaker:
            self.noisemaker.reset()
