"""
Data generation module for overlapping groups analysis.
Handles point distribution and data sampling.
"""

import numpy as np


def get_distribution():
    """
    Returns the point distribution across all regions.

    Returns:
        dict: Distribution of points across regions
    """
    # Constraint: ABC should be ~1/3 of each group (i.e., ~667 points per group)
    # Each group has 2000 points, so ABC = 667 is approximately 1/3
    distribution = {
        'A_only': 700,
        'B_only': 733,
        'C_only': 700,
        'AB_only': 300,
        'AC_only': 333,
        'BC_only': 300,
        'ABC': 667
    }
    return distribution


def generate_data(distribution, seed=42):
    """
    Generate data points with different Gaussian distributions for each region.

    Args:
        distribution (dict): Point distribution across regions
        seed (int): Random seed for reproducibility

    Returns:
        dict: Data arrays for each region
    """
    np.random.seed(seed)

    # Using different Gaussian distributions to simulate distinct groups
    data = {
        'A_only': np.random.normal(loc=10, scale=2, size=distribution['A_only']),
        'B_only': np.random.normal(loc=15, scale=2.5, size=distribution['B_only']),
        'C_only': np.random.normal(loc=20, scale=3, size=distribution['C_only']),
        'AB_only': np.random.normal(loc=12.5, scale=2, size=distribution['AB_only']),
        'AC_only': np.random.normal(loc=15, scale=2.5, size=distribution['AC_only']),
        'BC_only': np.random.normal(loc=17.5, scale=2.5, size=distribution['BC_only']),
        'ABC': np.random.normal(loc=15, scale=2, size=distribution['ABC'])
    }

    return data


def combine_groups(data):
    """
    Combine data into three groups based on overlapping regions.

    Args:
        data (dict): Data arrays for each region

    Returns:
        tuple: (group_A, group_B, group_C) numpy arrays
    """
    group_A = np.concatenate([data['A_only'], data['AB_only'], data['AC_only'], data['ABC']])
    group_B = np.concatenate([data['B_only'], data['AB_only'], data['BC_only'], data['ABC']])
    group_C = np.concatenate([data['C_only'], data['AC_only'], data['BC_only'], data['ABC']])

    return group_A, group_B, group_C
