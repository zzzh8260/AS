from .System import *
from .stimuli import *
from .Sensor import *
from .noise import *
from .EnergySensor import *
from .BumpSensor import *

class Agent(System):
    """
        An :class:`Agent` is an abstract subclass of :class:`System`. Classes which represent specific types of mobile agents, e.g. :class:`Robot` are subclasses of :class:`Agent`.

        An :class:`Agent` is a mobile :class:`System` with position and orientation. It is expected that an :class:`Agent` will have sensors, a controller, and some way of moving through its environment.

        When you subclass :class:`Agent`, you will need to implement the following methods:

        * ``step_sensors(dt)``
        * ``control(activations, dt)``
        * ``step_actuators(speed_commands, dt)``
        * ``integrate(actual_speeds, dt)``
        * and ``update_children_positions()``
        * as well as ``pygame_draw(self, screen, scale: float, shiftx: float, shifty: float)``, if you are going to animate your simulation
        * ``update_energy`` can also be optionally implemented, if you want your agent to have an internal energy level

        These methods split up the :class:`Agent`'s side of its sensorimotor loop. The main reason for splitting them up is to make it easier to subclass agent implementations. For example, to add sensors to an existing :class:`Agent` subclass, you would only need to override ``step_sensors`` and ``control`` - ``step_actuators`` and ``integrate`` don't need to be touched. Another example would be if you wanted to change the dynamics of motion when subclassing an existing :class:`Agent` - it may only be necessary to override the ``integrate`` method, and leave the other methods as they are.

        All instances of :class:`Agent` will have two sensors: the first is an :class:`EnergySensor`, which detects the agent's internal energy level. The second is a :class:`BumpSensor`, which can register collisions with other agents and objects. 

    """
    # I'm not entirely sure about theta=None
    # - this would be an odd kind of agent!
    def __init__(self, x: float, y: float, colour: str,  theta: float=None, radius: float=1, light: LightSource=None, energy_sensor_noisemaker=None, action_energy_cost: float=0, metabolism_energy_cost: float=0, alive: bool=True, maximum_energy: float=0, initial_energy: float=1, init_fun: Callable=None, perturb_fun: Callable=None, pheromone_manager=None, drop_interval=0.5, p_bump_noise=0):
        """
            __init__(self, x: float, y: float, colour: str,  theta: float=None, radius: float=1, light: LightSource=None, energy_sensor_noisemaker=None, action_energy_cost: float=0, metabolism_energy_cost: float=0, alive: bool=True, maximum_energy: float=0, initial_energy: float=1, init_fun: Callable=None, perturb_fun: Callable=None, pheromone_manager=None, drop_interval=0.5)

            :param x: The :class:`Agent`'s initial x-coordinate.
            :type x: float

            :param y: The :class:`Agent`'s initial y-coordinate.
            :type y: float

            :param theta: The :class:`Agent`'s initial orientation. Defaults to ``None``.
            :type theta: float

            :param radius: The radius of the :class:`Agent`'s body. Defaults to ``1``.
            :type radius: float

            :param colour: The colour of the :class:`Agent`'s body.
            :type colour: str

            :param light: The :class:`LightSource` attached to the :class:`Agent`'s body. Defaults to ``None``.
            :type light: :class:`LightSource`

            :param energy_sensor_noisemaker: A source of noise for the `Agent`'s energy sensor. Defaults to ``None``.
            :type energy_sensor_noisemaker: subclass of :class:`NoiseSource`

            :param action_energy_cost: The energetic cost of action. The actual cost for a subclass of :class:`Agent` will differ from one class to another, and typically depend on how many motors the agent makes use of. Defaults to ``0``.
            :type action_energy_cost: float

            :param metabolism_energy_cost: The energetic cost of existing. The main reason for this cost is that without it, agents can survive for indefinite periods without moving/acting at all. When agents can "die" by not acting, there is a pressure (e.g. selective pressure, if evolving) to act, and potentially to also adapt. Defaults to ``0``.
            :type metabolism_energy_cost: float

            :param alive: If an agent runs our of energy, it will die, at which point its ``alive`` parameter will be set to ``False``, and the agent will cease to act (although in the current implementation, its controller will continue to function as normal). Defaults to ``True``.
            :type alive: bool

            :param maximum_energy: The maximum energy level the agent can have. Defaults to ``0``.
            :type maximum_energy: float

            :param initial_energy: The agent's initial energy level. Defaults to ``1``.
            :type initial_energy: float

            :param init_fun: A function which can be used to set the initial state of the system in each simulation run. Defaults to ``None``.
            :type init_fun: function

            :param perturb_fun: A function which can be used to perturb the system's state. This will  typically be used at the beginning of simulation runs.  Defaults to ``None``.
            :type perturb_fun: function

            :param pheromone_manager: If an :class:`Agent` has a pheromone manager, then it will drop pheromones (similarly to an ant laying trails). Defaults to ``None``.
            :type pheromone_manager: :class:`PheromoneManager`

            :param drop_interval: The rate at which the agent will drop pheromones, if its ``pheromone_manager`` is not ``None``. Defaults to ``0.5``.
            :type drop_interval: float
        """
        super().__init__(x, y, theta, init_fun=init_fun, perturb_fun=perturb_fun)  # call System constructor. xy-variables are handled there
        self.colour: str = colour
        self.radius: float = radius
        self.light: LightSource = light
        self.sensors: List[Sensor] = [EnergySensor(self, self.x, self.y, energy_sensor_noisemaker), BumpSensor(p_noise=p_bump_noise)]

        self.action_energy_cost = action_energy_cost
        self.metabolism_energy_cost = metabolism_energy_cost
        self.alive = alive
        self.maximum_energy = maximum_energy
        self.energy = initial_energy  # set initial energy level
        self.energies = [initial_energy]  # store energy level

        self.drop_interval = drop_interval
        self.pheromone_manager = pheromone_manager  # the manager which new pheromones will be added to
        self.timer = 0  # used to determine when it is time to drop the next pheromone

    def step(self, dt: float) -> None:
        """
            Step the agent forwards in time.

            :param dt: Interval of time to integrate the agent's dynamics over.
            :type dt: float
        """
        if self.pheromone_manager is not None:
            self.drop_pheromones(dt)

        activations = self.step_sensors(dt)

        # step controller
        speed_commands = self.control(activations, dt)

        # step motor objects, if agent has any, or otherwise deal with any
        # dynamics of speed change such as inertia
        actual_speeds = self.step_actuators(speed_commands, dt)

        if self.alive:
            # integrate agent's motion
            self.integrate(actual_speeds, dt)

            # update energy - agent may die in this called method
            self.update_energy(actual_speeds, dt)

        self.energies.append(self.energy)

        # call System's step method
        super().step(dt)  # this call goes to System

        # update light and light sensor positions
        self.update_children_positions()

    def get_data(self):
        """
            A function to get the data from an :class:`Agent`, in the form of a string-keyed dict.

            These data, as and when they are included in the returned dict, can be accessed with the following keys:

            * data inherited from :class:`System`: see :class:`System`
            * The history of the agent's energy level over the simulation: ``data["energies"]``
        """
        data = super().get_data()

        data["energies"] = self.energies[:]

        return data

    def reset(self):
        """
            Reset an :class:`Agent` to its original state upon its construction, e.g. so that it can be re-used in another simulation run.
        """
        super().reset()

        self.energy = self.energies[0]
        self.energies = [self.energy]

        self.timer = 0

    def update_energy(self, actual_speeds, dt):
        """
            A placeholder. Subclasses of :class:`Agent` will need to implement this method, if they are to have internal energy levels.

            param actual_speeds: the actual speeds of the agent's motors.
            type actual_speeds: list[float]

            :param dt: The interval of time to integrate the energy cost over.
            :type dt: float
        """
        pass

    def drop_pheromones(self, dt):
        """
            All agents can potentially drop pheromones (see :class:`PheromoneSource`), if they have pheromone managers (see :class:`PheromoneManager`) passed to them when they are constructed. This method will make the agent drop pheromones all the time, at the constant rate specified by the agent's ``drop_interval`` parameter.

            :param dt: The interval of time to integrate the pheromone drop timer over.
            :type dt: float
        """
        self.timer += dt  # increment timer
        if self.timer >= self.drop_interval:  # if timer has expired, then drop a pheromone and restart timer
            self.timer = 0
            self.pheromone_manager.add_pheromone_at(self.x, self.y)

    def push(self, x: float=None, y: float=None, theta: float=None):
        """
            A method used to "push" an :class:`Agent` to a new position and orientation. The agent can be pushed in any single axis (x, y, rotation) or any combination of those axes.

            This method is here for environmental interactions such as those between an :class:`Agent` and an :class:`Arena`. The :class:`Arena` takes care of watching for collisions between agents and its walls, and when it detects one, it pushes the colliding agent back inside, using this method. It is important that this method is used, rather than just directly changing the agent's ``x``, ``y``, and ``theta`` attributes, as this method will also update the states of attached systems, such as sensors.

            :param x: The x-coordinate to push the agent to. Defaults to ``None``, in which case the agent's x-coordinate will be unchanged.
            :type x: float

            :param y: The y-coordinate to push the agent to. Defaults to ``None``, in which case the agent's y-coordinate will be unchanged.
            :type y: float

            :param theta: The orientation to push the agent to. Defaults to ``None``, in which case the agent's orientation will be unchanged.
            :type theta: float
        """
        if x:
            self.x = x
            self.xs[-1] = x
        if y:
            self.y = y
            self.ys[-1] = y
        if theta:
            self.theta = theta
            self.thetas[-1] = theta
        self.update_children_positions()

    def register_bump(self):

        self.sensors[1].register_bump()

    def __eq__(self, other) -> bool:
        """
            Overrides the == operator for instances of this class.

            :param other: The instance of :class:`Agent` that this instance will be compared to.
            :type other: :class:`Agent`
        """
        is_eq = super().__eq__(other)

        is_eq = is_eq and self.colour == other.colour
        is_eq = is_eq and self.radius == other.radius
        is_eq = is_eq and self.light == other.light
        is_eq = is_eq and self.sensors == other.sensors

        is_eq = is_eq and self.action_energy_cost == other.action_energy_cost
        is_eq = is_eq and self.metabolism_energy_cost == other.metabolism_energy_cost
        is_eq = is_eq and self.alive == other.alive
        is_eq = is_eq and self.maximum_energy == other.maximum_energy
        is_eq = is_eq and self.energy == other.energy
        is_eq = is_eq and self.energies == other.energies

        is_eq = is_eq and self.drop_interval == other.drop_interval
        is_eq = is_eq and self.pheromone_manager == other.pheromone_manager
        is_eq = is_eq and self.timer == other.timer

        return is_eq
