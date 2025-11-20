class FeedbackController:
    """
    This class represents a PID controller. It can be used as a simple proportional controller, if only the proportional gain is set to a non-zero value. It can also be used as a PD or a PI controller, if the integral gain or derivative gain, respectively, is set to zero. The equation for the controller is as follows:

    .. math:: c(t) = K_p e(t) + K_i \int_{0}^{t} e(\\tau) \,d \\tau + K_d \\frac{de(t)}{dt}.

    As time is discretised in *Sandbox*, in the implementation :math:`\Delta t` replaces :math:`dt`, and the integral becomes a summation of errors divided by :math:`\Delta t`.
    """

    def __init__(self, p_gain, d_gain=0, i_gain=0, sensor=None, ref_value=None):
        """

        __init__(self, p_gain, d_gain=0, i_gain=0, sensor=None, ref_value=None)

        :param p_gain: The proportional gain factor, :math:`K_p`.
        :type p_gain: float

        :param i_gain: The integral gain factor, :math:`K_i`. Because past errors are integrated, having this term can allow a controller to eliminate steady-state errors, but can also be a source of instabliity if not used carefully.
        :type i_gain: float

        :param d_gain: The derivative gain factor, :math:`K_d`. Having this term can help to prevent, or minimise, overshoot, as the rate of change of the error has predictive value.
        :type d_gain: float

        :param sensor: The sensor attached to the controller for measuring the controlled variable. Defaults to ``None``, meaning that no sensor is attached. If there is no sensor, then the value of the controlled variable must be passed into the controller's ``step`` method, using the ``sensor_sig`` parameter, every time it is updated.
        :type sensor: :class:`Sensor`

        :param ref_value: If the controller will have a constant reference value, then it an be set here. If the reference value will change, then the reference variable must be passed into the controller's ``step`` method, using the `ref_sig`` parameter, every time it is updated. Defaults to ``None``, meaning that no reference value is specified other than that passed to the step method.
        :type ref_value: float

        """
        self.sensor = sensor
        self.ref_value = ref_value
        self.control_sig = 0
        self.control_sigs = [self.control_sig]  # keep history of controller reference values
        self.p_gain = p_gain
        self.d_gain = d_gain
        self.i_gain = i_gain
        self.errors = [0]  # keep history of errors. 0 is not really right ...
        self.i_error = 0  # integral of error
        self.i_errors = [0]  # keep history of error integral
        self.d_errors = [0]  # keep history of error derivatives

    def step(self, dt, sensor_sig=None, ref_sig=None):
        """

        :param dt: The simulation time step duration.
        :type dt: float

        :param sensor_sig: The sensor signal input, for the controlled variable, if there is one. Defaults to ``None``. If both the ``Sensor`` set in ``__init__`` and this value are None, then the controller will simply output ``0``, and no control values or errors will be recorded internally. If a sensor was previously added to measure the controlled variable, then a value passed for this parameter will override it.
        :type sensor_sig: float

        :param ref_sig: The reference signal input, if there is one. Defaults to ``None``. If both the constant reference value set in ``__init__`` and this value are None, then the controller will simply output ``0``, and no control values or errors will be recorded internally. If a constant reference value was previously set, then a value passed for this parameter will override it.
        :type ref_sig: float
        """
        # a reference signal can be passed in to this method in every
        # simulation step
        # - if a signal is input, then it will override the reference
        #   value set earlier
        # - if not, and a reference value was set in __init__, that will be used
        # - otherwise, there is no reference signal to track, and so this method
        #   will simply return zero
        ref = ref_sig
        if ref is None:
            if self.ref_value is not None:
                ref = self.ref_value
            else:
                return 0

        # the controller can either use its own sensor, set in __init__,
        # or it can have a sensory signal passed in to this method in every
        # simulation step
        # - if a sensor signal is input, then it will override the controller's
        # 	sensor
        # - if not, and a sensor was set in __init__, then that sensor will be used
        # - otherwise, there is no sensor signal to compare to the reference, and
        #   so this method will simply return zero
        if sensor_sig is None:
            if self.sensor is not None:
                sensor_sig = self.sensor.step(dt)
            else:
                return 0

        # calculate error
        error = ref - sensor_sig
        # store record of error
        self.errors.append(error)
        # calculate control output
        self.i_error += error * dt
        self.i_errors.append(self.i_error)
        d_error = 0
        if len(self.errors) >= 0:
            d_error = (self.errors[-1] - self.errors[-2]) / dt
        self.d_errors.append(d_error)
        self.control = (
            (self.p_gain * error)
            + (self.d_gain * d_error)
            + (self.i_gain * self.i_error)
        )
        # store record of control output
        self.control_sigs.append(self.control)

        # return control output
        return self.control
