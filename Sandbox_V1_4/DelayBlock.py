class DelayBlock:
    """
        A class which implements a delay to a signal, currently only used in :class:`Sensor` classes. The class uses a buffer to store delayed signal values.
    """
    def __init__(self, delay_n: int):
        """
            __init__(self, delay_n: int)

            :param delay_n: the number of simulation steps a signal will be delayed for.
            :type delay_n: int
        """
        # allow a delay of 0, but not negative delays, which make no sense
        assert delay_n >= 0, "delay_n must be >= 0. Negative time delays make no sense here."
        # set the number of steps that the block will delay a signal for
        self.delay_n = delay_n
        # set up the delayed signal vector
        self.sig = [0] * delay_n
        # we will keep a record of the outputs from the delay block for plotting later
        self.outputs = [0]

        if delay_n > 0:
            # set up the current index for inputs
            self.input_index = 0
            # set up the current index for outputs
            self.output_index = self.delay_n-1

    def step(self, input):
        """
            Step the delayed signal forwards. Every time the delay block is stepped, the new input is placed in the buffer, and the oldest one is returned as the delayed value.

            :param input: The current signal value
            :type input: any

            :return: The delayed signal value
            :rtype: any
        """
        # default output for a zero-delay block
        output = input
        if self.delay_n > 0:
            # add the new input to the delay block
            self.sig[self.input_index] = input
            # increment the input index for the next input, and use the modulo operator to "wrap round"
            self.input_index = (self.input_index + 1) % self.delay_n
            # increment the input index for the next output, and use the modulo operator to "wrap round"
            self.output_index = (self.input_index + self.delay_n) % self.delay_n
            # set the output to the delayed output
            output = self.sig[self.output_index]
        # add the output to the record
        self.outputs.append(output)
        # return the output
        return output
