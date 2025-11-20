from .base import *
from .stimuli import *
from .LightSensor import *
from .Agent import *
from .Motor import *
from .MotorSpeedSensor import *
from .RobotController import *
from .noise import *
from .pygame_functions import *

class Robot(Agent):
    """
        A class to represent a robot with a differential drive.
    """
    def __init__(self, x: float,
                       y: float,
                       controller: RobotController,
                       sensors: List[LightSensor],
                       sensor_angles: List[float],
                       radius: float=1,
                       theta: float=0,
                       left_motor_max_speed: float=2,
                       right_motor_max_speed: float=2,
                       left_motor_inertia: float=0,
                       right_motor_inertia: float=0,
                       left_motor_noisemaker: NoiseSource=None,
                       right_motor_noisemaker: NoiseSource=None,
                       left_motor_reversed: bool=False,
                       right_motor_reversed: bool=False,
                       left_motor_sensor_noisemaker: NoiseSource=None,
                       right_motor_sensor_noisemaker: NoiseSource=None,
                       energy_sensor_noisemaker: NoiseSource=None,
                       colour: str='darkblue',
                       light: LightSource=None,
                       action_energy_cost: float=0,
                       metabolism_energy_cost: float=0,
                       alive: bool=True,
                       maximum_energy: float=0,
                       initial_energy: float=1,
                       consumables=None,
                       init_fun: Callable=None,
                       perturb_fun: Callable=None,
                       pheromone_manager=None,
                       drop_interval=0.5,
                       p_bump_noise=0):
        """
            __init__(self, x: float, y: float, controller: RobotController, sensors: List[LightSensor], sensor_angles: List[float], radius: float=1, theta: float=0, left_motor_max_speed: float=2, right_motor_max_speed: float=2, left_motor_inertia: float=0, right_motor_inertia: float=0, left_motor_noisemaker: NoiseSource=None, right_motor_noisemaker: NoiseSource=None, left_motor_reversed: bool=False, right_motor_reversed: bool=False, left_motor_sensor_noisemaker: NoiseSource=None, right_motor_sensor_noisemaker: NoiseSource=None, energy_sensor_noisemaker: NoiseSource=None, colour: str='darkblue', light: LightSource=None, action_energy_cost: float=0, metabolism_energy_cost: float=0, alive: bool=True, maximum_energy: float=0, initial_energy: float=1, consumables=None, init_fun: Callable=None, perturb_fun: Callable=None, pheromone_manager=None, drop_interval=0.5, p_bump_noise=0)

            :param x: The :class:`Robot`'s initial x-coordinate.
            :type x: float

            :param y: The :class:`Robot`'s initial y-coordinate.
            :type y: float

            :param theta: The :class:`Robot`'s initial orientation. Defaults to ``0``.
            :type theta: float

            :param radius: The radius of the :class:`Robot`'s body. Defaults to ``1``.
            :type radius: float

            :param light: The :class:`LightSource` attached to the :class:`Robot`'s body. Defaults to ``None``.
            :type light: :class:`LightSource`

            :param colour: The colour of the :class:`Robot`'s body. Defaults to ``"darkblue"``.
            :type colour: str

            :param energy_sensor_noisemaker: A source of noise for the `Robot`'s energy sensor. Defaults to ``None``.
            :type energy_sensor_noisemaker: subclass of :class:`NoiseSource`

            :param action_energy_cost: The energetic cost of action. Defaults to ``0``. The cost of action in a single simulation step, for each of the robot's 2 motors, is ``abs(motor speed) * dt * action_energy_cost``.
            :type action_energy_cost: float

            :param metabolism_energy_cost: The energetic cost of existing. The main reason for this cost is that without it, robots can survive for indefinite periods without moving/acting at all. When robots can "die" by not acting, there is a pressure (e.g. selective pressure, if evolving) to act, and potentially to also adapt. Defaults to ``0``.
            :type metabolism_energy_cost: float

            :param alive: If a robot runs our of energy, it will "die", at which point its ``alive`` parameter will be set to ``False``, and the robot will cease to act (although in the current implementation, its controller will continue to function as normal). Defaults to ``True``.
            :type alive: bool

            :param maximum_energy: The maximum energy level the robot can have. Defaults to ``0``.
            :type maximum_energy: float

            :param initial_energy: The robot's initial energy level. Defaults to ``1``.
            :type initial_energy: float

            :param init_fun: A function which can be used to set the initial state of the system in each simulation run. Defaults to ``None``.
            :type init_fun: function

            :param perturb_fun: A function which can be used to perturb the robot's state. This will  typically be used at the beginning of simulation runs.  Defaults to ``None``.
            :type perturb_fun: function

            :param pheromone_manager: If a :class:`Robot` has a pheromone manager, then it will drop pheromones (similarly to an ant laying trails). Defaults to ``None``.
            :type pheromone_manager: :class:`PheromoneManager`

            :param drop_interval: The interval between which the robot will drop pheromones, if its ``pheromone_manager`` is not ``None``. Defaults to ``0.5``.
            :type drop_interval: float

            :param left_motor_max_speed: The maximum speed, in either direction, for the robot's left motor. Defaults to ``2``.
            :type left_motor_max_speed: float

            :param right_motor_max_speed: The maximum speed, in either direction, for the robot's right motor. Defaults to ``2``.
            :type right_motor_max_speed: float

            :param left_motor_inertia: The inertia (resistance to change of speed) of the robot's left motor. Defaults to ``0``.
            :type left_motor_inertia: float

            :param right_motor_inertia: The inertia (resistance to change of speed) of the robot's right motor. Defaults to ``0``.
            :type right_motor_inertia: float

            :param left_motor_noisemaker: A source of noise for the robot's left :class:`Motor`.
            :type left_motor_noisemaker: :class:`NoiseSource`

            :param right_motor_noisemaker: A source of noise for the robot's right :class:`Motor`.
            :type right_motor_noisemaker: :class:`NoiseSource`

            :param left_motor_reversed: A flag to determine whether the robot's left motor is running in the forwards (for ``False``) or reversed direction (for ``True``). Defaults to ``False``.
            :type left_motor_reversed: bool

            :param right_motor_reversed: A flag to determine whether the robot's right motor is running in the forwards (for ``False``) or reversed direction (for ``True``). Defaults to ``False``.
            :type right_motor_reversed: bool

            :param left_motor_sensor_noisemaker: A source of noise for the robot's left :class:`MotorSpeedSensor`.
            :type left_motor_sensor_noisemaker: :class:`NoiseSource`

            :param right_motor_sensor_noisemaker: A source of noise for the robot's right :class:`MotorSpeedSensor`.
            :type right_motor_sensor_noisemaker: :class:`NoiseSource`

            :param controller: The robot's controller.
            :type controller: :class:`RobotController`

            :param sensors: A :class:`Robot` has a list of 4 sensors by default: an internal energy sensor, a bump sensor, and a motor speed sensor for each of its 2 motors. The list of sensors passed in here will be joined to that list. The robot's energy sensor is at index ``0`` in the list, the bump sensor is at index ``1``, its left motor speed sensor is at index ``2``, and its right motor speed sensor is at index ``3``. Therefore, any other sensors will be at indices ``4`` and up.
            :type sensors: list[:class:`Sensor`]

            :param sensor_angles: A list of angles for the sensors passed in as the ``sensors`` parameter. This list should have exactly the same length as ``sensors``. For any sensor which has ``None`` as its corresponding entry in ``sensor_angles``, its position will be at the centre of the robot's body. For any sensor which has an angle specified, the sensor will lie on the circumference of the robot's body, at the specified angle from its forward direction.
            :type sensor_angles: list[float]

            :param consumables: The list of consumables which this agent can consume.
            :type consumables: list(:class:`Consumable`)
        """
        super().__init__(x, y, colour, theta, radius, light, energy_sensor_noisemaker, action_energy_cost, metabolism_energy_cost, alive, maximum_energy, initial_energy, init_fun=init_fun, perturb_fun=perturb_fun, pheromone_manager=pheromone_manager, drop_interval=drop_interval, p_bump_noise=p_bump_noise)  # call Agent constructor

        self.controller: Controller = controller  # the controller for the robot, which will set motor speeds according to how stimulated the robot's sensors are

        # self.sensors: List[LightSensor] = sensors
        self.sensor_angles: List[float] = [None, None, None, None] + sensor_angles

        self.left_motor: Motor = Motor(max_speed=left_motor_max_speed, motor_inertia_coeff=left_motor_inertia, reversed=left_motor_reversed, noisemaker=left_motor_noisemaker, name_str="Left motor")
        self.right_motor: Motor = Motor(max_speed=right_motor_max_speed, motor_inertia_coeff=right_motor_inertia, reversed=right_motor_reversed, noisemaker=right_motor_noisemaker, name_str ="Right motor")

        left_motor_sensor = MotorSpeedSensor(motor=self.left_motor, noisemaker=left_motor_sensor_noisemaker, name_str="Left motor sensor")
        right_motor_sensor = MotorSpeedSensor(motor=self.right_motor, noisemaker=right_motor_sensor_noisemaker, name_str="Right motor sensor")

        self.sensors += [left_motor_sensor, right_motor_sensor] + sensors

        self.consumables = consumables

        self.initial_sensors = cp.copy(self.sensors)
        self.initial_sensor_angles = cp.copy(self.sensor_angles)

        self.update_children_positions()  # update sensor positions according to robot's state

    def step_sensors(self, dt: float) -> List[float]:
        """
            Only called from step().

            A method which steps the sensors in the robot's `sensors` list, and returns the sensor activations in a list.

            :param dt: Interval of time to integrate the robot's sensors over.
            :type dt: float
        """
        activations: List[float] = []
        for sensor in self.sensors:
            s = sensor.step(dt)
            activations.append(s)

        return activations

    def control(self, activations: List[float], dt: float) -> List[float]:
        """
            Only called from step().

            A method which gets motor speed commands by calling the step method of the robot's controller.

            :param dt: Interval of time to integrate the robot's controller over.
            :type dt: float

            :param activations: The sensory inputs to the robot's controller. A list of the activation levels for each of the robot's sensors.
            :type activations: list[float]
        """
        # get motor speeds from controller
        left_speed, right_speed = self.controller.step(dt, activations)

        # return speeds to step method
        return [left_speed, right_speed]

    def step_actuators(self, speed_commands: List[float], dt: float) -> List[float]:
        """
            Update the robot's motor speeds, based on the commands from the robot's controller and its motors' dynamics (i.e. current speeds and inertias).

            :param dt: Interval of time to integrate the robot's motors over.
            :type dt: float

            :param speed_commands: The motor speed commands which are generated by the robot's controller.
            :type speed_commands: list[float]
        """
        left_speed = self.left_motor.step(speed_commands[0], dt)
        right_speed = self.right_motor.step(speed_commands[1], dt)

        return [left_speed, right_speed]

    # this is separated from the step method in case we want to override it
    # - one example of why we might want to do this is if we wanted to add collisions
    #   to the simulation. to achieve this, we could do something like create a subclass of
    #   Robot, with its own integrate method, which calls this one and then superimposes
    #   an additional movement due to collisions
    def integrate(self, speeds: List[float], dt: float) -> None:
        """
            Integrate the robot's motion based on its motor speeds.

            Only called from step().

            Applies a motor activation vector to a robot state, and simulates the consequences using Euler integration over a dt interval.

            :param dt: Interval of time to integrate the robot's motion over.
            :type dt: float

            :param speeds: The robot's motor speeds.
            :type speeds: list[float]
        """
        # calculate the linear speed and angular speed
        v = np.mean([speeds[0], speeds[1]])
        omega = (speeds[1] - speeds[0]) / (2.0 * self.radius)

        state = np.array([self.x, self.y, self.theta])

        # calculate time derivative of state
        deriv = [v * np.cos(state[2]), v * np.sin(state[2]), omega]

        # perform Euler integration
        state = dt * np.array(deriv) + state

        # store robot state
        self.x = state[0]
        self.y = state[1]
        self.theta = state[2]

    def update_energy(self, actual_speeds, dt):
        """
            Update the robot's energy level, based on its metabolic and action costs.

            :param dt: Interval of time to integrate the robot's energy losses over.
            :type dt: float

            :param actual_speeds: The robot's current motor speeds.
            :type actual_speeds: list[float]
        """
        # energy losses - allows robot to die here *before* it can consume anything
        if self.alive:
            # update energy. the faster the robot's wheels turn, the quicker it loses energy
            self.energy -= np.abs(actual_speeds[0]) * dt * self.action_energy_cost
            self.energy -= np.abs(actual_speeds[1]) * dt * self.action_energy_cost
            self.energy -= dt * self.metabolism_energy_cost  # some energy is lost even if the robot does not move
            self.energy = max(self.energy, 0)  # prevent energy falling below zero

            if self.energy <= 0:
                self.alive = False

        # energy consumption - can include gains and losses ("negative energy")
        if self.consumables is not None and self.alive:
            for consumable in self.consumables:
                if np.linalg.norm([self.x-consumable.x, self.y-consumable.y]) < consumable.radius:
                    self.energy += consumable.consume()
            self.energy = max(self.energy, 0) # prevent energy falling below zero
            self.energy = min(self.energy, self.maximum_energy) # prevent energy going over "full"

            if self.energy <= 0:
                self.alive = False

    # update positions and orientations of all sensors
    def update_children_positions(self) -> None:
        """
            This method is used to update the positions and orientations of a robot's attached subsystems, such as its sensors, as the robot moves.
        """
        # update light positions
        if self.light:
            self.light.x = self.x
            self.light.y = self.y
            self.light.theta = self.theta

        # update sensor positions
        for i, sensor in enumerate(self.sensors):
            if self.sensor_angles[i] is None:
                sensor.x = self.x
                sensor.y = self.y
            else:
                sensor.x = self.x + (self.radius * np.cos(self.theta + self.sensor_angles[i]))
                sensor.y = self.y + (self.radius * np.sin(self.theta + self.sensor_angles[i]))
                sensor.theta = self.thetas[-1] + self.sensor_angles[i]

    def get_data(self) -> Dict[str, Dict[str, Any]]:
        """
            A function to get the data from an :class:`Robot`, in the form of a string-keyed dict.

            These data, as and when they are included in the returned dict, can be accessed with the following keys:

            * data inherited from :class:`Agent`: see :class:`Agent`
            * class name (Robot): ``data["classname"]``
            * data from the robot's controller: ``data["controller"]``
            * data from the robot's sensors: ``data["sensors"]``
            * data from the robot's motors: ``data["motors"]``
        """
        data = super().get_data()

        data["classname"] = "Robot"

        data["sensors"] = []
        for sensor in self.sensors:
            data["sensors"].append(sensor.get_data())

        # keep these lines temporarily, so as not to break plotting code
        data["left_motor"] = self.left_motor.get_data()
        data["right_motor"] = self.right_motor.get_data()
        # this will replace the lines above
        data["motors"] = [self.left_motor.get_data(), self.right_motor.get_data()]

        data["controller"] = self.controller.get_data()

        return data

    def reset(self, reset_controller: bool=True) -> None:
        """
            This method resets a robot's state and simulation data to their initial values, so that it can be used again.

            :param reset_controller: determines whether or not the robot's controller is also reset, defaults to ``True``. This is because sometimes you might want to reset a robot and simulate it again taking advantage of any information or learning which the controller has acquired.
            :type reset_controller: bool
        """
        super().reset()
        self.left_motor.reset()
        self.right_motor.reset()

        # this assumes that no sensors have been added or removed
        for i, sensor in enumerate(self.sensors):
            sensor.reset()
            self.sensors[i] = self.initial_sensors[i]
        for i, a in enumerate(self.sensor_angles):
            self.sensor_angles[i] = self.initial_sensor_angles[i]

        self.update_children_positions()

        if reset_controller:
            self.controller.reset()

    def __eq__(self, other):
        """
            Overrides the == operator for instances of this class.

            :param other: The instance of :class:`Robot` that this instance will be compared to.
            :type other: System
        """

        if other == None:
            return False

        is_eq = super().__eq__(other)

        is_eq = is_eq and self.sensor_angles and other.sensor_angles
        is_eq = is_eq and self.left_motor == other.left_motor
        is_eq = is_eq and self.right_motor == other.right_motor

        return is_eq

    # draw robot in the specified matplotlib axes
    def draw(self, ax) -> None:
        """
            Draw robot in specified Matplotlib axes.

            :param ax: The Matplotlib axes to draw the robot on.
            :type ax: Matplotlib axes
        """
        ax.plot([self.x, self.x+self.radius*np.cos(self.theta)],
                 [self.y, self.y+self.radius*np.sin(self.theta)], 'k--', linewidth='2')
        ax.add_artist(mpatches.Circle((self.x, self.y), self.radius, color=self.colour))
        wheels = [mpatches.Rectangle((-0.5*self.radius, y), width=self.radius, height=0.2*self.radius, color="black") for y in (-1.1*self.radius, 0.9*self.radius)]
        tr = mtransforms.Affine2D().rotate(self.theta).translate(self.x, self.y) + ax.transData
        for wheel in wheels:
            wheel.set_transform(tr)
            ax.add_artist(wheel)

        for sensor in self.sensors[3:]:
            sensor.draw(ax)
            # self.__draw_FOV(sensor, ax)

        if self.light:
            self.light.draw(ax)

    def __wheel_ends(self) -> Tuple[float, float, float, float, float, float, float, float]:
        """
            Generate coordinates used for drawing robot's wheels.
        """
        offset = 0.95

        left_mid_x = self.x + (offset * self.radius * math.cos(self.theta + math.pi/2))
        left_mid_y = self.y + (offset * self.radius * math.sin(self.theta + math.pi/2))

        right_mid_x = self.x + (offset * self.radius * math.cos(self.theta + -math.pi/2))
        right_mid_y = self.y + (offset * self.radius * math.sin(self.theta + -math.pi/2))

        half_wheel_len = 0.5 * self.radius

        left_end_x = left_mid_x + half_wheel_len * math.cos(self.theta)
        left_end_y = left_mid_y + half_wheel_len * math.sin(self.theta)

        right_end_x = right_mid_x + half_wheel_len * math.cos(self.theta)
        right_end_y = right_mid_y + half_wheel_len * math.sin(self.theta)

        left_end_x2 = left_mid_x - half_wheel_len * math.cos(self.theta)
        left_end_y2 = left_mid_y - half_wheel_len * math.sin(self.theta)

        right_end_x2 = right_mid_x - half_wheel_len * math.cos(self.theta)
        right_end_y2 = right_mid_y - half_wheel_len * math.sin(self.theta)

        return left_end_x, left_end_y, right_end_x, right_end_y, left_end_x2, left_end_y2, right_end_x2, right_end_y2

    # draw robot in a pygame display
    def pygame_draw(self, screen, scale: float, shiftx: float, shifty: float) -> None:
        """
            Draw robot on PyGame display.

            :param screen: The PyGame display to draw on.
            :type screen: PyGame display

            :param scale: The scale to draw at.
            :type scale: float

            :param shiftx: The offset from centre in the x-axis for drawing.
            :type shiftx: float

            :param shifty: The offset from centre in the y-axis for drawing.
            :type shifty: float
        """
        self.__pygame_draw_wheels(screen, scale, shiftx, shifty)

        pygame_drawcircle(screen, shiftx, shifty, scale, self.x, self.y, self.radius, self.colour)

        for sensor in self.sensors[3:]:
            sensor.pygame_draw(screen, scale, shiftx, shifty)

        end_x = self.x + self.radius * np.cos(self.theta)
        end_y = self.y + self.radius * np.sin(self.theta)
        pygame_drawline(screen, shiftx, shifty, scale, self.x, self.y, end_x, end_y, 'green', 2)

        if self.light:
            self.light.pygame_draw(screen, scale, shiftx, shifty)

    def __pygame_draw_wheels(self, screen, scale: float, shiftx: float, shifty: float) -> None:
        """
            Draw the robot's wheels on a PyGame display.

            :param screen: The PyGame display to draw on.
            :type screen: PyGame display

            :param scale: The scale to draw at.
            :type scale: float

            :param shiftx: The offset from centre in the x-axis for drawing.
            :type shiftx: float

            :param shifty: The offset from centre in the y-axis for drawing.
            :type shifty: float
        """
        left_end_x, left_end_y, right_end_x, right_end_y, left_end_x2, left_end_y2, right_end_x2, right_end_y2 = self.__wheel_ends()

        pygame_drawline(screen, shiftx, shifty, scale, left_end_x, left_end_y, left_end_x2, left_end_y2, 'red', 6)

        pygame_drawline(screen, shiftx, shifty, scale, right_end_x, right_end_y, right_end_x2, right_end_y2, 'red', 6)
