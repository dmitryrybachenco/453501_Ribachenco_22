import math
from typing import List, Dict, Any
from collections import Counter


class StatisticalAnalyzer:
    """Class for statistical analysis of sequences"""

    @staticmethod
    def mean(data: List[float]) -> float:
        """
        Calculate arithmetic mean

        Args:
            data: List of numbers

        Returns:
            Arithmetic mean
        """
        if not data:
            return 0.0
        return sum(data) / len(data)

    @staticmethod
    def median(data: List[float]) -> float:
        """
        Calculate median

        Args:
            data: List of numbers

        Returns:
            Median value
        """
        if not data:
            return 0.0

        sorted_data = sorted(data)
        n = len(sorted_data)
        mid = n // 2

        if n % 2 == 0:
            return (sorted_data[mid - 1] + sorted_data[mid]) / 2
        else:
            return sorted_data[mid]

    @staticmethod
    def mode(data: List[float]) -> List[float]:
        """
        Calculate mode(s) - most frequent value(s)

        Args:
            data: List of numbers

        Returns:
            List of mode values
        """
        if not data:
            return []

        counter = Counter(data)
        max_count = max(counter.values())
        return [value for value, count in counter.items() if count == max_count]

    @staticmethod
    def variance(data: List[float], ddof: int = 1) -> float:
        """
        Calculate variance

        Args:
            data: List of numbers
            ddof: Delta degrees of freedom (0 for population, 1 for sample)

        Returns:
            Variance
        """
        if len(data) <= ddof:
            return 0.0

        mean_val = StatisticalAnalyzer.mean(data)
        squared_diff = sum((x - mean_val) ** 2 for x in data)
        return squared_diff / (len(data) - ddof)

    @staticmethod
    def std_deviation(data: List[float], ddof: int = 1) -> float:
        """
        Calculate standard deviation

        Args:
            data: List of numbers
            ddof: Delta degrees of freedom

        Returns:
            Standard deviation
        """
        return math.sqrt(StatisticalAnalyzer.variance(data, ddof))

    @staticmethod
    def get_all_statistics(data: List[float]) -> Dict[str, Any]:
        """
        Calculate all statistical parameters

        Args:
            data: List of numbers

        Returns:
            Dictionary with all statistics
        """
        if not data:
            return {}

        return {
            'mean': StatisticalAnalyzer.mean(data),
            'median': StatisticalAnalyzer.median(data),
            'mode': StatisticalAnalyzer.mode(data),
            'variance': StatisticalAnalyzer.variance(data),
            'std_deviation': StatisticalAnalyzer.std_deviation(data),
            'min': min(data),
            'max': max(data),
            'count': len(data)
        }