import time
from typing import Callable, Any
from threading import Thread

import numpy as np
import pygame
from pymunk.pygame_util import to_pygame, from_pygame

from projectile.includes.constants import SIZE

def after(time_value: int, command: Callable[[], Any] | str = ...,
          args: list | tuple = ..., use_thread_and_join: bool = True):
    """
    It runs a function after a certain amount of time

    :param time_value: The time to wait before executing the command
    :type time_value: int
    :param command: The function you want to run after the time_value
    :type command: Callable[[], Any] | str
    :param args: list | tuple = ..
    :type args: list | tuple
    :param use_thread_and_join: If True, the function will be run in a thread and the thread will be
    joined, defaults to True
    :type use_thread_and_join: bool (optional)
    """
    time.sleep(time_value)
    pass_args = None
    if isinstance(args, tuple | list):
        pass_args = tuple(args)
    if use_thread_and_join:
        if pass_args:
            th = Thread(target=command, args=pass_args)
        else:
            th = Thread(target=command)
        th.start()
        th.join()
    else:
        if pass_args:
            command(*pass_args)
        else:
            command()

def blur_screen(screen: pygame.Surface, strength: int | str = ..., color: str = "#7A7A7A"):
    """
    It blurs the screen

    :param screen: The surface to blur
    :type screen: pygame.Surface
    :param strength: The strength of the blur
    :type strength: int | str
    :param color: The color of the blur, defaults to #7A7A7A
    :type color: str (optional)
    """
    if color.startswith("#"):
        color = color[1:]
    if isinstance(strength, int):
        strength = hex(strength)[2:]
    blur = pygame.Surface(SIZE, pygame.SRCALPHA)
    blur.fill(rf"#{color}{strength[:2]}")
    screen.blit(blur, (0, 0))

def pg_coord(tuple1, tuple2, surface, operation="-"):
    """
    It takes two tuples, a surface, and an operation, and returns a new tuple as pygame coordinates
    
    :param tuple1: First tuple
    :param tuple2: The coordinates of the point you want to move
    :param surface: The surface you want to draw on
    :param operation: The operation to be performed on the two tuples, defaults to - (optional)
    :return: A tuple of the coordinates of the point in the pygame window.
    """
    if operation == "+":
        return to_pygame(tuple(np.add(tuple1, tuple2)), surface)
    else:
        return to_pygame(tuple(np.subtract(tuple1, tuple2)), surface)

def pm_coord(tuple1, tuple2, surface, op="-"):
    """
    It takes two tuples, a surface, and an operation, and returns a new tuple as pymunk coordinates
    
    :param tuple1: First tuple
    :param tuple2: The position of the object you want to move
    :param surface: The surface you're drawing on
    :param op: The operation to be performed, defaults to - (optional)
    :return: A tuple of the coordinates of the point in the pygame coordinate system.
    """
    if op == "+":
        return from_pygame(tuple(np.add(tuple1, tuple2)), surface)
    else:
        return from_pygame(tuple(np.subtract(tuple1, tuple2)), surface)

def get_offset(camera):
    """
    It returns the x and y offset of the camera

    :param camera: The camera object
    :return: The x and y offset of the camera.
    """
    return (camera.x_offset, camera.y_offset)

def toggle_buttons(state: str = "normal", *buttons):
    """
    It takes a state (defaults to "normal") and a list of buttons, and sets the state of each button to
    the given state

    :param state: The state of the button, defaults to normal
    :type state: str (optional)
    """
    for button in buttons:
        button.config(state=state)
