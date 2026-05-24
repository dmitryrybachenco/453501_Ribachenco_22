import numpy as np
from typing import Tuple, Any

from numpy import floating


class MatrixAnalyzer:
    """Class for matrix analysis using NumPy"""

    def __init__(self, matrix: np.ndarray):
        """
        Initialize MatrixAnalyzer with a matrix

        Args:
            matrix: 2D numpy array
        """
        self.matrix = matrix
        self.n, self.m = matrix.shape

    @classmethod
    def create_random_matrix(cls, rows: int, cols: int,
                             low: int = -50, high: int = 50) -> 'MatrixAnalyzer':
        """
        Create a random integer matrix

        Args:
            rows: Number of rows
            cols: Number of columns
            low: Minimum value (inclusive)
            high: Maximum value (exclusive)

        Returns:
            MatrixAnalyzer instance
        """
        matrix = np.random.randint(low, high, size=(rows, cols))
        return cls(matrix)

    def get_secondary_diagonal(self) -> np.ndarray:
        """
        Get the secondary diagonal (anti-diagonal) elements

        Returns:
            Array of secondary diagonal elements
        """
        return np.array([self.matrix[i, self.n - 1 - i]
                         for i in range(min(self.n, self.m))])

    def find_min_on_secondary_diagonal(self) -> Tuple[float, Tuple[int, int]]:
        """
        Find minimum element on secondary diagonal

        Returns:
            Tuple (min_value, (row_index, col_index))
        """
        min_val = float('inf')
        min_pos = (-1, -1)

        for i in range(min(self.n, self.m)):
            j = self.n - 1 - i
            if j < self.m:
                if self.matrix[i, j] < min_val:
                    min_val = self.matrix[i, j]
                    min_pos = (i, j)

        return min_val, min_pos

    def calculate_variance_numpy(self, data: np.ndarray) -> floating[Any]:
        """
        Calculate variance using numpy's built-in function

        Returns:
            Variance value
        """
        return np.var(data)

    def calculate_variance_formula(self, data: np.ndarray) -> float:
        """
        Calculate variance using the mathematical formula

        Returns:
            Variance value
        """

        mean_val = np.mean(data)
        squared_diff_sum = np.sum((data - mean_val) ** 2)
        return squared_diff_sum / len(data)

    def get_matrix_info(self) -> dict:
        """
        Get comprehensive matrix information

        Returns:
            Dictionary with matrix information
        """
        secondary_diag = self.get_secondary_diagonal()
        min_val, min_pos = self.find_min_on_secondary_diagonal()

        return {
            'shape': self.matrix.shape,
            'matrix': self.matrix,
            'secondary_diagonal': secondary_diag,
            'secondary_diagonal_size': len(secondary_diag),
            'min_on_secondary_diag': min_val,
            'min_position': min_pos,
            'variance_numpy': self.calculate_variance_numpy(secondary_diag),
            'variance_formula': self.calculate_variance_formula(secondary_diag),
            'mean': np.mean(secondary_diag),
            'std': np.std(secondary_diag)
        }

    def display_matrix(self) -> None:
        """Display matrix in a formatted way"""
        print("\n" + "=" * 60)
        print("MATRIX:")
        print("=" * 60)
        for i in range(self.n):
            row_str = "  "
            for j in range(self.m):
                if j == self.n - 1 - i:
                    row_str += f"[{self.matrix[i, j]:4d}] "
                else:
                    row_str += f" {self.matrix[i, j]:4d}  "
            print(row_str)

    def display_secondary_diagonal(self) -> None:
        """Display secondary diagonal elements"""
        diag = self.get_secondary_diagonal()
        print("\n" + "=" * 60)
        print("SECONDARY DIAGONAL (Anti-diagonal):")
        print("=" * 60)
        for i, val in enumerate(diag):
            pos = (i, self.n - 1 - i)
            print(f"  Position [{pos[0]}, {pos[1]}]: {val}")