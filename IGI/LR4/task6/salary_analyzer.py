import pandas as pd
from typing import Tuple


class SalaryAnalyzer:
    """Specialized analyzer for Salary dataset"""

    def __init__(self, data: pd.DataFrame):
        """
        Initialize SalaryAnalyzer

        Args:
            data: Salary DataFrame with columns: Salary, Gender, Years of Experience
        """
        self.data = data
        self._validate_data()

    def _validate_data(self):
        """Validate required columns exist"""
        required_columns = ['Salary', 'Gender', 'Years of Experience']
        for col in required_columns:
            if col not in self.data.columns:
                raise ValueError(f"Required column '{col}' not found in dataset")

    def clean_data(self) -> pd.DataFrame:
        """
        Clean the dataset

        Returns:
            Cleaned DataFrame
        """
        cleaned = self.data.copy()

        cleaned = cleaned.dropna(subset=['Salary', 'Gender', 'Years of Experience'])

        cleaned = cleaned[cleaned['Salary'] > 0]

        cleaned = cleaned[cleaned['Years of Experience'] >= 0]

        return cleaned

    def create_salary_series(self) -> pd.Series:
        """
        Create Series from Salary column

        Returns:
            Series with salary values
        """
        return pd.Series(self.data['Salary'].values, name='salary_series')

    def print_salary_series_info(self) -> None:
        """Print information about salary series"""
        salary_series = self.create_salary_series()

        print("\n" + "=" * 60)
        print("TASK A.1: SALARY SERIES")
        print("=" * 60)
        print(f"\nType: {type(salary_series)}")
        print(f"Name: {salary_series.name}")
        print(f"Length: {len(salary_series)}")
        print(f"Mean: ${salary_series.mean():.2f}")
        print(f"Median: ${salary_series.median():.2f}")
        print(f"Std: ${salary_series.std():.2f}")
        print(f"Min: ${salary_series.min():.2f}")
        print(f"Max: ${salary_series.max():.2f}")
        print(f"\nFirst 10 values:")
        print(salary_series.head(10))

    def split_salary_by_gender(self) -> Tuple[pd.Series, pd.Series]:
        """
        Split salary Series into Male and Female Series

        Returns:
            Tuple (male_salary_series, female_salary_series)
        """
        male_salary = self.data[self.data['Gender'] == 'Male']['Salary']
        female_salary = self.data[self.data['Gender'] == 'Female']['Salary']

        return male_salary, female_salary

    def print_gender_split(self) -> None:
        """Print salary split by gender"""
        male_series, female_series = self.split_salary_by_gender()

        print("\n" + "=" * 60)
        print("TASK A.2: SALARY SPLIT BY GENDER")
        print("=" * 60)

        print(f"\n MALE employees:")
        print(f"   Count: {len(male_series)}")
        print(f"   Mean salary: ${male_series.mean():.2f}")
        print(f"   Median salary: ${male_series.median():.2f}")
        print(f"   Min salary: ${male_series.min():.2f}")
        print(f"   Max salary: ${male_series.max():.2f}")
        print(f"\n   First 5 values:")
        print(male_series.head())

        print(f"\n FEMALE employees:")
        print(f"   Count: {len(female_series)}")
        print(f"   Mean salary: ${female_series.mean():.2f}")
        print(f"   Median salary: ${female_series.median():.2f}")
        print(f"   Min salary: ${female_series.min():.2f}")
        print(f"   Max salary: ${female_series.max():.2f}")
        print(f"\n   First 5 values:")
        print(female_series.head())

    def get_salary_by_experience(self) -> pd.DataFrame:
        """
        Get salary grouped by years of experience

        Returns:
            DataFrame with average salary by experience
        """
        return self.data.groupby('Years of Experience')['Salary'].agg(['mean', 'count', 'std'])

    def find_max_and_min_experience_salary(self) -> Tuple[float, float, int, int]:
        """
        Find average salary for employees with max and min experience

        Returns:
            Tuple (avg_salary_max_exp, avg_salary_min_exp, max_exp, min_exp)
        """
        max_exp = self.data['Years of Experience'].max()
        min_exp = self.data['Years of Experience'].min()

        avg_salary_max_exp = self.data[self.data['Years of Experience'] == max_exp]['Salary'].mean()
        avg_salary_min_exp = self.data[self.data['Years of Experience'] == min_exp]['Salary'].mean()

        return avg_salary_max_exp, avg_salary_min_exp, max_exp, min_exp

    def calculate_salary_ratio(self) -> Tuple[float, float, float, int, int]:
        """
        Calculate ratio of average salary (max experience vs min experience)

        Returns:
            Tuple (ratio, avg_salary_max_exp, avg_salary_min_exp, max_exp, min_exp)
        """
        avg_max, avg_min, max_exp, min_exp = self.find_max_and_min_experience_salary()

        if avg_min > 0:
            ratio = avg_max / avg_min
        else:
            ratio = float('inf')

        return ratio, avg_max, avg_min, max_exp, min_exp

    def print_experience_salary_analysis(self) -> None:
        """Print analysis of salary by experience"""
        ratio, avg_max, avg_min, max_exp, min_exp = self.calculate_salary_ratio()

        print("\n" + "=" * 60)
        print("TASK B: SALARY ANALYSIS BY YEARS OF EXPERIENCE")
        print("=" * 60)

        print(f"\n Experience statistics:")
        exp_stats = self.data['Years of Experience'].describe()
        print(f"   Min years: {exp_stats['min']:.0f}")
        print(f"   Max years: {exp_stats['max']:.0f}")
        print(f"   Mean years: {exp_stats['mean']:.2f}")
        print(f"   Median years: {exp_stats['50%']:.0f}")

        print(f"\n Salary by experience:")
        print(f"   Average salary (min experience = {min_exp} years): ${avg_min:.2f}")
        print(f"   Average salary (max experience = {max_exp} years): ${avg_max:.2f}")

        print(f"\n RATIO: {ratio:.2f}")
        print(f"\n ANSWER: The average salary of employees with {max_exp} years of experience")
        print(f"   is {ratio:.2f} times higher than employees with {min_exp} years of experience.")
