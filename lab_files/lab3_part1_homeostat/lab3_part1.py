# import packages
import sys
import yaml

# import Sandbox
sys.path.insert(1, '../../') # relative path to folder which contains the Sandbox module
from Sandbox_V1_4 import *

# import local files
from Homeostat import *

def main():

    #########################################################################
    #                        Read parameter file                            #
    #########################################################################

    # read parameters from file
    with open('params.yaml', 'r') as file:
        params_dict = yaml.safe_load(file)

    n_units = params_dict["n_units"]
    upper_limit = params_dict["upper_limit"]
    lower_limit = params_dict["lower_limit"]
    upper_viability = params_dict["upper_viability"]
    lower_viability = params_dict["lower_viability"]
    adapt_fun = params_dict["adapt_fun"]
    adapt_enabled = True if params_dict["adapt_enabled"] == 1 else False
    test_interval = params_dict["test_interval"]
    weights_set_size = params_dict["weights_set_size"]
    show_legends = True if params_dict["show_legends"] == 1 else False

    if weights_set_size == 0:
        weights_set = None
    else:
        weights_set = np.linspace(-1, 1, num=weights_set_size)

    if adapt_fun == "random_val":
        adapt_fun = random_val
    elif adapt_fun == "random_creeper":
        adapt_fun = random_creeper
    elif adapt_fun == "random_selector":
        adapt_fun = random_selector
    else:
        assert False, "please check your adapt_fun name in params.yaml!"

    # simulation parameters
    duration = params_dict["duration"]

    #########################################################################
    #                           Set up agents                               #
    #########################################################################

    homie = Homeostat(n_units=n_units, upper_viability=upper_viability, lower_viability=lower_viability, upper_limit=upper_limit, lower_limit=lower_limit, adapt_fun=adapt_fun, adapt_enabled=adapt_enabled, test_interval=test_interval, weights_set=weights_set)

    # # uncomment these lines if you want to see what happens
    # # when there is no damping in the system
    # for unit in homie.units:
    #     unit.k = 0

    # # uncomment these lines if to randomise the parameters of the
    # # equations of motion for the units
    # for u in homie.units:
    #     u.randomise_params()

    #########################################################################
    #                      Set up and run simulation                        #
    #########################################################################

    # set up simulation time variables
    t = 0
    ts = [t]
    dt = 0.01

    while t < duration:
        # unit.step(dt)
        homie.step(dt)
        t += dt
        ts.append(t)

    #########################################################################
    #                     Plotting and analysis section                     #
    #########################################################################

    # PLOT 1: plot system state over time, showing when weights change
    plt.figure()
    for i, unit in enumerate(homie.units):
        plt.plot(ts, unit.thetas, label='Unit '+str(i))

    # plot upper and lower viability boundaries
    plt.plot([ts[0], ts[-1]],[homie.units[0].upper_viability, homie.units[0].upper_viability], 'r--', label='Viability boundaries')
    plt.plot([ts[0], ts[-1]],[homie.units[0].lower_viability, homie.units[0].lower_viability], 'r--')

    # plot upper and lower hard limits
    plt.plot([ts[0], ts[-1]],[homie.units[0].upper_limit, homie.units[0].upper_limit], 'g--', label='Hard limits')
    plt.plot([ts[0], ts[-1]],[homie.units[0].lower_limit, homie.units[0].lower_limit], 'g--')

    # plot times when units start testing new weights
    for i, t_t in enumerate(homie.units[0].test_times):
        if i:
            l = None
        else:
            l = 'Weights begin to change'
        plt.plot([t_t, t_t], [homie.units[0].lower_limit, homie.units[0].upper_limit], 'b--', label=l, linewidth=3)

    plt.xlabel('t')
    plt.ylabel(r'$\theta$')
    if show_legends: plt.legend()
    plt.title("System state over time")

    # PLOT 2: plot system state over time, *without* showing when weights change
    plt.figure()
    for i, unit in enumerate(homie.units):
        plt.plot(ts, unit.thetas, label='Unit ' + str(i))

    # plot upper and lower hard limits
    plt.plot([ts[0], ts[-1]],[homie.units[0].upper_viability, homie.units[0].upper_viability], 'r--', label='Viability boundaries')
    plt.plot([ts[0], ts[-1]],[homie.units[0].lower_viability, homie.units[0].lower_viability], 'r--')

    # plot upper and lower hard limits
    plt.plot([ts[0], ts[-1]],[homie.units[0].upper_limit, homie.units[0].upper_limit], 'g--', label='Hard limits')
    plt.plot([ts[0], ts[-1]],[homie.units[0].lower_limit, homie.units[0].lower_limit], 'g--')

    plt.xlabel('t')
    plt.ylabel(r'$\theta$')
    if show_legends: plt.legend()
    plt.title("System state over time")

    # PLOT 3: plot all Homeostat unit weights over time
    plt.figure()
    for i, unit in enumerate(homie.units):
        plt.plot(ts, unit.weights_hist, label='Unit ' + str(i) + ': weight')
    plt.title('Homeostat unit weights')
    plt.xlabel('t')
    plt.ylabel('Weights')
    if show_legends: plt.legend()

    # PLOT 4: plot when all Homeostat units are adapting
    plt.figure()
    for i, unit in enumerate(homie.units):
        plt.plot(ts, unit.testing_hist, label='Unit ' + str(i))
    plt.xlabel('t')
    plt.ylabel('Adapting (new weights are being tested)')
    plt.title('Units in process of adapting (searching for a stable field)')
    if show_legends: plt.legend()

    min_theta_dots = 1E6
    max_theta_dots = -1E6
    for unit in homie.units:
        min_theta_dots = min([min_theta_dots, min(unit.theta_dots)])
        max_theta_dots = max([max_theta_dots, max(unit.theta_dots)])

    # PLOT 5: plot phase portraits
    plt.figure()
    for i, unit in enumerate(homie.units):
        plt.plot(unit.thetas, unit.theta_dots, label='Unit ' + str(i))
        plt.plot(unit.thetas[-1], unit.theta_dots[-1], 'ko')
    plt.plot([homie.units[0].lower_viability, homie.units[0].lower_viability], [min_theta_dots, max_theta_dots], 'r--')
    plt.plot([homie.units[0].upper_viability, homie.units[0].upper_viability], [min_theta_dots, max_theta_dots], 'r--')
    plt.xlabel(r'$\theta$')
    plt.ylabel(r'$\dot{\theta}$')
    plt.title(r'Unit $\theta$ phase portraits')

    n_steps = len(homie.units[0].testing_hist)
    stable_ind = -1
    for i in range(n_steps):
        ind = n_steps-i-1
        stable = True
        for unit in homie.units:
            stable = stable and not unit.testing_hist[ind]
        if stable:
            stable_ind = ind
        else:
            break

    max_len = 2000
    end_ind = n_steps-1
    if stable_ind != -1:
        end_ind = stable_ind
    start_ind = end_ind - (max_len-1)
    if start_ind < 0: start_ind = 0
        
    min_theta_dots = 1E6
    max_theta_dots = -1E6
    for unit in homie.units:
        min_theta_dots = min([min_theta_dots, min(unit.theta_dots[start_ind:end_ind+1])])
        max_theta_dots = max([max_theta_dots, max(unit.theta_dots[start_ind:end_ind+1])])

    # PLOT 6: plot phase portraits
    # in the previous plot, which shows the phase prtraits over the whole simulation, it is sometimes 
    #   difficult to see anything clearly
    # in this plot, we see either just the last part of the simulation, or the steps which led to the 
    #   simulation reaching stability
    plt.figure()
    for i, unit in enumerate(homie.units):
        plt.plot(unit.thetas[start_ind:end_ind+1], unit.theta_dots[start_ind:end_ind+1], label='Unit ' + str(i))
        plt.plot(unit.thetas[end_ind], unit.theta_dots[end_ind], 'ko')
    plt.plot([homie.units[0].lower_viability, homie.units[0].lower_viability], [min_theta_dots, max_theta_dots], 'r--')
    plt.plot([homie.units[0].upper_viability, homie.units[0].upper_viability], [min_theta_dots, max_theta_dots], 'r--')
    plt.xlabel(r'$\theta$')
    plt.ylabel(r'$\dot{\theta}$')
    plt.title(r'Unit $\theta$ phase portraits: end of simulation or move to stability')

    plt.show()

if __name__ == '__main__':
    main()
