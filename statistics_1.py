"""
Statistics module for overlapping Gaussian distributions.
Calculates means, covariances, overlap detection, and statistical summaries.

Following PRD specifications:
- PDF-based overlap detection
- Threshold: 20% of center point's minimum PDF
- Target overlap: 30-35% of total points
"""

import numpy as np
from scipy.stats import multivariate_normal


def calculate_statistics(data, labels, true_params):
    """
    Calculate comprehensive statistics for each distribution.

    PRD FR4: Statistical Analysis
    Calculates sample mean, std dev, covariance for each group.

    Args:
        data (np.ndarray): Nx2 array of data points
        labels (np.ndarray): N array of group labels (1, 2, 3)
        true_params (dict): True distribution parameters

    Returns:
        dict: Statistics for each group including means, covariances, and comparisons
    """
    stats = {}

    for group_idx, group_name in enumerate(['Group 1', 'Group 2', 'Group 3'], start=1):
        # Extract group data
        group_data = data[labels == group_idx]

        # Calculate sample statistics (MLE estimators)
        sample_mean = np.mean(group_data, axis=0)
        sample_cov = np.cov(group_data, rowvar=False)

        # Get true parameters
        true_mean = true_params[group_name]['mean']
        true_cov = true_params[group_name]['cov']

        # Calculate standard deviations
        sample_std = np.sqrt(np.diag(sample_cov))
        true_std = np.sqrt(np.diag(true_cov))

        stats[group_name] = {
            'n': len(group_data),
            'sample_mean': sample_mean,
            'true_mean': true_mean,
            'sample_cov': sample_cov,
            'true_cov': true_cov,
            'sample_std': sample_std,
            'true_std': true_std,
            'color': true_params[group_name]['color'],
            'edge_color': true_params[group_name]['edge_color']
        }

    return stats


def detect_overlap_region(data, labels, stats):
    """
    Detect points in the overlap region using PDF-based method.

    PRD FR3: Overlap Region Detection
    Algorithm:
    1. Calculate PDF for each point under all three distributions
    2. For each point, find minimum PDF across distributions
    3. Calculate threshold: 20% of center point's minimum PDF
    4. Points with min_pdf > threshold are in overlap region

    This ensures approximately 30-35% of points in overlap region.

    Args:
        data (np.ndarray): Nx2 array of data points
        labels (np.ndarray): N array of group labels
        stats (dict): Statistics for each group

    Returns:
        dict: Contains overlap indices, counts, and percentages
    """
    n_points = len(data)

    # Step 1: Create multivariate normal distributions for each group
    distributions = []
    for group_name in ['Group 1', 'Group 2', 'Group 3']:
        mean = stats[group_name]['true_mean']  # Use true params for overlap detection
        cov = stats[group_name]['true_cov']
        distributions.append(multivariate_normal(mean=mean, cov=cov))

    # Step 2: Calculate PDF for each point under all distributions
    pdfs = np.zeros((n_points, 3))
    for i, dist in enumerate(distributions):
        pdfs[:, i] = dist.pdf(data)

    # Step 3: Calculate minimum PDF for each point
    min_pdfs = np.min(pdfs, axis=1)

    # Step 4: Calculate threshold based on center point
    # Center point is the centroid of the three means
    center_point = np.mean([stats[gn]['true_mean'] for gn in ['Group 1', 'Group 2', 'Group 3']], axis=0)
    center_pdfs = np.array([dist.pdf(center_point) for dist in distributions])
    center_min_pdf = np.min(center_pdfs)
    threshold = 0.20 * center_min_pdf

    # Step 5: Identify overlap region
    # Points where minimum PDF > threshold are in overlap region
    overlap_mask = min_pdfs > threshold

    overlap_indices = np.where(overlap_mask)[0]
    overlap_count = len(overlap_indices)
    overlap_percentage = (overlap_count / n_points) * 100

    # Count overlap points per group
    group_overlap_counts = {}
    for group_idx, group_name in enumerate(['Group 1', 'Group 2', 'Group 3'], start=1):
        group_mask = labels == group_idx
        group_overlap_mask = overlap_mask & group_mask
        count = np.sum(group_overlap_mask)
        percentage = (count / np.sum(group_mask)) * 100
        group_overlap_counts[group_name] = {
            'count': count,
            'percentage': percentage
        }

    return {
        'overlap_indices': overlap_indices,
        'overlap_mask': overlap_mask,
        'total_overlap_count': overlap_count,
        'total_overlap_percentage': overlap_percentage,
        'group_overlap_counts': group_overlap_counts,
        'threshold': threshold,
        'center_point': center_point,
        'center_min_pdf': center_min_pdf
    }


def print_statistics(stats, overlap_info, n_total):
    """
    Print formatted statistical summary to console.

    Args:
        stats (dict): Statistics for each group
        overlap_info (dict): Overlap detection results
        n_total (int): Total number of points
    """
    print("\n" + "=" * 80)
    print(" " * 20 + "STATISTICAL SUMMARY")
    print("=" * 80)

    for group_name, stat in stats.items():
        print(f"\n{group_name}:")
        print("-" * 80)
        print(f"  Sample Size: {stat['n']} points")
        print(f"\n  Mean Vector:")
        print(f"    True:   [{stat['true_mean'][0]:7.4f}, {stat['true_mean'][1]:7.4f}]")
        print(f"    Sample: [{stat['sample_mean'][0]:7.4f}, {stat['sample_mean'][1]:7.4f}]")
        print(f"\n  Standard Deviations:")
        print(f"    True (X):   {stat['true_std'][0]:.4f}")
        print(f"    Sample (X): {stat['sample_std'][0]:.4f}")
        print(f"    True (Y):   {stat['true_std'][1]:.4f}")
        print(f"    Sample (Y): {stat['sample_std'][1]:.4f}")
        print(f"\n  Covariance Matrix (Sample):")
        print(f"    [{stat['sample_cov'][0,0]:7.4f}, {stat['sample_cov'][0,1]:7.4f}]")
        print(f"    [{stat['sample_cov'][1,0]:7.4f}, {stat['sample_cov'][1,1]:7.4f}]")

    print("\n" + "=" * 80)
    print(" " * 25 + "OVERLAP ANALYSIS")
    print("=" * 80)
    print(f"\nTotal Points in Overlap Region: {overlap_info['total_overlap_count']} / {n_total}")
    print(f"Overlap Percentage: {overlap_info['total_overlap_percentage']:.2f}%")
    print("\nOverlap by Group:")
    for group_name, counts in overlap_info['group_overlap_counts'].items():
        print(f"  {group_name}: {counts['count']} points ({counts['percentage']:.2f}%)")
    print("=" * 80)
