# import packages
import sys

# import Sandbox
sys.path.insert(1, '../../') # relative path to folder which contains the Sandbox module
from Sandbox_V1_4 import *

'''
    In most, or possibly all, labs involving sensorimotor behaviour, we will use a "controllers.py" file
    for any code purely related to controlling our agents'. We separate this code from the main lab file
    so that we can keep that file as small and clear as possible.
'''


'''
    Technically, this function is not a Sandbox Controller, which you will learn more about
    soon. This is actually a control function which a Controller uses. It implements a simple
    feedforward neural network which connects 2 inputs to 2 neurons, which generate the function's
    outputs. The network uses a linear activation function with a bias in each of its 2 neurons.
'''
def generalised_braitenberg(dt, inputs, params, state=[]) -> List[float]:

    ### set left motor speed
    # weighted connection from left sensor to left motor command
    left_speed_command = inputs[4] * params[0]
    # weighted connection from right sensor to left motor command
    left_speed_command += inputs[5] * params[1]
    # add bias term to left motor command
    left_speed_command += params[2]
    ### set right motor speed
    # weighted connection from left sensor to right motor command
    right_speed_command = inputs[4] * params[3]
    # weighted connection from right sensor to right motor command
    right_speed_command += inputs[5] * params[4]
    # add bias term to right motor command
    right_speed_command += params[5]

    # return motor speed commands to robot's controller
    return [left_speed_command, right_speed_command], None
