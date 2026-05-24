from abc import ABC, abstractmethod
import math
from typing import Tuple, Optional


class ShapeColor:
    """Class for shape color management using property decorator"""

    def __init__(self, color: str = "blue"):
        """
        Initialize shape color

        Args:
            color: Color name or hex code
        """
        self._color = color

    @property
    def color(self) -> str:
        """Getter for color"""
        return self._color

    @color.setter
    def color(self, value: str):
        """Setter for color with validation"""
        valid_colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta',
                        'orange', 'purple', 'pink', 'brown', 'gray', 'black']
        if value.lower() in valid_colors or value.startswith('#'):
            self._color = value
        else:
            print(f"Warning: '{value}' may not be a valid color")
            self._color = value

    def __str__(self) -> str:
        return f"Color: {self._color}"


class GeometricFigure(ABC):
    """Abstract base class for geometric figures"""

    figure_type = "Geometric Figure"

    def __init__(self):
        """Initialize geometric figure"""
        self._color_obj = None

    @abstractmethod
    def calculate_area(self) -> float:
        """Abstract method to calculate figure area"""
        pass

    @abstractmethod
    def get_parameters(self) -> dict:
        """Abstract method to get figure parameters"""
        pass

    def set_color(self, color: str):
        """Set figure color"""
        self._color_obj = ShapeColor(color)

    def get_color(self) -> Optional[str]:
        """Get figure color"""
        return self._color_obj.color if self._color_obj else None

    def get_info(self) -> str:
        """Get formatted information about the figure"""
        params = self.get_parameters()
        param_str = ", ".join([f"{k}={v}" for k, v in params.items()])
        return (f"{self.__class__.__name__}: {param_str}, "
                f"Area: {self.calculate_area():.2f}, "
                f"Color: {self.get_color() or 'not set'}")


class Parallelogram(GeometricFigure):
    """
    Parallelogram class inheriting from GeometricFigure
    Parallelogram defined by sides a, b and angle A between them
    """

    shape_name = "Parallelogram"

    def __init__(self, side_a: float, side_b: float, angle_deg: float, color: str = "blue"):
        """
        Initialize parallelogram

        Args:
            side_a: Length of side a
            side_b: Length of side b
            angle_deg: Angle between sides a and b in degrees
            color: Shape color
        """
        super().__init__()
        self._side_a = side_a
        self._side_b = side_b
        self._angle_deg = angle_deg
        self._angle_rad = math.radians(angle_deg)
        self.set_color(color)
        self._validate_parameters()

    def _validate_parameters(self):
        """Validate input parameters"""
        if self._side_a <= 0 or self._side_b <= 0:
            raise ValueError("Side lengths must be positive")
        if self._angle_deg <= 0 or self._angle_deg >= 180:
            raise ValueError("Angle must be between 0 and 180 degrees (exclusive)")

    @property
    def side_a(self) -> float:
        return self._side_a

    @side_a.setter
    def side_a(self, value: float):
        if value <= 0:
            raise ValueError("Side a must be positive")
        self._side_a = value

    @property
    def side_b(self) -> float:
        return self._side_b

    @side_b.setter
    def side_b(self, value: float):
        if value <= 0:
            raise ValueError("Side b must be positive")
        self._side_b = value

    @property
    def angle_deg(self) -> float:
        return self._angle_deg

    @angle_deg.setter
    def angle_deg(self, value: float):
        if value <= 0 or value >= 180:
            raise ValueError("Angle must be between 0 and 180 degrees")
        self._angle_deg = value
        self._angle_rad = math.radians(value)

    def get_angle_rad(self) -> float:
        return self._angle_rad

    def calculate_area(self) -> float:
        """Calculate parallelogram area: A = a * b * sin(angle)"""
        return self._side_a * self._side_b * math.sin(self._angle_rad)

    def calculate_perimeter(self) -> float:
        """Calculate parallelogram perimeter: P = 2 * (a + b)"""
        return 2 * (self._side_a + self._side_b)

    def calculate_diagonals(self) -> Tuple[float, float]:
        """
        Calculate diagonals of the parallelogram

        Returns:
            Tuple (diagonal1, diagonal2)
        """
        cos_angle = math.cos(self._angle_rad)
        d1 = math.sqrt(self._side_a ** 2 + self._side_b ** 2 + 2 * self._side_a * self._side_b * cos_angle)
        d2 = math.sqrt(self._side_a ** 2 + self._side_b ** 2 - 2 * self._side_a * self._side_b * cos_angle)
        return d1, d2

    def calculate_height(self) -> float:
        """Calculate height relative to side a"""
        return self._side_b * math.sin(self._angle_rad)

    def get_vertices(self) -> list:
        """
        Calculate vertices coordinates for plotting

        Returns:
            List of (x, y) tuples for the four vertices
        """
        x1, y1 = 0, 0
        x2, y2 = self._side_a, 0
        x3, y3 = (self._side_a + self._side_b * math.cos(self._angle_rad),
                  self._side_b * math.sin(self._angle_rad))
        x4, y4 = (self._side_b * math.cos(self._angle_rad),
                  self._side_b * math.sin(self._angle_rad))

        return [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]

    def get_parameters(self) -> dict:
        """Get parallelogram parameters"""
        d1, d2 = self.calculate_diagonals()
        return {
            'side_a': self._side_a,
            'side_b': self._side_b,
            'angle_deg': self._angle_deg,
            'angle_rad': round(self._angle_rad, 4),
            'area': round(self.calculate_area(), 2),
            'perimeter': round(self.calculate_perimeter(), 2),
            'diagonal1': round(d1, 2),
            'diagonal2': round(d2, 2),
            'height': round(self.calculate_height(), 2)
        }

    def get_info(self) -> str:
        """Override get_info method with formatting using format()"""
        info_template = "{name}: a={a:.2f}, b={b:.2f}, angle={angle:.1f}°, area={area:.2f}, color={color}"
        return info_template.format(
            name=self.shape_name,
            a=self._side_a,
            b=self._side_b,
            angle=self._angle_deg,
            area=self.calculate_area(),
            color=self.get_color() or "not set"
        )

    @classmethod
    def get_shape_name(cls) -> str:
        """Class method to return shape name"""
        return cls.shape_name

    def __str__(self) -> str:
        return self.get_info()

    def __repr__(self) -> str:
        return f"Parallelogram(a={self._side_a}, b={self._side_b}, angle={self._angle_deg}, color='{self.get_color()}')"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Parallelogram):
            return False
        return (self._side_a == other._side_a and
                self._side_b == other._side_b and
                self._angle_deg == other._angle_deg)