from .Sensor import *

class BumpSensor(Sensor):

    def __init__(self, p_noise=0, name_str: str='BumpSensor', delay_steps: float=0):

        super().__init__(name_str=name_str, delay_steps=delay_steps)
        self.activation = False
        self.activations = [self.activation]
        self.p_noise = p_noise

    def step(self, dt):
        super().step(dt)

        if np.random.random() < self.p_noise:
            self.activation = not self.activation

        r = self.update(dt)

        self.activation = False

    def register_bump(self):

        self.activation = True

    # A method to get the sensor's data, in the form of a dict.
    def get_data(self) -> dict:
        """
            A function to get the data from a :class:`CompassSensor`, in the form of a string-keyed dict.

            These data, as and when they are included in the returned dict, can be accessed with the following keys:

            * data inherited from :class:`Sensor`: see :class:`Sensor`
            * data of sensor's noise source, if it has one: ``data["noises"]``
            * history of sensor outputs (activations): ``data["activations"]``

            :return: The sensors's data.
            :rtype: dict
        """
        data = super().get_data()
        data["activations"] = self.activations
        data["noises"] =  None
        if self.noisemaker:
            data["noises"] = self.noisemaker.get_data()["noises"]
        return data

    def reset(self):
        """
            A method to reset the sensor to its initial state, so that it can be reused in a later simulation.
        """
        super().reset()
        self.activation = self.activations[0]
        self.activations = [self.activation]
        if self.noisemaker:
            self.noisemaker.reset()
