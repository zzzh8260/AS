from Sandbox_V1_4.Controller import Controller
import numpy as np


class BraitenbergController(Controller):
    def __init__(self):
        # 2 inputs (Light sensors), 2 outputs (Motors)
        # We call super().__init__ with appropriate counts
        super().__init__(inputs_n=2, commands_n=2)

        # Fixed Weights (Sensor -> Motor)
        # A "Fear" vehicle (Crossed connections): Left Sensor -> Right Motor
        # This causes it to turn away from light.
        # A "Aggression" vehicle (Uncrossed): Left Sensor -> Left Motor
        # This causes it to turn towards light.

        # Let's use simple aggression (uncrossed) for approaching light
        # w_ll = left sensor to left motor
        # w_rr = right sensor to right motor
        self.weights = np.array([
            [1.0, 0.0],  # Inputs to Left Motor (Left Sensor, Right Sensor)
            [0.0, 1.0]  # Inputs to Right Motor (Left Sensor, Right Sensor)
        ])
        self.bias = 0.0

    def step(self, dt, inputs):
        """
        dt: timestep
        inputs: list of sensor activations [left_light, right_light]
        """
        # 1. Convert inputs to numpy array
        inp = np.array(inputs)

        # 2. Compute Motor Outputs (Linear or Sigmoid)
        # outputs = weights * inputs + bias
        # Using matrix multiplication
        outputs = np.dot(self.weights, inp) + self.bias

        # 3. Apply Sigmoid activation (Crucial for Williams 2005 comparison)
        # Williams uses: y = 1 / (1 + e^-(potential + bias))
        # But standard Braitenberg is often linear.
        # Let's use a sigmoid so we can demonstrate saturation later.
        outputs = 1 / (1 + np.exp(-outputs))

        # Scale up? Sigmoid is 0.0 to 1.0. Motors might need -1 to 1 or 0 to 2.
        # Let's assume 0-1 is fine for now, or scale by max_speed in the Robot class.

        # Store history (Required for analysis plots!)
        super().step(dt, inputs)

        return outputs