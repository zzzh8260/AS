from .System import *
from .noise import *
from .Controller import *

import math

class FauxKilobotController(Controller):
    """
        This class represents a controller for an :class:`FauxKilobot`.
    """
    def __init__(self, inputs_n: int,
                       step_fun: Callable[[float, List[float], List[float], List[float]], List[float]],
                       noisemakers: List[NoiseSource]=None,
                       noisemakers_inds=None,
                       params: List[float]=None,
                       adapt_fun: Callable[[List[float], List[float], List[float]], None]=None,
                       adapt_enabled: bool=True,
                       test_interval: float=0,
                       state_n: int=0,
                       initial_state: List[float]=None):
        """
            __init__(self, inputs_n: int, step_fun: Callable[[float, List[float], List[float], List[float]], List[float]], noisemakers: List[NoiseSource]=None, noisemakers_inds=None, params: List[float]=None, adapt_fun: Callable[[List[float], List[float], List[float]], None]=None, adapt_enabled: bool=True, test_interval: float=0, state_n: int=0, initial_state: List[float]=None)

            :param inputs_n: The number of inputs expected by the controller.
            :type inputs_n: int

            :param state_n: The number of state variables that the controller expects to be returned from its ``step_fun`` method.
            :type commands_n: int

            :param initial_state: The controller's initial state vector, if it has one. Defaults to ``None``. Should be a list with ``state_n`` entries.
            :type initial_state: list[float]

            :param step_fun: The function which will be used to generate the controller's outputs, given the inputs to the controller's ``step`` method, the interval of time to integrate over, and any state and parameters the controller makes use of.
            :type step_fun: a function

            :param noisemakers: A list of noise sources which will potentially affect the commands the controller outputs.
            :type noisemakers: List of NoiseSource objects.

            :param noisemaker_inds: A list of indices of commands which will potentially have noise added to them. Any indices which are out of range in either the list of noisemakers or commands will be ignored.
            :type noisemaker_inds: List of integers.

            :param params: A list of parameters used by the controller. These parameters will be used in the controller's ``step_fun`` function, which will be caused from the controller's ``step`` method.
            :type params: list of floats.

            :param adapt_fun: A function wich can be used to adapt a controller, by changing its parameters. It only has access to the same data that the controller does: its histories of inputs, outputs, and parameter values.
            :type adapt_fun: a function

            :param adapt_enabled: When a :class:`Controller` has an ``adapt_fun``, that function will only be used when ``adapt_enabled`` is set to True.
            :type adapt_enabled: bool

            :param test_interval: The period of time to wait between parameter changes, if an adapt_fun is being used.
            :type test_interval: float
        """
        super().__init__(inputs_n=inputs_n,
                         commands_n=2,
                         step_fun=step_fun,
                         noisemakers=noisemakers,
                         noisemakers_inds=noisemakers_inds,
                         params=params,
                         adapt_fun=adapt_fun,
                         adapt_enabled=adapt_enabled,
                         test_interval=test_interval,
                         state_n=state_n,
                         initial_state=initial_state)

    def step(self, dt: float, inputs: List[float], radio) -> List[float]:
        """
            A method to step a controller forwards in time.

            :param dt: The interval of time to integrate the controller over.
            :type dt: float

            :param inputs: The inputs to the controller.
            :type inputs: list of floats

            :param radio: A :class:`Radio`. If the controller will use communication with other robots with radios, then it will need to set and receive messages in its ``step_fun``.
            :type radio: :class:`Radio`

            :return: List of commands.
            :rtype: list of floats.
        """
        self.t += dt  # increment time variable by simulation step size

        # store new inputs
        self.inputs_hist.append(inputs)

        # adapt params
        if self.adapt_fun and self.adapt_enabled:
            if self.t >= self.test_interval:
                self.t = 0
                self.params = self.adapt_fun(dt, np.array(self.inputs_hist), np.array(self.commands_hist), np.array(self.params_hist))

        params_copy = self.params

        # store new params
        if self.params is not None:
            self.params_hist.append(self.params[:])
            params_copy = self.params[:]

        # get commands
        commands, state = self.step_fun(dt, inputs, params_copy, self.state, radio)

        if self.state is not None:
            self.state = state
            self.state_hist.append(state)

        # add noise to commands
        if self.noisemakers_inds:
            for ind in self.noisemakers_inds:
                # check that there is a noisemaker and a command at the given index in each list
                if ind < len(self.noisemakers) and ind < len(commands):
                    commands[ind] += self.noisemakers[ind].step(dt)

        # store new commands
        self.commands_hist.append(commands)

        # return commands
        return commands

def fauxlobot_random_walk(dt, inputs, params, state, radio):
    """

    """
    heading = random_in_interval(-math.pi, math.pi)
    speed = random_in_interval(1, 1)

    return [speed, heading], None
