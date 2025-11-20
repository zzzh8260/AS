from .base import *
from .System import *
from .pygame_functions import *

class FloorPatch(System):
	"""
        A class to represent a rectangular coloured patch on the ground.
	"""
	def __init__(self, x_left: float, x_right: float, y_top: float, y_bottom: float, colour: str='grey', label: str='grey'):
		"""
			__init__(self, x_left: float, x_right: float, y_top: float, y_bottom: float, colour: str='grey', label: str='grey')

			:param x_left: The left edge x-coordinate of the patch.
			:type x_left: float

			:param x_right: The right edge x-coordinate of the patch.
			:type x_right: float

			:param y_top: The top edge y-coordinate of the patch.
			:type y_top: float

			:param y_bottom: The bottom edge y-coordinate of the patch.
			:type y_bottom: float

			:param colour: The colour of the patch, for drawing.
			:type colour: str

			:param label: The label of the patch. Only sensors with the same label, or ``None`` as their label, can potentially detect this patch.
			:type label: str
		"""
		# call System constructor
		super().__init__(x=0, y=0, theta=None)

		self.x_left = x_left
		self.x_right = x_right
		self.y_top = y_top
		self.y_bottom = y_bottom
		self.colour = colour
		self.label = label

	def is_in(self, x: float, y: float) -> bool:
		"""
			A method to determine whether the passed in coordiante lies within the patch. Used for sensing.

			:param x: The x-coordinate to check (e.g. of a sensor)
			:type x: float

			:param y: The y-coordinate to check (e.g. of a sensor)
			:type y: float
		"""
		return x < self.x_right and x > self.x_left and y < self.y_top and y > self.y_bottom

	def draw(self, ax) -> None:
		"""
			A method to draw a :class:`FloorPatch` on Matplotlib axes.

			:param ax: The Matplotlib axes to draw the Arena on.
			:type ax: Matplotlib axes
		"""
		ax.add_artist(mpatches.Rectangle((self.x_left, self.y_bottom), width=self.x_right-self.x_left, height=self.y_top-self.y_bottom, color=self.colour))

	def pygame_draw(self, screen, scale: float, shiftx: float, shifty: float):
		"""
			A method for drawing a :class:`FloorPatch` on a PyGame display.

			:param screen: The PyGame display to draw on.
			:type screen: PyGame display

			:param scale: The scale to draw at.
			:type scale: float

			:param shiftx: The offset from centre in the x-axis for drawing.
			:type shiftx: float

			:param shifty: The offset from centre in the y-axis for drawing.
			:type shifty: float
		"""
		pygame_drawrectangle(screen, shiftx, shifty, scale, self.x_left, self.x_right, self.y_top, self.y_bottom, self.colour)

class CircularFloorPatch(FloorPatch):
	"""
        A class to represent a circular coloured patch on the ground.
	"""
	def __init__(self, x: float, y: float, radius: float, colour: str='grey', label: str='grey'):
		"""
			:param x: The x-coordinate of the patch's centre.
			:type x: float

			:param y: The y-coordinate of the patch's centre.
			:type y: float

			:param radius: The radius of the patch.
			:type radius: float

			:param colour: The colour of the patch, for drawing.
			:type colour: str

			:param label: The label of the patch. Only sensors with the same label, or ``None`` as their label, can potentially detect this patch.
			:type label: str
		"""
		# call System constructor
		System.__init__(self, x=0, y=0, theta=None)

		self.x = x
		self.y = y
		self.radius = radius
		self.colour = colour
		self.label = label

	def is_in(self, x: float, y: float) -> bool:
		"""
			A method to determine whether the passed in coordiante lies within the patch. Used for sensing.

			:param x: The x-coordinate to check (e.g. of a sensor)
			:type x: float

			:param y: The y-coordinate to check (e.g. of a sensor)
			:type y: float
		"""
		dist = math.sqrt((x-self.x)**2 + (y-self.y)**2)
		return dist < self.radius

	def draw(self, ax) -> None:
		"""
			A method to draw a :class:`CircularFloorPatch` on Matplotlib axes.

			:param ax: The Matplotlib axes to draw the Arena on.
			:type ax: Matplotlib axes
		"""
		ax.add_artist(mpatches.Circle((self.x, self.y), self.radius, color=self.colour))

	def pygame_draw(self, screen, scale: float, shiftx: float, shifty: float):
		"""
			A method for drawing a :class:`CircularFloorPatch` on a PyGame display.

			:param screen: The PyGame display to draw on.
			:type screen: PyGame display

			:param scale: The scale to draw at.
			:type scale: float

			:param shiftx: The offset from centre in the x-axis for drawing.
			:type shiftx: float

			:param shifty: The offset from centre in the y-axis for drawing.
			:type shifty: float
		"""
		pygame_drawcircle(screen, shiftx, shifty, scale, self.x, self.y, self.radius, self.colour)
