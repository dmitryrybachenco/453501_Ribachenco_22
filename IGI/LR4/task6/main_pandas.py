import os
from .salary_analyzer import SalaryAnalyzer
from .data_loader import load_salary_data_from_file

def main():
    """Main function for Task 6"""
    print("\n" + "=" * 70)
    print("LABORATORY WORK No. 4 - TASK 6 (VARIANT 22)")
    print("Salary Dataset Analysis")
    print("=" * 70)

    csv_file = "Salary_Data.csv"

    if os.path.exists(csv_file):
        df = load_salary_data_from_file(csv_file)
    else:
        print(f"\n File '{csv_file}' not found!")
        print("Please make sure the Salary_Data.csv file is in the current directory.")
        return

    analyzer = SalaryAnalyzer(df)

    analyzer.print_salary_series_info()

    analyzer.print_gender_split()

    analyzer.print_experience_salary_analysis()

    print("\n" + "=" * 70)
    print(" Task 6 completed successfully!")
    print("=" * 70)