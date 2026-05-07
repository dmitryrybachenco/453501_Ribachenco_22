import csv
import pickle
from typing import List
from .models import Student, StudentGroup


class StudentSerializer:
    """Base class for student serialization"""

    @staticmethod
    def save_to_csv(group: StudentGroup, filename: str) -> bool:
        """
        Save students to CSV file

        Args:
            group: StudentGroup object
            filename: Name of the CSV file

        Returns:
            True if successful, False otherwise
        """
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Last Name', 'Age', 'Grade', 'Age Group'])
                for student in group.students:
                    writer.writerow([
                        student.last_name,
                        student.age,
                        student.grade if student.grade else '',
                        student.age_group
                    ])
            return True
        except Exception as e:
            print(f"Error saving to CSV: {e}")
            return False

    @staticmethod
    def load_from_csv(group: StudentGroup, filename: str) -> bool:
        """
        Load students from CSV file

        Args:
            group: StudentGroup object to populate
            filename: Name of the CSV file

        Returns:
            True if successful, False otherwise
        """
        try:
            students_list = []
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    last_name = row['Last Name']
                    age = int(row['Age'])
                    grade = int(row['Grade']) if row['Grade'] else None
                    student = Student(last_name, age, grade)
                    students_list.append(student)

            for student in students_list:
                group.add_student(student)
            return True

        except FileNotFoundError:
            print(f"File {filename} not found.")
            return False
        except Exception as e:
            print(f"Error loading from CSV: {e}")
            return False

    @staticmethod
    def save_to_pickle(group: StudentGroup, filename: str) -> bool:
        """
        Save students to pickle file

        Args:
            group: StudentGroup object
            filename: Name of the pickle file

        Returns:
            True if successful, False otherwise
        """
        try:
            with open(filename, 'wb') as file:
                pickle.dump(group.students, file)
            return True
        except Exception as e:
            print(f"Error saving to pickle: {e}")
            return False

    @staticmethod
    def load_from_pickle(group: StudentGroup, filename: str) -> bool:
        """
        Load students from pickle file

        Args:
            group: StudentGroup object to populate
            filename: Name of the pickle file

        Returns:
            True if successful, False otherwise
        """
        try:
            with open(filename, 'rb') as file:
                students = pickle.load(file)
                for student in students:
                    group.add_student(student)
            return True
        except FileNotFoundError:
            print(f"File {filename} not found.")
            return False
        except Exception as e:
            print(f"Error loading from pickle: {e}")
            return False