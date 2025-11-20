from .stimuli import *

# subclass LightSource to create a LightSource which has a quantity. The quantity decays from 1 towards 0, is controlled
# by a PheromoneManager, and in this class it affects the brightness of the light, as perceived by LightSensors, and
# the opacity of the light when it is drawn in pygame and matplotlib
class PheromoneSource(LightSource):
    """
        A class to represent a deposit of pheromones on the ground. The :class:`PheromoneSource` extends :class:`LightSource`, so pheromones can be detected with ordinary light sensors.
    """
    # construct pheromone
    def __init__(self, x, y, brightness=1, gradient=0.01, model='inv_sq', is_on=True):
        """
            __init__(self, x, y, brightness=1, gradient=0.01, model='inv_sq', is_on=True)

            :param x: The x-coordinate of the pheromone. Defaults to ``None``.
            :type x: float

            :param y: The y-coordinate of the pheromone. Defaults to ``None``.
            :type y: float

            :param brightness: The brightness of the light, at its own coordinate (but this will be multiplied by the pheromone's concentration).
            :type brightness: float

            :param gradient: The gradient of brightness decay with distance, when the linear model is used.
            :type gradient: float

            :param model: The light decay model. ``inv_sq``, ``linear``, and ``binary`` are valid models.
            :type model: str

            :param is_on: A flag which can be use to determine whether or not a pheromone can be detected. Defaults to ``True``. This allows for the pheromone to be turned on and off.
            :type is_on: bool
        """
        super().__init__(x=x, y=y, brightness=brightness, gradient=gradient, model=model, is_on=is_on)
        self.quantity = 1

    # as the quantity of pheromone decays, the light dims
    def get_brightness_at(self, x, y, theta):
        """
            A method to get the concentration of the pheromone (or brightness of light, as it is perceived) at the given xy coordinates, according to the light source's ``model``, and which angles it can be perceived from (determined by the light's ``spread`` attribute).

            :param x: The x-component of the position to find the brightness at.
            :type x: float

            :param y: The y-component of the position to find the brightness at.
            :type y: float

            :param theta: The orientation of the sensor at the position to find the brightness at. For lights which are not omni-directional, this will affect whether the sensor can detect the light.
            :type theta: float

            :return: The perceived brightness at the given coordinates, which is the light brightness multiplied by the pheromone concentration (``quantity``).
            :rtype: float
        """
        return self.quantity * super().get_brightness_at(x, y, theta)

    # draw pheromone in the specified matplotlib axes
    def draw(self, ax):
        """
            A method to draw the pheromone in the specified matplotlib axes. The concentration of pheromones is used to set the opacity of the pheromone.

            :param ax: The Matplotlib axes to draw the light on.
            :type ax: Matplotlib axes.
        """
        ax.add_artist(mpatches.Circle((self.x, self.y), 0.7, color='yellow', alpha=self.quantity))
        ax.add_artist(mpatches.Circle((self.x, self.y), 0.2, color='orange', alpha=self.quantity))
        ax.plot(self.x, self.y, 'r.')

    # draw pheromone in a pygame display
    def pygame_draw(self, screen, scale, shiftx, shifty):
        """
            A method to draw the pheromone in the specified PyGame display.
            A :class:`PheromoneSource` is drawn as a circle with colour specified by the light source's ``colour`` attribute, multiplied by its pheromone concentration.

            :param screen: The PyGame display to draw on.
            :type screen: PyGame display

            :param scale: The scale to draw at.
            :type scale: float

            :param shiftx: The offset from centre in the x-axis for drawing.
            :type shiftx: float

            :param shifty: The offset from centre in the y-axis for drawing.
            :type shifty: float
        """
        width = 0
        # pygame.draw.circle(screen, center=(scale*self.x+shiftx, scale*self.y+shifty), color=pygame.Color(255, int(255*(1-self.quantity)), int(255*(1-self.quantity))), width=width, radius=scale*0.7)
        pygame.draw.circle(screen, center=(scale*self.x+shiftx, scale*self.y+shifty), color=pygame.Color(int(255*self.quantity), 0, 0), width=width, radius=scale*0.7)


# a class to handle a collection of pheromones, which can be added to and removed when they decay to 0
class PheromoneManager(System):
    """
        A class for managing the decay of a list of :class:`PheromoneSource` objects.
    """
    # construct pheromone manager
    def __init__(self, pheromones=[], decay_rate=0.01):
        """
            :param pheromones: Defaults to an empty list.
            :type pheromones: list(:class:`PheromoneSource`)

            :param decay_rate: The rate at which all pheromones managed by an instance of this class will decay by. In every simulation step, the amount of pheromone in each :class:`PheromoneSource` in the ``pheromones`` list decays by ``dt * decay_rate``, until the point when the pheromone's level falls below ``0`` and the :class:`PheromoneSource` is deleted. Defaults to ``0.01``.
            :type decay_rate: float
        """
        self.pheromones = pheromones
        self.decay_rate = decay_rate  # rate of pheromone decay per unit of simulation time

        super().__init__()

    # add pheromone at given coordinate
    def add_pheromone_at(self, x, y):
        """
            A method for adding a :class:`PheromoneSource` at the given coordinates.

            :param x: The x-coordinate to add the pheromone source at.
            :type x: float

            :param y: The y-coordinate to add the pheromone source at.
            :type y: float
        """
        self.pheromones.append(PheromoneSource(x, y))

    # add an already existing PheromoneSource (not currently used)
    def add_pheromone(self, p):
        """
            A method for adding an existing :class:`PheromoneSource` to the ``pheromones`` list.

            :param p: The :class:`PheromoneSource` to add to the list.
            :type p: :class:`PheromoneSource`
        """
        self.pheromones.append(p)

    # step pheromone manager
    def step(self, dt):
        """
            Step :class:`PheromoneManager` forwards in time.

            Every :class:`PheromoneSource` belonging to the :class:`PheromoneManager` will decay, and vanish if completely depleted.

            :param dt: The interval of time to integrate the pheromones over. Currently unused here.
            :type dt: float
        """
        for p in self.pheromones:
            p.quantity -= dt * self.decay_rate  # all pheromones decay by the same amount
        self.pheromones[:] = [p for p in self.pheromones if p.quantity > 0]  # remove all pheromones which are depleted

    # draw all pheromones in specified matplotlib axes
    def draw(self, ax):
        """
            A method to draw all the instances of :class:`PheromoneSource` belonging to a :class:`PheromoneManager` on Matplotlib axes.

            :param ax: The Matplotlib axes to draw the Arena on.
            :type ax: Matplotlib axes
        """
        for p in self.pheromones:
            p.draw(ax)

    # draw all pheromones in pygame screen
    def pygame_draw(self, screen, scale, shiftx, shifty):
        """
            A method to draw all the instances of :class:`PheromoneSource` belonging to a :class:`PheromoneManager` on a PyGame display.

            :param screen: The PyGame display to draw on.
            :type screen: PyGame display

            :param scale: The scale to draw at.
            :type scale: float

            :param shiftx: The offset from centre in the x-axis for drawing.
            :type shiftx: float

            :param shifty: The offset from centre in the y-axis for drawing.
            :type shifty: float
        """
        for p in self.pheromones:
            p.pygame_draw(screen, scale, shiftx, shifty)

    def reset(self):
        """
            Reset a :class:`PheromoneManager` to its original state upon its construction, e.g. so that it can be re-used in another simulation run.
        """
        # empty pheromone list
        self.pheromones.clear()
