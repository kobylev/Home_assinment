"""
Visualization module for overlapping Gaussian distributions.
Creates dual-panel visualizations with confidence ellipses and overlap highlighting.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from scipy.spatial import ConvexHull
from matplotlib.collections import PatchCollection


def plot_confidence_ellipse(ax, mean, cov, n_std=2, facecolor='none', edgecolor='black', linewidth=2, **kwargs):
    """
    Plot a confidence ellipse for a 2D Gaussian distribution.

    Args:
        ax: Matplotlib axis object
        mean: Mean vector [x, y]
        cov: 2x2 covariance matrix
        n_std: Number of standard deviations for the ellipse
        facecolor: Fill color
        edgecolor: Edge color
        linewidth: Line width
    """
    # Calculate eigenvalues and eigenvectors for ellipse orientation
    eigenvalues, eigenvectors = np.linalg.eig(cov)
    angle = np.degrees(np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0]))

    # Width and height are 2*n_std times the sqrt of eigenvalues
    width, height = 2 * n_std * np.sqrt(eigenvalues)

    ellipse = Ellipse(mean, width, height, angle=angle,
                     facecolor=facecolor, edgecolor=edgecolor,
                     linewidth=linewidth, **kwargs)
    ax.add_patch(ellipse)


def create_dual_panel_visualization(data, labels, stats, overlap_info, filename='gaussian_overlap_analysis.png'):
    """
    Create dual-panel visualization: (1) Distribution view, (2) Overlap view.

    Args:
        data (np.ndarray): Nx2 array of data points
        labels (np.ndarray): N array of group labels
        stats (dict): Statistics for each group
        overlap_info (dict): Overlap detection results
        filename (str): Output filename
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

    # Color scheme
    colors = {
        'Group 1': '#FF0000',  # Red
        'Group 2': '#0000FF',  # Blue
        'Group 3': '#008000'   # Green
    }
    edge_colors = {
        'Group 1': '#8B0000',  # Dark red
        'Group 2': '#00008B',  # Dark blue
        'Group 3': '#006400'   # Dark green
    }

    # ==================== LEFT PANEL: Distribution View ====================
    ax1.set_facecolor('white')
    ax1.grid(True, alpha=0.3, color='lightgray')

    # Plot points for each group
    for group_idx, group_name in enumerate(['Group 1', 'Group 2', 'Group 3'], start=1):
        group_data = data[labels == group_idx]
        ax1.scatter(group_data[:, 0], group_data[:, 1],
                   c=colors[group_name], s=15, alpha=0.5,
                   edgecolors=edge_colors[group_name], linewidths=0.5,
                   label=group_name, zorder=2)

        # Plot mean
        mean = stats[group_name]['sample_mean']
        ax1.scatter(mean[0], mean[1], c='black', s=200, marker='X',
                   edgecolors='white', linewidths=2, zorder=5)
        ax1.text(mean[0], mean[1] + 0.3, f'{group_name}\nMean',
                ha='center', va='bottom', fontweight='bold', fontsize=9,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

        # Plot confidence ellipse (2 standard deviations = ~95%)
        plot_confidence_ellipse(ax1, stats[group_name]['sample_mean'],
                              stats[group_name]['sample_cov'],
                              n_std=2, edgecolor=edge_colors[group_name],
                              linewidth=2, linestyle='--', alpha=0.7, zorder=3)

    # Add statistics box
    textstr = f'Total Points: {len(data)}\n'
    for group_name in ['Group 1', 'Group 2', 'Group 3']:
        textstr += f'{group_name}: {stats[group_name]["n"]}\n'
    textstr += f'\nOverlap: {overlap_info["total_overlap_count"]} '
    textstr += f'({overlap_info["total_overlap_percentage"]:.1f}%)'

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    ax1.text(0.02, 0.98, textstr, transform=ax1.transAxes, fontsize=9,
            verticalalignment='top', fontfamily='monospace', bbox=props)

    ax1.set_xlabel('X', fontweight='bold', fontsize=12)
    ax1.set_ylabel('Y', fontweight='bold', fontsize=12)
    ax1.set_title('Distribution View', fontweight='bold', fontsize=14)
    ax1.legend(loc='upper right', fontsize=8, framealpha=0.9)

    # ==================== RIGHT PANEL: Overlap View ====================
    ax2.set_facecolor('white')
    ax2.grid(True, alpha=0.3, color='lightgray')

    overlap_mask = overlap_info['overlap_mask']

    # Plot non-overlap points (faded)
    non_overlap_data = data[~overlap_mask]
    non_overlap_labels = labels[~overlap_mask]

    for group_idx, group_name in enumerate(['Group 1', 'Group 2', 'Group 3'], start=1):
        group_data = non_overlap_data[non_overlap_labels == group_idx]
        ax2.scatter(group_data[:, 0], group_data[:, 1],
                   c=colors[group_name], s=10, alpha=0.15,
                   edgecolors='none', zorder=1)

    # Plot overlap points (highlighted)
    overlap_data = data[overlap_mask]
    overlap_labels_arr = labels[overlap_mask]

    for group_idx, group_name in enumerate(['Group 1', 'Group 2', 'Group 3'], start=1):
        group_overlap_data = overlap_data[overlap_labels_arr == group_idx]
        ax2.scatter(group_overlap_data[:, 0], group_overlap_data[:, 1],
                   c='#FFFF00', s=20, alpha=0.7,  # Yellow fill
                   edgecolors='#FFA500', linewidths=1,  # Orange edges
                   label=f'{group_name} (overlap)', zorder=3)

    # Draw convex hull around overlap region
    if len(overlap_data) > 2:
        try:
            hull = ConvexHull(overlap_data)
            hull_points = overlap_data[hull.vertices]
            hull_points = np.vstack([hull_points, hull_points[0]])  # Close the polygon
            ax2.plot(hull_points[:, 0], hull_points[:, 1],
                    'orange', linewidth=2.5, linestyle='-',
                    label='Overlap Region Boundary', zorder=4)
            ax2.fill(hull_points[:, 0], hull_points[:, 1],
                    color='#FFFF00', alpha=0.2, zorder=2)
        except:
            pass  # Skip if convex hull fails

    # Plot confidence ellipses (lighter)
    for group_idx, group_name in enumerate(['Group 1', 'Group 2', 'Group 3'], start=1):
        plot_confidence_ellipse(ax2, stats[group_name]['sample_mean'],
                              stats[group_name]['sample_cov'],
                              n_std=2, edgecolor=edge_colors[group_name],
                              linewidth=1.5, linestyle=':', alpha=0.4, zorder=3)

    # Add group counts box
    textstr = 'Overlap Points by Group:\n'
    for group_name, counts in overlap_info['group_overlap_counts'].items():
        textstr += f'{group_name}: {counts["count"]} ({counts["percentage"]:.1f}%)\n'

    props = dict(boxstyle='round', facecolor='lightyellow', alpha=0.9)
    ax2.text(0.02, 0.98, textstr, transform=ax2.transAxes, fontsize=9,
            verticalalignment='top', fontfamily='monospace', bbox=props)

    ax2.set_xlabel('X', fontweight='bold', fontsize=12)
    ax2.set_ylabel('Y', fontweight='bold', fontsize=12)
    ax2.set_title('Overlap View', fontweight='bold', fontsize=14)
    ax2.legend(loc='upper right', fontsize=8, framealpha=0.9)

    # Match axis limits
    all_data = data
    x_margin = (all_data[:, 0].max() - all_data[:, 0].min()) * 0.1
    y_margin = (all_data[:, 1].max() - all_data[:, 1].min()) * 0.1
    ax1.set_xlim(all_data[:, 0].min() - x_margin, all_data[:, 0].max() + x_margin)
    ax1.set_ylim(all_data[:, 1].min() - y_margin, all_data[:, 1].max() + y_margin)
    ax2.set_xlim(all_data[:, 0].min() - x_margin, all_data[:, 0].max() + x_margin)
    ax2.set_ylim(all_data[:, 1].min() - y_margin, all_data[:, 1].max() + y_margin)

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"[OK] Dual-panel visualization saved to '{filename}'")
