from .System import *
from .Agent import *
from .noise import *
from .Motor import *
from .MotorSpeedSensor import *
from .CompassSensor import *
from .AntController import *

import math

class Ant(Agent):
    """

    """
    def __init__(self, x: float, y: float, theta: float,
                       controller: AntController,
                       sensors: List[Sensor],
                       sensor_angles: List[float],
                       radius: float=1,
                       move_motor_max_speed: float=2,
                       move_motor_inertia: float=0,
                       move_motor_reversed: bool=False,
                       move_motor_noisemaker: NoiseSource=None,
                       move_motor_sensor_noisemaker: NoiseSource=None,
                       turn_motor_max_speed: float=0.4,
                       turn_motor_inertia: float=0,
                       turn_motor_reversed: bool=False,
                       turn_motor_noisemaker: NoiseSource=None,
                       turn_motor_sensor_noisemaker: NoiseSource=None,
                       colour: str='0x6F0E00FF',
                       light: LightSource=None,
                       energy_sensor_noisemaker: NoiseSource=None,
                       compass_sensor_noisemaker: NoiseSource=None,
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

            :param x: The :class:`Ant`'s initial x-coordinate.
            :type x: float

            :param y: The :class:`Ant`'s initial y-coordinate.
            :type y: float

            :param theta: The :class:`Ant`'s initial orientation.
            :type theta: float

            :param controller: The ant's controller.
            :type controller: :class:`AntController`

            :param sensors: An :class:`Ant` has a list of 5 sensors by default: an internal energy sensor, a compass sensors, and a motor speed sensor for each of its 2 motors. The list of sensors passed in here will be joined to that list. The ant's :class:`EnergySensor` is at index ``0`` in the list, its :class:`BumpSensor` is at index ``1``, its :class:`CompassSensor` is at index ``2``, and its move and turn motor sensors are at indices ``3`` and ``4`` respectively. Therefore, any other sensors will be at indices ``5`` and up.
            :type sensors: list[:class:`Sensor`]

            :param sensor_angles: A list of angles for the sensors passed in as the ``sensors`` parameter. This list should have exactly the same length as ``sensors``. For any sensor which has ``None`` as its corresponding entry in ``sensor_angles``, its position will be at the centre of the ant's body. For any sensor which has an angle specified, the sensor will lie on the circumference of the ant's body, at the specified angle from its forward direction.
            :type sensor_angles: list[float]

            :param radius: The radius of the :class:`Ant`'s body. Defaults to ``1``.
            :type radius: float

            :param move_motor_max_speed: The maximum speed that the ant can move at in the x-y plane. Defaults to ``2``
            :type move_motor_max_speed: float

            :param move_motor_inertia: The inertia on the ant's move motor. Defaults to ``0``.
            :type move_motor_inertia: float

            :param move_motor_reversed: The reversed state of the ant's move motor. Defaults to ``False``.
            :type move_motor_reversed: bool

            :param move_motor_noisemaker: The noise source for the ant's move motor. Defaults to ``None``.
            :type move_motor_noisemaker: NoiseSource

            :param move_motor_sensor_noisemaker: The noise source for the ant's move motor sensor. Defaults to ``None``.
            :type move_motor_sensor: NoiseSource

            :param turn_motor_max_speed: The maximum speed for the ant's turn motor. Defaults to ``0.4``
            :type turn_motor_max_speed: float

            :param turn_motor_inertia: The inertia on the ant's turn motor. Defaults to ``0``.
            :type turn_motor_inertia: float

            :param turn_motor_reversed: The reversed state of the ant's turn motor. Defaults to ``False``.
            :type turn_motor_reversed: bool

            :param turn_motor_noisemaker: The noise source for the ant's turn motor. Defaults to ``None``.
            :type turn_motor_noisemaker: NoiseSource

            :param turn_motor_sensor_noisemaker: The noise source for the ant's turn motor sensor. Defaults to ``None``.
            :type turn_motor_sensor_noisemaker: NoiseSource

            :param colour: The colour of the ant's body. Defaults to ``'0x6F0E00FF``
            :type colour: str

            :param light: The :class:`LightSource` attached to the :class:`Ant`'s body. Defaults to ``None``.
            :type light: :class:`LightSource`

            :param energy_sensor_noisemaker: A source of noise for the `Ant`'s energy sensor. Defaults to ``None``.
            :type energy_sensor_noisemaker: subclass of :class:`NoiseSource`

            :param compass_sensor_noisemaker: The noise source for the ant's compass sensor. Defaults to ``None``,
            :type compass_sensor_noisemaker: :class:`NoiseSource`

            :param action_energy_cost: The energetic cost of action. Defaults to ``0``. The cost of action in a single simulation step, for each of the ant's 2 motors, is ``abs(motor speed) * dt * action_energy_cost``.
            :type action_energy_cost: float

            :param metabolism_energy_cost: The energetic cost of existing. The main reason for this cost is that without it, ants can survive for indefinite periods without moving/acting at all. When ants can "die" by not acting, there is a pressure (e.g. selective pressure, if evolving) to act, and potentially to also adapt. Defaults to ``0``.
            :type metabolism_energy_cost: float

            :param alive: If an ant runs our of energy, it will "die", at which point its ``alive`` parameter will be set to ``False``, and the ant will cease to act (although in the current implementation, its controller will continue to function as normal). Defaults to ``True``.
            :type alive: bool

            :param maximum_energy: The maximum energy level the ant can have. Defaults to ``0``.
            :type maximum_energy: float

            :param initial_energy: The ant's initial energy level. Defaults to ``1``.
            :type initial_energy: float

            :param init_fun: A function which can be used to set the initial state of the system in each simulation run. Defaults to ``None``.
            :type init_fun: function

            :param perturb_fun: A function which can be used to perturb the ant's state. This will  typically be used at the beginning of simulation runs.  Defaults to ``None``.
            :type perturb_fun: function

            :param pheromone_manager: If a :class:`Ant` has a pheromone manager, then it will drop pheromones (similarly to an ant laying trails). Defaults to ``None``.
            :type pheromone_manager: :class:`PheromoneManager`

            :param drop_interval: The interval between which the ant will drop pheromones, if its ``pheromone_manager`` is not ``None``. Defaults to ``0.5``.
            :type drop_interval: float

            :param consumables: The list of consumables which this agent can consume.
            :type consumables: list(:class:`Consumable`)

		"""
        super().__init__(x, y, colour, theta, radius, light, energy_sensor_noisemaker, action_energy_cost, metabolism_energy_cost, alive, maximum_energy, initial_energy, init_fun=init_fun, perturb_fun=perturb_fun, pheromone_manager=pheromone_manager, drop_interval=drop_interval, p_bump_noise=p_bump_noise)  # call Agent constructor

        self.controller: AntController = controller

        self.move_motor: Motor = Motor(max_speed=move_motor_max_speed, motor_inertia_coeff=move_motor_inertia, reversed=move_motor_reversed, noisemaker=move_motor_noisemaker, name_str="Speed motor")
        self.turn_motor: Motor = Motor(max_speed=turn_motor_max_speed, motor_inertia_coeff=turn_motor_inertia, reversed=turn_motor_reversed, noisemaker=turn_motor_noisemaker, name_str="Orientation & Heading motor")

        self.sensor_angles: List[float] = [None, None, 0, None, None] + sensor_angles

        self.sensors.append(CompassSensor(x=x, y=y, theta=theta, noisemaker=compass_sensor_noisemaker))

        move_motor_sensor = MotorSpeedSensor(motor=self.move_motor,  noisemaker=move_motor_sensor_noisemaker, name_str="Move motor sensor")
        turn_motor_sensor = MotorSpeedSensor(motor=self.turn_motor,  noisemaker=turn_motor_sensor_noisemaker, name_str="Turn motor sensor")

        self.sensors += [move_motor_sensor, turn_motor_sensor] + sensors

        self.consumables = consumables

        self.initial_sensors = cp.copy(self.sensors)
        self.initial_sensor_angles = cp.copy(self.sensor_angles)

        self.update_children_positions()  # update sensor positions according to ant's state

    def step_sensors(self, dt: float) -> List[float]:
        """
            Only called from step().

            A method which steps the sensors in the ant's `sensors` list, and returns the sensor activations in a list.

            :param dt: Interval of time to integrate the ant's sensors over.
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

            A method which gets motor speed commands by calling the step method of the ant's controller.

            :param dt: Interval of time to integrate the ant's controller over.
            :type dt: float

            :param activations: The sensory inputs to the ant's controller. A list of the activation levels for each of the ant's sensors.
            :type activations: list[float]
        """
        return self.controller.step(dt, activations)

    def step_actuators(self, speed_commands: List[float], dt: float) -> List[float]:
        """
            Update the ant's motor speeds, based on the commands from the ant's controller and its motors' dynamics (i.e. current speeds and inertias).

            :param dt: Interval of time to integrate the ant's motors over.
            :type dt: float

            :param speed_commands: The motor speed commands which are generated by the ant's controller.
            :type speed_commands: list[float]
        """
        move_speed = self.move_motor.step(speed_commands[0], dt)
        turn_speed = self.turn_motor.step(speed_commands[1], dt)

        return [move_speed, turn_speed]

    def integrate(self, speeds: List[float], dt: float) -> None:
        """
            Integrate the ant's motion based on its motor speeds.

            Only called from step().

            Applies a motor activation vector to an ant state, and simulates the consequences using Euler integration over a dt interval.

            :param dt: Interval of time to integrate the ant's motion over.
            :type dt: float

            :param speeds: The ant's motor speeds.
            :type speeds: list[float]
        """
        self.theta += speeds[1] * dt

        self.x += speeds[0] * math.cos(self.theta) * dt
        self.y += speeds[0] * math.sin(self.theta) * dt

    def update_energy(self, actual_speeds, dt):
        """
            Update the ant's energy level, based on its metabolic and action costs.

            :param dt: Interval of time to integrate the ant's energy losses over.
            :type dt: float

            :param actual_speeds: The ant's current motor speeds.
            :type actual_speeds: list[float]
        """
        # energy losses - allows ant to die here *before* it can consume anything
        if self.alive:
            # update energy. the faster the ant's wheels turn, the quicker it loses energy
            self.energy -= np.abs(actual_speeds[0]) * dt * self.action_energy_cost
            self.energy -= np.abs(actual_speeds[1]) * dt * self.action_energy_cost
            self.energy -= dt * self.metabolism_energy_cost  # some energy is lost even if the ant does not move
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
            This method is used to update the positions and orientations of a ant's attached subsystems, such as its sensors, as the ant moves.
        """
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
            Get the ant's simulation data, including the data from its sensors, motors and controller.

            These data, as and when they are included in the returned dict, can be accessed with the following keys:

            * data inherited from :class:`Agent`: see :class:`Agent`
            * class name (Ant): ``data["classname"]``
            * data from the ant's controller: ``data["controller"]``
            * data from the ant's sensors: ``data["sensors"]``
            * data from the ant's motors: ``data["motors"]``
        """
        data = super().get_data()

        data["classname"] = "Ant"

        data["sensors"] = []
        for sensor in self.sensors:
            data["sensors"].append(sensor.get_data())

        # data["move_motor"] = self.move_motor.get_data()
        # data["turn_motor"] = self.turn_motor.get_data()

        data["motors"] = [self.move_motor.get_data(), self.turn_motor.get_data()]

        data["controller"] = self.controller.get_data()

        # WHAT TO DO ABOUT CONSUMABLES?

        return data

    def reset(self, reset_controller: bool=True) -> None:
        """
            This method resets an ant's state and simulation data to their initial values, so that it can be used again.

            :param reset_controller: determines whether or not the ant's controller is also reset, defaults to ``True``. This is because sometimes you might want to reset a ant and simulate it again taking advantage of any information or learning which the controller has acquired.
            :type reset_controller: bool
        """
        super().reset()
        self.move_motor.reset()
        self.turn_motor.reset()

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

            :param other: The instance of System that this instance will be compared to.
            :type other: System
        """

        if other == None:
            return False

        is_eq = super().__eq__(other)

        is_eq = is_eq and self.sensors == other.sensors
        is_eq = is_eq and self.sensor_angles and other.sensor_angles
        is_eq = is_eq and self.controller == other.controller
        is_eq = is_eq and self.move_motor == other.move_motor
        is_eq = is_eq and self.turn_motor == other.turn_motor

        return is_eq

    def draw(self, ax) -> None:
        """
            Draw ant in specified Matplotlib axes.

            :param
            :type
        """
        ax.plot([self.x, self.x+self.radius*np.cos(self.theta)],
                 [self.y, self.y+self.radius*np.sin(self.theta)], 'k--', linewidth='2')
        ax.add_artist(mpatches.Circle((self.x, self.y), self.radius, color=self.colour))
        wheels = [mpatches.Rectangle((-0.5*self.radius, y), width=self.radius, height=0.2*self.radius, color="black") for y in (-1.1*self.radius, 0.9*self.radius)]

        for sensor in self.sensors[1:]:
            sensor.draw(ax)
            # self.__draw_FOV(sensor, ax)

        if self.light:
            self.light.draw(ax)

    def pygame_draw(self, screen, scale: float, shiftx: float, shifty: float) -> None:
        """
            A method for drawing an :class:`Ant` on a PyGame display.

            :param screen: The PyGame display to draw on.
            :type screen: PyGame display

            :param scale: The scale to draw at.
            :type scale: float

            :param shiftx: The offset from centre in the x-axis for drawing.
            :type shiftx: float

            :param shifty: The offset from centre in the y-axis for drawing.
            :type shifty: float
        """
        self.__pygame_draw_legs(screen, scale, shiftx, shifty)

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

    def __pygame_draw_legs(self, screen, scale: float, shiftx: float, shifty: float) -> None:
        """
            A method for drawing an :class:`Ant`'s legs on a PyGame display.

            :param screen: The PyGame display to draw on.
            :type screen: PyGame display

            :param scale: The scale to draw at.
            :type scale: float

            :param shiftx: The offset from centre in the x-axis for drawing.
            :type shiftx: float

            :param shifty: The offset from centre in the y-axis for drawing.
            :type shifty: float
        """
        x1, y1, x2, y2 = self.leg_ends(0.4, 1.3)
        pygame.draw.line(screen, color='red',
                         start_pos=(scale * x1 + shiftx, scale * y1 + shifty),
                         end_pos=(scale * x2 + shiftx, scale * y2 + shifty), width=2)

        x1, y1, x2, y2 = self.leg_ends(0, 1.3)
        pygame.draw.line(screen, color='red',
                         start_pos=(scale * x1 + shiftx, scale * y1 + shifty),
                         end_pos=(scale * x2 + shiftx, scale * y2 + shifty), width=2)

        x1, y1, x2, y2 = self.leg_ends(-0.4, 1.3)
        pygame.draw.line(screen, color='red',
                      start_pos=(scale * x1 + shiftx, scale * y1 + shifty),
                      end_pos=(scale * x2 + shiftx, scale * y2 + shifty), width=2)

    def leg_ends(self, offset_scale, relative_length):
        """
            A method for calculating the coordinates of an ant's leg ends.

            :param
            :type

            :param
            :type
        """
        offset = offset_scale * self.radius
        mid_x = self.x + offset * math.cos(self.theta)
        mid_y = self.y + offset * math.sin(self.theta)

        x1 = mid_x + relative_length * math.cos(self.theta + math.pi/2)
        y1 = mid_y + relative_length * math.sin(self.theta + math.pi/2)
        x2 = mid_x + relative_length * math.cos(self.theta - math.pi/2)
        y2 = mid_y + relative_length * math.sin(self.theta - math.pi/2)

        return x1, y1, x2, y2
