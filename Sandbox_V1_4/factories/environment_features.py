from ..base import *
from ..stimuli import *

# generate a circular arrangement of light sources
def sources_circle(n=20, r=9, x=0, y=0, brightness=1, label: str=None, colour='yellow'):
    '''
        A function to generate a circular arrangment of ``n`` lights, with radius ``r``.
        See :class:`Sandbox_V1_3.LightSource` for explanations of the light properties ``brightness``, ``label`` and ``color``.
    '''
    sources = []
    for i in range(n):
        a = i * 2*np.pi / n
        sources.append(LightSource(x + r * np.cos(a), y + r * np.sin(a), label=label, colour=colour, brightness=brightness))
    return sources

# generate a circular arrangement of light sources
def sources_ellipse(n=20, a=9, b=12, x=0, y=0, brightness=1, label: str=None, colour='yellow'):
    '''
        A function to generate an elliptical arrangment of ``n`` lights, with width = 2a and height = 2b.
        See :class:`Sandbox_V1_3.LightSource` for explanations of the light properties ``brightness``, ``label`` and ``color``.
    '''
    sources = []
    for i in range(n):
        theta = i * 2*np.pi / n
        sources.append(LightSource(x + a * np.cos(theta), y + b * np.sin(theta), label=label, colour=colour, brightness=brightness))
    return sources

def sources_rectangle(x_n=10, y_n=10, x=0, y=0, width=20, height=20, brightness=1, label: str=None, colour='yellow'):
    '''
        A function to generate a rectangular arrangement of lights, with x_n lights in the x-axis and y_n lights in the y-axis.
        See :class:`Sandbox_V1_3.LightSource` for explanations of the light properties ``brightness``, ``label`` and ``color``.
    '''
    sources = []

    x_left = x - (width/2)
    x_right = x_left + width
    x_step = width / (x_n-1)

    y_bottom = y - (height/2)
    y_top = y_bottom + height
    y_step = height / (y_n-1)

    y_co = y_bottom
    for _ in range(y_n-2):
        y_co += y_step
        sources.append(LightSource(x_left, y_co, label=label, colour=colour, brightness=brightness))
        sources.append(LightSource(x_right, y_co, label=label, colour=colour, brightness=brightness))

    x_co = x_left
    for _ in range(x_n):
        sources.append(LightSource(x_co, y_bottom, label=label, colour=colour, brightness=brightness))
        sources.append(LightSource(x_co, y_top, label=label, colour=colour, brightness=brightness))
        x_co += x_step

    return sources

def sources_vertical_line(x, y_min, y_max, n, brightness=1, label: str=None, colour='yellow'):
    '''
        A function which generates ``n`` lights along the vertical line which connects the coordinates [x, y_min] and [x, y_max].
        See :class:`Sandbox_V1_3.LightSource` for explanations of the light properties ``brightness``, ``label`` and ``color``.
    '''
    return sources_line(x, y_min, x, y_max, n, brightness, label, colour)

def sources_horizontal_line(x_min, x_max, y, n, brightness=1, label: str=None, colour='yellow'):
    '''
        A function which generates ``n`` lights along the horizontal line which connects the coordinates [x_min, y] and [x_max, y].
        See :class:`Sandbox_V1_3.LightSource` for explanations of the light properties ``brightness``, ``label`` and ``color``.
    '''
    return sources_line(x_min, y, x_max, y, n, brightness, label, colour)

def sources_line(x1, y1, x2, y2, n, brightness=1, label: str=None, colour='yellow'):
    '''
        A function which generates ``n`` lights along the line which connects the coordinates [x1, y1] and [x2, y2].
        See :class:`Sandbox_V1_3.LightSource` for explanations of the light properties ``brightness``, ``label`` and ``color``.
    '''
    sources = []
    x_diff = x2 - x1
    y_diff = y2 - y1
    x_step = x_diff / (n - 1)
    y_step = y_diff / (n - 1)
    x_co = x1
    y_co = y1
    for i in range(n):
        sources.append(LightSource(x_co, y_co, label=label, colour=colour, brightness=brightness))
        x_co += x_step
        y_co += y_step

    return sources

def sources_arc(centre_x, centre_y, rad, theta1, theta2, n, brightness=1, label: str=None, colour='yellow'):
    sources = []
    theta_diff = theta2 - theta1
    theta_step = theta_diff / (n - 1)
    theta = theta1
    for i in range(n):
        x_co = centre_x + (rad * math.cos(theta))
        y_co = centre_y + (rad * math.sin(theta))
        print(x_co, y_co, theta, centre_x, centre_y)
        sources.append(LightSource(x_co, y_co, label=label, colour=colour, brightness=brightness))
        theta += theta_step

    return sources

def random_sources(x_min=-10, x_max=10, y_min=-10, y_max=10, brightness=1, n=20, colour='yellow', label='yellow'):
    '''
        A function which generates ``n`` lights at random coordinates in the rectangular region specifed by the x-interval [x_min, x_max] and the y-interval [y_min, y_max].
        See :class:`Sandbox_V1_3.LightSource` for explanations of the light properties ``brightness``, ``label`` and ``color``.
    '''
    sources = []
    for _ in range(n):
        x = random_in_interval(minimum=x_min, maximum=x_max)
        y = random_in_interval(minimum=y_min, maximum=y_max)
        sources.append(LightSource(x, y, colour=colour, label=label, brightness=brightness))

    return sources

# "perturbables" will probably be removed altogether, now that System can be perturbed...

# # generate a circular arrangement of light sources
# def perturbable_sources_circle(n=20, r=9, x=0, y=0, brightness=1, label: str=None, colour='yellow'):
#     sources = []
#     for i in range(n):
#         a = i * 2*np.pi / n
#         sources.append(PerturbableLightSource(x + r * np.cos(a), y + r * np.sin(a), label=label, colour=colour, brightness=brightness))
#     return sources
