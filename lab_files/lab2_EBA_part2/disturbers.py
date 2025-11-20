# import packages
import sys

# import Sandbox
sys.path.insert(1, '../../') # relative path to folder which contains the Sandbox module
from Sandbox_V1_4 import *

'''
    In most, or possibly all, labs involving sensorimotor behaviour, we will use a "disturbances.py" file
    for any code purely related to disturbing our agents or their environmments. We separate this code
    from the main lab file so that we can keep that file as small and clear as possible.
'''

'''
    This function will return a disturbance source which generates noise on the robot's left motor.
    The kind of noise, if any, that it generates is determined by the boolean values passed to the function.
    The noise interferes with the motor by directly modifying (i.e. adding noise to) its speed.
'''
def get_motor_noise_disturber(robot, white_noise=False, brown_noise=False, spike_noise=False):
    white_noise_params=[0,0]
    brown_noise_step=0
    spike_noise_params=[0,0,0]
    start_times = []
    if white_noise:
        white_noise_params = [0.3, -0.3]
    if brown_noise:
        brown_noise_step = 0.01
    if spike_noise:
        spike_noise_params = [0.05, 1, -1]
    if white_noise or brown_noise or spike_noise:
        start_times = [0]
    return MotorNoiseDisturbanceSource(robot.left_motor, white_noise_params=white_noise_params, spike_noise_params=spike_noise_params, brown_noise_step=brown_noise_step, start_times=start_times)
