"""
Task 1: Series expansion for hyperbolic sine: sh(x) = x - x^3/3! + x^5/5! - ...
Author: Ribachenko Dmitriy
Date: 18.03.2026
"""

import math
from typing import Tuple
import utils

def arcsin_series(x: float, eps: float, max_iter: int =500) -> Tuple[float, int]:
    """
    Calculate arcsin using series expansion.
    """
    if abs(x) >= 1:
        raise ValueError("|x| must be less than 1")

    result = x
    term = x
    n = 0

    while n < max_iter:
        n += 1
        term = term * ((2 * n - 1) ** 2 * x * x) / (2 * n * (2 * n + 1))
        result += term

        if abs(term) < eps:
            break

    if n >= max_iter:
        print(f"Warning: Maximum iterations ({max_iter}) reached. Required precision may not be achieved.")

    return result, n

@utils.decorator_repeat
def calculate_and_display(x: float, eps: float) -> None:
    """
    Calculate series value and display results.
    """
    try:
        series_value, n_terms = arcsin_series(x, eps)
        math_value = math.sinh(x)

        print("\n" + "=" * 60)
        print("RESULTS FOR HYPERBOLIC SINE CALCULATION")
        print("-" * 76)
        print(f"| {'x':^10} | {'n':^8} | {'F(x)':^15} | {'Math F(x)':^15} | {'eps':^12} |")
        print("-" * 76)
        print(f"| {x:^10.6f} | {n_terms:^8} | {series_value:^15.10f} | {math_value:^15.10f} | {eps:^12.1e} |")
        print("-" * 76)

    except Exception as e:
        print(f"Error during calculation: {e}")


def run_task1() -> None:
    """Main function to run Task 1."""
    print("\n" + "=" * 60)
    print("TASK 1: SERIES EXPANSION FOR ARCSIN")
    print("=" * 60)

    while True:
        try:
            while True:
                x = utils.get_float_input("Enter x (|x| < 1): ")
                if abs(x) >= 1:
                    print("|x| must be less than 1")
                    continue
                break
            eps = utils.get_float_input("Enter eps (precision, e.g., 0.0001): ")

            if eps <= 0:
                print("Precision must be positive. Using default 0.0001.")
                eps = 0.0001

            calculate_and_display(x, eps)
            break

        except Exception as e:
            print(f"Error: {e}")