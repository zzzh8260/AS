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


'''
    Homeostatic Braitenberg Controller
    This controller implements Synaptic Homeostasis (Bias Adaptation).
    It adjusts the bias dynamically to maintain a target firing rate (motor speed).

    Rule: delta_bias = learning_rate * (target_rate - current_output) * dt

    state[0]: current bias for left motor
    state[1]: current bias for right motor
'''


def homeostatic_braitenberg(dt, inputs, params, state=[]) -> List[float]:
    ######################################################################
    # Fix for nested list bug
    if len(state) == 1 and isinstance(state[0], list):
        state = state[0]
    ######################################################################

    # Unpack extra parameters (appended after the standard 6 params)
    # params structure: [w_ll, w_rl, b_l_init, w_lr, w_rr, b_r_init, target_rate, learning_rate]
    target_rate = params[6]
    learning_rate = params[7]

    # Unpack new Lesion params (with defaults to prevent crashes if params list is short)
    enable_lesion = params[8] if len(params) > 8 else 0
    lesion_start_time = params[9] if len(params) > 9 else 100
    lesion_factor = params[10] if len(params) > 10 else 0.5
    ambient_light = params[11] if len(params) > 11 else 0.0

    # Initialize state (biases) if it's the first step
    # We use the initial biases defined in params.yaml as the starting point
    # Initialize state: [bias_l, bias_r, current_time]
    if not state:
        state = [params[2], params[5], 0.0]
    elif len(state) == 2:
        state.append(0.0)

    current_bias_l = state[0]
    current_bias_r = state[1]
    current_time = state[2]

    # --- 实验逻辑：处理传感器输入 ---
    processed_inputs = list(inputs)  # 复制一份输入

    # 1. 施加环境光干扰 (Experiment 5)
    # 在所有光照传感器读数上叠加环境光
    if ambient_light > 0:
        processed_inputs[4] += ambient_light
        processed_inputs[5] += ambient_light

    # 如果开启了损伤实验 且 时间到达触发点
    if enable_lesion == 1 and current_time > lesion_start_time:
        # 模拟损伤：所有光照传感器读数减半
        # inputs[4] 和 inputs[5] 是传感器读数
        processed_inputs[4] *= lesion_factor
        processed_inputs[5] *= lesion_factor
        # 可选：打印一次提示 (仅在变化瞬间)
        if abs(current_time - lesion_start_time) < dt:
            print(f"[Experiment] Lesion Triggered at t={current_time:.1f}s! Factor: {lesion_factor}.")
    ### Calculate Motor Outputs (Standard Braitenberg logic but using DYNAMIC bias)

    # Left Motor
    # Weighted inputs + Dynamic Bias
    left_sensor_input = (processed_inputs[4] * params[0]) + (processed_inputs[5] * params[1])
    left_speed_command = left_sensor_input + current_bias_l

    # Right Motor
    # Weighted inputs + Dynamic Bias
    right_sensor_input = (processed_inputs[4] * params[3]) + (processed_inputs[5] * params[4])
    right_speed_command = right_sensor_input + current_bias_r

    ### Apply Homeostatic Plasticity Rule
    # We want the output (speed) to be close to target_rate.
    # If speed > target, bias should decrease.
    # If speed < target, bias should increase.

    delta_b_l = learning_rate * (target_rate - left_speed_command) * dt
    delta_b_r = learning_rate * (target_rate - right_speed_command) * dt

    new_bias_l = current_bias_l + delta_b_l
    new_bias_r = current_bias_r + delta_b_r

    # 更新时间
    new_time = current_time + dt

    # Return commands and the NEW state (updated biases)
    print(f"L Bias: {new_bias_l:.2f}, Speed: {left_speed_command:.2f}")
    return [left_speed_command, right_speed_command], [new_bias_l, new_bias_r, new_time]