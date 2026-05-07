import math
from typing import List, Tuple, Dict


class SeriesExpansion:
    """Class for series expansion calculations"""

    def __init__(self, x_values: List[float], epsilon: float = 1e-10, max_terms: int = 100):
        """
        Initialize series expansion

        Args:
            x_values: List of x values to evaluate
            epsilon: Required precision
            max_terms: Maximum number of terms to sum
        """
        self.x_values = x_values
        self.epsilon = epsilon
        self.max_terms = max_terms
        self._results = []
        self._calculate_all()

    def _calculate_term(self, n: int, x: float) -> float:
        """
        Calculate nth term of arcsin series using recurrence

        Args:
            n: Term index
            x: Input value

        Returns:
            nth term value
        """
        if n == 0:
            return x

        term = x
        for i in range(1, n + 1):
            term *= ((2 * i - 1) ** 2 * x ** 2) / (2 * i * (2 * i + 1))
        return term

    def _calculate_series(self, x: float) -> Tuple[float, int]:
        """
        Calculate series sum for a given x

        Args:
            x: Input value

        Returns:
            Tuple (series_sum, number_of_terms_used)
        """
        if abs(x) >= 1:
            raise ValueError(f"|x| must be < 1 for arcsin series. Got x={x}")

        series_sum = 0.0
        n = 0

        while n < self.max_terms:
            term = self._calculate_term(n, x)
            series_sum += term
            n += 1

            if abs(term) < self.epsilon:
                break

        return series_sum, n

    def _calculate_all(self) -> None:
        """Calculate series for all x values"""
        self._results = []
        for x in self.x_values:
            try:
                series_value, n_terms = self._calculate_series(x)
                math_value = math.asin(x)
                error = abs(series_value - math_value)
                self._results.append({
                    'x': x,
                    'series_value': series_value,
                    'math_value': math_value,
                    'n_terms': n_terms,
                    'error': error
                })
            except ValueError as e:
                print(f"Warning: {e}")
                self._results.append({
                    'x': x,
                    'series_value': None,
                    'math_value': math.asin(x) if abs(x) <= 1 else None,
                    'n_terms': 0,
                    'error': None
                })

    def get_results(self) -> List[Dict]:
        """Get calculation results"""
        return self._results

    def get_series_values(self) -> List[float]:
        """Get series values list"""
        return [r['series_value'] for r in self._results if r['series_value'] is not None]

    def get_math_values(self) -> List[float]:
        """Get math.asin values list"""
        return [r['math_value'] for r in self._results if r['math_value'] is not None]

    def get_x_values(self) -> List[float]:
        """Get x values list"""
        return self.x_values

    def get_errors(self) -> List[float]:
        """Get error values list"""
        return [r['error'] for r in self._results if r['error'] is not None]