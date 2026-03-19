"""
Utility functions for laboratory work No. 3.
Author: Ribachenko Dmitriy
Date: 18.03.2026
"""

from typing import List, Callable
import functools

def get_user_choice(prompt: str, min_val: int = 0, max_val: int = 5) -> int:
    """
    Get and validate user menu choice.
    """
    while True:
        try:
            choice = int(input(prompt))
            if min_val <= choice <= max_val:
                return choice
            else:
                print(f"Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input! Please enter a valid integer.")


def get_float_input(prompt: str) -> float:
    """
    Get and validate float input from user.
    """
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Invalid input! Please enter a valid number.")


def get_int_input(prompt: str, allow_zero: bool = True) -> int:
    """
    Get and validate integer input from user.
    """
    while True:
        try:
            value = int(input(prompt))
            if allow_zero or value != 0:
                return value
            else:
                print("Zero is not allowed. Please enter a non-zero value.")
        except ValueError:
            print("Invalid input! Please enter a valid integer.")


def continue_prompt() -> None:
    """Ask user if they want to continue and wait for Enter key."""
    input("\nPress Enter to continue...")


def input_list_from_user() -> List[float]:
    """
    Input list elements from user.
    """
    elements = []
    while True:
        try:
            n = get_int_input("Enter the number of elements (positive integer): ", allow_zero=False)
            if n > 0:
                break
            else:
                print("Number of elements must be positive.")
        except ValueError:
            print("Invalid input!")

    print(f"Enter {n} real numbers:")
    for i in range(n):
        while True:
            try:
                value = float(input(f"Element {i + 1}: "))
                elements.append(value)
                break
            except ValueError:
                print("Invalid input! Please enter a valid real number.")

    return elements


def generate_list_random() -> List[float]:
    """
    Generate list with random values.
    """
    import random

    n = random.randint(3, 10)
    return [round(random.uniform(-10, 10), 2) for _ in range(n)]


def input_string_from_user() -> str:
    """
    Input string from user.
    """
    return input("Enter a string: ")


def decorator_repeat(func: Callable) -> Callable:
    """
    Decorator to repeat function execution.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"\nFunction '{func.__name__}' executed successfully.")
        return result

    return wrapper