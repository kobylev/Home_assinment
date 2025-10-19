"""
Statistics module for overlapping groups analysis.
Handles statistical calculations and verification.
"""

import numpy as np
import pandas as pd


def calculate_group_stats(group_A, group_B, group_C):
    """
    Calculate mean, variance, and standard deviation for each group.

    Args:
        group_A (np.ndarray): Data for Group A
        group_B (np.ndarray): Data for Group B
        group_C (np.ndarray): Data for Group C

    Returns:
        dict: Statistics for each group
    """
    stats = {
        'Group A': {
            'n': len(group_A),
            'mean': np.mean(group_A),
            'variance': np.var(group_A, ddof=1),  # Sample variance
            'std': np.std(group_A, ddof=1)
        },
        'Group B': {
            'n': len(group_B),
            'mean': np.mean(group_B),
            'variance': np.var(group_B, ddof=1),
            'std': np.std(group_B, ddof=1)
        },
        'Group C': {
            'n': len(group_C),
            'mean': np.mean(group_C),
            'variance': np.var(group_C, ddof=1),
            'std': np.std(group_C, ddof=1)
        }
    }
    return stats


def print_statistics(distribution, stats):
    """
    Print formatted statistics output.

    Args:
        distribution (dict): Point distribution across regions
        stats (dict): Group statistics
    """
    print("=" * 60)
    print("STATISTICAL ANALYSIS OF OVERLAPPING GROUPS")
    print("=" * 60)
    print("\nPoint Distribution by Region:")
    print("-" * 60)
    for region, count in distribution.items():
        print(f"{region:15s}: {count:4d} points")
    print(f"{'Total Unique':15s}: {sum(distribution.values()):4d} points")

    print("\n" + "=" * 60)
    print("GROUP STATISTICS")
    print("=" * 60)
    for group_name, stat in stats.items():
        print(f"\n{group_name}:")
        print(f"  Sample Size (n)    : {stat['n']}")
        print(f"  Mean (mu-hat)      : {stat['mean']:.4f}")
        print(f"  Variance (sigma^2) : {stat['variance']:.4f}")
        print(f"  Std Deviation (s)  : {stat['std']:.4f}")


def verify_constraints(group_A, group_B, group_C, distribution):
    """
    Verify that all constraints are satisfied.

    Args:
        group_A (np.ndarray): Data for Group A
        group_B (np.ndarray): Data for Group B
        group_C (np.ndarray): Data for Group C
        distribution (dict): Point distribution across regions
    """
    print("\n" + "=" * 60)
    print("CONSTRAINT VERIFICATION")
    print("=" * 60)
    print(f"Group A total: {len(group_A)} (expected: 2000) [OK]" if len(group_A) == 2000 else f"Group A total: {len(group_A)} (expected: 2000) [FAIL]")
    print(f"Group B total: {len(group_B)} (expected: 2000) [OK]" if len(group_B) == 2000 else f"Group B total: {len(group_B)} (expected: 2000) [FAIL]")
    print(f"Group C total: {len(group_C)} (expected: 2000) [OK]" if len(group_C) == 2000 else f"Group C total: {len(group_C)} (expected: 2000) [FAIL]")
    print(f"\nABC intersection: {distribution['ABC']} points")
    print(f"  Percentage of Group A: {distribution['ABC']/2000*100:.1f}%")
    print(f"  Percentage of Group B: {distribution['ABC']/2000*100:.1f}%")
    print(f"  Percentage of Group C: {distribution['ABC']/2000*100:.1f}%")


def save_statistics(stats, filename='group_statistics.csv'):
    """
    Save statistics to CSV file.

    Args:
        stats (dict): Group statistics
        filename (str): Output filename
    """
    stats_df = pd.DataFrame(stats).T
    stats_df.to_csv(filename)
    print(f"\n[OK] Statistics saved to '{filename}'")


def save_data(group_A, group_B, group_C, distribution, filename='group_data.npz'):
    """
    Save raw data to NPZ file.

    Args:
        group_A (np.ndarray): Data for Group A
        group_B (np.ndarray): Data for Group B
        group_C (np.ndarray): Data for Group C
        distribution (dict): Point distribution across regions
        filename (str): Output filename
    """
    np.savez(filename,
             group_A=group_A,
             group_B=group_B,
             group_C=group_C,
             distribution=distribution)
    print(f"[OK] Data saved to '{filename}'")
