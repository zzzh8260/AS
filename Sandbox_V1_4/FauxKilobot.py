from .Agent import *
from .FauxKilobotController import *
from .Motor import *
from .noise import *
from .pygame_functions import *
from .Radio import *
from .CompassSensor import *
from .HeadingSensor import *
from .MotorSpeedSensor import *

class FauxKilobot(Agent):
    """
        A class to simulate a robot which is loosely inspired by Kilobot.
    """
    def __init__(self, x: float, y: float, theta: float,
                       controller: FauxKilobotController,
                       sensors: List[Sensor],
                       sensor_angles: List[float],
                       radius: float=1,
                       move_motor_max_speed: float=2,
                       colour: str='#A020F0',
                       light: LightSource=None,
                       energy_sensor_noisemaker: NoiseSource=None,
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
                       radio_t_range=3,
                       radio_r_range=3,
                       radio_enabled=True,
                       move_motor_sensor_noisemaker=None,
                       turn_motor_sensor_noisemaker=None,
                       move_motor_noisemaker=None,
                       turn_motor_noisemaker=None,
					   p_bump_noise=0):
        """
            __init__(self, x: float, y: float, theta: float, controller: FauxKilobotController, sensors: List[Sensor], sensor_angles: List[float], radius: float=1, move_motor_max_speed: float=2, colour: str='#A020F0', light: LightSource=None, energy_sensor_noisemaker: NoiseSource=None, action_energy_cost: float=0, metabolism_energy_cost: float=0, alive: bool=True, maximum_energy: float=0, initial_energy: float=1, consumables=None, init_fun: Callable=None, perturb_fun: Callable=None, pheromone_manager=None, drop_interval=0.5, radio_t_range=3, radio_r_range=3, radio_enabled=True, move_motor_sensor_noisemaker=None, turn_motor_sensor_noisemaker=None, move_motor_noisemaker=None, turn_motor_noisemaker=None,
            p_bump_noise=0)

            :param x: The :class:`FauxKilobot`'s initial x-coordinate.
            :type x: float

            :param y: The :class:`FauxKilobot`'s initial y-coordinate.
            :type y: float

            :param theta: The :class:`FauxKilobot`'s initial orientation. Defaults to ``0``.
            :type theta: float

            :param radius: The radius of the :class:`FauxKilobot`'s body. Defaults to ``1``.
            :type radius: float

            :param colour: The colour of the :class:`FauxKilobot`'s body. Defaults to ``'#A020F0'``.
            :type colour: str

            :param light: The :class:`LightSource` attached to the :class:`FauxKilobot`'s body. Defaults to ``None``.
            :type light: :class:`LightSource`

            :param controller: the FauxKilobot's controller.
            :type controller: :class:`FauxKilobotController`

            :param sensors: A :class:`FauxKilobot` has a list of 6 sensors by default: an internal energy sensor, a bump sensor, compass and heading sensors, and a motor speed sensor for each of its 2 motors. The list of sensors passed in here will be joined to that list. The FauxKilobot's :class:`EnergySensor` is at index ``0`` in the list, its :class:`BumpSensor` is at index ``1`` in the list, its :class:`CompassSensor` is at index ``2``, and its :class:`HeadingSensor` is at index ``3``. Its :class:`MotorSpeedSensor` for its translational speed is at index ``4``, and its :class:`MotorSpeedSensor` for its angular speed (to change its body orientation) is at index ``5``. Therefore, any other sensors will be at indices ``6`` and up.
            :type sensors: list[:class:`Sensor`]

            :param sensor_angles: A list of angles for the sensors passed in as the ``sensors`` parameter. This list should have exactly the same length as ``sensors``. For any sensor which has ``None`` as its corresponding entry in ``sensor_angles``, its position will be at the centre of the FauxKilobot's body. For any sensor which has an angle specified, the sensor will lie on the circumference of the FauxKilobot's body, at the specified angle from its forward direction.
            :type sensor_angles: list[float]

            :param energy_sensor_noisemaker: A source of noise for the FauxKilobot's energy sensor. Defaults to ``None``.
            :type energy_sensor_noisemaker: subclass of :class:`NoiseSource`

            :param action_energy_cost: The energetic cost of action. Defaults to ``0``. The cost of action in a single simulation step, for each of the FauxKilobot's 2 motors, is ``abs(motor speed) * dt * action_energy_cost``.
            :type action_energy_cost: float

            :param metabolism_energy_cost: The energetic cost of existing. The main reason for this cost is that without it, FauxKilobots can survive for indefinite periods without moving/acting at all. When FauxKilobots can "die" by not acting, there is a pressure (e.g. selective pressure, if evolving) to act, and potentially to also adapt. Defaults to ``0``.
            :type metabolism_energy_cost: float

            :param alive: If a FauxKilobot runs our of energy, it will "die", at which point its ``alive`` parameter will be set to ``False``, and the FauxKilobot will cease to act (although in the current implementation, its controller will continue to function as normal). Defaults to ``True``.
            :type alive: bool

            :param maximum_energy: The maximum energy level the FauxKilobot can have. Defaults to ``0``.
            :type maximum_energy: float

            :param initial_energy: The FauxKilobot's initial energy level. Defaults to ``1``.
            :type initial_energy: float

            :param init_fun: A function which can be used to set the initial state of the system in each simulation run. Defaults to ``None``.
            :type init_fun: function

            :param perturb_fun: A function which can be used to perturb the FauxKilobot's state. This will  typically be used at the beginning of simulation runs.  Defaults to ``None``.
            :type perturb_fun: function

            :param pheromone_manager: If a :class:`FauxKilobot` has a pheromone manager, then it will drop pheromones (similarly to an FauxKilobot laying trails). Defaults to ``None``.
            :type pheromone_manager: :class:`PheromoneManager`

            :param drop_interval: The interval between which the FauxKilobot will drop pheromones, if its ``pheromone_manager`` is not ``None``. Defaults to ``0.5``.
            :type drop_interval: float

            :param consumables: The list of consumables which this agent can consume.
            :type consumables: list(:class:`Consumable`)

            :param turn_motor_noisemaker: The noise source for the FauxKilobot's turn motor. Defaults to ``None``.
            :type turn_motor_noisemaker: NoiseSource

            :param turn_motor_sensor_noisemaker: The noise source for the FauxKilobot's turn motor sensor. Defaults to ``None``.
            :type turn_motor_sensor_noisemaker: NoiseSource

            :param move_motor_noisemaker: The noise source for the FauxKilobot's move motor. Defaults to ``None``.
            :type move_motor_noisemaker: NoiseSource

            :param move_motor_sensor_noisemaker: The noise source for the FauxKilobot's move motor sensor. Defaults to ``None``.
            :type move_motor_sensor: NoiseSource

            :param move_motor_max_speed: The maximum speed that the FauxKilobot can move at in the x-y plane. Defaults to ``2``
            :type move_motor_max_speed: float

            :param radio_t_range: FauxKilobot's :class:`Radio` transmitter range. Defaults to ``3``.
            :type radio_t_range: float

            :param radio_r_range: FauxKilobot's :class:`Radio` receiver range. Defaults to ``3``.
            :type radio_r_range: float

            :param radio_enabled: A flag to set whether the FauxKilobot's :class:`Radio` is enabled. Defaults to ``True``.
            :type radio_enabled: bool

        """
        super().__init__(x, y, colour, theta, radius, light, energy_sensor_noisemaker, action_energy_cost, metabolism_energy_cost, alive, maximum_energy, initial_energy, init_fun=init_fun, perturb_fun=perturb_fun, pheromone_manager=pheromone_manager, drop_interval=drop_interval, p_bump_noise=p_bump_noise)  # call Agent constructor

        self.controller: FauxKilobotController = controller

        self.sensors.append(CompassSensor(x=x, y=y, theta=theta))
        self.sensors.append(HeadingSensor(self))

        self.sensor_angles: List[float] = [None, None, 0, None, None, None] + sensor_angles

        self.move_motor: Motor = Motor(max_speed=move_motor_max_speed, motor_inertia_coeff=0, reversed=False, noisemaker=move_motor_noisemaker, name_str="Speed motor")
        self.turn_motor: Motor = Motor(max_speed=np.inf, motor_inertia_coeff=0, reversed=False, noisemaker=turn_motor_noisemaker, name_str="Orientation & Heading motor")

        move_motor_sensor = MotorSpeedSensor(motor=self.move_motor, noisemaker=move_motor_sensor_noisemaker, name_str="Move motor sensor")
        turn_motor_sensor = MotorSpeedSensor(motor=self.turn_motor, noisemaker=turn_motor_sensor_noisemaker, name_str="Turn motor sensor")

        self.sensors += [move_motor_sensor, turn_motor_sensor] + sensors
        self.consumables = consumables

        self.heading = 0
        self.headings = [self.heading]

        self.radio = Radio(x=self.x, y=self.y, transmitter_range=radio_t_range, receiver_range=radio_r_range, enabled=radio_enabled)

        self.initial_sensors = cp.copy(self.sensors)
        self.initial_sensor_angles = cp.copy(self.sensor_angles)

        self.update_children_positions()  # update sensor positions according to FauxKilobot's state

    def step_sensors(self, dt: float) -> List[float]:
        """
            Only called from step().

            A method which steps the sensors in the FauxKilobot's `sensors` list, and returns the sensor activations in a list.

            :param dt: Interval of time to integrate the FauxKilobot's sensors over.
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

            A method which gets motor speed commands by calling the step method of the FauxKilobot's controller.

            :param dt: Interval of time to integrate the FauxKilobot's controller over.
            :type dt: float

            :param activations: The sensory inputs to the FauxKilobot's controller. A list of the activation levels for each of the FauxKilobot's sensors.
            :type activations: list[float]
        """
        return self.controller.step(dt, activations, self.radio)

    def step_actuators(self, speed_commands: List[float], dt: float) -> List[float]:
        """
            Update the FauxKilobot's motor speeds, based on the commands from the FauxKilobot's controller and its motors' dynamics (i.e. current speeds and inertias).

            :param dt: Interval of time to integrate the FauxKilobot's motors over.
            :type dt: float

            :param speed_commands: The motor speed commands which are generated by the FauxKilobot's controller.
            :type speed_commands: list[float]
        """
        move_speed = self.move_motor.step(speed_commands[0], dt)
        turn_speed = self.turn_motor.step(speed_commands[1], dt)

        return [move_speed, turn_speed]

    def integrate(self, speeds: List[float], dt: float) -> None:
        """
            Integrate the FauxKilobot's motion based on its motor speeds.

            Only called from step().

            Applies a motor activation vector to a FauxKilobot state, and simulates the consequences using Euler integration over a dt interval.

            :param dt: Interval of time to integrate the FauxKilobot's motion over.
            :type dt: float

            :param speeds: The FauxKilobot's motor speeds.
            :type speeds: list[float]
        """
        self.heading += speeds[1] * dt

        self.x += speeds[0] * math.cos(self.heading) * dt
        self.y += speeds[0] * math.sin(self.heading) * dt

    def update_energy(self, actual_speeds, dt):
        """
            Update the FauxKilobot's energy level, based on its metabolic and action costs.

            :param dt: Interval of time to integrate the FauxKilobot's energy losses over.
            :type dt: float

            :param actual_speeds: The FauxKilobot's current motor speeds.
            :type actual_speeds: list[float]
        """
        # energy losses - allows FauxKilobot to die here *before* it can consume anything
        if self.alive:
            # update energy. the faster the robot's motors turn, the quicker it loses energy
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
            This method is used to update the positions and orientations of a FauxKilobot's attached subsystems, such as its sensors, as the FauxKilobot moves.
        """
        self.radio.x = self.x
        self.radio.y = self.y

        # update light positions
        if self.light:
            self.light.x = self.x
            self.light.y = self.y

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
            A function to get the data from a :class:`FauxKilobot`, in the form of a string-keyed dict.

            These data, as and when they are included in the returned dict, can be accessed with the following keys:

            * data inherited from :class:`Agent`: see :class:`Agent`
            * class name (FauxKilobot): ``data["classname"]``
            * data from the FauxKilobot's controller: ``data["controller"]``
            * data from the FauxKilobot's sensors: ``data["sensors"]``
            * data from the FauxKilobot's motors: ``data["motors"]``
            * a complete history of the FauxKilobot's heading: ``data["headings"]``
        """
        data = super().get_data()

        data["classname"] = "FauxKilobot"

        data["sensors"] = []
        for sensor in self.sensors:
            data["sensors"].append(sensor.get_data())

        data["headings"] = self.headings

        data["motors"] = [self.move_motor.get_data(), self.turn_motor.get_data()]

        data["controller"] = self.controller.get_data()

        return data

    def reset(self, reset_controller: bool=True) -> None:
        """
            This method resets a FauxKilobot's state and simulation data to their initial values, so that it can be used again.

            :param reset_controller: determines whether or not the FauxKilobot's controller is also reset, defaults to ``True``. This is because sometimes you might want to reset a FauxKilobot and simulate it again taking advantage of any information or learning which the controller has acquired.
            :type reset_controller: bool
        """
        super().reset()
        self.turn_motor.reset()
        self.move_motor.reset()

        # this assumes that no sensors have been added or removed
        for i, sensor in enumerate(self.sensors):
            sensor.reset()
            self.sensors[i] = self.initial_sensors[i]
        for i, a in enumerate(self.sensor_angles):
            self.sensor_angles[i] = self.initial_sensor_angles[i]

        self.update_children_positions()

        self.heading = self.headings[0]
        self.headings = [self.heading]

        if reset_controller:
            self.controller.reset()

        self.radio.reset()

    def __eq__(self, other):
        """
            Overrides the == operator for instances of this class.

            :param other: The instance of FauxKilobot that this instance will be compared to.
            :type other: System
        """

        if other == None:
            return False

        is_eq = super().__eq__(other)

        is_eq = is_eq and self.sensor_angles and other.sensor_angles
        is_eq = is_eq and self.turn_motor == other.turn_motor
        is_eq = is_eq and self.move_motor == other.move_motor
        is_eq = is_eq and self.heading == other.heading
        is_eq = is_eq and self.headings == other.headings

        return is_eq

    def pygame_draw(self, screen, scale: float, shiftx: float, shifty: float) -> None:
        """
            Draw FauxKilobot on PyGame display.

            :param screen: The PyGame display to draw on.
            :type screen: PyGame display

            :param scale: The scale to draw at.
            :type scale: float

            :param shiftx: The offset from centre in the x-axis for drawing.
            :type shiftx: float

            :param shifty: The offset from centre in the y-axis for drawing.
            :type shifty: float
        """
        pygame.draw.circle(screen, center=(scale*self.x+shiftx, scale*self.y+shifty), color=self.colour, radius=scale*self.radius)

        for sensor in self.sensors:
            sensor.pygame_draw(screen, scale, shiftx, shifty)

        end_x = self.x + self.radius * np.cos(self.theta)
        end_y = self.y + self.radius * np.sin(self.theta)
        pygame.draw.line(screen, color='green',
                         start_pos=(scale * self.x + shiftx, scale * self.y + shifty),
                         end_pos=(scale * end_x + shiftx, scale * end_y + shifty), width=2)

        if self.light:
            self.light.pygame_draw(screen, scale, shiftx, shifty)
