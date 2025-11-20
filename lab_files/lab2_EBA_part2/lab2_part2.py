# import packages
import sys
import yaml

# import Sandbox
sys.path.insert(1, '../../') # relative path to folder which contains the Sandbox module
from Sandbox_V1_4 import *

# import local files
from controllers import *
from initialisers import *
from analyses import *
from disturbers import *

def main():

    #########################################################################
    #                        Read parameter file                            #
    #########################################################################

    # read parameters from file
    with open('params.yaml', 'r') as file:
        params_dict = yaml.safe_load(file)

    # controller params
    params = [0] * 6
    params[2] = params_dict["b_l"]
    params[5] = params_dict["b_r"]
    params[1] = params_dict["w_rl"]
    params[0] = params_dict["w_ll"]
    params[4] = params_dict["w_rr"]
    params[3] = params_dict["w_lr"]

    # simulation params
    n_runs = params_dict["n_runs"]
    duration = params_dict["duration"]
    screen_width = params_dict["screen_width"]
    animate = True if params_dict["animate"] == 1 else False
    animation_frame_delay = params_dict["animation_frame_delay"]

    # left motor noise params
    white_noise_on = True if params_dict["white"] == 1 else False
    brown_noise_on = True if params_dict["brown"] == 1 else False
    spike_noise_on = True if params_dict["spike"] == 1 else False

    # most robot data will only be plotted if this is set to 1
    plot_data = True if params_dict["plot_data"] == 1 else False

    #########################################################################
    #                         Set up environment                            #
    #########################################################################

    # set up environmental systems - even if there is only one light source in the environment, we always use a list
    light_sources = [LightSource(0, 0, 2)]

    patches = []
    patches.append(FloorPatch(x_left=2, x_right=4, y_top=4, y_bottom=-4, colour='blue', label='blue'))
    patches.append(FloorPatch(x_left=-4, x_right=-2, y_top=4, y_bottom=-4, colour='blue', label='blue'))
    patches.append(FloorPatch(x_left=-4, x_right=-1, y_top=-2, y_bottom=-4, colour='blue', label='blue'))

    #########################################################################
    #                           Set up agents                               #
    #########################################################################

    # set up controller - uncomment only one of these lines, for the part of the lab which you are working on
    # controller = Controller(step_fun=part1controller, inputs_n=4, commands_n=2, params=[2, 0.1, 5])
    controller = RobotController(step_fun=extended_braitenberg, inputs_n=8, params=params)
    # controller = Controller(step_fun=part3controller, inputs_n=4, commands_n=2, params=[2, 0.1, 10])

    # set up sensors
    x = 0
    y = 0
    FOV = 10*math.pi/8
    sensors = []
    sensors.append(LightSensor(light_sources=light_sources, x=x, y=y, FOV=FOV, colour="yellow"))
    sensors.append(LightSensor(light_sources=light_sources, x=x, y=y, FOV=FOV, colour="yellow"))
    left_floor_sensor = FloorPatchSensor(floor_patches=patches, x=x, y=y, label='blue', name_str="Left blue patch sensor")
    left_floor_sensor.initial_state['colour'] = 'cyan'
    right_floor_sensor = FloorPatchSensor(floor_patches=patches, x=x, y=y, label='blue', name_str="Right blue patch sensor")        
    right_floor_sensor.initial_state['colour'] = 'cyan'
    front_floor_sensor = FloorPatchSensor(floor_patches=patches, x=x, y=y, label='blue', name_str="Front blue patch sensor")        
    front_floor_sensor.initial_state['colour'] = 'cyan'
    # specify angular positions of sensors on robot's body
    sensors += [left_floor_sensor, right_floor_sensor, front_floor_sensor]
    sensor_angles = [2*math.pi/8, -2*math.pi/8, math.pi/8 - 0., -(math.pi/8 - 0.), 0]

    # construct Robot
    robot = Robot(x=x, y=y, theta=0, controller=controller, sensors=sensors, sensor_angles=sensor_angles, light=LightSource(x=x, y=y, model='linear'))

    # put robot into list of agents for Simulator
    agents=[robot]

    #########################################################################
    #                    Set up experimental conditions                     #
    #########################################################################

    # use these lines to set up ensembles of initial conditions for the robot
    # - use init_fun1 with the perturb_fun line comnmented out
    # - or use init_fun2 in conjunction with perturb2
    # - or comment the init_fun lines out and use perturb2 on its own
    # - or see what happens if you comment both of these lines out
    robot.init_fun = init_fun2 # init_fun2 # use init_fun1 or init_fun2
    robot.initial_state["init_fun"] = robot.init_fun
    robot.perturb_fun = perturb2
    robot.initial_state["perturb_fun"] = robot.perturb_fun

    # set up a noise source, which will affect the robot's left motor
    motor_disturber = get_motor_noise_disturber(robot, white_noise_on, brown_noise_on, spike_noise_on)
    # put disturbances in list - we always use the list, even if we have 0, 1, or multiple disturbances which we want to apply
    disturbances = [motor_disturber]

    #########################################################################
    #                      Set up and run simulation                        #
    #########################################################################

    # get Simulator object - note that agents, environmental systems, and disturbances lists are all passed to its constructor
    sim = Simulator(agents=agents, envs=light_sources+patches, duration=duration, dt=0.1, disturbances=disturbances)
    # get SimulationRunner object
    sim_runner = SimulationRunner(sim, animate=animate, pause_ani=False, animation_delay=animation_frame_delay, screen_width=screen_width)
    # Run simulation n times
    sim_data = sim_runner.run_sims(n=n_runs)

    #########################################################################
    #                     Plotting and analysis section                     #
    #########################################################################

    # plot agents' trajectories
    ax = plot_all_sims_trajectories(sim_data, show_cbar=False, cbar_fig=True)
    # plot all light sources
    for light in light_sources:
        light.draw(ax)
    # plot line showing agents' initial orientations
    for data in sim_data:
        robot_data = data["agents"][0] # agents are always in a list, even if there is only 1 of them
        x = robot_data["xs"][0]
        y = robot_data["ys"][0]
        plt.plot(x, y, 'ok')
        theta = robot_data["thetas"][0]
        plt.plot([x, x + math.cos(theta)], [y, y + math.sin(theta)], 'r')

    for patch in patches:
        patch.draw(ax)

    # plot robots' basic data (plots of robot's various noisemakers are not produced by this function call)
    if plot_data:
        plot_all_robots_basic_data(sim_data, multiple_plots=False, show_motors=True, show_controllers=True, show_sensors=True)
        # plot noise - actually, there is no robot noise recorded in this simulation, as the robot is disturbed by an external force,
        # not an internal one
        plot_all_robots_noise(sim_data)

    # get simulation data for phase plane plotting
    # - note that however many times you run the simulation, the phase portrait is only for the first run
    #   this run is selected by simdata[0]
    ts = sim_data[0]["ts"]
    robot_data = sim_data[0]["agents"][0] # agents are always in a list, even if there is only 1 of them
    # look at unsmoothed/smoothed data and phase portraits
    do_phase_portraits(ts, robot_data)

    plt.show()

if __name__ == '__main__':
    main()
