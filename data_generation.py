"""
Data generation module for overlapping Gaussian distributions.
Generates 2D multivariate normal distributions with equilateral triangle arrangement.

Following PRD specifications:
- Three distributions arranged in equilateral triangle
- Radius from origin: 2.0 units
- Shared covariance matrix: [[3.85, 0], [0, 3.85]]
- Positions: 0°, 120°, 240° (equilateral triangle)
"""

import numpy as np


def generate_gaussian_dataset(n=10000, seed=42):
    """
    Generate synthetic dataset with three overlapping 2D Gaussian distributions.

    Distributions are arranged in an equilateral triangle pattern with:
    - Group 1 mean: [2.0, 0.0] (0° angle)
    - Group 2 mean: [-1.0, 1.732] (120° angle)
    - Group 3 mean: [-1.0, -1.732] (240° angle)
    - Shared covariance: [[3.85, 0], [0, 3.85]] for all groups

    This configuration ensures approximately 30-35% overlap region.

    Args:
        n (int): Total population size (must be divisible by 3)
        seed (int): Random seed for reproducibility (default: 42)

    Returns:
        dict: Contains 'data' (Nx2 array), 'labels' (N array), and 'params' (distribution parameters)
    """
    if n % 3 != 0:
        raise ValueError("Population size must be divisible by 3")

    np.random.seed(seed)

    points_per_group = n // 3

    # PRD FR2: Distribution Configuration
    # Equilateral triangle arrangement with radius = 2.0
    # Shared covariance matrix for all three distributions
    shared_cov = np.array([[3.85, 0.0], [0.0, 3.85]])

    params = {
        'Group 1': {
            'mean': np.array([2.0, 0.0]),           # 0° position
            'cov': shared_cov.copy(),
            'color': '#FF0000',                      # Red
            'edge_color': '#8B0000'                  # Dark red
        },
        'Group 2': {
            'mean': np.array([-1.0, 1.732]),        # 120° position
            'cov': shared_cov.copy(),
            'color': '#0000FF',                      # Blue
            'edge_color': '#00008B'                  # Dark blue
        },
        'Group 3': {
            'mean': np.array([-1.0, -1.732]),       # 240° position
            'cov': shared_cov.copy(),
            'color': '#008000',                      # Green
            'edge_color': '#006400'                  # Dark green
        }
    }

    # PRD FR1: Data Generation
    # Use numpy.random.multivariate_normal for sampling
    data_group1 = np.random.multivariate_normal(
        params['Group 1']['mean'],
        params['Group 1']['cov'],
        points_per_group
    )
    data_group2 = np.random.multivariate_normal(
        params['Group 2']['mean'],
        params['Group 2']['cov'],
        points_per_group
    )
    data_group3 = np.random.multivariate_normal(
        params['Group 3']['mean'],
        params['Group 3']['cov'],
        points_per_group
    )

    # Combine all data
    data = np.vstack([data_group1, data_group2, data_group3])
    labels = np.array([1]*points_per_group + [2]*points_per_group + [3]*points_per_group)

    return {
        'data': data,
        'labels': labels,
        'params': params,
        'n_per_group': points_per_group
    }
