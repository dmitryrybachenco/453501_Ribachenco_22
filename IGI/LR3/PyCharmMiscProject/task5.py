"""
Task 5: Real number list processing.
Author: Ribachenko Dmitriy
Date: 18.03.2026
"""

from typing import List, Tuple, Optional
import initialization
import utils


def display_list(lst: List[float], title: str = "List") -> None:
    """
    Display list elements.
    """
    print(f"\n{title}:")
    print("-" * 40)
    for i, value in enumerate(lst):
        print(f"  [{i}]: {value:.4f}")
    print("-" * 40)


def find_min_abs_index(lst: List[float]) -> int:
    """
    Find index of minimum absolute value element.
    """
    if not lst:
        return -1

    min_abs = abs(lst[0])
    min_index = 0

    for i in range(1, len(lst)):
        if abs(lst[i]) < min_abs:
            min_abs = abs(lst[i])
            min_index = i

    return min_index


def find_first_positive_index(lst: List[float]) -> int:
    """
    Find index of first positive element.
    """
    for i, value in enumerate(lst):
        if value > 0:
            return i
    return -1


def sum_after_first_positive(lst: List[float]) -> Tuple[Optional[float], int]:
    """
    Calculate sum of elements after first positive element.
    """
    pos_index = find_first_positive_index(lst)

    if pos_index == -1 or pos_index == len(lst) - 1:
        return None, -1

    total = sum(lst[pos_index + 1:])
    return total, pos_index


def find_min_abs_element_and_sum_after_first_positive(lst: List[float]) -> None:
    """
    Find minimum absolute value element and sum after first positive.
    """
    print("\n" + "=" * 60)
    print("TASK 5 RESULTS")
    print("=" * 60)

    display_list(lst, "Original list")

    min_abs_index = find_min_abs_index(lst)
    if min_abs_index != -1:
        print(f"Minimum absolute value element:")
        print(f"  Index: {min_abs_index}")
        print(f"  Value: {lst[min_abs_index]:.4f}")
        print(f"  |Value|: {abs(lst[min_abs_index]):.4f}")

    sum_after, pos_index = sum_after_first_positive(lst)

    if pos_index == -1:
        print("\nNo positive elements found in the list.")
    elif sum_after is None:
        print("\nFirst positive element is the last element.")
        print("No elements after it to sum.")
    else:
        print(f"\nFirst positive element:")
        print(f"  Index: {pos_index}")
        print(f"  Value: {lst[pos_index]:.4f}")
        print(f"Sum of elements after first positive: {sum_after:.4f}")
        print(f"Elements after index {pos_index}: {lst[pos_index + 1:]}")


@utils.decorator_repeat
def run_task5() -> None:
    """Main function to run Task 5."""
    print("\n" + "=" * 60)
    print("TASK 5: REAL NUMBER LIST PROCESSING")
    print("=" * 60)

    init_func = initialization.get_initialization_method()

    lst = init_func()

    find_min_abs_element_and_sum_after_first_positive(lst)