"""Object selector"""


import enum


class ObjectSelector(enum.Enum):
    """The class is a list of objects that can be drawn on the canvas"""
    LINE = 0
    SQUARE = 1
    RECTANGLE = 2
    ISOSCELES_TRIANGLE = 3
    TRAPEZOID = 4
    CIRCLE = 5
    CUSTOM = 6
