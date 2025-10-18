# Overlapping Groups Statistical Analysis
## Computational Statistics Assignment

---

## 1. Point Distribution

### Region Breakdown

| Region | Description | Points |
|--------|-------------|--------|
| A only | Points exclusive to Group A | 700 |
| B only | Points exclusive to Group B | 733 |
| C only | Points exclusive to Group C | 700 |
| A ∩ B | Points in A and B, not C | 300 |
| A ∩ C | Points in A and C, not B | 333 |
| B ∩ C | Points in B and C, not A | 300 |
| **A ∩ B ∩ C** | **Points in all three groups** | **667** |
| **Total** | **Unique points** | **3,733** |

### Group Totals

| Group | Composition | Total Points |
|-------|-------------|--------------|
| **Group A** | 700 + 300 + 333 + 667 | **2,000** |
| **Group B** | 733 + 300 + 300 + 667 | **2,000** |
| **Group C** | 700 + 333 + 300 + 667 | **2,000** |

**Key Constraint:** The ABC intersection contains **667 points**, representing **33.35%** of each group (approximately 1/3 as required).

---

## 2. Data Generation

Each point was assigned a continuous value sampled from Gaussian distributions:

- **A only**: N(μ=10, σ²=4)
- **B only**: N(μ=15, σ²=6.25)
- **C only**: N(μ=20, σ²=9)
- **A ∩ B**: N(μ=12.5, σ²=4)
- **A ∩ C**: N(μ=15, σ²=6.25)
- **B ∩ C**: N(μ=17.5, σ²=6.25)
- **A ∩ B ∩ C**: N(μ=15, σ²=4)

This simulates a scenario where overlapping regions contain points with intermediate characteristics.

---

## 3. Statistical Analysis

### Group A Statistics

- **Sample Size**: n = 2,000
- **Mean (μ̂_A)**: 12.15
- **Variance (σ̂²_A)**: 11.85
- **Standard Deviation (σ̂_A)**: 3.44

### Group B Statistics

- **Sample Size**: n = 2,000
- **Mean (μ̂_B)**: 14.99
- **Variance (σ̂²_B)**: 8.87
- **Standard Deviation (σ̂_B)**: 2.98

### Group C Statistics

- **Sample Size**: n = 2,000
- **Mean (μ̂_C)**: 17.20
- **Variance (σ̂²_C)**: 11.36
- **Standard Deviation (σ̂_C)**: 3.37

---

## 4. Connection to MLE and GMM

### Maximum Likelihood Estimation (MLE)

For each group, assuming Gaussian distribution, the MLE estimators are:

**Mean estimator:**
```
μ̂ = (1/n) Σ x_i
```

**Variance estimator:**
```
σ̂² = (1/(n-1)) Σ (x_i - μ̂)²
```

These are exactly what we computed for each group. Under the assumption of normally distributed data, these MLE estimators are:
- **Unbiased** (for variance, using Bessel's correction with n-1)
- **Consistent** (converge to true parameters as n → ∞)
- **Efficient** (achieve minimum variance among unbiased estimators)

### Gaussian Mixture Models (GMM)

This assignment structure mirrors a 3-component GMM where:

1. **Components**: Three Gaussian distributions (Groups A, B, C)
2. **Mixing coefficients**: Each group has equal weight (π_A = π_B = π_C = 1/3)
3. **Overlapping memberships**: Points in intersection regions have partial membership in multiple components

In a full GMM framework:
- The **E-step** would compute responsibilities (posterior probabilities) for each point's membership in each component
- The **M-step** would update μ̂, σ̂², and π for each component using weighted MLE

Our overlapping structure represents a simplified case where memberships are known (hard assignments), but the principle of estimating component parameters via MLE remains central.

### Special Focus: The Triple Intersection (A ∩ B ∩ C)

The constraint that **~1/3 of each group must belong to the central intersection** has important implications:

1. **Mixture Complexity**: The 667 shared points represent observations that could plausibly belong to all three components, increasing model complexity
2. **Parameter Estimation**: These shared points influence all three group statistics simultaneously, creating dependencies between component estimates
3. **Identifiability**: In unsupervised GMM, having such significant overlap (33% shared) makes component separation more challenging

### Key Insights

1. **Parameter Estimation**: We use MLE to estimate mean and variance for each group
2. **Mixture Nature**: The overlapping structure creates a natural mixture where some observations belong to multiple groups
3. **Identifiability**: With known memberships (unlike unsupervised GMM), parameters are directly identifiable
4. **Reproducibility**: Setting random seed ensures reproducible results, critical for statistical analysis

---

## 5. Visualizations

![Venn Diagram](venn_diagram.png)
*Figure 1: Point distribution across overlapping groups with central intersection highlighted*

![Distributions](distributions.png)
*Figure 2: Histogram distributions for each group with estimated means*

---

## 6. Reproducibility

To reproduce this analysis:

```bash
python analysis.py
```

This generates:
- `group_statistics.csv` - Summary statistics
- `group_data.npz` - Raw data arrays
- `venn_diagram.png` - Visual representation
- `distributions.png` - Histogram plots

---

## 7. Verification

All constraints satisfied:
- ✓ Each group contains exactly 2,000 points
- ✓ Total of 6,000 points distributed (counting overlaps)
- ✓ All groups overlap with each other
- ✓ A ∩ B ∩ C contains 667 points (33.35% of each group)
- ✓ Total unique points: 3,733
