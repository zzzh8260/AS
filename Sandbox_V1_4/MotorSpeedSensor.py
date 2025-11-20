from .base import *
from .Motor import *
from .noise import *
from .Sensor import *

import math

class MotorSpeedSensor(Sensor):
    """
        A class to implement a motor speed (technically, velocity, as it has direction) sensor.
    """
    def __init__(self, motor: Motor, x: float=None, y: float=None, noisemaker: NoiseSource=None, name_str: str='MotorSensor', delay_steps: int=0):
        """
            __init__(self, motor: Motor, x: float=None, y: float=None, noisemaker: NoiseSource=None, name_str: str='MotorSensor', delay_steps: int=0)

            :param x: The initial x-coordinate of the :class:`MotorSpeedSensor`, defaults to ``None``.
            :type x: float

            :param y: The initial y-coordinate of the :class:`MotorSpeedSensor`, defaults to ``None``.
            :type y: float

            :param motor: The motor that the sensor is attached to.
            :type motor: :class:`Motor`

            :param noisemaker: The sensor's source of noise.
            :type noisemaker: :class:`NoiseSource`

            :param name_str: The name of the sensor, used in plotting simulation data.
            :type name_str: str

            :param delay_steps: The number of simulation steps a sensor signal will be delayed for.
            :type delay_steps: int
        """
        super().__init__(x=x, y=y, name_str=name_str, noisemaker=noisemaker, delay_steps=delay_steps)
        self.motor = motor
        self.noisemaker = noisemaker
        self.activation = 0
        self.activations = [self.activation]

    def step(self, dt: float) -> float:
        """
            A method to step an energy sensor forwards in time. A :class:`MotorSpeedSensor` has no dynamics, apart from a potential delay from a :class:`DelayBlock`, so technically is not integrated, but ``dt`` is passed to this method for consistency with the step methods of other classes.

            :param dt: Integration interval - not used here.
            :type dt: float

            :return: The activation (level of stimulation) of the sensor.
            :rtype: float
        """
        super().step(dt)
        self.activation = self.motor.speed

        return self.update(dt)

    def get_data(self):
        """
            A function to get the data from an :class:`MotorSpeedSensor`, in the form of a string-keyed dict.

            These data, as and when they are included in the returned dict, can be accessed with the following keys:

            * data inherited from :class:`Sensor`: see :class:`Sensor`
            * data of sensor's noise source, if it has one: ``data["noises"]``
            * sensor's current output (activation): ``data["activation"]``
            * history of sensor outputs (activations): ``data["activations"]``

            :return: The sensors's data.
            :rtype: dict
        """
        data = super().get_data()
        data["activation"] = self.activation
        data["activations"] = self.activations[:]
        data["noises"] =  None
        if self.noisemaker:
            data["noises"] = self.noisemaker.get_data()["noises"][:]
        return data

    def reset(self) -> None:
        """
            A method to reset the sensor to its initial state, so that it can be reused in a later simulation.
        """
        super().reset()
        self.activation = 0
        self.activations = [self.activation]

        if self.noisemaker:
            self.noisemaker.reset()
