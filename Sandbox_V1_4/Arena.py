from .System import *
from .Agent import *

class Arena(System):
    """
        .. figure:: images/arena.png
          :width: 600
          :align: center
          :alt: Robot in arena

          A robot inside an Arena, which will not allow it to escape.

        A class to represent a rectangular arena, which will confine any agents
        which are inside of its walls and in its list.
    """
    # construct Arena with a list of agents to constrain and coordinates of walls
    def __init__(self, agents: List[Agent], x_left: float, x_right: float, y_top: float, y_bottom: float, keep_out=False):
        """
            __init__(agents: List[Agent], x_left: float, x_right: float, y_top: float, y_bottom: float)

            Note: in the current implementation, the code does not check that x_right > x_left and y_top > y_bottom - you have to make sure you get this right yourself.

            :param agents: List of agents which are confined or kept out by the Arena's walls. Agents must have a radius attribute for Arena to work.
            :type agents: List of :class:`Agent`

            :param x_left: The x-coordinate of the arena's left wall.
            :type x_left: float

            :param x_right: The x-coordinate of the arena's right wall.
            :type x_right: float

            :param y_top: The y-coordinate of the arena's top wall.
            :type y_top: float

            :param y_bottom: The y-coordinate of the arena's bottom wall.
            :type y_bottom: float

            :param keep_out: A flag to determine whether the arena keeps agents in (for ``False``) or out (for ``True``). Defaults to ``False``.
            :type keep_out: bool
        """

        # call System constructor
        super().__init__()
        # set attributes
        self.agents = agents
        self.x_left = x_left
        self.x_right = x_right
        self.y_top = y_top
        self.y_bottom = y_bottom
        self.keep_out = keep_out

        self.initial_state = self.get_data()

    # step arena
    def step(self, dt: float, x_move: float=None, y_move: float=None) -> None:
        """
            Step :class:`Arena` forwards in time. If any :class:`Agent` s in its ``agents`` list have crossed its walls, they will be pushed back inside.

            :param dt: The interval of time to integrate the :class:`Arena` over. Currently unused here.
            :type dt: float

            :param x_move: The distance to move the :class:`Arena` by in the x-axis.
            :type x_move: float

            :param y_move: The distance to move the :class:`Arena` by in the y-axis.
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
                # constrain in y
                if (agent.y + agent.radius) > self.y_top:
                    agent.push(y=self.y_top - agent.radius)
                    agent.register_bump()
                elif (agent.y - agent.radius) < self.y_bottom:
                    agent.push(y=self.y_bottom + agent.radius)
                    agent.register_bump()
                # constrain in x
                if (agent.x + agent.radius) > self.x_right:
                    agent.push(x=self.x_right - agent.radius)
                    agent.register_bump()
                elif (agent.x - agent.radius) < self.x_left:
                    agent.push(x=self.x_left + agent.radius)
                    agent.register_bump()

        else:
            # for all agents, constrain them to remain outside the box
            for agent in self.agents:
                inside_left = agent.x > self.x_left
                inside_right = agent.x < self.x_right

                below_top = (agent.y - agent.radius) < self.y_top
                above_bottom = (agent.y + agent.radius) > self.y_bottom

                if inside_left and inside_right:

                    if below_top and above_bottom:
                        if(abs(agent.y - self.y_top) < abs(agent.y - self.y_bottom)):
                            agent.push(y=self.y_top + agent.radius)
                            agent.register_bump()
                        else:
                            agent.push(y=self.y_bottom - agent.radius)
                            agent.register_bump()

                inside_top = (agent.y - agent.radius) < self.y_top
                inside_bottom = (agent.y + agent.radius) > self.y_bottom

                over_left = (agent.x + agent.radius) > self.x_left
                over_right = (agent.x - agent.radius) < self.x_right

                if inside_top and inside_bottom:

                    if over_left and over_right:
                        if abs(agent.x < self.x_right) < abs(agent.x > self.x_left):
                            agent.push(x=self.x_right + agent.radius)
                            agent.register_bump()
                        else:
                            agent.push(x=self.x_left - agent.radius)
                            agent.register_bump()

                # constrain in y
                # if (agent.y - agent.radius) < self.y_top:
                #     if (agent.y + agent.radius) > self.y_bottom:
                #         if(abs(agent.y - self.y_top) < abs(agent.y - self.y_bottom)):
				#
                #     agent.push(y=self.y_top + agent.radius)
                # elif (agent.y + agent.radius) > self.y_bottom:
                #     agent.push(y=self.y_bottom - agent.radius)
                # constrain in x
                # if (agent.x - agent.radius) < self.x_right:
                #     agent.push(x=self.x_right + agent.radius)
                # elif (agent.x + agent.radius) > self.x_left:
                #     agent.push(x=self.x_left - agent.radius)

    # move (translate) arena by specifed increments
    def move(self, x_move: float, y_move: float) -> None:
        """
            A method which can be used to move an :class:`Arena` by the distance specified in the x and y dimensions. This method would normally be called from an :class:`Arena`'s ``step`` method.

            :param x_move: The distance to move the :class:`Arena` by in the x-axis.
            :type x_move: float

            :param y_move: The distance to move the :class:`Arena` by in the y-axis.
            :type y_move: float
        """
        # self.x += x_move
        # self.y += y_move
        self.x_left += x_move
        self.x_right += x_move
        self.y_top += y_move
        self.y_bottom += y_move

    def reset(self):
        """
            Reset an :class:`Arena` to its original state upon its construction, e.g. so that it can be re-used in another simulation run.
        """
        # reset System attributes
        super().reset()

        self.x_left = self.initial_state["x_left"]
        self.x_right = self.initial_state["x_right"]
        self.y_top = self.initial_state["y_top"]
        self.y_bottom = self.initial_state["y_bottom"]
        self.keep_out = self.initial_state["keep_out"]
        # self.agents = self.initial_state["agents"]

    def get_data(self):
        """
            A function to get the data from an :class:`Arena`, in the form of a string-keyed dict.

            These data, as and when they are included in the returned dict, can be accessed with the following keys:

            * data inherited from :class:`System`: see :class:`System`
            * arena left x-co-ordinate: ``data["x_left"]``
            * arena right x-co-ordinate: ``data["x_right"]``
            * arena top y-co-ordinate: ``data["y_top"]``
            * arena bottom y-co-ordinate: ``data["y_bottom"]``
            * keep_out flag: ``data["keep_out"]``

            :return: The System's data.
            :rtype: dict
        """
        data = super().get_data()

        data["x_left"] = self.x_left
        data["x_right"] = self.x_right
        data["y_top"] = self.y_top
        data["y_bottom"] = self.y_bottom
        data["keep_out"] = self.keep_out
        # data["agents"] = cp.deepcopy(self.agents)

        return data

    # draw arena in the specified matplotlib axes
    def draw(self, ax) -> None:
        """
            A method to draw an :class:`Arena` on Matplotlib axes.

            :param ax: The Matplotlib axes to draw the Arena on.
            :type ax: Matplotlib axes
        """
        ax.plot([self.x_left, self.x_left,
                 self.x_right, self.x_right,
                 self.x_left],
                [self.y_bottom, self.y_top,
                 self.y_top, self.y_bottom,
                 self.y_bottom], 'r', linewidth=4)

    # draw arena in whichever matplotlib plot was last used, or
    # a new window if there aren't any open
    def draw2(self) -> None:
        """
            A method to draw an :class:`Arena` on a Matplotlib figure. If there is no figure already open, a new one will be opened. If there is already one or more figure open, then the arena will be drawn on the last one used.
        """
        plt.plot([self.x_left, self.x_left,
                  self.x_right, self.x_right,
                  self.x_left],
                 [self.y_bottom, self.y_top,
                  self.y_top, self.y_bottom,
                  self.y_bottom], 'r')

    # draw arena in a pygame display
    def pygame_draw(self, screen, scale: float, shiftx: float, shifty: float):
        """
            A method for drawing an :class:`Arena` on a PyGame display.

            :param screen: The PyGame display to draw on.
            :type screen: PyGame display

            :param scale: The scale to draw at.
            :type scale: float

            :param shiftx: The offset from centre in the x-axis for drawing.
            :type shiftx: float

            :param shifty: The offset from centre in the y-axis for drawing.
            :type shifty: float
        """
        self.line_drawer(self.x_left, self.x_left, self.y_bottom, self.y_top,
                         screen, scale, shiftx, shifty)
        self.line_drawer(self.x_left, self.x_right, self.y_top, self.y_top,
                         screen, scale, shiftx, shifty)

        self.line_drawer(self.x_right, self.x_right, self.y_top, self.y_bottom,
                      screen, scale, shiftx, shifty)
        self.line_drawer(self.x_right, self.x_left, self.y_bottom, self.y_bottom,
                         screen, scale, shiftx, shifty)

    # a function for drawing a line in the pygame window
    def line_drawer(self, x1: float, x2: float, y1: float, y2: float, screen, scale: float, shiftx: float, shifty:float) -> None:
        """
            A method for drawing a straight line between two points on a PyGame display.

            :param x1: The x-coordinate of the first point.
            :type x1: float

            :param x2: The x-coordinate of the second point.
            :type x2: float

            :param y1: The y-coordinate of the first point.
            :type y1: float

            :param y2: The y-coordinate of the second point.
            :type y2: float

            :param screen: The PyGame display to draw on.
            :type screen: PyGame display

            :param scale: The scale to draw at.
            :type scale: float

            :param shiftx: The offset from centre in the x-axis for drawing.
            :type shiftx: float

            :param shifty: The offset from centre in the y-axis for drawing.
            :type shifty: float
        """
        pygame.draw.line(screen, color='green',
                         start_pos=(scale * x1 + shiftx, scale * y1 + shifty),
                         end_pos=(scale * x2 + shiftx, scale * y2 + shifty),
                         width=2)
