from .Agent import *

class AgentCollisionManager(System):

	def __init__(self, agents):

		self.agents = agents

		super().__init__()


	def step(self, dt):

		bumps = False
		max_attempts = 10
		attempts = 0
		while not bumps and attempts < max_attempts:
			bumps = False
			np.random.shuffle(self.agents)
			for a in self.agents:
				for a2 in self.agents:
					if a != a2:
						delta_x = a.x - a2.x
						delta_y = a.y - a2.y
						dist = math.sqrt((delta_x ** 2) + (delta_y ** 2))
						sep = dist - (a.radius + a2.radius)
						if sep < 0:
							angle = math.atan2(delta_y, delta_x)
							d = abs(sep/2) + 0.01 # add a small gap, so agents will not be touching
							a.push(a.x + d*math.cos(angle), a.y + d*math.sin(angle))
							a.register_bump()
							a2.push(a2.x + -d*math.cos(angle), a2.y + -d*math.sin(angle))
							a2.register_bump()
							bumps = True
							# print("bump between", a.get_data()["classname"], "[", a.x, ",", a.y, "]", "and", a2.get_data()["classname"], "[", a2.x, ",", a2.y, "]")
			attempts += 1

	def pygame_draw(self, screen, scale: float, shiftx: float, shifty: float):
		pass
