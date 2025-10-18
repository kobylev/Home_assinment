"""
Visualization module for overlapping groups analysis.
Handles creation of Venn diagrams and distribution plots.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Circle


def create_venn_diagram(distribution, filename='venn_diagram.png'):
    """
    Create and save a Venn diagram showing point distribution.

    Args:
        distribution (dict): Point distribution across regions
        filename (str): Output filename
    """
    fig, ax = plt.subplots(figsize=(12, 10))

    # Draw three circles
    circle_A = Circle((0.35, 0.5), 0.3, color='red', alpha=0.3, label='Group A')
    circle_B = Circle((0.65, 0.5), 0.3, color='blue', alpha=0.3, label='Group B')
    circle_C = Circle((0.5, 0.25), 0.3, color='green', alpha=0.3, label='Group C')

    ax.add_patch(circle_A)
    ax.add_patch(circle_B)
    ax.add_patch(circle_C)

    # Add labels for regions
    ax.text(0.20, 0.60, str(distribution['A_only']), fontsize=14, fontweight='bold', ha='center')  # A only
    ax.text(0.80, 0.60, str(distribution['B_only']), fontsize=14, fontweight='bold', ha='center')  # B only
    ax.text(0.50, 0.10, str(distribution['C_only']), fontsize=14, fontweight='bold', ha='center')  # C only
    ax.text(0.50, 0.60, str(distribution['AB_only']), fontsize=14, fontweight='bold', ha='center')  # AB only
    ax.text(0.35, 0.30, str(distribution['AC_only']), fontsize=14, fontweight='bold', ha='center')  # AC only
    ax.text(0.65, 0.30, str(distribution['BC_only']), fontsize=14, fontweight='bold', ha='center')  # BC only
    ax.text(0.50, 0.42, str(distribution['ABC']), fontsize=14, fontweight='bold', ha='center')  # ABC

    # Add group labels
    ax.text(0.20, 0.85, 'Group A\n(2000 points)', fontsize=12, fontweight='bold',
            ha='center', bbox=dict(boxstyle='round', facecolor='red', alpha=0.5))
    ax.text(0.80, 0.85, 'Group B\n(2000 points)', fontsize=12, fontweight='bold',
            ha='center', bbox=dict(boxstyle='round', facecolor='blue', alpha=0.5))
    ax.text(0.50, -0.10, 'Group C\n(2000 points)', fontsize=12, fontweight='bold',
            ha='center', bbox=dict(boxstyle='round', facecolor='green', alpha=0.5))

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
    print(f"✓ Venn diagram saved to '{filename}'")


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
    print(f"✓ Distribution histograms saved to '{filename}'")
