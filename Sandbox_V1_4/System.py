from .base import *

from typing import Callable

class System:
    '''
        Every object in a Sandbox simulation is an instance of a subclass of the abstract class :class:`System`. In some cases, this is for conceptual reasons rather than practical ones, e.g. in the case of a :class:`DisturbanceSource`, which certainly can be considered a system but which doesn't currently inherit anything from :class:`System` (although this may well change in a future implementation).
    '''
    def __init__(self, x: float=None, y: float=None, theta: float=None, init_fun: Callable=None, perturb_fun: Callable=None):
        """
            __init__(x: float=None, y: float=None, theta: float=None, perturb_fun: Callable=None, init_fun: Callable=None)

            Construct :class:`System`. If either ``x`` or ``y`` are specified in the call to ``init``, then the system will have position and will keep a history of both its x- and y-coordinates over time. If ``theta`` is specified in the call to ``__init__``, then the system has orientation, and will keep a history of its orientation over time.

            :param x: The system's x-coordinate. Defaults to `None`.
            :type x: float

            :param y: The system's y-coordinate. Defaults to `None`.
            :type y: float

            :param theta: The system's angular orientation. Defaults to `None`. In *Sandbox*, orientations are in radians.
            :type theta: float

            :param perturb_fun: A placeholder for a function which can be used to perturb the system's state. This will  typically be used at the beginning of simulation runs. Defaults to `None`.
            :type perturb_fun: function

            :param init_fun: A placeholder for a function which can be used to set the initial state of the system in each simulation run. Defaults to `None`.
            :type init_fun: function

        """
        self.has_position: bool = (x is not None) and (y is not None)
        if self.has_position:
            self.init_xy(x, y)
        self.has_orientation: bool = theta is not None
        if self.has_orientation:
            self.init_theta(theta)

        self.perturb_fun: Callable = perturb_fun
        self.init_fun: Callable = init_fun
        self.init_ind: int = 0

        self.initial_state = System.get_data(self)

    def step(self, dt: float) -> None:
        """
            Step the :class:`System` forwards in time. Subclasses of :class:`System` will generally override this method, to implement class-specific functionality, but they will also need to call this method if they have either position or orientation, as this is where the history of thos variables over time gets updated.

            :param dt: The interval of time to integrate the system over (strictly speaking, should be delta_t). Currently unused here, but will often be used in subclasses.
            :type dt: float
        """
        if self.has_position:
            self.xs.append(self.x)
            self.ys.append(self.y)
        if self.has_orientation:
            self.thetas.append(self.theta)

    def get_data(self) -> Dict[str, Union[float, List[float]]]:
        """
            A function to get the data from a :class:`System`, in the form of a string-keyed dict. If a :class:`System` has position, then its current coordinates plus their histories will be included in the data. If a :class:`System` has orientation, then its current orientation and its orientation history are incuded in the data.

            These data, as and when they are included in the returned dict, can be accessed with the following keys:

            * current x-coordinate: ``data["x"]``
            * history of x-coordinates over time: ``data["xs"]``
            * current y-coordinate: ``data["y"]``
            * history of y-coordinates over time: ``data["ys"]``
            * current orientation: ``data["theta"]``
            * history of orientations over time: ``data["thetas"]``

            :return: The System's data.
            :rtype: dict
        """
        data: Dict[str, Union[float, List[float]]] = {"x": None, "y": None,
                                                      "theta": None, "xs": None,
                                                      "ys": None, "thetas": None, "has_position": self.has_position, "has_orientation":  self.has_orientation, "perturb_fun": self.perturb_fun, "init_fun": self.init_fun, "init_ind": self.init_ind}

        if self.has_position:
            data["xs"] = self.xs[:]
            data["x"] = self.x
            data["ys"] = self.ys[:]
            data["y"] = self.y
        if self.has_orientation:
            data["thetas"] = self.thetas[:]
            data["theta"] = self.theta

        return data

    def reset(self) -> None:
        """
            Reset a :class:`System` to its original state upon its construction, e.g. so that it can be re-used in another simulation run.
        """
        self.has_position = self.initial_state["has_position"]
        self.has_orientation = self.initial_state["has_orientation"]
        self.perturb_fun = self.initial_state["perturb_fun"]
        self.init_fun = self.initial_state["init_fun"]
        # self.init_ind = self.initial_state["init_ind"]

        if self.has_position:
            self.init_xy(self.initial_state["x"], self.initial_state["y"])

        if self.has_orientation:
            self.init_theta(self.initial_state["theta"])

    def get_data_and_reset(self) -> Dict[str, dict]:
        """
            Reset a :class:`System` to its original state and return its data.
        """
        data = self.get_data()
        self.reset()
        return data

    def init_xy(self, x: float, y: float) -> None:
        """
            Set the systems initial x- and y-coordinates to the passed in values.

            :param x: The system's x-coordinate.
            :type x: float

            :param y: The system's y-coordinate.
            :type y: float
        """
        self.x = x
        self.y = y
        self.xs = [x]
        self.ys = [y]

    def init_theta(self, theta: float) -> None:
        """
            Set the systems initial orientation to the passed in value.

            :param theta: The system's orientation.
            :type theta: float
        """
        self.theta = theta
        self.thetas = [theta]

    def perturb(self) -> None:
        """
            A placeholder for a method which can be used to perturb the state of the system. An example of how this might be used is: every time a mobile agent is simulated, in a set of runs, its pose, [x, y, theta], is shifted by some random amount so that it doesn't always start from exactly the same place or orientation.
        """
        if self.perturb_fun:
            self.perturb_fun(self)

    def init_conditions(self) -> None:
        """
            A placeholder for a method which can be used to set the system's initial state. An example of this is: an init_conditions method for a mobile agent defines lists of x, y, and theta values. Every time the agent is simulated, in a set of runs, the next set of x, y, and theta values is used, so that the agent's position and orientaton are varied in a controlled way.
        """
        if self.init_fun:
            self.init_fun(self)
            self.init_ind += 1

    def __eq__(self, other):
        """
            Overrides the == operator for instances of this class.

            :param other: The instance of System that this instance will be compared to.
            :type other: System
        """

        if other == None:
            return False

        is_eq = True

        if self.has_position:
            is_eq = is_eq and self.x == other.x
            is_eq = is_eq and self.y == other.y
            is_eq = is_eq and self.xs == other.xs
            is_eq = is_eq and self.ys == other.ys
        if self.has_orientation:
            is_eq = is_eq and self.theta == other. theta
            is_eq = is_eq and self.thetas == other. thetas

        is_eq = is_eq and self.perturb_fun == other.perturb_fun
        is_eq = is_eq and self.init_fun == other.init_fun

        # I may change my mind about this, but I don't think init_ind should be compared
        # is_eq = is_eq and self.init_ind == other.init_ind

        is_eq = is_eq and self.initial_state == other.initial_state

        return is_eq
