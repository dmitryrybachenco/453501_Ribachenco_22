import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from typing import Optional
from .shapes import Parallelogram


class ParallelogramDrawer:
    """Class for drawing parallelograms"""

    def __init__(self, parallelogram: Parallelogram):
        """
        Initialize drawer with parallelogram

        Args:
            parallelogram: Parallelogram object to draw
        """
        self.parallelogram = parallelogram

    def draw(self, title: str = "Parallelogram", save_path: Optional[str] = None) -> None:
        """
        Draw the parallelogram using matplotlib

        Args:
            title: Plot title
            save_path: Path to save the image (optional)
        """
        vertices = self.parallelogram.get_vertices()

        fig, ax = plt.subplots(figsize=(10, 8))

        polygon = patches.Polygon(vertices, closed=True,
                                 facecolor=self.parallelogram.get_color(),
                                 edgecolor='black',
                                 linewidth=2,
                                 alpha=0.7)
        ax.add_patch(polygon)

        for i, (x, y) in enumerate(vertices):
            ax.plot(x, y, 'ro', markersize=8)
            ax.annotate(f' {chr(65+i)}', (x, y), fontsize=12, fontweight='bold')

        mid_a_x = (vertices[0][0] + vertices[1][0]) / 2
        mid_a_y = (vertices[0][1] + vertices[1][1]) / 2
        mid_b_x = (vertices[0][0] + vertices[3][0]) / 2
        mid_b_y = (vertices[0][1] + vertices[3][1]) / 2

        ax.annotate(f'a = {self.parallelogram.side_a:.2f}',
                   (mid_a_x, mid_a_y - 0.3),
                   fontsize=10, ha='center',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        ax.annotate(f'b = {self.parallelogram.side_b:.2f}',
                   (mid_b_x - 0.5, mid_b_y),
                   fontsize=10, ha='center',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        angle_rad = self.parallelogram.get_angle_rad()
        arc_radius = min(self.parallelogram.side_a, self.parallelogram.side_b) * 0.3
        arc_theta = np.linspace(0, angle_rad, 50)
        arc_x = arc_radius * np.cos(arc_theta)
        arc_y = arc_radius * np.sin(arc_theta)
        ax.plot(arc_x, arc_y, 'k--', linewidth=1)
        ax.annotate(f'{self.parallelogram.angle_deg:.0f}°',
                   (arc_radius * 0.7 * np.cos(angle_rad/2),
                    arc_radius * 0.7 * np.sin(angle_rad/2)),
                   fontsize=10,
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        ax.set_aspect('equal')
        ax.set_xlabel('X', fontsize=12)
        ax.set_ylabel('Y', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)

        info_text = self.parallelogram.get_info()
        ax.text(0.02, 0.98, info_text, transform=ax.transAxes, fontsize=10,
               verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

        margin = max(self.parallelogram.side_a, self.parallelogram.side_b) * 0.2
        all_x = [v[0] for v in vertices]
        all_y = [v[1] for v in vertices]
        ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
        ax.set_ylim(min(all_y) - margin, max(all_y) + margin)

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"Figure saved to {save_path}")

        plt.show()

    def save_to_file(self, filename: str) -> None:
        """
        Save shape information to text file

        Args:
            filename: Name of file to save
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("PARALLELOGRAM INFORMATION\n")
            f.write("=" * 60 + "\n\n")

            params = self.parallelogram.get_parameters()
            f.write("BASIC PARAMETERS:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Side a: {params['side_a']:.2f}\n")
            f.write(f"Side b: {params['side_b']:.2f}\n")
            f.write(f"Angle: {params['angle_deg']:.1f}°\n")
            f.write(f"Angle (rad): {params['angle_rad']:.4f}\n\n")

            f.write("GEOMETRIC CHARACTERISTICS:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Area: {params['area']:.2f}\n")
            f.write(f"Perimeter: {params['perimeter']:.2f}\n")
            f.write(f"Height: {params['height']:.2f}\n")
            f.write(f"Diagonal 1: {params['diagonal1']:.2f}\n")
            f.write(f"Diagonal 2: {params['diagonal2']:.2f}\n\n")

            f.write("VISUAL PARAMETERS:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Color: {self.parallelogram.get_color()}\n")
            f.write(f"Shape type: {self.parallelogram.get_shape_name()}\n")
            f.write("\n" + "=" * 60 + "\n")

        print(f"Information saved to {filename}")