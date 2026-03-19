"""
Task 2: Sum of cubes until number 12 is entered.
Author: Ribachenko Dmitriy
Date: 18.03.2026
"""

import utils

@utils.decorator_repeat
def sum_of_cubes_until_12() -> None:
    """
    Calculate sum of cubes of entered numbers until 12 is entered.
    """
    total = 0
    count = 0

    print("\nEnter integers (enter 12 to stop):")
    print("-" * 40)

    while True:
        try:
            num = utils.get_int_input(f"Number {count + 1}: ", allow_zero=True)

            if num == 12:
                print(f"\nNumber 12 entered. Stopping input.")
                break

            total += num ** 3
            count += 1
            print(f"Current sum of cubes: {total}")

        except ValueError:
            print("Invalid input! Please enter a valid integer.")

    print("\n" + "=" * 40)
    print("FINAL RESULTS")
    print("=" * 40)
    print(f"Numbers entered (excluding 12): {count}")
    print(f"Sum of cubes: {total}")
    print("=" * 40)


def run_task2() -> None:
    """Main function to run Task 2."""
    print("\n" + "=" * 60)
    print("TASK 2: SUM OF CUBES UNTIL NUMBER 12")
    print("=" * 60)

    sum_of_cubes_until_12()