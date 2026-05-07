import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def run_task1():
    """Run Task 1: Student questionnaire"""
    print("\n" + "=" * 70)
    print("RUNNING TASK 1: STUDENT QUESTIONNAIRE")
    print("=" * 70)

    from task1.models import Student, StudentGroup
    from task1.serializers import StudentSerializer
    from task1.menu import (display_menu, print_age_groups,
                                      show_all_students, add_student_interactive,
                                      remove_student_interactive, find_student_interactive)

    group = StudentGroup("Class 9A")
    sample_students = [
        ("Ivanov", 10, 4), ("Petrova", 12, 6), ("Sidorov", 15, 9),
        ("Kuznetsova", 17, 10), ("Smirnov", 8, 2), ("Volkova", 14, 8)
    ]
    for last_name, age, grade in sample_students:
        group.add_student(Student(last_name, age, grade))

    print(f"\nLoaded {len(group)} sample students.")

    while True:
        display_menu()
        choice = input("\nChoose option (0-9): ").strip()

        if choice == '0':
            break
        elif choice == '1':
            add_student_interactive(group)
        elif choice == '2':
            remove_student_interactive(group)
        elif choice == '3':
            print_age_groups(group)
        elif choice == '4':
            find_student_interactive(group)
        elif choice == '5':
            filename = input("Enter filename: ")
            StudentSerializer.save_to_csv(group, filename)
        elif choice == '6':
            filename = input("Enter filename: ")
            StudentSerializer.save_to_pickle(group, filename)
        elif choice == '7':
            filename = input("Enter filename: ")
            StudentSerializer.load_from_csv(group, filename)
        elif choice == '8':
            filename = input("Enter filename: ")
            StudentSerializer.load_from_pickle(group, filename)
        elif choice == '9':
            show_all_students(group)
        else:
            print("Invalid option!")


def run_task2():
    """Run Task 2: Text analysis with regex (Variant 22)"""
    print("\n" + "=" * 70)
    print("RUNNING TASK 2: TEXT ANALYSIS (VARIANT 22)")
    print("=" * 70)

    from task2.main_analyzer import main as task2_main
    task2_main()


def run_task3():
    """Run Task 3: Series expansion"""
    print("\n" + "=" * 70)
    print("RUNNING TASK 3: SERIES EXPANSION")
    print("=" * 70)

    import numpy as np
    from task3.series import SeriesExpansion
    from task3.statistics import StatisticalAnalyzer
    from task3.plotter import SeriesPlotter

    x_values = np.linspace(-0.95, 0.95, 20)
    series = SeriesExpansion(x_values)
    results = series.get_results()

    plotter = SeriesPlotter(results)
    print(plotter.create_table())

    stats = StatisticalAnalyzer()
    series_stats = stats.get_all_statistics(series.get_series_values())
    print(f"\nSeries values mean: {series_stats['mean']:.10f}")
    print(f"Series values median: {series_stats['median']:.10f}")

    plotter.create_plot("arcsin_series_plot.png")


def run_task4():
    """Run Task 4: Geometric shapes"""
    print("\n" + "=" * 70)
    print("RUNNING TASK 4: PARALLELOGRAM")
    print("=" * 70)

    from task4.main_shapes import task4_main
    task4_main()


def run_task5():
    """Run Task 5: NumPy matrix analysis"""
    print("\n" + "=" * 70)
    print("RUNNING TASK 5: NUMPY MATRIX ANALYSIS")
    print("=" * 70)

    from task5.matrix_analyzer import MatrixAnalyzer

    analyzer = MatrixAnalyzer.create_random_matrix(5, 5, -20, 50)
    analyzer.display_matrix()
    analyzer.display_secondary_diagonal()

    info = analyzer.get_matrix_info()
    print(f"\nMinimum on secondary diagonal: {info['min_on_secondary_diag']}")
    print(f"Variance (NumPy): {info['variance_numpy']:.4f}")
    print(f"Variance (Formula): {info['variance_formula']:.4f}")
    print(f"Rounded to hundredths: {info['variance_numpy']:.2f}")


def run_task6():
    """Run Task 6: Pandas Salary Dataset Analysis"""
    print("\n" + "=" * 70)
    print("RUNNING TASK 6: PANDAS SALARY DATASET ANALYSIS")
    print("=" * 70)

    from task6.main_pandas import main as task6_main
    task6_main()


def main():
    """Main function to run all tasks"""
    print("\n" + "=" * 70)
    print("LABORATORY WORK No. 4 - VARIANT 22")
    print("Developer: Student")
    print("Date: 2024")
    print("=" * 70)

    tasks = {
        '1': ("Student Questionnaire", run_task1),
        '2': ("Text Analysis with Regex (Variant 22)", run_task2),
        '3': ("Series Expansion (arcsin x)", run_task3),
        '4': ("Geometric Shapes (Parallelogram)", run_task4),
        '5': ("NumPy Matrix Analysis", run_task5),
        '6': ("Pandas Airbnb Analysis", run_task6)
    }

    while True:
        print("\n" + "-" * 50)
        print("SELECT TASK TO RUN:")
        print("-" * 50)
        for key, (name, _) in tasks.items():
            print(f"  {key}. {name}")
        print("  a. Run ALL tasks")
        print("  0. Exit")
        print("-" * 50)

        choice = input("\nEnter choice: ").strip()

        if choice == '0':
            print("\nGoodbye!")
            break
        elif choice == 'a':
            for _, (_, func) in tasks.items():
                func()
        elif choice in tasks:
            tasks[choice][1]()
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()