from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from .mixins import DisplayMixin


class Person(ABC):
    """Abstract base class for a person"""

    species = "Homo sapiens"

    def __init__(self, last_name: str, age: int):
        """
        Constructor for Person class

        Args:
            last_name: Person's last name
            age: Person's age
        """
        self._last_name = last_name
        self._age = age

    @abstractmethod
    def get_info(self) -> str:
        """Abstract method to get person information"""
        pass

    @property
    def last_name(self) -> str:
        return self._last_name

    @last_name.setter
    def last_name(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("Last name must be a non-empty string")
        self._last_name = value

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int):
        if not isinstance(value, int) or value < 0 or value > 120:
            raise ValueError("Age must be an integer between 0 and 120")
        self._age = value

    def __str__(self) -> str:
        return f"Person: {self._last_name}, Age: {self._age}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Person):
            return False
        return self._last_name == other._last_name and self._age == other._age


class Student(Person, DisplayMixin):
    """Student class inheriting from Person"""

    def __init__(self, last_name: str, age: int, grade: Optional[int] = None):
        """
        Constructor for Student class

        Args:
            last_name: Student's last name
            age: Student's age
            grade: Student's grade (optional)
        """
        super().__init__(last_name, age)
        self._grade = grade
        self._age_group = self._determine_age_group()

    def _determine_age_group(self) -> str:
        """Determine age group based on age"""
        if self._age <= 10:
            return "Junior (7-10 years)"
        elif self._age <= 13:
            return "Middle (11-13 years)"
        elif self._age <= 15:
            return "Teen (14-15 years)"
        elif self._age <= 17:
            return "Senior (16-17 years)"
        else:
            return "Graduate (18+ years)"

    @property
    def grade(self) -> Optional[int]:
        return self._grade

    @grade.setter
    def grade(self, value: Optional[int]):
        if value is not None and (value < 1 or value > 11):
            raise ValueError("Grade must be between 1 and 11")
        self._grade = value

    @property
    def age_group(self) -> str:
        self._age_group = self._determine_age_group()
        return self._age_group

    def get_info(self) -> str:
        """Implementation of abstract method"""
        info = f"Student: {self._last_name}, Age: {self._age}"
        if self._grade:
            info += f", Grade: {self._grade}"
        info += f", Age Group: {self._age_group}"
        return info

    def __str__(self) -> str:
        return self.get_info()


class StudentGroup:
    """Class for managing a group of students"""

    def __init__(self, name: str = "Class Group"):
        """
        Constructor for StudentGroup class

        Args:
            name: Name of the group
        """
        self._name = name
        self._students: List[Student] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def students(self) -> List[Student]:
        return self._students.copy()

    def add_student(self, student: Student) -> None:
        """Add a student to the group"""
        if not isinstance(student, Student):
            raise TypeError("Only Student objects can be added")
        self._students.append(student)

    def remove_student(self, last_name: str) -> bool:
        """Remove a student by last name"""
        for i, student in enumerate(self._students):
            if student.last_name.lower() == last_name.lower():
                self._students.pop(i)
                return True
        return False

    def get_age_groups(self) -> Dict[str, List[Student]]:
        """Get students grouped by age group"""
        groups = {}
        for student in self._students:
            group = student.age_group
            if group not in groups:
                groups[group] = []
            groups[group].append(student)
        return groups

    def find_student(self, last_name: str) -> Optional[Student]:
        """Find a student by last name"""
        for student in self._students:
            if student.last_name.lower() == last_name.lower():
                return student
        return None

    def __len__(self) -> int:
        return len(self._students)

    def __getitem__(self, index: int) -> Student:
        return self._students[index]