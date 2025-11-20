# import packages
import sys

# import Sandbox
sys.path.insert(1, '../../') # relative path to folder which contains the Sandbox module
from Sandbox_V1_4 import *

'''
    Complete and use this function for part 1 of the lab.
    As well as adding any code/functions for calculating the motor speed commands, you can use
    as many parameters in your controller as you like, which are passed in to the function via
    the params variable.
'''
def part1controller(dt, inputs, params, state):

    # you can use these parameters in your controller, if you want to
    weights1 = params[0]
    weights2 = params[1]
    weights3 = params[2]

    # replace these lines with your code for setting the motor speed commands
    left_speed_command = 0
    right_speed_command = 0

    return [left_speed_command, right_speed_command], None

'''
    Complete and use this function for part 2 of the lab.
    As well as adding any code/functions for calculating the motor speed commands, you can use
    as many parameters in your controller as you like, which are passed in to the function via
    the params variable.
'''
def part2controller(dt, inputs, params, state):

    # replace these lines with your code for setting the motor speed commands
    left_speed_command = 0
    right_speed_command = 0

    return [left_speed_command, right_speed_command], None

'''
    Complete and use this function for part 3 of the lab.
    As well as adding any code/functions for calculating the motor speed commands, you can use
    as many parameters in your controller as you like, which are passed in to the function via
    the params variable.
'''
def part3controller(dt, inputs, params, state):

    # replace these lines with your code for setting the motor speed commands
    left_speed_command = 0
    right_speed_command = 0

    return [left_speed_command, right_speed_command], None
