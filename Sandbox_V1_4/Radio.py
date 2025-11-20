from .System import *
import random

class Radio(System):
	"""
        A class to implement a simple 2-way radio. A radio constantly transmits its message. It only receives messages from other radios which are within its own ``radios`` list. It has separate parameters for the range of its transmitter and of its receiver. Because this radio implements both transmitter and receiver, it appears under both actuators and sensors in this documentation.
	"""
	def __init__(self, x, y, transmitter_range, receiver_range, radios=[], enabled: bool=True):
		"""
            __init__(self, x, y, transmitter_range, receiver_range, radios=[], enabled: bool=True)

            :param x: The radio's x-coordinate. If the radio is attached to a robot (as in :class:`Fauxkilobot`), then it's position will track that of the robot.
            :type x: float

            :param y: The radio's y-coordinate. If the radio is attached to a robot (as in :class:`Fauxkilobot`), then it's position will track that of the robot.
            :type y: float

            :param transmitter_range: Only radios within ``transmitter_range`` of this radio will possibly receive its message.
            :type transmitter_range: float

            :param receiver_range: This radio will only possibly receive the transmission of radios within ``receiver_range`` of it.
            :type receiver_range: float

            :param radios: The list of radios which this one can potentially receive messages from. Defaults to ``[]`` - it will normally be more convenient to add radios to this list *after* construction, using the ``add_radio()`` method. For example, if you have :math:`n` agents which you want to all communicate with each other, it is probably going to be easiest to construct all of the robots first, and then subsequently connect all of their radios.
            :type radios: list(:class:`Radio`)

            :param enabled: A flag which can potentially be used to disable a radio. Not used in the current implementation, but will be in future.
            :type enabled: bool
		"""
		super().__init__(x=x, y=y)
		self.enabled = enabled
		self.radios = radios
		self.message = None
		self.received_messages = []
		self.transmitter_range = transmitter_range
		self.receiver_range = receiver_range

		self.initial_state = self.get_data()

	def add_radio(self, radio):
		"""
            Add a radio to the list of radios that this one can potentially communicate with.

            :param radio: The radio to add to the list.
            :type radio: :class:`Radio`
		"""
		self.radios.append(radio)

	def receive_messages(self):
		"""
            Receive messages from any in-range radios which this one can potentially communicate with.
		"""
		random.shuffle(self.radios)

		self.received_messages = []
		for radio in self.radios:
			dist = math.sqrt((self.x - radio.x) ** 2 + (self.y - radio.y) ** 2)
			if dist <= self.receiver_range and dist <= radio.transmitter_range:
				self.received_messages.append(radio.message)

	def reset(self, reset_controller: bool=True) -> None:
		"""
			This method resets a radios's state and simulation data to its initial values, so that it can be used again.

			:param reset_controller: ONLY LEFT HERE BY MISTAKE - NOT USED AND WILL BE REMOVED LATER.
			:type reset_controller: bool
		"""
		super().reset()
		self.message = self.initial_state["message"]
		self.received_messages = self.initial_state["received_messages"]
		self.enabled = self.initial_state["enabled"]
		self.radios = self.initial_state["radios"]
		self.receiver_range = self.initial_state["receiver_range"]
		self.transmitter_range = self.initial_state["transmitter_range"]

	def get_data(self):
		"""
            A function to get a radios's data.

            These data, as and when they are included in the returned dict, can be accessed with the following keys:

            * enabled state: ``data["enabled"]``
            * list of radios that this radio can potentially receive messages from: ``data["radios"]``
            * message that this radio is transmitting: ``data["message"]``
            * list of messages received in the last simulation step: ``data["received_messages"]``
            * transmitter range: ``data["transmitter_range"]``
            * receiver range: ``data["receiver_range"]``
		"""
		data = super().get_data()

		data["enabled"] = self.enabled
		data["radios"] = self.radios[:]
		data["message"] = self.message
		data["received_messages"] = self.received_messages[:]
		data["transmitter_range"] = self.transmitter_range
		data["receiver_range"] = self.receiver_range

		return data

	def set_message(self, message):
		"""
            Set the message which this radio will transmit.
		"""
		self.message = message
