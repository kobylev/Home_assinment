"""
Visualization module for overlapping groups analysis.
Handles creation of Venn diagrams and distribution plots.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


def create_venn_diagram(distribution, filename='venn_diagram.png', data=None):
    """
    Create and save a Venn diagram showing point distribution.

    Args:
        distribution (dict): Point distribution across regions
        filename (str): Output filename
        data (dict, optional): Dictionary containing data arrays for each region
    """
    fig, ax = plt.subplots(figsize=(12, 10))

    # Draw three circles with lighter colors
    circle_A = Circle((0.35, 0.5), 0.3, color='#FFB3B3', alpha=0.5, label='Group A')  # Light red
    circle_B = Circle((0.65, 0.5), 0.3, color='#B3C7FF', alpha=0.5, label='Group B')  # Light blue
    circle_C = Circle((0.5, 0.25), 0.3, color='#B3FFB3', alpha=0.5, label='Group C')  # Light green

    ax.add_patch(circle_A)
    ax.add_patch(circle_B)
    ax.add_patch(circle_C)

    # Plot actual data points if provided
    if data is not None:
        np.random.seed(42)  # For consistent point placement

        # Function to generate random points within a region
        def generate_region_points(count, center_x, center_y, radius=0.12):
            angles = np.random.uniform(0, 2*np.pi, count)
            radii = np.random.uniform(0, radius, count)
            x = center_x + radii * np.cos(angles)
            y = center_y + radii * np.sin(angles)
            return x, y

        # Plot points for each region with smaller dots
        # A only
        x, y = generate_region_points(distribution['A_only'], 0.20, 0.60)
        ax.scatter(x, y, c='darkred', s=1, alpha=0.6, zorder=3)

        # B only
        x, y = generate_region_points(distribution['B_only'], 0.80, 0.60)
        ax.scatter(x, y, c='darkblue', s=1, alpha=0.6, zorder=3)

        # C only
        x, y = generate_region_points(distribution['C_only'], 0.50, 0.10)
        ax.scatter(x, y, c='darkgreen', s=1, alpha=0.6, zorder=3)

        # AB only
        x, y = generate_region_points(distribution['AB_only'], 0.50, 0.60)
        ax.scatter(x, y, c='purple', s=1, alpha=0.6, zorder=3)

        # AC only
        x, y = generate_region_points(distribution['AC_only'], 0.35, 0.30)
        ax.scatter(x, y, c='brown', s=1, alpha=0.6, zorder=3)

        # BC only
        x, y = generate_region_points(distribution['BC_only'], 0.65, 0.30)
        ax.scatter(x, y, c='teal', s=1, alpha=0.6, zorder=3)

        # ABC (center intersection)
        x, y = generate_region_points(distribution['ABC'], 0.50, 0.42, radius=0.08)
        ax.scatter(x, y, c='black', s=1, alpha=0.7, zorder=3)

    # Add labels for regions with point counts
    ax.text(0.20, 0.75, str(distribution['A_only']), fontsize=14, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))  # A only
    ax.text(0.80, 0.75, str(distribution['B_only']), fontsize=14, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))  # B only
    ax.text(0.50, -0.02, str(distribution['C_only']), fontsize=14, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))  # C only
    ax.text(0.50, 0.70, str(distribution['AB_only']), fontsize=14, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))  # AB only
    ax.text(0.25, 0.28, str(distribution['AC_only']), fontsize=14, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))  # AC only
    ax.text(0.75, 0.28, str(distribution['BC_only']), fontsize=14, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))  # BC only
    ax.text(0.50, 0.42, str(distribution['ABC']), fontsize=14, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9))  # ABC

    # Calculate group totals
    group_A_total = distribution['A_only'] + distribution['AB_only'] + distribution['AC_only'] + distribution['ABC']
    group_B_total = distribution['B_only'] + distribution['AB_only'] + distribution['BC_only'] + distribution['ABC']
    group_C_total = distribution['C_only'] + distribution['AC_only'] + distribution['BC_only'] + distribution['ABC']

    # Add group labels with totals
    ax.text(0.20, 0.85, f'Group A\n({group_A_total} points)', fontsize=12, fontweight='bold',
            ha='center', bbox=dict(boxstyle='round', facecolor='#FF6B6B', alpha=0.7))
    ax.text(0.80, 0.85, f'Group B\n({group_B_total} points)', fontsize=12, fontweight='bold',
            ha='center', bbox=dict(boxstyle='round', facecolor='#6B9AFF', alpha=0.7))
    ax.text(0.50, -0.10, f'Group C\n({group_C_total} points)', fontsize=12, fontweight='bold',
            ha='center', bbox=dict(boxstyle='round', facecolor='#6BFF6B', alpha=0.7))

    ax.set_xlim(0, 1)
    ax.set_ylim(-0.2, 1)
    ax.set_aspect('equal')
    ax.axis('off')

    total_unique = sum(distribution.values())
    ax.set_title(f'Overlapping Groups - Point Distribution\nTotal: {total_unique} unique points | Each group: 2,000 points\nABC intersection: {distribution["ABC"]} points (~33% of each group)',
                 fontsize=16, fontweight='bold', pad=20)

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] Venn diagram saved to '{filename}'")


def create_distribution_histograms(group_A, group_B, group_C, stats, filename='distributions.png'):
    """
    Create and save distribution histograms for all groups.

    Args:
        group_A (np.ndarray): Data for Group A
        group_B (np.ndarray): Data for Group B
        group_C (np.ndarray): Data for Group C
        stats (dict): Group statistics
        filename (str): Output filename
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    # Group A
    axes[0].hist(group_A, bins=30, color='red', alpha=0.7, edgecolor='black')
    axes[0].axvline(stats['Group A']['mean'], color='darkred', linestyle='--',
                    linewidth=2, label=f"μ̂ = {stats['Group A']['mean']:.2f}")
    axes[0].set_title('Group A Distribution', fontweight='bold')
    axes[0].set_xlabel('Value')
    axes[0].set_ylabel('Frequency')
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    # Group B
    axes[1].hist(group_B, bins=30, color='blue', alpha=0.7, edgecolor='black')
    axes[1].axvline(stats['Group B']['mean'], color='darkblue', linestyle='--',
                    linewidth=2, label=f"μ̂ = {stats['Group B']['mean']:.2f}")
    axes[1].set_title('Group B Distribution', fontweight='bold')
    axes[1].set_xlabel('Value')
    axes[1].set_ylabel('Frequency')
    axes[1].legend()
    axes[1].grid(alpha=0.3)

    # Group C
    axes[2].hist(group_C, bins=30, color='green', alpha=0.7, edgecolor='black')
    axes[2].axvline(stats['Group C']['mean'], color='darkgreen', linestyle='--',
                    linewidth=2, label=f"μ̂ = {stats['Group C']['mean']:.2f}")
    axes[2].set_title('Group C Distribution', fontweight='bold')
    axes[2].set_xlabel('Value')
    axes[2].set_ylabel('Frequency')
    axes[2].legend()
    axes[2].grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] Distribution histograms saved to '{filename}'")
