from .Controller import *
from .noise import *

import math

class AntController(Controller):
    """
        This class represents a controller for an :class:`Ant`.

        In the current implementation, all this class does is wrap :class:`Controller` with a very slightly smaller ``init`` method - see that class for details of any parameters.
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

def dummy(dt, inputs, params, state):
    """

    """
    return [0, 0], None

def ant_correlated_random_walk(dt, inputs, params, state):
    """

    """
    turn_speed = random_in_interval(minimum=-0.03, maximum=0.03)
    move_speed = max(0.2, params[0] + random_in_interval(-0.4, 0.4))

    return [move_speed, turn_speed], None
