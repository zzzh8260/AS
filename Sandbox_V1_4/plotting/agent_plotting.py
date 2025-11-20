from . import *
from . import timeColouredPlots as tcp
import matplotlib.pyplot as plt
import numpy as np

def get_agents_data(sim_data):
    all_ts = []
    all_agents_data = []
    for data in sim_data:
        ind = 0
        for agent_data in data["agents"]:
            agent_data["run_n"] = data["run_n"]
            agent_data["ind"] = ind
            ind += 1
            all_agents_data.append(agent_data)
            all_ts.append(data["ts"])
    return all_agents_data, all_ts

def plot_all_agents_basic_data(sim_data, show_motors=True, show_sensors=True, show_controllers=False, show_noise=False):

    all_agents_data, all_ts = get_agents_data(sim_data)

    if show_motors:
        for ts, agent_data in zip(all_ts, all_agents_data):
            plot_single_agent_motors(ts, agent_data)

    if show_controllers:
        for ts, agent_data in zip(all_ts, all_agents_data):
            plot_single_agent_controllers(ts, agent_data)

    if show_sensors:
        for ts, agent_data in zip(all_ts, all_agents_data):
            plot_single_agent_sensors(ts, agent_data)

    if show_noise:
        for ts, agent_data in zip(all_ts, all_agents_data):
            plot_single_robot_noise(ts, agent_data)

def plot_single_agent_sensors(ts, agent_data):
    n = len(agent_data["sensors"])
    fig, ax = plt.subplots(n, 1)

    for i, sensor_data in enumerate(agent_data["sensors"]):
        ax[i].plot(ts, sensor_data["activations"], label='sensor ' + str(i))
        ax[i].set_xlabel('Time')
        ax[i].set_ylabel('Activation')
        ax[i].set_title(sensor_data["name_str"])

    fig.suptitle("Run " + str(agent_data["run_n"]) + ", " + agent_data["classname"] + " " + str(agent_data["ind"]))
    fig.tight_layout()

def plot_single_agent_motors(ts, agent_data):
    n = len(agent_data["motors"])
    fig, ax = plt.subplots(n, 1)

    for i, motor_data in enumerate(agent_data["motors"]):
        ax[i].plot(ts, motor_data["speeds"], label='sensor ' + str(i))
        ax[i].set_xlabel('Time')
        ax[i].set_ylabel('Speed')
        ax[i].set_title(motor_data["name_str"])

    fig.suptitle("Run " + str(agent_data["run_n"]) + ", " + agent_data["classname"] + " " + str(agent_data["ind"]))
    fig.tight_layout()

def plot_single_agent_controllers(ts, agent_data):
    n = len(agent_data["controller"]["commands_hist"][-1])
    fig, ax = plt.subplots(n, 1)

    commands = np.array(agent_data["controller"]["commands_hist"])

    for i in range(n):
        ax[i].plot(ts, commands[:,i], linewidth='2')
        ax[i].set_xlabel('Time')
        ax[i].set_title('Controller output ' + str(i))

    fig.suptitle("Run " + str(agent_data["run_n"]) + ", " + agent_data["classname"] + " " + str(agent_data["ind"]))
    fig.tight_layout()

def check_for_noise_data(agent_data):
    sensor_noise = False
    controller_noise = False

    sensor_noise_n = 0
    for sensor_data in agent_data["sensors"]:
        if sensor_data["noises"]:
            sensor_noise_n += 1
            sensor_noise = True

    print(sensor_noise_n)

    controller_noise_n = 0
    controller_noise_data = agent_data["controller"]["noises"]
    if controller_noise_data:
        for noise_data in controller_noise_data:
            controller_noise_n += 1
            controller_noise = True

    noise_n = sensor_noise_n + controller_noise_n

    return sensor_noise, controller_noise, sensor_noise_n, controller_noise_n, noise_n

def plot_single_robot_noise(ts, agent_data):

    sensor_noise, controller_noise, sensor_noise_n, controller_noise_n, noise_n = check_for_noise_data(agent_data)

    if noise_n == 0:
        return

    dummy_ax = False
    if noise_n == 1:
        noise_n += 1
        dummy_ax = True

    fig, ax = plt.subplots(noise_n, 1)

    ax_ind = 0

    if sensor_noise_n > 0:
        for i, sensor_data in enumerate(agent_data["sensors"]):
            if sensor_data["noises"]:
                ax[ax_ind].plot(ts, sensor_data["noises"], label='Sensor ' + str(i) + ' noise')
                # ax[ax_ind].legend()
                ax[ax_ind].set_title(sensor_data["name_str"] + ' noise')
                ax_ind += 1

    if controller_noise_n > 0:
        for i, noise_data in enumerate(agent_data["controller"]["noises"]):
            ax[ax_ind].plot(ts, noise_data, label='Controller output ' + str(i) + ' noise')
            ax[ax_ind].set_title('Controller output ' + str(i) + ' noise')
            ax_ind += 1

    if dummy_ax:
        fig.delaxes(ax[1])

    fig.suptitle("Run " + str(agent_data["run_n"]) + ", " + agent_data["classname"] + " " + str(agent_data["ind"]))
    fig.tight_layout()
