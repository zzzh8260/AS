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

    #########################################################################
    #                           Set up agents                               #
    #########################################################################

    # set up controller
    generalised_controller = RobotController(inputs_n=5, step_fun=generalised_braitenberg, noisemakers=[], noisemakers_inds=[], params=params)

    # set parameters for robot sensor morphology (roughly speaking, morphology means the structure and properties of the body)
    field_of_view = 0.9 * math.pi
    left_sensor_angle = np.pi/6
    right_sensor_angle = -np.pi/6

    # construct robot, using the controller and parameters specified above
    robot = new_light_seeking_Robot(x=-5, y=0, theta=0, light_sources=light_sources, controller=generalised_controller, FOV=field_of_view, left_sensor_angle=left_sensor_angle, right_sensor_angle=right_sensor_angle, left_motor_inertia=10, right_motor_inertia=10)

    # put robot into list of agents for Simulator - we *always* need this list, even if there is only one agent in it
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
    sim = Simulator(agents=agents, envs=light_sources, duration=duration, dt=0.1, disturbances=disturbances)
    # get SimulationRunner object
    sim_runner = SimulationRunner(sim, animate=animate, pause_ani=True, animation_delay=animation_frame_delay, screen_width=screen_width)
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
