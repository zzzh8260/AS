from .Controller import *
from .noise import *
import copy as cp

class RobotController(Controller):
    """
        This class represents a controller for an :class:`Robot`.

        In the current implementation, all this class does is wrap :class:`Controller` with a very slightly smaller ``init`` method - see that class for details of any parameters.
    """
    def __init__(self, inputs_n: int,
                       step_fun: Callable[[float, List[float], List[float], List[float]], List[float]],
                       noisemakers: List[NoiseSource]=None,
                       noisemakers_inds=None, params: List[float]=None,
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
