"""
Main script for Overlapping Groups Statistical Analysis.

This script orchestrates the complete analysis pipeline:
1. Data generation with overlapping groups
2. Statistical analysis (MLE-based estimators)
3. Visualization (Venn diagram and histograms)

Usage:
    python main.py
"""

from data_generation import get_distribution, generate_data, combine_groups
from statistics_1 import (
    calculate_group_stats,
    print_statistics,
    verify_constraints,
    save_statistics,
    save_data,
)
from visualization import create_venn_diagram, create_distribution_histograms


def main():
    """Main analysis pipeline."""
    print("=" * 60)
    print("OVERLAPPING GROUPS STATISTICAL ANALYSIS")
    print("=" * 60)
    print("\nStarting analysis...\n")

    # Step 1: Get distribution and generate data
    distribution = get_distribution()
    data = generate_data(distribution, seed=42)

    # Step 2: Combine data into groups
    group_A, group_B, group_C = combine_groups(data)

    # Step 3: Calculate statistics
    stats = calculate_group_stats(group_A, group_B, group_C)

    # Step 4: Print results
    print_statistics(distribution, stats)
    verify_constraints(group_A, group_B, group_C, distribution)

    # Step 5: Save outputs
    save_statistics(stats)
    save_data(group_A, group_B, group_C, distribution)

    # Step 6: Create visualizations
    create_venn_diagram(distribution)
    create_distribution_histograms(group_A, group_B, group_C, stats)

    # Final message
    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)
    print("\nGenerated files:")
    print("  - group_statistics.csv")
    print("  - group_data.npz")
    print("  - venn_diagram.png")
    print("  - distributions.png")


if __name__ == "__main__":
    main()
