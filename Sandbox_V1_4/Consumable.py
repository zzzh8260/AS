from .System import *
from .stimuli import *

# A consumable object, which can be placed in the environment, can be food, water or poison, and can be detected by
# LightSensors as it has a LightSource attached.
class Consumable(System):
    """
        A class to implement a consumable item, which can either give or take energy from a system which consumes it. In this way, it can be used to model, in a very simple way, the effects of food or toxins (poison).

        A :class:`Consumable` has a :class:`LightSource` attached to it, and so can be detected by an agent's light sensors.
    """
    # construct consumable
    def __init__(self, x, y, radius=0.5, quantity=10, recovery_time=10, colour='green'):
        """
            __init__(self, x, y, radius=0.5, quantity=10, recovery_time=10, colour='green')

            :param x: The x-coordinate of the consumable.
            :type x: float

            :param y: The y-coordinate of the consumable.
            :type y: float

            :param radius: An agent which is set up to "eat" instances of :class:`Consumable` will consume one if it passes within this distance of its position. Defaults to ``0.5``.
            :type radius: float

            :param quantity: The amount of energy which a :class:`Consumable` will add to or remove from an agent which consumes it. Positive quantities will increase the agent's energy level, like food, while negative quantities will drain the agent's energy, like (a potentially mild) toxin, or poison. Defaults to ``10``.
            :type quantity: float

            :param recovery_time: The time it takes for a consumable to be replenished (e.g. by growing back) after it has been consumed. If you would prefer for it not to ever grow back, then make this number larger than the duration of your simulation. Defaults to ``10``.
            :type recovery_time: float

            :param colour: The colour of the consumable's attached light source. Needs to be a value which PyGame (and potentially Matplotlib) will recognise. Defaults to ``"green"``.
            :type colour: str
        """
        super().__init__(x, y)  # call System constructor, to allow for the possibility that a Consumable will move
        self.colour = colour
        self.stimulus = LightSource(x=x, y=y, colour=self.colour, label=self.colour)  # construct LightSource
        self.quantity = quantity  # the quantity determines how much of an effect consuming the item has on a HungryRobot
        self.initial_quantity = quantity
        self.recovery_time = recovery_time  # when an item is consumed, it can reappear when the recovery time expires. if you don't want it to recover, then just make this time longer than your simulation duration
        self.initial_recovery_time = recovery_time
        self.depleted = False  # initially, a Consumable is not depleted. When it is consumed, it is depleted and will be invisible until (and if) it recovers
        self.depleteds = [False]
        self.time_since_consumed = 0  # used to track time to recover
        self.radius = radius  # this is the radius within which an Agent will potentially consume this Consumable
        self.initial_radius = radius

    def step(self, dt):
        """
            A method to step a :class:`Consumable` forwards in time. If the consumable has been depleted, then this method uses a time to determine when it should become replenished.

            :param dt: The interval of time to integrate the :class:`Consumable` over. 
            :type dt: float
        """
        super().step(dt)  # call System step method, to allow for the possibility that a Consumable will move
        if self.depleted: # if the Consumable has been depleted, then wait for recovery_time to replenish and make it detectable again
            if self.time_since_consumed >= self.recovery_time:  # if consumable has reached recovery_time
                self.depleted = False  # replenish consumable
                self.stimulus.is_on = True  # make consumable detectable again
            else:
                self.time_since_consumed += dt  # increment time since consumable was depleted
        self.depleteds.append(self.depleted)

    def consume(self):
        """
            A method to implement the consumption of a :class:`Consumable`. If the consumable is already depleted, nothing happens. Otherwise, it will be depleted, and the light source attached to it will be switched off until it is replenished.
        """
        if self.depleted:  # if already depleted, return zero
            return 0
        else:  # if not already depleted, return the quantity which determines how much of an effect will be had on the robot
            self.depleted = True  # set to depleted
            self.stimulus.is_on = False  # turn LightSource off, to make the Consumable invisible
            self.time_since_consumed = 0
            return self.quantity

    def draw(self, ax):
        """
            A method to draw a :class:`Consumable` on Matplotlib axes. If the Consumable is currently "full" it will be drawn with full opacity. If it is currently in a depleted, or consumed, state then it will be drawn with only 30% opacity.

            :param ax: The Matplotlib axes to draw the Arena on.
            :type ax: Matplotlib axes
        """
        alpha = 1
        if self.depleted:
            alpha = 0.3
        ax.add_artist(mpatches.Circle((self.x, self.y), self.radius, color=self.color, alpha=alpha))
        ax.plot(self.x, self.y, 'k.')

    # draw consumable in a pygame display
    def pygame_draw(self, screen, scale, shiftx, shifty):
        """
            A method for drawing a :class:`Consumable` on a PyGame display. If the Consumable is currently "full" it will be drawn as a filled circle. If it is currently in a depleted, or consumed, state then it will be drawn as an unfilled circle.


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
        if self.depleted:
            width = 2
        pygame.draw.circle(screen, center=(scale*self.x+shiftx, scale*self.y+shifty), color=self.colour, width=width, radius=scale*self.radius)

    def reset(self) -> None:
        """
            Reset a :class:`Consumable` to its original state upon its construction, e.g. so that it can be re-used in another simulation run.
        """
        super().reset()
        self.depleted = False  # initially, a Consumable is not depleted. When it is consumed, it is depleted and will be invisible until (and if) it recovers
        self.depleteds = [False]
        self.time_since_consumed = 0  # used to track time to recover
        self.stimulus.reset()
        self.radius = self.initial_radius
        self.recovery_time = self.initial_recovery_time
        self.quantity = self.initial_quantity

    def get_data(self):
        """
            A function to get the data from a :class:`Consumable`, in the form of a string-keyed dict.

            These data, as and when they are included in the returned dict, can be accessed with the following keys:

            * data inherited from :class:`System`: see :class:`System`
            * data from the attached :class:`LightSource`: ``data["light_source"]``
            * the history of when the consumable is/isn't depleted: ``data["depleteds"]``
        """
        data = super().get_data()
        data["light_source"] = self.stimulus.get_data()
        data["depleteds"] = self.depleteds


        return data
