"""
Task 3: Check if string is a binary number.
Author: Ribachenko Dmitriy
Date: 18.03.2026
"""

import utils


@utils.decorator_repeat
def is_binary_number(s: str) -> bool:
    """
    Check if a string represents a binary number.
    """
    if not s:
        return False

    for char in s:
        if char not in '01':
            return False

    return True


def analyze_string() -> None:
    """
    Get string from user and analyze if it's binary.
    """
    s = utils.input_string_from_user()

    if is_binary_number(s):
        print(f"\n'{s}' IS a binary number.")
    else:
        print(f"\n'{s}' is NOT a binary number.")


def run_task3() -> None:
    """Main function to run Task 3."""
    print("\n" + "=" * 60)
    print("TASK 3: BINARY NUMBER CHECKER")
    print("=" * 60)

    analyze_string()