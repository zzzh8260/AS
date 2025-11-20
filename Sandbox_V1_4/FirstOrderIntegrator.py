from .System import *

class FirstOrderIntegrator(System):
    """

    """
    def __init__(self, time_constant: float, initial_state: float=0) -> None:
        """

        """
        assert time_constant > 0, "time constant must be > 0"
        self.inv_time_constant = 1/time_constant
        self.state = initial_state
        self.states = [initial_state]

    def step(self, force_input: float, dt: float) -> float:
        """

        """
        self.state += self.inv_time_constant * force_input
        self.states.append(self.state)
        return self.state
