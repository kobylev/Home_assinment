"""
Gaussian Overlap Dataset Generator

A Python tool that generates synthetic 2D datasets consisting of three overlapping
Gaussian distributions arranged in an equilateral triangle pattern.

Following PRD specifications:
- Equilateral triangle arrangement (radius=2.0, angles: 0°, 120°, 240°)
- Shared covariance matrix: [[3.85, 0], [0, 3.85]]
- PDF-based overlap detection (30-35% target)
- Comprehensive statistical analysis and visualization
- Reproducible with seed=42

Usage:
    python main.py [population_size]

Example:
    python main.py 10000

Features (PRD compliant):
- FR1: Pure Gaussian distribution generation with controlled parameters
- FR2: Equilateral triangle configuration for optimal overlap
- FR3: PDF-based overlap detection (threshold = 20% of center min PDF)
- FR4: Comprehensive statistical analysis (mean, std dev, covariance)
- FR5: Distribution view with confidence ellipses
- FR6: Overlap view with convex hull highlighting
- FR7: Formatted console output
- FR8: Interactive matplotlib visualization
"""

import sys
import time
from data_generation import generate_gaussian_dataset
from statistics_1 import calculate_statistics, detect_overlap_region, print_statistics
from visualization import create_dual_panel_visualization


def main(n=10000):
    """
    Main analysis pipeline following PRD specifications.

    Implements the complete workflow:
    1. Data generation with equilateral triangle arrangement
    2. Statistical analysis using MLE estimators
    3. PDF-based overlap detection
    4. Dual-panel visualization creation

    Args:
        n (int): Population size (must be divisible by 3)

    Returns:
        None (outputs to console and file)
    """
    start_time = time.time()

    # PRD FR7: Console Output - Header
    print("\n" + "=" * 80)
    print(" " * 15 + "GAUSSIAN OVERLAP DATASET GENERATOR")
    print("=" * 80)
    print(f"\nPopulation Size: {n:,} points")
    print(f"Distributions: 3 overlapping 2D Gaussians (equilateral triangle)")
    print(f"Arrangement: Radius=2.0, Angles: 0°, 120°, 240°")
    print(f"Covariance: [[3.85, 0], [0, 3.85]] (shared)")
    print(f"Random Seed: 42 (for reproducibility)")
    print("\n" + "-" * 80)

    # PRD FR1: Data Generation
    print("\n[1/4] Generating synthetic dataset...")
    dataset = generate_gaussian_dataset(n=n, seed=42)
    data = dataset['data']
    labels = dataset['labels']
    params = dataset['params']
    print(f"      [OK] Generated {len(data):,} points across 3 groups")
    print(f"      [OK] Each group: {dataset['n_per_group']:,} points")

    # PRD FR4: Statistical Analysis
    print("\n[2/4] Calculating statistics...")
    stats = calculate_statistics(data, labels, params)
    print("      [OK] Computed sample means (MLE)")
    print("      [OK] Computed sample covariances (MLE with Bessel's correction)")
    print("      [OK] Computed standard deviations")

    # PRD FR3: Overlap Region Detection
    print("\n[3/4] Detecting overlap regions (PDF-based)...")
    overlap_info = detect_overlap_region(data, labels, stats)
    print(f"      [OK] Center point: [{overlap_info['center_point'][0]:.4f}, {overlap_info['center_point'][1]:.4f}]")
    print(f"      [OK] Center min PDF: {overlap_info['center_min_pdf']:.6e}")
    print(f"      [OK] Threshold (20%): {overlap_info['threshold']:.6e}")
    print(f"      [OK] Found {overlap_info['total_overlap_count']:,} points in overlap region "
          f"({overlap_info['total_overlap_percentage']:.2f}%)")

    # PRD FR5 & FR6: Visualization
    print("\n[4/4] Creating dual-panel visualization...")
    create_dual_panel_visualization(data, labels, stats, overlap_info)

    # PRD FR7: Console Output - Detailed Statistics
    print_statistics(stats, overlap_info, len(data))

    # Performance metrics and validation
    elapsed_time = time.time() - start_time
    print("\n" + "=" * 80)
    print(" " * 28 + "EXECUTION SUMMARY")
    print("=" * 80)
    print(f"\nExecution Time: {elapsed_time:.3f} seconds")
    print(f"Points Generated: {len(data):,}")
    print(f"Overlap Percentage: {overlap_info['total_overlap_percentage']:.2f}%")
    print(f"Output File: gaussian_overlap_analysis.png")
    print("\n" + "-" * 80)
    print("VALIDATION RESULTS:")
    print("-" * 80)

    # NFR1: Performance requirement (< 5 seconds for n=10,000)
    if elapsed_time < 5.0:
        print(f"[PASS] Performance: < 5 seconds")
    else:
        print(f"[WARN] Performance: {elapsed_time:.3f}s >= 5 seconds")

    # PRD Target: Overlap percentage 30-35%
    if 30.0 <= overlap_info['total_overlap_percentage'] <= 35.0:
        print(f"[PASS] Overlap Range: 30-35%")
    else:
        print(f"[WARN] Overlap Range: {overlap_info['total_overlap_percentage']:.2f}% not in 30-35%")

    # Check equal distribution
    expected_per_group = n // 3
    all_equal = all(stats[gn]['n'] == expected_per_group for gn in ['Group 1', 'Group 2', 'Group 3'])
    if all_equal:
        print(f"[PASS] Equal Distribution: {expected_per_group} points per group")
    else:
        print(f"[WARN] Equal Distribution: unequal group sizes")

    print("\n" + "=" * 80)
    print(" " * 25 + "Analysis Complete!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    # NFR4: Usability - Simple command-line interface
    # Parse command-line argument for population size
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
            if n < 100 or n > 100000:
                print("Warning: Recommended population size is between 100 and 100,000")
                print("         (PRD NFR1: Performance constraint)")
        except ValueError:
            print("Error: Population size must be an integer")
            sys.exit(1)
    else:
        n = 10000  # Default as per PRD example

    # Ensure n is divisible by 3 (PRD FR1 requirement)
    if n % 3 != 0:
        original_n = n
        n = (n // 3) * 3  # Round down to nearest multiple of 3
        print(f"\nNote: Population size adjusted from {original_n} to {n} (must be divisible by 3)")
        print()

    # Execute main pipeline
    main(n)
