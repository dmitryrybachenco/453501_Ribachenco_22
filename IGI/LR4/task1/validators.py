from typing import Optional


def validate_name(name: str) -> bool:
    """
    Validate student name

    Args:
        name: Name to validate

    Returns:
        True if valid, False otherwise
    """
    if not name or not isinstance(name, str):
        return False
    if not name.replace(" ", "").isalpha():
        return False
    if len(name.strip()) < 2:
        return False
    return True


def validate_age(age: int) -> bool:
    """
    Validate student age

    Args:
        age: Age to validate

    Returns:
        True if valid, False otherwise
    """
    return isinstance(age, int) and 5 <= age <= 20


def validate_grade(grade: Optional[int]) -> bool:
    """
    Validate student grade

    Args:
        grade: Grade to validate

    Returns:
        True if valid, False otherwise
    """
    if grade is None:
        return True
    return isinstance(grade, int) and 1 <= grade <= 11


def get_valid_name(prompt: str) -> str:
    """
    Get and validate a name from user input

    Args:
        prompt: Prompt message to display

    Returns:
        Validated name string
    """
    while True:
        name = input(prompt).strip()
        if validate_name(name):
            return name
        print("Invalid name! Please use only letters (minimum 2 characters).")


def get_valid_age(prompt: str) -> int:
    """
    Get and validate an age from user input

    Args:
        prompt: Prompt message to display

    Returns:
        Validated age integer
    """
    while True:
        try:
            age = int(input(prompt))
            if validate_age(age):
                return age
            print("Invalid age! Age must be between 5 and 20 years.")
        except ValueError:
            print("Please enter a valid number.")


def get_valid_grade(prompt: str) -> Optional[int]:
    """
    Get and validate a grade from user input

    Args:
        prompt: Prompt message to display

    Returns:
        Validated grade integer or None
    """
    while True:
        grade_input = input(prompt).strip()
        if grade_input == "":
            return None
        try:
            grade = int(grade_input)
            if validate_grade(grade):
                return grade
            print("Invalid grade! Grade must be between 1 and 11.")
        except ValueError:
            print("Please enter a valid number or leave empty.")