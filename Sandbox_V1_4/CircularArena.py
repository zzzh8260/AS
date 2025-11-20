from .System import *
from .Agent import *
from .pygame_functions import *

class CircularArena(System):
    """
        .. figure:: images/circular_arena.png
          :width: 600
          :align: center
          :alt: Robot in arena

          A robot inside an Arena, which will not allow it to escape.

        A class to represent a circular arena, which will confine any agents
        which are inside of its walls and in its list.
    """
    # construct Arena with a list of agents to constrain and coordinates of walls
    def __init__(self, agents: List[Agent], x: float, y: float, radius: float, keep_out=False):
        """
            __init__(agents: List[Agent], x_left: float, x_right: float, y_top: float, y_bottom: float)

            :param agents: List of agents which are confined or kept out by the CircularArena's wall. Agents must have a radius attribute for CircularArena to work.
            :type agents: List of :class:`Agent`

            :param x_left: The x-coordinate of the arena's centre.
            :type x_left: float

            :param x_right: The x-coordinate of the arena's centre.
            :type x_right: float

            :param radius: The arena's radius.
            :type radius: float

            :param keep_out: A flag to determine whether the arena keeps agents in (for ``False``) or out (for ``True``). Defaults to ``False``.
            :type keep_out: bool
        """
        # call System constructor
        super().__init__(x=x, y=y, theta=None)
        # set attributes
        self.agents = agents
        self.radius = radius
        self.keep_out = keep_out

        self.initial_state = self.get_data()

    # step arena
    def step(self, dt: float, x_move: float=None, y_move: float=None) -> None:
        """
            Step :class:`CircularArena` forwards in time. If any :class:`Agent` s in its ``agents`` list have crossed its walls, they will be pushed back inside.

            :param dt: The interval of time to integrate the :class:`CircularArena` over. Currently unused here.
            :type dt: float

            :param x_move: The distance to move the :class:`CircularArena` by in the x-axis.
            :type x_move: float

            :param y_move: The distance to move the :class:`CircularArena` by in the y-axis.
            :type y_move: float
        """
        # if move parameters are passed to step, then shift the arena
        if x_move and y_move:
            self.move(x_move, y_move)
        # call step of System, so that new xy-coordinates are stored
        super().step(dt)

        if not self.keep_out:
            # for all agents, constrain them to remain inside the box
            for agent in self.agents:
                x_diff = agent.x - self.x
                y_diff = agent.y - self.y
                dist = math.sqrt(x_diff ** 2 + y_diff ** 2)
                if (dist + agent.radius) > self.radius:
                    angle = math.atan2(y_diff, x_diff)
                    set_length = self.radius - agent.radius
                    agent.push(x=self.x+set_length*math.cos(angle), y=self.y+set_length*math.sin(angle))
                    agent.register_bump()
        else:
            for agent in self.agents:
                x_diff = agent.x - self.x
                y_diff = agent.y - self.y
                dist = math.sqrt(x_diff ** 2 + y_diff ** 2)
                if (dist - agent.radius) < self.radius:
                    angle = math.atan2(y_diff, x_diff)
                    set_length = self.radius + agent.radius
                    agent.push(x=self.x+set_length*math.cos(angle), y=self.y+set_length*math.sin(angle))
                    agent.register_bump()

    # move (translate) arena by specifed increments
    def move(self, x_move: float, y_move: float) -> None:
        """
            A method which can be used to move an :class:`CircularArena` by the distance specified in the x and y dimensions. This method would normally be called from an :class:`CircularArena`'s ``step`` method.

            :param x_move: The distance to move the :class:`CircularArena` by in the x-axis.
            :type x_move: float

            :param y_move: The distance to move the :class:`CircularArena` by in the y-axis.
            :type y_move: float
        """
        self.x += x_move
        self.y += y_move

    def reset(self):
        """
            Reset a :class:`CircularArena` to its original state upon its construction, e.g. so that it can be re-used in another simulation run.
        """
        # reset System attributes
        super().reset()

        self.radius = self.initial_state["radius"]
        self.keep_out = self.initial_state["keep_out"]
        # self.agents = self.initial_state["agents"]

    def get_data(self):
        """
            A function to get the data from a :class:`CircularArena`, in the form of a string-keyed dict.

            These data, as and when they are included in the returned dict, can be accessed with the following keys:

            * data inherited from :class:`System`: see :class:`System`
            * arena radius: ``data["radius"]``
            * keep_out flag: ``data["keep_out"]``

            :return: The System's data.
            :rtype: dict
        """
        data = super().get_data()

        data["radius"] = self.radius
        data["keep_out"] = self.keep_out
        # data["agents"] = cp.deepcopy(self.agents)

        return data

    # draw arena in the specified matplotlib axes
    def draw(self, ax) -> None:
        """
            A method to draw a :class:`CircularArena` on Matplotlib axes.

            :param ax: The Matplotlib axes to draw the Arena on.
            :type ax: Matplotlib axes
        """
        xs, ys = self.get_points()
        ax.plot(xs, ys, 'r', linewidth=4)

    # draw arena in whichever matplotlib plot was last used, or
    # a new window if there aren't any open
    def draw2(self) -> None:
        """
            A method to draw a :class:`CircularArena` on a Matplotlib figure. If there is no figure already open, a new one will be opened. If there is already one or more figure open, then the arena will be drawn on the last one used.
        """
        xs, ys = self.get_points()
        plt.plot(xs, ys, 'r', linewidth=4)

    def get_points(self, n=180):
        """
            A method to generate the coordinates for approximating the arena's circular form with straight line segments.
        """
        angles = np.linspace(0, 2*math.pi, num=n)
        xs = self.x + self.radius * np.cos(angles)
        ys = self.y + self.radius * np.sin(angles)
        return xs, ys

    # draw arena in a pygame display
    def pygame_draw(self, screen, scale: float, shiftx: float, shifty: float):
        """
            A method for drawing aa :class:`CircularArena` on a PyGame display.

            :param screen: The PyGame display to draw on.
            :type screen: PyGame display

            :param scale: The scale to draw at.
            :type scale: float

            :param shiftx: The offset from centre in the x-axis for drawing.
            :type shiftx: float

            :param shifty: The offset from centre in the y-axis for drawing.
            :type shifty: float
        """
        pygame_drawcircle(screen, shiftx, shifty, scale, self.x, self.y, self.radius, "red", 2)
