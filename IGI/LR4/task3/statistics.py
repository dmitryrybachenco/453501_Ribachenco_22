import math
from typing import List, Dict, Any
from collections import Counter


class StatisticalAnalyzer:
    """Class for statistical analysis of sequences"""

    @staticmethod
    def mean(data: List[float]) -> float:
        """
        Calculate arithmetic mean

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
    def mode(data: List[float]) -> float:
        """
        Calculate mode(s) - most frequent value(s)

        Returns:
            List of mode values
        """
        if not data:
            return 0.0

        counter = Counter(data)
        mode_value = counter.most_common(1)[0][0]
        return mode_value

    @staticmethod
    def variance(data: List[float]) -> float:
        """
        Calculate variance

        Returns:
            Variance
        """

        mean_val = StatisticalAnalyzer.mean(data)
        squared_diff = sum((x - mean_val) ** 2 for x in data)
        return squared_diff / len(data)

    @staticmethod
    def std_deviation(data: List[float]) -> float:
        """
        Calculate standard deviation

        Returns:
            Standard deviation
        """
        return math.sqrt(StatisticalAnalyzer.variance(data))

    @staticmethod
    def get_all_statistics(data: List[float]) -> Dict[str, Any]:
        """
        Calculate all statistical parameters

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