# Lab 1 reflections

In lab 1, we saw how a relatively simple controller (a very small neural network) can lead to very different behaviours *in the sensorimotor loop*, depending on how we set its parameters. The neural network itself is incredibly simple, but when it is embedded in a closed loop, with nonlinear interactions between the robot's body and the environment, can still lead to some interesting behaviours. 

My parameters for the different behaviours are here:

[aggressor_params.yaml](https://canvas.sussex.ac.uk/courses/34985/files/6084036?wrap=1)[Download aggressor_params.yaml](https://canvas.sussex.ac.uk/courses/34985/files/6084036/download?download_frd=1)

[coward_params.yaml](https://canvas.sussex.ac.uk/courses/34985/files/6084033?wrap=1)[Download coward_params.yaml](https://canvas.sussex.ac.uk/courses/34985/files/6084033/download?download_frd=1)

[lover_params.yaml](https://canvas.sussex.ac.uk/courses/34985/files/6084034?wrap=1)[Download lover_params.yaml](https://canvas.sussex.ac.uk/courses/34985/files/6084034/download?download_frd=1)

[monocular_params.yaml](https://canvas.sussex.ac.uk/courses/34985/files/6084035?wrap=1)[Download monocular_params.yaml](https://canvas.sussex.ac.uk/courses/34985/files/6084035/download?download_frd=1)

For the relatively simple sensorimotor behaviours we wanted our robots to achieve, and the relatively simple environment the robots operate in, it is often best to keep our controllers as simple as possible - it is the closing of the sensorimotor loop that makes these controllers able to handle *a certain amount* of variation in initial conditions, and disturbances in the form of noise. If you experimented with noise, then you probably found that some types of noise (e.g. white noise, which averages to 0, over a long enough period of time) are easier for a closed-loop system to tolerate and react to than others. What you didn't see in this lab is that, in *Sandbox,* we can have a lot of control over the scale of each type of noise, as well as what in the simulation noise affects, and when.

Finally, I will add that once the parameters of the robot's controller are set, its behaviour is purely reflexive or reactive - it is not *self*-adaptive. However, the fact that it has parameters which affect its behaviour means that it has the *potential* to be adapt*ed*, by external agents or processes - when we change its parameters to achieve a behaviour, *we* are adapt*ing* it to that task.

I asked you to consider the phase portrait that the code plotted - phase portraits will feature more in later lectures and at least one more lab. They are very important and useful in the analysis of dynamical systems, and can often help us to detect patterns in a system's behaviour. If you studied the phase portraits carefully for different vehicles, then you may have noticed a surprising consistency - from a certain point of view, *aggressors* (light seekers) and *cowards* (light avoiders) both do the same thing - move in such a way as to equalise the signals coming from their light sensors. When the signals are equalised,  , and this is a stable equilibrium for both *aggressors* and *cowards*. If you added high levels of noise to the simulation, then the equilibrium may have become unstable, as a sufficiently high force will be able to push any system away from its equilibrium points (if you think back to the example of the ball on surface with hills and valleys, then even when a ball is in a valley, a hard enough kick may send it high enough in the air to escape the valley altogether). 





# Reflections on Lab 3

### Lab 3 part 1

#### The number of units

Because the units in the simulated Homeostat are fully connected, as the number of units is increased, there are two effects that impact upon the system's performance:

1. The complexity of the dynamics of the system increases rapidly, due to the growing number of feedback loops in the system.
2. The number of dimensions in the complete search space of the Homeostat rises geometrically, as the number of weights is the square of the number of units. 

Due to these combined effects, you probably found - if you were using my simple example `adapt_fun `functions - that with 4 units it is already not guaranteed that the system will find its way to viability in a short space of time. For more than 4 units, it is likely that good results will be rare - in theory, even with random search the system *can* find a good set of parameters, which will restore viability, but on average this will take longer than we want to wait for.

#### Hard and soft constraints

If the hard limits for the Homeostat unit essential variables (the values) are set to be quite close to the region of viability, then we might expect it to be easier for the system to find its way back to the viable region whenever it is in a non-viable state. These limits can be interpreted as a hard constraint, and one which can be used to make the essential variables much easier to control, or *regulate*. In real systems, it will often be impossible to set hard constraints so conveniently for our systems as we can in the simulated Homeostat. On the other hand, if there are hard physical constraints *inside* the region of viability, the problem of regulating the essential variables becomes more difficult.

If we increase the damping parameter for the Homeostat units to a large number, then we will find that the system tends to stabilise very quickly after a disturbance. At first glance, this might seem to be a good thing. However, we need to think carefully about why this happens, and what its significance might be.

There is one trivial way for the system to find stability very easily - simply set all of the weights to 0! However, weights of 0 are functionally equivalent to disconnection, and the stable point in the system dynamics that this leads to is the metaphoric death of the system - from here it does nothing and responds to nothing. The Homeostat is a very abstract system, so we have to think about what it might be an analogy for, or model of. If we think of it as being like a small nervous system (this is not the only kind of ultrastable system we could think about here, but just the most obvious one), then it is clear that a functionally disconnected and non-responsive network is of no use at all.  

The effect of making the damping parameter is somewhat similar to the above - as damping is a kind of resistance to change, increasing it makes the system less responsive to change, and therefore may increase the stability of the system, but in a trivial way. We can think of damping as a kind of soft physical constraint - damping constrains how quickly the system's variables can change, but in a varying way that is proportionate to how quickly they are already changing.

#### Choices

For some systems, the more parameters we have for adjusting/adapting the systems' behaviours, the more routes (or the more *choices*) we have to success. However, for any kind of search algorithm (e.g. random or evolutionary) increasing the number of parameters increases the dimensionality of the search space, and so makes the search slower. For our simulated Homeostat, the situation is worse than that - as noted above, the number of parameters only increases as the complexity of the system is increased.

The `random_selector `function is the closest of my example `adapt_fun `functions to the way that Ashby's Homeostat actually worked. Like Ashby's machine, this function randomly *chooses* from discrete sets of parameters. When we use `random_selector`, the `weights_set_size `parameter in `params.yaml` determines the number of choices available to the system. If the number of parameters in the system is , and there are choices for each parameter, then the number of different combinations of parameters for the whole system is . However, even though this is a very large number of combinations, the number of actual values that can be used for each parameter is still only . For example, if we set to 2 for a 4-unit Homeostat then every parameter can only be set to either -1 or 1, and even though there are 65536 combinations of parameter values for the whole system, it is unlikely that weights with only these two values will lead to good results. I have not actually investigated this, but I expect that there will be an optimal value for (which may vary for different sizes of system), where the system has a sufficient number of choices, without making the dimensionality of the search space too high and therefore slowing the search down.

### Waiting for stability

Like Ashby's real Homeostat machine, my simulated one normally waits for some interval of time after changing its parameters, to see if the new parameters lead the system back to viability and stability. For a dynamical system, this makes sense - the essential variables won't simply jump to exactly where we want them every time we update the system's parameters - there will be some period of movement towards viability before the system stabilises. 

In my simulation, we can set how long the system waits to see if the most recently selected parameters lead to stability using the `time_interval `parameter. If we make this parameter too large, then the system spends too long waiting between parameter changes, which slows down the search, and the overall time to adapt may be very high. In most systems, I would also expect there to be `time_interval `values which are too small - if the system is not given long enough to find stability between parameter changes, then perhaps it will never stabilise. However, with my simulated Homeostat we have found that having `time_interval `of 0 leads to good results! Why might this be? I have not yet had time to fully investigate this, but my best *hypothesis* is based on the realisation that as the weights are randomly varied, their average values are 0. The system cannot respond quickly enough to be affected by parameter changes in every simulation step (a bit like a low-pass filter, it will smooth their effects out), and so it responds more to their average values, which are all 0. As long as the weights are changing so quickly, the system will move towards its natural stable point, with all values being equal to 0, and from there it will be easier to find parameters which lead to stability. To reiterate, this is only a hypothesis, which is yet to be properly tested - testing hypotheses like this could form part of a good coursework project.

### Lab 3 part 2

![disturbing2](C:\Users\zh826\Desktop\AS_lab\disturbing2.png)

**Figure 1. A minimal case of adapting to disturbances. By the end of the simulation, Unit 1 has found parameters which allow it to be both viable \*and\* responsive to disturbances.**

What we see in **Figure 1** is one of the simplest possible cases of a system successfully adapting to disturbances. The essential variable of Unit 0 is being driven by a `SquareWaveDisturbanceSource `in and out of the region of viability. This causes Unit 0 to keep searching for weights (i.e. parameters) which will allow it to return to viability, as it does when the disturbance is inactive from t~=475 to t~=725. Because Unit 1 is coupled to Unit 0, when Unit 0 is disturbed, the effect will tend to propagate (or be transferred) to Unit 1, and that is exactly what we see early in the simulation. The interesting thing happens at t~=775, where Unit 1 finds a set of parameters which allow it to remain responsive to the disturbance it receives from Unit 0, but *within its region of viability at the same time*.

### Parameter sweeps

On the lab page, I gave an example of a parameter sweep which only gave good results when a sufficiently large number of runs was used. We won't necessarily know in advance what a sufficiently large number is, although as we become more experienced in these techniques we may be able to make good (informed) guesses. 

#### Why multiple runs?

Firstly, because I could tell in class that I hadn't made this clear enough before, I will reiterate why we should run a simulation multiple times for any experiment which involves one or more sources of randomness. In **Figure 2**, I show how the state of a 4-unit Homestat varied over time in 2 consecutive runs of the simulation. I didn't change any parameters of the simulation between these two runs, but I got very different results, one bad and one good. So is the system bad or good? Actually, this is the wrong question, because what we really need to know is how often and how quickly, on average, does the system actually find viability in the given simulated time. We can quantitatively evaluate the performance of the system in various ways, e.g. by how long it spends in a non-viable state, or by how much of the time it spends changing its weights. For both of these measures, it is easy to shift perspective and instead look at how much of the time the system spends in a viable state, as we just subtract the non-viable time from the total simulated time.

I tell students about this every year, and every year I still see coursework project reports where students only show me a few graphs of individual results and no quantitative analyses, and then go on to say how marvellous and successful their algorithms/systems were. It is impossible for me to entirely believe what they have written when I know very well that even a system which performs poorly on average will occasionally produce a result which looks very nice. If you want a really good mark for a project report, you must quantify the performance of your systems, and not only qualitatively analyse your favourite graphs - qualitative analyses are always useful, but should be backed up by quantitative ones, especially where randomness is involved.

| ![4units_run4](C:\Users\zh826\Desktop\AS_lab\4units_run4.png) | ![4units_run5](C:\Users\zh826\Desktop\AS_lab\4units_run5.png) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
|                                                              |                                                              |

**Figure 2.** **Because the Homeostat uses a random search for good parameters, every time we run the simulation we will see different results.**

#### How many runs, and how many different parameter values?

| ![k5vals3runs](C:\Users\zh826\Desktop\AS_lab\k5vals3runs.png) | ![k10vals5runs](C:\Users\zh826\Desktop\AS_lab\k10vals5runs.png) | ![k40vals](C:\Users\zh826\Desktop\AS_lab\k40vals.png) |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ----------------------------------------------------- |
|                                                              |                                                              |                                                       |

**Figure 3. For some systems, the results of a parameter sweep will be less affected by the number of runs per parameter value than by the number of parameter values tested.** 

In **Figure 3**, I include some results of a parameter sweep over the damping parameter. As mentioned above, a damper has a filtering effect, and so effect of the randomness in the way the Homeostat changes its weights is increasingly smoothed in the states of the system as the damping is increased. For this reason, even when I only used 2 runs per parameter value, as in the right-hand plot in **Figure 3**, the general trend in the plot is still clear, even though the curve is a little rough. Therefore only 5 runs per value, or even 10, will probably be sufficient for this analysis. However, as will normally be the case, the number of different parameter values I sweep over will have a large effect on the results - in the left-hand plot in **Figure 3** I have only used 5 different damping values, and as a result the plot gives the incorrect impression that the curve declines more gradually than is really the case. 

### Lab 3 part 3

If you completed this part of the lab, then you should have seen that it is the feedback weight, , which determines the shape of the field for unit 0. If the weight is negative, then the lines of behaviour for the system will spiral inwards towards a fixed point. If the feedback weight is positive, then the system is inherently unstable, as we might expect. , on the other hand, has the effect of shifting the lines of behaviour (or field) to the left or the right, like the bias in a neural network.

Is that all? Not quite, because we should remember that not all stable points are viable ones - for example, if you locked me in a freezer at 0 degrees C, then my temperature may stabilise, but not at a value which supports my continued existence. Similarly, as illustrated in **Figure 4**, we can distinguish between stability and stable viability for the Homeostat.

![unstable_because_nonviable](C:\Users\zh826\Desktop\AS_lab\unstable_because_nonviable.png)

**Figure 4. Although the field in this plot would appear to be stable, because the fixed point attractor the lines of behaviour spiral in towards is outside of the region of viability (red lines), the Homeostat will not stabilise here - instead, it will change its parameters until it finds a stable point inside the region of viability.**

 

 