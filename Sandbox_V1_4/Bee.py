from .base import *
from .stimuli import *
from .noise import *
from .Agent import *
from .Motor import *
from .CompassSensor import *
from .HeadingSensor import *
from .BeeController import *
from .MotorSpeedSensor import *

from typing import Dict, List

import math

class Bee(Agent):
    """
       A class to represent a bee, or a drone like a quadcopter, which can control its orientation and direction of travel independently.
    """
    def __init__(self, x: float,
                        y: float,
                        theta: float,
                        heading: float,
                        controller: BeeController,
                        sensors: List[Sensor],
                        sensor_angles: List[float],
                        radius: float=1,
                        max_speed: float=2,
                        theta_inertia: float=0,
                        speed_inertia: float=0,
                        heading_inertia: float=0,
                        colour: str='0x00FFFFFF',
                        light=None,
                        speed_motor_noisemaker=None,
                        heading_motor_noisemaker=None,
                        theta_motor_noisemaker=None,
                        speed_motor_sensor_noisemaker=None,
                        heading_motor_sensor_noisemaker=None,
                        theta_motor_sensor_noisemaker=None,
                        energy_sensor_noisemaker: NoiseSource=None,
                        compass_sensor_noisemaker: NoiseSource=None,
                        heading_sensor_noisemaker: NoiseSource=None,
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
            __init__(self, x: float, y: float, theta: float, heading: float, controller: BeeController, sensors: List[Sensor], sensor_angles: List[float], radius: float=1, max_speed: float=2, theta_inertia: float=0, speed_inertia: float=0, heading_inertia: float=0, colour: str='0x00FFFFFF', light=None, speed_motor_noisemaker=None, heading_motor_noisemaker=None, theta_motor_noisemaker=None, speed_motor_sensor_noisemaker=None, heading_motor_sensor_noisemaker=None, theta_motor_sensor_noisemaker=None, energy_sensor_noisemaker: NoiseSource=None, compass_sensor_noisemaker: NoiseSource=None, heading_sensor_noisemaker: NoiseSource=None, action_energy_cost: float=0, metabolism_energy_cost: float=0, alive: bool=True, maximum_energy: float=0, initial_energy: float=1, consumables=None, init_fun: Callable=None, perturb_fun: Callable=None, pheromone_manager=None, drop_interval=0.5, p_bump_noise=0)

            :param x: The :class:`Bee`'s initial x-coordinate.
            :type x: float

            :param y: The :class:`Bee`'s initial y-coordinate.
            :type y: float

            :param theta: The :class:`Bee`'s initial orientation. Defaults to ``0``.
            :type theta: float

            :param radius: The radius of the :class:`Bee`'s body. Defaults to ``1``.
            :type radius: float

            :param light: The :class:`LightSource` attached to the :class:`Bee`'s body. Defaults to ``None``.
            :type light: :class:`LightSource`

            :param heading: The direction the bee will fly in.
            :type heading: float

            :param controller: the bee's controller.
            :type controller: :class:`BeeController`

            :param sensors: A :class:`Bee` has a list of 7 sensors by default: an internal energy sensor, a bump sensor, compass and heading sensors, and a motor speed sensor for each of its 3 motors. The list of sensors passed in here will be joined to that list. The bee's :class:`EnergySensor` is at index ``0`` in the list, its :class:`BumpSensor` is at index ``1`` in this list, its :class:`CompassSensor` is at index ``2``, and its :class:`HeadingSensor` is at index ``3``. Its :class:`MotorSpeedSensor` for its translational speed is at index ``4``, its :class:`MotorSpeedSensor` for its angular speed (to change its body orientation) is at index ``5``, and its :class:`MotorSpeedSensor` for its angular heading speed (to change its direction of travel) is at index ``6``. Therefore, any other sensors will be at indices ``7`` and up.
            :type sensors: list[:class:`Sensor`]

            :param sensor_angles: A list of angles for the sensors passed in as the ``sensors`` parameter. This list should have exactly the same length as ``sensors``. For any sensor which has ``None`` as its corresponding entry in ``sensor_angles``, its position will be at the centre of the bee's body. For any sensor which has an angle specified, the sensor will lie on the circumference of the bee's body, at the specified angle from its forward direction.
            :type sensor_angles: list[float]

            :param max_speed: The maximum speed that the bee can move at in the x-y plane. Defaults to ``2``.
            :type max_speed: float

            :param theta_inertia: The inertia on the bee's orientation turning motor. Defaults to ``0``.
            :type theta_inertia: float

            :param speed_inertia: The inertia on the bee's linear speed motor. Defaults to ``0``.
            :type speed_inertia: float

            :param heading_inertia: The inertia on the bee's heading turning motor. Defaults to ``0``.
            :type heading_inertia: float

            :param speed_motor_noisemaker: The noise source for the bee's translational (x-y plane) speed motor. Defaults to ``None``,
            :type speed_motor_noisemaker: :class:`NoiseSource`

            :param heading_motor_noisemaker: The noise source for the bee's heading (direction of travel) speed motor. Defaults to ``None``,
            :type heading_motor_noisemaker: :class:`NoiseSource`

            :param theta_motor_noisemaker: The noise source for the bee's orientation (``theta``) speed motor. Defaults to ``None``,
            :type theta_motor_noisemaker: :class:`NoiseSource`

            :param heading_motor_sensor_noisemaker: The noise source for the bee's heading speed motor sensor. Defaults to ``None``,
            :type heading_motor_sensor_noisemaker: :class:`NoiseSource`

            :param theta_motor_sensor_noisemaker: The noise source for the bee's orientation speed motor sensor. Defaults to ``None``,
            :type theta_motor_sensor_noisemaker: :class:`NoiseSource`

            :param compass_sensor_noisemaker: The noise source for the bee's compass sensor. Defaults to ``None``,
            :type compass_sensor_noisemaker: :class:`NoiseSource`

            :param heading_sensor_noisemaker: The noise source for the bee's heading speed motor. Defaults to ``None``,
            :type heading_sensor_noisemaker: :class:`NoiseSource`

            :param colour: The colour of the :class:`Bee`'s body. Defaults to ``'0x00FFFFFF'``.
            :type colour: str

            :param energy_sensor_noisemaker: A source of noise for the `Bee`'s energy sensor. Defaults to ``None``.
            :type energy_sensor_noisemaker: subclass of :class:`NoiseSource`

            :param action_energy_cost: The energetic cost of action. Defaults to ``0``. The cost of action in a single simulation step, for each of the bee's 2 motors, is ``abs(motor speed) * dt * action_energy_cost``.
            :type action_energy_cost: float

            :param metabolism_energy_cost: The energetic cost of existing. The main reason for this cost is that without it, bees can survive for indefinite periods without moving/acting at all. When bees can "die" by not acting, there is a pressure (e.g. selective pressure, if evolving) to act, and potentially to also adapt. Defaults to ``0``.
            :type metabolism_energy_cost: float

            :param alive: If a bee runs our of energy, it will "die", at which point its ``alive`` parameter will be set to ``False``, and the bee will cease to act (although in the current implementation, its controller will continue to function as normal). Defaults to ``True``.
            :type alive: bool

            :param maximum_energy: The maximum energy level the bee can have. Defaults to ``0``.
            :type maximum_energy: float

            :param initial_energy: The bee's initial energy level. Defaults to ``1``.
            :type initial_energy: float

            :param init_fun: A function which can be used to set the initial state of the system in each simulation run. Defaults to ``None``.
            :type init_fun: function

            :param perturb_fun: A function which can be used to perturb the bee's state. This will  typically be used at the beginning of simulation runs.  Defaults to ``None``.
            :type perturb_fun: function

            :param pheromone_manager: If a :class:`Bee` has a pheromone manager, then it will drop pheromones (similarly to an ant laying trails). Defaults to ``None``.
            :type pheromone_manager: :class:`PheromoneManager`

            :param drop_interval: The interval between which the bee will drop pheromones, if its ``pheromone_manager`` is not ``None``. Defaults to ``0.5``.
            :type drop_interval: float

            :param consumables: The list of consumables which this agent can consume.
            :type consumables: list(:class:`Consumable`)
        """
        super().__init__(x, y, colour, theta, radius, light, energy_sensor_noisemaker, action_energy_cost, metabolism_energy_cost, alive, maximum_energy, initial_energy, init_fun=init_fun, perturb_fun=perturb_fun, pheromone_manager=pheromone_manager, drop_interval=drop_interval, p_bump_noise=p_bump_noise)  # call Agent constructor

        self.speed_motor = Motor(max_speed=max_speed, motor_inertia_coeff=speed_inertia, reversed=False, noisemaker=None, name_str="Speed motor")
        self.theta_motor = Motor(max_speed=1, motor_inertia_coeff=theta_inertia, reversed=False, noisemaker=None, name_str="Orientation motor")
        self.heading_motor = Motor(max_speed=1, motor_inertia_coeff=heading_inertia, reversed=False, noisemaker=None, name_str="Heading motor")

        self.sensors.append(CompassSensor(x=x, y=y, theta=theta, noisemaker=compass_sensor_noisemaker))
        self.sensors.append(HeadingSensor(self, noisemaker=heading_sensor_noisemaker))

        self.sensors.append(MotorSpeedSensor(self.speed_motor, noisemaker=speed_motor_sensor_noisemaker, name_str="Speed motor sensor"))
        self.sensors.append(MotorSpeedSensor(self.theta_motor, noisemaker=speed_motor_sensor_noisemaker, name_str="Orientation motor sensor"))
        self.sensors.append(MotorSpeedSensor(self.heading_motor, noisemaker=speed_motor_sensor_noisemaker, name_str="Heading motor sensor"))

        self.sensor_angles = [None, None, 0, None, None, None, None]

        self.sensors += sensors
        self.sensor_angles += sensor_angles

        # self.initial_sensor_angles: List[float] = []
        # # I CAN JUST COPY THE LIST DIRECTLY!
        # for sensor_angle in sensor_angles:
        #     self.initial_sensor_angles.append(sensor_angle)

        self.consumables = consumables

        self.initial_sensors = cp.copy(self.sensors)
        self.initial_sensor_angles = cp.copy(self.sensor_angles)

        # self.max_speed: float = max_speed
        # self.theta_inertia: float = theta_inertia
        # self.speed_inertia: float = 0

        self.controller: NewBeeController = controller

        self.heading = heading
        self.headings: List[float] = [heading]

        self.speed: float = 0
        self.speeds: List[float] = [self.speed]

        self.update_children_positions()

    def step_sensors(self, dt: float) -> List[float]:
        """
            Only called from step().

            A method which steps the sensors in the bee's `sensors` list, and returns the sensor activations in a list.

            :param dt: Interval of time to integrate the bee's sensors over.
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

            A method which gets motor speed commands by calling the step method of the bee's controller.

            :param dt: Interval of time to integrate the bee's controller over.
            :type dt: float

            :param activations: The sensory inputs to the bee's controller. A list of the activation levels for each of the bee's sensors.
            :type activations: list[float]
        """
        return self.controller.step(dt, activations)

    def step_actuators(self, speed_commands: List[float], dt: float) -> List[float]:
        """
            Update the bee's motor speeds, based on the commands from the bee's controller and its motors' dynamics (i.e. current speeds and inertias).

            :param dt: Interval of time to integrate the bee's motors over.
            :type dt: float

            :param speed_commands: The motor speed commands which are generated by the bee's controller.
            :type speed_commands: list[float]
        """
        # speed inertia
        speed_commands[1] = self.speed_motor.step(dt=dt, speed_command=speed_commands[1])
        # body rotation - the way the Bee is looking
        speed_commands[0] = self.theta_motor.step(dt=dt, speed_command=speed_commands[0])
        # heading - the way the Bee is flying
        speed_commands[2] = self.heading_motor.step(dt=dt, speed_command=speed_commands[2])

        return speed_commands

    def update_energy(self, actual_speeds, dt):
        """
            Update the bee's energy level, based on its metabolic and action costs.

            :param dt: Interval of time to integrate the bee's energy losses over.
            :type dt: float

            :param actual_speeds: The bee's current motor speeds.
            :type actual_speeds: list[float]
        """
        # energy losses - allows bee to die here *before* it can consume anything
        if self.alive:
            # update energy. the faster the bee's wheels turn, the quicker it loses energy
            self.energy -= np.abs(actual_speeds[0]) * dt * self.action_energy_cost
            self.energy -= np.abs(actual_speeds[1]) * dt * self.action_energy_cost
            self.energy -= np.abs(actual_speeds[2]) * dt * self.action_energy_cost
            self.energy -= dt * self.metabolism_energy_cost  # some energy is lost even if the bee does not move
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

    def integrate(self, speeds: List[float], dt: float) -> None:
        """
            Integrate the bee's motion based on its motor speeds.

            Only called from step().

            Applies a motor activation vector to a bee state, and simulates the consequences using Euler integration over a dt interval.

            :param dt: Interval of time to integrate the bee's motion over.
            :type dt: float

            :param speeds: The bee's motor speeds.
            :type speeds: list[float]
        """
        self.speed = speeds[1]
        self.speeds.append(self.speed)

        self.theta += speeds[0] * dt

        self.heading += speeds[2] * dt
        self.headings.append(self.heading)

        self.x += self.speed * math.cos(self.heading) * dt
        self.y += self.speed * math.sin(self.heading) * dt

    # update positions and orientations of all sensors
    def update_children_positions(self) -> None:
        """
            This method is used to update the positions and orientations of a bee's attached subsystems, such as its sensors, as the bee moves.
        """
        # update light positions
        if self.light:
            self.light.x = self.x
            self.light.y = self.y

        # update sensor positions
        for i, sensor in enumerate(self.sensors):
            if sensor.has_position:
                if self.sensor_angles[i] is None:
                    sensor.x = self.x
                    sensor.y = self.y
                else:
                    sensor.x = self.x + (self.radius * np.cos(self.theta + self.sensor_angles[i]))
                    sensor.y = self.y + (self.radius * np.sin(self.theta + self.sensor_angles[i]))
            if sensor.has_orientation and self.sensor_angles[i] != None:
                sensor.theta = self.thetas[-1] + self.sensor_angles[i]

    def get_data(self) -> Dict[str, Dict[str, Any]]:
        """
            A function to get the data from a :class:`Bee`, in the form of a string-keyed dict.

            These data, as and when they are included in the returned dict, can be accessed with the following keys:

            * data inherited from :class:`Agent`: see :class:`Agent`
            * class name (Bee): ``data["classname"]``
            * data from the bee's controller: ``data["controller"]``
            * data from the bee's sensors: ``data["sensors"]``
            * data from the bee's motors: ``data["motors"]``
            * a complete history of the bee's speed: ``data["speeds"]``
            * a complete history of the bee's heading: ``data["headings"]``
        """
        data = super().get_data()

        data["classname"] = "Bee"

        data["sensors"] = []
        for sensor in self.sensors:
            data["sensors"].append(sensor.get_data())

        data["motors"] = [self.speed_motor.get_data(), self.theta_motor.get_data(), self.heading_motor.get_data()]
        data["headings"] = self.headings[:]
        data["speeds"] = self.speeds[:]
        data["controller"] = self.controller.get_data()

        # WHAT TO DO ABOUT CONSUMABLES?

        return data

    def reset(self, reset_controller: bool=True) -> None:
        """
            This method resets a bee's state and simulation data to their initial values, so that it can be used again.

            :param reset_controller: determines whether or not the bee's controller is also reset, defaults to ``True``. This is because sometimes you might want to reset a bee and simulate it again taking advantage of any information or learning which the controller has acquired.
            :type reset_controller: bool
        """
        super().reset()
        self.speed_motor.reset()
        self.theta_motor.reset()
        self.heading_motor.reset()

        self.heading = self.headings[0]
        self.headings = [self.heading]

        self.speed = self.speeds[0]
        self.speeds = [self.speed]

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

            :param other: The instance of :class:`Bee` that this instance will be compared to.
            :type other: System
        """

        if other == None:
            return False

        is_eq = super().__eq__(other)

        is_eq = is_eq and self.sensors == other.sensors
        is_eq = is_eq and self.sensor_angles and other.sensor_angles
        is_eq = is_eq and self.controller == other.controller
        is_eq = is_eq and self.heading == other.heading
        is_eq = is_eq and self.headings == other.headings
        is_eq = is_eq and self.speed == other.speed
        is_eq = is_eq and self.speeds == other.speeds
        is_eq = is_eq and self.speed_motor == other.speed_motor
        is_eq = is_eq and self.theta_motor == other.theta_motor
        is_eq = is_eq and self.heading_motor == other.heading_motor

        return is_eq

    # draw bee in the specified matplotlib axes
    def draw(self, ax) -> None:
        """
            Draw bee in specified Matplotlib axes.

            :param ax: The Matplotlib axes to draw the bee on.
            :type ax: Matplotlib axes
        """
        ax.plot([self.x, self.x+self.radius*np.cos(self.theta)],
                 [self.y, self.y+self.radius*np.sin(self.theta)], 'k--', linewidth='2')
        ax.add_artist(mpatches.Circle((self.x, self.y), self.radius, color='blue'))

        for sensor in self.sensors:
            sensor.draw(ax)
            # self.__draw_FOV(sensor, ax)

        if self.light:
            self.light.draw(ax)

    def pygame_draw(self, screen, scale: float, shiftx: float, shifty: float) -> None:
        """
            Draw bee on PyGame display.

            :param screen: The PyGame display to draw on.
            :type screen: PyGame display

            :param scale: The scale to draw at.
            :type scale: float

            :param shiftx: The offset from centre in the x-axis for drawing.
            :type shiftx: float

            :param shifty: The offset from centre in the y-axis for drawing.
            :type shifty: float
        """
        self.__pygame_draw_wings(screen, scale, shiftx, shifty)

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

        end_x = self.x + self.radius * np.cos(self.heading) * 1.3
        end_y = self.y + self.radius * np.sin(self.heading) * 1.3
        pygame.draw.line(screen, color='red',
                         start_pos=(scale * self.x + shiftx, scale * self.y + shifty),
                         end_pos=(scale * end_x + shiftx, scale * end_y + shifty), width=2)

    def __pygame_draw_wings(self, screen, scale: float, shiftx: float, shifty: float) -> None:
        """
            Draw the bee's wings on a PyGame display.

            :param screen: The PyGame display to draw on.
            :type screen: PyGame display

            :param scale: The scale to draw at.
            :type scale: float

            :param shiftx: The offset from centre in the x-axis for drawing.
            :type shiftx: float

            :param shifty: The offset from centre in the y-axis for drawing.
            :type shifty: float
        """
        a1 = 3*math.pi/8
        a_inc = 0.35
        offset = 0.2
        l = 1.6
        self.__pygame_draw_wing(screen, scale, shiftx, shifty, a1, a1+a_inc, 7, offset, l)

        self.__pygame_draw_wing(screen, scale, shiftx, shifty, -a1, -(a1+a_inc), 7, offset, l)

        a1 = 5*math.pi/8
        a_inc = 0.25
        offset = 0.2
        l = 1.6

        self.__pygame_draw_wing(screen, scale, shiftx, shifty, a1, a1+a_inc, 5, offset, l)

        self.__pygame_draw_wing(screen, scale, shiftx, shifty, -a1, -(a1+a_inc), 5, offset, l)

    def __pygame_draw_wing(self, screen, scale: float, shiftx: float, shifty: float, start_angle: float, end_angle:float, n: int, offset: float, l: float) -> None:
        """
            Draw one of the bee's "wings" on a PyGame display.

            :param screen: The PyGame display to draw on.
            :type screen: PyGame display

            :param scale: The scale to draw at.
            :type scale: float

            :param shiftx: The offset from centre in the x-axis for drawing.
            :type shiftx: float

            :param shifty: The offset from centre in the y-axis for drawing.
            :type shifty: float

            :param start_angle:
            :type start_angle:

            :param end_angle:
            :type end_angle:

            :param n:
            :type n:

            :param offset:
            :type offset:

            :param l:
            :type l:
        """
        angles = np.linspace(start_angle, end_angle, n)
        for angle in angles:
            x1, y1, x2, y2 = self.wing_ends(offset, angle, l)

            pygame.draw.line(screen, color='red',
                             start_pos=(scale * x1 + shiftx, scale * y1 + shifty),
                             end_pos=(scale * x2 + shiftx, scale * y2 + shifty), width=2)

    def wing_ends(self, offset_scale, angle, relative_length):
        """
            A method to generate coordinates for drawing "wings".
        """
        a = angle + self.theta

        offset = offset_scale * self.radius
        x1 = self.x + offset * math.cos(self.theta)
        y1 = self.y + offset * math.sin(self.theta)

        x2 = x1 + relative_length * math.cos(a)
        y2 = y1 + relative_length * math.sin(a)

        return x1, y1, x2, y2
