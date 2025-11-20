# import packages
import sys
import yaml

# import Sandbox
sys.path.insert(1, '../../') # relative path to folder which contains the Sandbox module
from Sandbox_V1_4 import *

# import local files
from controllers import *

#########################################################################
#                        Read parameter file                            #
#########################################################################

# read parameters from file
with open('params.yaml', 'r') as file:
    params_dict = yaml.safe_load(file)

duration = params_dict["duration"]
screen_width = params_dict["screen_width"]
animate = True if params_dict["animate"] == 1 else False
animation_frame_delay = params_dict["animation_frame_delay"]
plot_data = True if params_dict["plot_data"] == 1 else False

#########################################################################
#                         Set up environment                            #
#########################################################################

# for parts 1 and 2, set this variable to True, so that all lights are yellow
# for part 3, set this variable to False, so that lights are red/yellow
parts1_2 = False

# set colour of second group of lights
if parts1_2:
    colour2 = 'yellow'
    n = 5
else:
    colour2 = 'red'
    n = 10

# generate environmental objects
yellow_light_sources = random_sources(x_min=-10, x_max=10, y_min=-10, y_max=10, brightness=1, n=10, colour='yellow', label='yellow')

if not parts1_2:
    # generate environmental objects
    red_light_sources = random_sources(x_min=-10, x_max=10, y_min=-10, y_max=10, brightness=1, n=10, colour='red', label=colour2)
else:
    red_light_sources = yellow_light_sources

#########################################################################
#                           Set up agents                               #
#########################################################################

# set up controller - uncomment only one of these lines, for the part of the lab which you are working on
# controller = Controller(step_fun=part1controller, inputs_n=4, commands_n=2, params=[2, 0.1, 5])
controller = RobotController(step_fun=part3controller, inputs_n=7, params=[7, 0.05, 5])
# controller = Controller(step_fun=part3controller, inputs_n=4, commands_n=2, params=[2, 0.1, 10])

# set up sensors
x = 0
y = 0
FOV = 7*math.pi/8
sensors = []
sensors.append(LightSensor(light_sources=yellow_light_sources, x=x, y=y, FOV=FOV, colour="yellow"))
sensors.append(LightSensor(light_sources=yellow_light_sources, x=x, y=y, FOV=FOV, colour="yellow"))
sensors.append(LightSensor(light_sources=red_light_sources, x=x, y=y, FOV=FOV, colour="red"))
sensors.append(LightSensor(light_sources=red_light_sources, x=x, y=y, FOV=FOV, colour="red"))
# specify angular positions of sensors on robot's body
sensor_angles = [2*math.pi/8, -2*math.pi/8, math.pi/4 - 0.3, -(math.pi/4 - 0.3)]

# construct Robot
robot = Robot(x=x, y=y, theta=0, controller=controller, sensors=sensors, sensor_angles=sensor_angles, light=LightSource(x=x, y=y, model='linear'))

# put robot into list of agents for Simulator
agents=[robot]

#########################################################################
#                    Set up experimental conditions                     #
#########################################################################

# nothing to set up this time, but we will still need a list of disturbances, even if it is empty
disturbances = []

#########################################################################
#                      Set up and run simulation                        #
#########################################################################

# get Simulator object - note that agents, environmental systems, and disturbances are all passed to its constructor
sim = Simulator(agents=agents, envs=yellow_light_sources+red_light_sources, duration=duration, dt=0.1, disturbances=disturbances)
# get SimulationRunner object
sim_runner = SimulationRunner(sim, animate=animate, pause_ani=True, animation_delay=animation_frame_delay, screen_width=screen_width)
# use SimulationRunner to run Simulation n number of times
sim_data = sim_runner.run_sims(n=1)

#########################################################################
#                     Plotting and analysis section                     #
#########################################################################

# plot agents' trajectories
ax = plot_all_sims_trajectories(sim_data, show_cbar=True, cbar_fig=False)
# draw all light sources
for light in yellow_light_sources+red_light_sources:
    light.draw(ax)
# draw robot
robot.draw(ax)

if plot_data:
    # plot robots' basic data (plots of robot's various noisemakers are not produced by this function call)
    plot_all_robots_basic_data(sim_data, multiple_plots=False, show_motors=True, show_controllers=True, show_sensors=True)

plt.show()
