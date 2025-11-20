from .System import *
from .noise import *

class Motor(System):
    """
        A class representing a motor. A motor has a maximum speed at which it will turn in either the forwards or backwards direction. Positive motor speeds results in forwards motion, and negative speeds result in backwards direction. This relationship can be reversed by setting the robot's ``reversed`` parameter to ``True``.  A motor can also have inertia, which is the motor's resistance to changes of speed. If the inertia is set to 0, then the motor can change speed instantaneously. See the figure below for examples of how motors can behave with different combinations of maximum speed and inertia.

        .. figure:: images/Motor.svg
          :width: 400
          :align: center
          :alt: Motor examples

          In the figure, the response of three different motors to a constant command of 20 is shown. Motor 1 has max_speed = 10, motor_inertia_coeff = 100. Motor 2 has max_speed = 40, motor_inertia_coeff = 50. Motor 3 has max_speed = 10, motor_inertia_coeff = 0. Motor 3 changes speed to the commanded valuse in a simgle time step. The speeds of motors 1 and 3 both saturate at their maximum speed value, which is less than the commanded value. The speed of motor 2 changes most slowly, as it has the highest inertia.
    """
    def __init__(self, max_speed: float, motor_inertia_coeff: float=0, reversed: bool=False, noisemaker: NoiseSource=None,  name_str: str='Motor'):
        """
            __init__(self, max_speed: float, motor_inertia_coeff: float=0, reversed: bool=False, noisemaker: NoiseSource=None,  name_str: str='Motor')


            :param max_speed: The maximum speed the motor can run at. Negative values will be converted to positive ones when they are copied to the motor's attributes.
            :type max_speed: float

            :param motor_inertia_coeff: A parameter used to determine how quickly the motor's speed can change. Defaults to 0, in which case the motor can change speed instantaneously.
            :type motor_inertia_coeff: float

            :param reversed: A flag which determines whether the motor runs in the forwards or reverse direction. Defaults to ``False``, in which case the motor runs forwards.
            :type reversed: bool

            :param noisemaker: A :class:`NoiseSource` object, to generate noise which is added to the motor's actual speed.
            :type noisemaker: :class:`NoiseSource`

            :param name_str: The name of the motor, used in plotting simulation data.
            :type name_str: str
        """
        # motors can have noise sources attached to them
        self.noisemaker = noisemaker
        # current speed and history of speed
        self.speed = 0.0
        self.speeds = [0.0]

        # system parameters
        self.motor_inertia_coeff = max(0, motor_inertia_coeff) + 1 # limits rate of change of speed
        self.initial_motor_inertia_coeff = self.motor_inertia_coeff

        self.max_speed: float = np.abs(max_speed)
        self.initial_max_speed = self.max_speed

        self.reversed = reversed
        self.reverseds = [reversed]

        self.name_str = name_str

    def step(self, speed_command: float, dt: float) -> float:
        """
            Function to step motor forward in time.

            :param speed_command: New speed command
            :type speed_command: float

            :param dt: Integration interval
            :type dt: float

            :return: Motor speed after stepping
            :rtype: float
        """
        # if motor is reversed, then reverse the control input
        if self.reversed:
            speed_command = -speed_command

        self.reverseds.append(self.reversed)

        # calculate speed change
        speed_change = (1/self.motor_inertia_coeff) * (speed_command - self.speed) # * dt

        # change speed
        self.speed += speed_change

        # apply noise
        if self.noisemaker is not None:
            self.speed += self.noisemaker.step(dt)

        # constrain motor speed
        if self.speed > 0:
            self.speed = min(self.speed, self.max_speed)
        else:
            self.speed = max(self.speed, -self.max_speed)

        # keep record of speed
        self.speeds.append(self.speed)

        # return speed
        return self.speed

    def reset(self) -> None:
        """
            A function to reset a motor to its initial state. Resets ``max_speed``, ``motor_inertia_coeff``, ``speed``, history of ``speeds``, ``reversed``, and history of ``reverseds``, as well as the motor's noise source, if it has one.
        """
        self.speed = self.speeds[0]
        self.speeds = [self.speed]

        self.reversed = self.reverseds[0]
        self.reverseds = [self.reversed]

        self.max_speed = self.initial_max_speed
        self.motor_inertia_coeff = self.initial_motor_inertia_coeff

        if self.noisemaker:
            self.noisemaker.reset()

    def get_data(self) -> Dict[str, Union[List[float], List[bool]]]:
        """
            A function to get a motor's data.

            These data, as and when they are included in the returned dict, can be accessed with the following keys:

            * history of speeds over time: ``data["speeds"]``
            * data of motor's noise source, if it has one: ``data["noises"]``
            * motor's name string: ``data["name_str"]``

            :return: Motor's data.
            :rtype: dict
        """
        data = {"speeds": self.speeds, "reverseds": self.reverseds, "noises": None}
        if self.noisemaker:
            data["noises"] = self.noisemaker.get_data()["noises"]
        data["name_str"] = self.name_str
        return data

    def __eq__(self, other):
        """
            Overrides the == operator for instances of this class.

            :param other: The instance of System that this instance will be compared to.
            :type other: System
        """

        if other == None:
            return False

        # is_eq = super().__eq__(other)

        is_eq = self.speed == other.speed
        is_eq = is_eq and self.speeds == other.speeds

        is_eq = is_eq and self.reversed == other.reversed
        is_eq = is_eq and self.reverseds == other.reverseds

        is_eq = is_eq and self.max_speed == other.max_speed
        is_eq = is_eq and self.motor_inertia_coeff == other.motor_inertia_coeff

        is_eq = is_eq and self.noisemaker == other.noisemaker

        return is_eq
