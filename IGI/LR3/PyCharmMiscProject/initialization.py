"""
Module for sequence initialization functions.
Author: Ribachenko Dmitriy
Date: 18.03.2026
"""

from typing import List, Callable
import utils


def init_by_generator() -> List[float]:
    """
    Initialize sequence using generator function.
    """
    return utils.generate_list_random()


def init_by_user_input() -> List[float]:
    """
    Initialize sequence using user input.
    """
    return utils.input_list_from_user()


def get_initialization_method() -> Callable:
    """
    Let user choose initialization method.
    """
    print("\nChoose initialization method:")
    print("1. Generate random sequence")
    print("2. Enter sequence manually")

    choice = utils.get_user_choice("Your choice (1-2): ", 1, 2)

    if choice == 1:
        return init_by_generator
    else:
        return init_by_user_input