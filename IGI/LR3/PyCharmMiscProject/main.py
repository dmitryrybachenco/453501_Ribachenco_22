"""
Laboratory Work No. 3
Author: Ribachenko Dmitriy
Date: 18.03.2026
Version: 1.0
"""

import task1, task2, task3, task4, task5, utils

def print_menu():
    """Display the main menu of the program."""
    print("\n" + "=" * 60)
    print("LABORATORY WORK No. 3 - VARIANT 22")
    print("=" * 60)
    print("1. Task 1 - Series Expansion")
    print("2. Task 2 - Sum of cubes until number 12 is entered")
    print("3. Task 3 - Check if string is a binary number")
    print("4. Task 4 - Text analysis (Alice in Wonderland excerpt)")
    print("5. Task 5 - List processing (real numbers)")
    print("0. Exit")
    print("-" * 60)


def main():
    """
    Main function to run the laboratory work program.
    Demonstrates the use of modules and functions.
    """

    while True:
        print_menu()
        choice = utils.get_user_choice("Select task (0-5): ", 0, 5)

        if choice == 0:
            print("\nThank you for using the program. Goodbye!")
            break
        elif choice == 1:
            task1.run_task1()
        elif choice == 2:
            task2.run_task2()
        elif choice == 3:
            task3.run_task3()
        elif choice == 4:
            task4.run_task4()
        elif choice == 5:
            task5.run_task5()

        if choice != 0:
            utils.continue_prompt()


if __name__ == "__main__":
    main()