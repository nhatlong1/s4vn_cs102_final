"""
Sprites for projectile motion
"""
import enum
from typing import Sequence, Tuple

import pymunk
import numpy as np

try:
    from projectile.includes.constants import WIDTH, HEIGHT
except ImportError:
    WIDTH, HEIGHT = 600, 600

#!: This file is a modified version of Circle and Box from this tutorial
#!: https://pymunk-tutorial.readthedocs.io/en/latest/mouse/mouse.html

# The class _ShapeDefinition is an enumeration of the shapes Line, Square, Rectangle,
# IsoscelesTriangle, and Trapezoid. Each shape is defined by a list of points
class _ShapeDefinition(enum.Enum):
    Line = [(0, 0), (0, 10)]
    Square = [(0, 0), (10, 0), (10, 10), (0, 10)]
    Rectangle = [(0, 0), (20, 0), (20, 10), (0, 10)]
    IsoscelesTriangle = [(5, 0), (10, 10), (0, 10)]
    Trapezoid = [(5, 0), (10, 0), (15, 20), (0, 20)]

class Projectile:
    """Projectile class. For spawning projectiles
    """
    def __init__(self, pos: tuple | list = (0, 0), radius: int =25):
        """
        Initiate projectile

        :param pos: Spawn position
        :type pos: tuple | list
        :param radius: The radius of the circle, defaults to 25
        :type radius: int (optional)
        """
        self.__body = pymunk.Body()
        self.__body.position = pos
        self.__shape = pymunk.Circle(self.__body, radius)
        self.__shape.density = 0.1
        self.__shape.friction = 0.9
        self.__shape.elasticity = 0.5

    @property
    def body(self):
        """__body getter

        Returns:
            _type_: _description_
        """
        return self.__body
    @property
    def shape(self):
        """__shape getter

        Returns:
            _type_: _description_
        """
        return self.__shape
    @body.setter
    def body_setter(self, value):
        """__body setter

        Args:
            value (_type_): _description_
        """
        self.__body = value
    @shape.setter
    def shape_setter(self, value):
        """__shape setter

        Args:
            value (_type_): _description_
        """
        self.__shape = value


class StaticObstacle:
    """This class represents a static obstacle."""
    def __init__(self, name: str, pos: tuple | list = (), shape: str | int = "Circle",
                 multiplier: int = 1, vertices: Sequence[Tuple[int, int]] | None = (),
                 radius: int = 20, density: float | int = 1.0, friction: float | int = 0.9,
                 elasticity: float | int = 0.5) -> None:
        """
        Obstacle class Object's shape (if not "Custom") is pre-defined and can only modified by changing
        it's multiplier. While "Custom" shape requires you to define it's vertices in form of a sequence
        of tuple.

        :param name: str
        :type name: str
        :param pos: The position of the object
        :type pos: tuple | list
        :param shape: str | int = "Circle",, defaults to Circle
        :type shape: str | int (optional)
        :param multiplier: int = 1, vertices: Sequence[Tuple[int, int]] | None = (),, defaults to 1
        :type multiplier: int (optional)
        :param vertices: Sequence[Tuple[int, int]] | None = (),
        :type vertices: Sequence[Tuple[int, int]] | None
        :param radius: Thickness (for "Line" or "Circle" radius). Defaults to 20
        :type radius: int (optional)
        :param density: The density of the body. This is used to calculate the mass of the body from the
        mass_properties
        :type density: float | int
        :param friction: The friction coefficient, usually in the range [0,1]
        :type friction: float | int
        :param elasticity: The amount of energy the object will retain after a collision
        :type elasticity: float | int
        """
        if not isinstance(name, str):
            raise TypeError("Unexpected type for name. Expected: str")
        if not isinstance(pos, tuple | list):
            raise TypeError("Unexpected type for pos. Expected: tuple, list")
        if len(pos) != 2:
            raise ValueError("Pos must only have 2 elements")
        if not isinstance(shape, str | int):
            raise TypeError("Unexpected type for shape. Expected: str | int")
        if not isinstance(radius, int):
            raise TypeError("Unexpected type for radius. Expected: int")
        if not isinstance(density, int | float):
            raise TypeError("Unexpected type for density. Expected: int, float")
        if not isinstance(friction, int | float):
            raise TypeError("Unexpected type for friction. Expected: int, float")
        if not isinstance(elasticity, int | float):
            raise TypeError("Unexpected type for elasticity. Expected: int, float")
        if (shape != "Circle" or shape != 5) and not isinstance(multiplier, int):
            raise TypeError("Unexpected type for multiplier. Expected: int")
        if (shape != "Custom" or shape != 6) and not isinstance(vertices, Sequence):
            raise TypeError("Unexpected type for vertices. Expected: Sequence type")
        self.__name = name
        self.__body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.__body.position = pos
        if shape == "Circle" or shape == 5:
            self.__shape = pymunk.Circle(self.__body, radius)
        elif shape == "Square" or shape == 1:
            self.__shape = pymunk.Poly(self.__body,
                                       tuple(np.multiply(_ShapeDefinition.Square.value,
                                                         multiplier).tolist()))
        elif shape == "Rectangle" or shape == 2:
            self.__shape = pymunk.Poly(self.__body,
                                       tuple(np.multiply(_ShapeDefinition.Rectangle.value,
                                                         multiplier).tolist()))
        elif shape == "IsoscelesTriangle" or shape == 3:
            self.__shape = pymunk.Poly(self.__body,
                                       tuple(np.multiply(_ShapeDefinition.IsoscelesTriangle.value,
                                                         multiplier).tolist()))
        elif shape == "Trapezoid" or shape == 4:
            self.__shape = pymunk.Poly(self.__body,
                                       tuple(np.multiply(_ShapeDefinition.Trapezoid.value,
                                                         multiplier).tolist()))
        elif shape == "Custom" or shape == 6:
            self.__shape = pymunk.Poly(self.__body, tuple(np.multiply(vertices,
                                                                      multiplier).tolist()))
        elif shape == "Line" or shape == 0:
            self.__shape = pymunk.Segment(self.__body, _ShapeDefinition.Line.value[0],
                                          tuple(np.multiply(_ShapeDefinition.Line.value[1],
                                                            multiplier)), 15)
        else:
            print("Unknown shape. Creating a segment with 15 as thickness instead")
            self.__shape = pymunk.Segment(self.__body, pos, tuple(np.add(pos, 10)), 15)
        self.__shape.density = density
        self.__shape.friction = friction
        self.__shape.elasticity = elasticity

    @property
    def body(self):
        """__body getter

        Returns:
            _type_: _description_
        """
        return self.__body
    @property
    def shape(self):
        """__shape getter

        Returns:
            _type_: _description_
        """
        return self.__shape
    @property
    def name(self):
        """__shape getter

        Returns:
            _type_: _description_
        """
        return self.__name
    @body.setter
    def body_setter(self, value):
        """__body setter

        Args:
            value (_type_): _description_
        """
        self.__body = value
    @shape.setter
    def shape_setter(self, value):
        """__shape setter

        Args:
            value (_type_): _description_
        """
        self.__shape = value
    @name.setter
    def name_setter(self, value):
        """__name setter

        Args:
            value (_type_): _description_
        """
        self.__name = value


class Boundary:
    """Boundary class.  For surrounding game window with a box (STATIC BODY)
    """
    def __init__(self, body, origin: tuple | list = (0, 0),
                 size: tuple | list = (WIDTH, HEIGHT), radius: int = 4):
        """
        Initiate Boundary

        :param body: The body to attach the boundary to
        :param origin: The origin is the point where the boundary starts
        :type origin: tuple | list
        :param size: A tuple contain Width and Height of the boundary. Defaults to (_WIDTH, _HEIGHT)
        :type size: tuple | list
        :param radius: The thickness of the boundary, defaults to 4
        :type radius: int (optional)
        """
        x0, y0 = origin
        width, height = size
        points = [(x0, y0), (width, y0), (width, height), (x0, height)]
        self.__segments = []
        for i in range(4):
            segment = pymunk.Segment(body, points[i], points[(i+1) % 4], radius)
            segment.elasticity = 1
            segment.friction = 1
            self.__segments.append(segment)

    @property
    def segments(self):
        """Getter for __segments
        """
        return self.__segments
    @segments.setter
    def segments_setter(self, value):
        """Setter for segment

        Args:
            value (Any): Anything
        """
        self.__segments = value
