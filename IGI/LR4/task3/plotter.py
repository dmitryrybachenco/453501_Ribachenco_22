import matplotlib.pyplot as plt
from typing import List, Dict, Optional


class SeriesPlotter:
    """Class for plotting series and math function graphs"""

    def __init__(self, results: List[Dict]):
        """
        Initialize plotter with results

        Args:
            results: List of calculation results
        """
        self.results = results
        self.x_values = [r['x'] for r in results if r['series_value'] is not None]
        self.series_values = [r['series_value'] for r in results if r['series_value'] is not None]
        self.math_values = [r['math_value'] for r in results if r['math_value'] is not None]
        self.errors = [r['error'] for r in results if r['error'] is not None]
        self.n_terms = [r['n_terms'] for r in results if r['series_value'] is not None]

    def create_plot(self, save_path: Optional[str] = None) -> None:
        """
        Create a simple single-plot visualization

        Args:
            save_path: Path to save the plot (optional)
        """
        plt.figure(figsize=(12, 8))

        plt.plot(self.x_values, self.series_values, 'b-', linewidth=2,
                 label='Series Expansion (arcsin x)', marker='o', markersize=4)
        plt.plot(self.x_values, self.math_values, 'r--', linewidth=2,
                 label='math.asin(x)', marker='s', markersize=4)

        plt.xlabel('x', fontsize=12)
        plt.ylabel('arcsin(x)', fontsize=12)
        plt.title('arcsin(x): Series Expansion vs math.asin()', fontsize=14)
        plt.legend(loc='best', fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.axhline(y=0, color='k', linewidth=0.5)
        plt.axvline(x=0, color='k', linewidth=0.5)

        # Add annotation
        plt.text(0.05, 0.95, 'Domain: |x| < 1\nSeries: ∑(2n)!/(4^n(n!)²(2n+1)) × x^(2n+1)',
                 transform=plt.gca().transAxes, fontsize=10, verticalalignment='top',
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"Plot saved to {save_path}")

        plt.show()

    def create_table(self) -> str:
        """
        Create a formatted table of results

        Returns:
            Formatted table string
        """
        table = "\n" + "=" * 85 + "\n"
        table += "RESULTS TABLE\n"
        table += "=" * 85 + "\n"
        table += f"{'x':>10} | {'Series F(x)':>18} | {'Math F(x)':>18} | {'n':>6} | {'Error':>15}\n"
        table += "-" * 85 + "\n"

        for r in self.results:
            if r['series_value'] is not None:
                table += (f"{r['x']:>10.6f} | {r['series_value']:>18.12f} | "
                          f"{r['math_value']:>18.12f} | {r['n_terms']:>6} | {r['error']:>15.10e}\n")

        table += "=" * 85 + "\n"
        return table