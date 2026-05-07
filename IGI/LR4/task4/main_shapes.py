from shapes import Parallelogram
from drawer import ParallelogramDrawer


def get_positive_float(prompt: str) -> float:
    """
    Get and validate positive float input from user

    Args:
        prompt: Prompt message to display

    Returns:
        Validated positive float
    """
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            print("Invalid input! Value must be positive. Please try again.")
        except ValueError:
            print("Invalid input! Please enter a valid number.")


def get_angle(prompt: str) -> float:
    """
    Get and validate angle input (0 < angle < 180)

    Args:
        prompt: Prompt message to display

    Returns:
        Validated angle in degrees
    """
    while True:
        try:
            value = float(input(prompt))
            if 0 < value < 180:
                return value
            print("Invalid input! Angle must be between 0 and 180 degrees (exclusive).")
        except ValueError:
            print("Invalid input! Please enter a valid number.")


def get_color(prompt: str) -> str:
    """
    Get color input from user

    Args:
        prompt: Prompt message to display

    Returns:
        Color string
    """
    colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta',
              'orange', 'purple', 'pink', 'brown', 'gray', 'black']

    print(f"Available colors: {', '.join(colors)}")

    while True:
        color = input(prompt).strip().lower()
        if color in colors:
            return color
        print(f"Invalid color! Choose from: {', '.join(colors)}")


def input_parallelogram_parameters() -> tuple:
    """
    Interactive input of parallelogram parameters

    Returns:
        Tuple (side_a, side_b, angle, color)
    """
    print("\n" + "=" * 60)
    print("ENTER PARALLELOGRAM PARAMETERS")
    print("=" * 60)

    print("\nEnter side lengths:")
    print("-" * 40)
    side_a = get_positive_float("   Side a length: ")
    side_b = get_positive_float("   Side b length: ")

    print("\nEnter angle between sides:")
    print("-" * 40)
    angle = get_angle("   Angle between sides a and b (degrees, 0-180): ")

    print("\nChoose shape color:")
    print("-" * 40)
    color = get_color("   Shape color: ")

    return side_a, side_b, angle, color


def display_parallelogram_info(parallelogram: Parallelogram) -> None:
    """
    Display detailed information about the parallelogram

    Args:
        parallelogram: Parallelogram object
    """
    print("\n" + "=" * 60)
    print("PARALLELOGRAM INFORMATION")
    print("=" * 60)

    params = parallelogram.get_parameters()

    print(f"\nBasic parameters:")
    print(f"   Side a: {params['side_a']:.2f}")
    print(f"   Side b: {params['side_b']:.2f}")
    print(f"   Angle: {params['angle_deg']:.1f}° ({params['angle_rad']:.4f} rad)")

    print(f"\nGeometric characteristics:")
    print(f"   Area: {params['area']:.2f} sq. units")
    print(f"   Perimeter: {params['perimeter']:.2f} units")
    print(f"   Height (to side a): {params['height']:.2f} units")
    print(f"   Diagonal 1: {params['diagonal1']:.2f} units")
    print(f"   Diagonal 2: {params['diagonal2']:.2f} units")

    print(f"\nVisual parameters:")
    print(f"   Color: {parallelogram.get_color()}")
    print(f"   Shape type: {parallelogram.get_shape_name()}")


def task4_main():
    """Main function for Task 4 with keyboard input"""

    try:
        side_a, side_b, angle, color = input_parallelogram_parameters()

        parallelogram = Parallelogram(side_a, side_b, angle, color)

        display_parallelogram_info(parallelogram)

        drawer = ParallelogramDrawer(parallelogram)

        filename = "parallelogram_info.txt"
        drawer.save_to_file(filename)

        print("-" * 40)
        title = input("   Enter plot title (press Enter for default): ").strip()
        if not title:
            title = f"Parallelogram: a={side_a}, b={side_b}, angle={angle}°"

        save_path = "parallelogram.png"

        drawer.draw(title=title, save_path=save_path)

    except ValueError as e:
        print(f"\nError: {e}")
    except KeyboardInterrupt:
        print("\n\nProgram interrupted.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")