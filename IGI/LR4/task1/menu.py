from .models import Student, StudentGroup
from .serializers import StudentSerializer
from .validators import get_valid_name, get_valid_age, get_valid_grade


def display_menu() -> None:
    """Display the main menu"""
    print("\n" + "=" * 50)
    print("STUDENT MANAGEMENT SYSTEM")
    print("=" * 50)
    print("1. Add a new student")
    print("2. Remove a student")
    print("3. View age groups")
    print("4. Find student information")
    print("5. Save to CSV file")
    print("6. Save to Pickle file")
    print("7. Load from CSV file")
    print("8. Load from Pickle file")
    print("9. Show all students")
    print("0. Exit")
    print("=" * 50)


def print_age_groups(group: StudentGroup) -> None:
    """Print all age groups with their students"""
    print("\n" + "=" * 60)
    print(f"AGE GROUPS IN {group.name.upper()}")
    print("=" * 60)

    groups = group.get_age_groups()
    if not groups:
        print("No students in the group.")
        return

    for group_name, students in sorted(groups.items()):
        print(f"\n{group_name}:")
        print("-" * 40)
        for student in students:
            student.display_info()


def show_all_students(group: StudentGroup) -> None:
    """Display all students in the group"""
    print("\n" + "=" * 50)
    print("ALL STUDENTS")
    print("=" * 50)
    if len(group) == 0:
        print("No students in the group.")
    else:
        for i, student in enumerate(group, 1):
            print(f"{i}. ", end="")
            student.display_info()


def add_student_interactive(group: StudentGroup) -> None:
    """Interactive student addition"""
    print("\n--- Add New Student ---")
    last_name = get_valid_name("Enter last name: ")
    age = get_valid_age("Enter age (5-20): ")
    grade = get_valid_grade("Enter grade (1-11) or press Enter to skip: ")
    student = Student(last_name, age, grade)
    group.add_student(student)
    print(f"Student {last_name} added successfully!")


def remove_student_interactive(group: StudentGroup) -> None:
    """Interactive student removal"""
    print("\n--- Remove Student ---")
    if len(group) == 0:
        print("No students to remove.")
        return
    last_name = input("Enter last name of student to remove: ").strip()
    if group.remove_student(last_name):
        print(f"Student {last_name} removed successfully!")
    else:
        print(f"Student with last name '{last_name}' not found.")


def find_student_interactive(group: StudentGroup) -> None:
    """Interactive student search"""
    print("\n--- Find Student ---")
    if len(group) == 0:
        print("No students in the group.")
        return
    last_name = input("Enter student's last name: ").strip()
    student = group.find_student(last_name)
    if student:
        print(f"\nStudent found:")
        student.display_info()
    else:
        print(f"Student with last name '{last_name}' not found.")