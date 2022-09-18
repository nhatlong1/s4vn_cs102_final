"""projectile's camera

This file containing the Camera class and default _CAM_CONTROL dictionary

Imports:
- Any from typing
- pymunk
- Everything from pygame.locals

Warnings:
- Use constants from pygame.locals when modifying default cam control. Unless you know the exact
  value of a key, do not use bare ints.
- Update Camera's __init__ docstring if you modify the default _CAM_CONTROL dictionary
"""
from typing import Any
import pymunk
from pygame.locals import *


_CAM_CONTROl = {
    "left": K_a,
    "right": K_d,
    "up": K_w,
    "down": K_s,
    "in": None,
    "out": None,
    "reset": K_SPACE
}

class Camera:
    """Camera class for Pymunk on Pygame
    """
    def __init__(self, scroll_speed: int = 1, zoom_speed: int | float = 0.01,
                 min_scaling: int | float = 1, max_scaling: int | float = 5,
                 controls: dict = _CAM_CONTROl) -> None:
        """
        Initiate camera

        :param scroll_speed: The speed at which the camera moves, defaults to 1
        :type scroll_speed: int (optional)
        :param zoom_speed: How fast the camera zooms in and out
        :type zoom_speed: int | float
        :param min_scaling: The minimum zoom level, defaults to 1
        :type min_scaling: int | float (optional)
        :param max_scaling: The maximum zoom level, defaults to 5
        :type max_scaling: int | float (optional)
        :param controls: dict = _CAM_CONTROl
        :type controls: dict
        """
        if not isinstance(scroll_speed, int):
            raise TypeError(f"Unexpected type for scroll_speed: {type(scroll_speed)}. "
                            "Expected: int")
        if not isinstance(zoom_speed, int | float):
            raise TypeError(f"Unexpected type for zoom_speed: {type(zoom_speed)}. "
                            "Expected: int, float")
        if not isinstance(min_scaling, int | float):
            raise TypeError(f"Unexpected type for min_scaling: {type(min_scaling)}. "
                            "Expected: int, float")
        if not isinstance(max_scaling, int | float):
            raise TypeError(f"Unexpected type for max_scaling: {type(max_scaling)}. "
                            "Expected: int, float")
        if not isinstance(controls, dict):
            raise TypeError(f"Unexpected type for controls: {type(controls)}. "
                            "Expected: dict")
        self.__translation       = pymunk.Transform()
        self.__translation_speed = scroll_speed
        self.__zoom_speed        = zoom_speed
        self.__controls          = controls
        self.__min_scaling       = min_scaling
        self.__max_scaling       = max_scaling
        self.__scaling           = 1
        self.__x_offset          = 0
        self.__y_offset          = 0

    def compute_translation_and_scaling(self, keys_pressed: Any):
        """
        It computes the translation and scaling of the surface

        :param keys_pressed: A list of key status
        :type keys_pressed: Any
        :return: A tuple of Transform information, scaling and rotation
        """
        left             = int(keys_pressed[self.__controls["left"]])
        up               = int(keys_pressed[self.__controls["up"]])
        down             = int(keys_pressed[self.__controls["down"]])
        right            = int(keys_pressed[self.__controls["right"]])

        if not self.__controls["in"] is None:
            zoom_in      = int(keys_pressed[self.__controls["in"]])
        else:
            zoom_in      = 0
        if not self.__controls["out"] is None:
            zoom_out     = int(keys_pressed[self.__controls["out"]])
        else:
            zoom_out     = 0
        if not self.__controls["reset"] is None:
            reset        = int(keys_pressed[self.__controls["reset"]])
        else:
            reset        = 0

        if not reset:
            self.__translation = self.__translation.translated(
                self.__translation_speed * left - self.__translation_speed * right,
                self.__translation_speed * up   - self.__translation_speed * down
            )
            self.__scaling  = min(
                max(
                    self.__scaling + (self.__zoom_speed * zoom_in - self.__zoom_speed * zoom_out),
                    self.__min_scaling
                ),
                self.__max_scaling
            )
            self.__x_offset += self.__translation_speed * left - self.__translation_speed * right
            self.__y_offset += self.__translation_speed * up   - self.__translation_speed * down
        else:
            self.__translation = self.__translation.translated(
                -self.__x_offset, -self.__y_offset
            )
            self.__x_offset = 0
            self.__y_offset = 0
            self.__scaling  = 1

        rotation = 0

        return (self.__translation, self.__scaling, rotation)


    @property
    def x_offset(self):
        """__x_offset property

        Though this property have a setter method, do not try to modify it directly
        """
        return self.__x_offset
    @property
    def y_offset(self):
        """__y_offset property

        Though this property have a setter method, do not try to modify it directly
        """
        return self.__y_offset
    @property
    def zoom_scale(self):
        """__scaling property

        Though this property have a setter method, do not try to modify it directly
        """
        return self.__scaling
    @x_offset.setter
    def x_offset(self, value):
        self.__x_offset = value
    @y_offset.setter
    def y_offset(self, value):
        self.__y_offset = value
    @zoom_scale.setter
    def zoom_scale(self, value):
        self.__scaling = value
