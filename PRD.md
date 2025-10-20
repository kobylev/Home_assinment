# Product Requirements Document (PRD)
## Gaussian Overlap Dataset Generator

**Version:** 1.0
**Date:** October 2024
**Status:** Implemented
**Author:** AI Dev Experts - Koby Lev

---

## Table of Contents

1. [Product Overview](#1-product-overview)
2. [Product Goals](#2-product-goals)
3. [Functional Requirements](#3-functional-requirements)
4. [Non-Functional Requirements](#4-non-functional-requirements)
5. [Technical Specifications](#5-technical-specifications)
6. [User Stories](#6-user-stories)
7. [Design Specifications](#7-design-specifications)
8. [Constraints and Assumptions](#8-constraints-and-assumptions)
9. [Future Enhancements](#9-future-enhancements)
10. [Testing Requirements](#10-testing-requirements)
11. [Acceptance Criteria](#11-acceptance-criteria)

---

## 1. Product Overview

### 1.1 Purpose
Develop a Python-based tool that generates synthetic 2D datasets consisting of three overlapping Gaussian distributions, with comprehensive visualization and statistical analysis capabilities.

### 1.2 Target Users
- Data scientists and machine learning engineers
- Statistics educators and students
- Researchers testing clustering algorithms
- Developers benchmarking classification models

### 1.3 Business Value
- Provides a standardized synthetic dataset for algorithm testing
- Enables reproducible research and experimentation
- Serves as an educational tool for understanding mixture distributions
- Reduces time spent creating test datasets manually

### 1.4 Key Differentiators
- **Equilateral triangle arrangement** for symmetric overlap
- **PDF-based overlap detection** (not distance-based)
- **Shared covariance structure** across all distributions
- **Reproducible results** with fixed random seed
- **Target overlap percentage** (30-35%) built into design

---

## 2. Product Goals

### 2.1 Primary Goals
1. Generate pure Gaussian distributions with controlled overlap regions
2. Provide clear visualizations of distribution characteristics and overlap
3. Calculate and report statistical properties of each distribution
4. Enable reproducible dataset generation with seed control

### 2.2 Success Metrics
- Consistent overlap percentage (30-35% of total points)
- Accurate statistical calculations (mean, std dev, covariance)
- High-quality visualizations suitable for publication
- Execution time < 5 seconds for n=10,000 points

### 2.3 Performance Targets
- **Speed**: < 5 seconds for n=10,000
- **Accuracy**: Sample statistics within 5% of true parameters
- **Overlap**: 30-35% of points in overlap region
- **Scalability**: Support 100 to 100,000 points

---

## 3. Functional Requirements

### 3.1 Core Features

#### FR1: Data Generation
- **Priority**: P0 (Critical)
- **Description**: Generate three multivariate Gaussian distributions
- **Requirements**:
  - Accept user-defined population size (n)
  - Distribute points equally across three groups (n/3 each)
  - Use `numpy.random.multivariate_normal` for sampling
  - Set random seed for reproducibility (seed=42)
  - Position distributions in equilateral triangle arrangement

**Implementation Details:**
```python
# Equal distribution
points_per_group = n // 3

# Sampling
data = np.random.multivariate_normal(mean, cov, points_per_group)
```

**Acceptance Criteria:**
- ✓ Exactly n/3 points per group
- ✓ Reproducible with same seed
- ✓ Valid multivariate normal samples

---

#### FR2: Distribution Configuration
- **Priority**: P0 (Critical)
- **Description**: Define Gaussian distribution parameters
- **Requirements**:
  - Group 1 mean: [2.0, 0.0] (0° angle)
  - Group 2 mean: [-1.0, 1.732] (120° rotation)
  - Group 3 mean: [-1.0, -1.732] (240° rotation)
  - Shared covariance matrix: [[3.85, 0], [0, 3.85]]
  - Radius from origin: 2.0 units

**Mathematical Basis:**
```
Equilateral triangle vertices at radius R=2.0:
- Vertex 1: (R, 0) = (2.0, 0.0)
- Vertex 2: (R·cos(120°), R·sin(120°)) = (-1.0, 1.732)
- Vertex 3: (R·cos(240°), R·sin(240°)) = (-1.0, -1.732)

Shared covariance:
Σ = [[σ², 0  ],
     [0,  σ²]]
where σ² = 3.85 → σ ≈ 1.962
```

**Design Rationale:**
- Equilateral arrangement ensures symmetric overlap
- Shared covariance simplifies analysis
- Diagonal covariance (no correlation) simplifies interpretation
- Variance chosen to create 30-35% overlap

**Acceptance Criteria:**
- ✓ Means form equilateral triangle
- ✓ All covariances identical
- ✓ Distance between any two means: ~3.464 units

---

#### FR3: Overlap Region Detection
- **Priority**: P0 (Critical)
- **Description**: Identify points in triple-overlap region using PDF-based method
- **Requirements**:
  - Calculate PDF for each point under all three distributions
  - Use minimum PDF criterion across all distributions
  - Set threshold at 20% of center point's minimum PDF
  - Target 30-35% of points in overlap region
  - Return boolean mask of overlap membership

**Algorithm:**
```python
# Step 1: Calculate center point
center = (mean1 + mean2 + mean3) / 3  # Origin: (0, 0)

# Step 2: Calculate PDFs at center
center_pdf1 = P(center | N(μ₁, Σ))
center_pdf2 = P(center | N(μ₂, Σ))
center_pdf3 = P(center | N(μ₃, Σ))

# Step 3: Determine threshold
center_min_pdf = min(center_pdf1, center_pdf2, center_pdf3)
threshold = 0.20 * center_min_pdf

# Step 4: Classify points
For each point p:
    pdf1 = P(p | N(μ₁, Σ))
    pdf2 = P(p | N(μ₂, Σ))
    pdf3 = P(p | N(μ₃, Σ))
    min_pdf = min(pdf1, pdf2, pdf3)

    if min_pdf > threshold:
        p is in overlap region
```

**Why PDF-based?**
- More principled than distance-based methods
- Accounts for distribution shape (covariance)
- Directly measures probability of ambiguous classification
- Threshold calibrated to achieve target overlap percentage

**Acceptance Criteria:**
- ✓ Overlap percentage between 30-35%
- ✓ Uses scipy.stats.multivariate_normal.pdf()
- ✓ Consistent across different population sizes
- ✓ Returns boolean mask and indices

---

#### FR4: Statistical Analysis
- **Priority**: P0 (Critical)
- **Description**: Calculate and report statistics for each group
- **Requirements**:
  - Sample mean (2D vector)
  - Sample standard deviation (per dimension)
  - Sample covariance matrix (2x2)
  - Number of points per group
  - Comparison with true parameters
  - Overlap point counts per group

**Estimators (MLE):**
```python
# Sample mean (unbiased)
μ̂ = (1/n) Σᵢ xᵢ

# Sample covariance (unbiased with Bessel's correction)
Σ̂ = (1/(n-1)) Σᵢ (xᵢ - μ̂)(xᵢ - μ̂)ᵀ

# Standard deviation
σ̂ = √(diag(Σ̂))
```

**Output Format:**
```
Group 1:
  Sample Mean: [2.0123, -0.0087]
  True Mean:   [2.0000,  0.0000]
  Sample Std:  [1.9734, 1.9589]
  True Std:    [1.9621, 1.9621]
  Covariance:  [[3.8943, -0.0234],
                [-0.0234,  3.8374]]
```

**Acceptance Criteria:**
- ✓ Displays true vs. sample parameters
- ✓ Uses numpy.mean() and numpy.cov()
- ✓ Formatted output with alignment
- ✓ Shows overlap counts per group

---

#### FR5: Visualization - Distribution View
- **Priority**: P0 (Critical)
- **Description**: Create comprehensive visualization of all three distributions
- **Requirements**:
  - Scatter plot with color coding (red, blue, green)
  - Mark distribution means with X markers
  - Draw 2-sigma confidence ellipses
  - Display all points with semi-transparency
  - Include grid and axis labels
  - Add legend with group information
  - Equal aspect ratio for accurate representation

**Visual Elements:**
1. **Scatter points**:
   - Size: 15 pixels
   - Alpha: 0.5 (semi-transparent)
   - Edge colors: Dark variants (#8B0000, #00008B, #006400)
   - Edge width: 0.5 pixels

2. **Mean markers**:
   - Symbol: 'X'
   - Size: 200 pixels
   - Color: Black
   - Edge: White, width 2 pixels
   - Labels: Text box with group name

3. **Confidence ellipses**:
   - Level: 2-sigma (~95% confidence)
   - Style: Dashed lines
   - Width: 2 pixels
   - Color: Dark edge colors
   - Alpha: 0.7

4. **Statistics box**:
   - Position: Top-left
   - Background: Wheat color
   - Alpha: 0.8
   - Font: Monospace, 9pt
   - Contents: Total points, group counts, overlap percentage

**Acceptance Criteria:**
- ✓ All points visible with proper colors
- ✓ Means marked clearly
- ✓ Ellipses show 95% confidence regions
- ✓ Professional appearance suitable for publication

---

#### FR6: Visualization - Overlap View
- **Priority**: P0 (Critical)
- **Description**: Highlight overlap region in separate panel
- **Requirements**:
  - Fade non-overlap points (alpha=0.2)
  - Emphasize overlap points (alpha=0.8, black edges)
  - Draw convex hull around overlap region
  - Show separate counts for each group's overlap
  - Maintain color coding consistency
  - Display overlap percentage in title

**Visual Elements:**
1. **Non-overlap points**:
   - Alpha: 0.15 (nearly invisible)
   - Size: 10 pixels
   - No edges

2. **Overlap points**:
   - Fill color: Yellow (#FFFF00)
   - Edge color: Orange (#FFA500)
   - Alpha: 0.7
   - Size: 20 pixels
   - Edge width: 1 pixel

3. **Convex hull**:
   - Line color: Orange
   - Line width: 2.5 pixels
   - Fill: Yellow with alpha=0.2
   - Style: Solid line

4. **Overlap statistics box**:
   - Position: Top-left
   - Background: Light yellow
   - Alpha: 0.9
   - Contents: Per-group overlap counts and percentages

**Acceptance Criteria:**
- ✓ Overlap region clearly highlighted
- ✓ Convex hull encloses all overlap points
- ✓ Non-overlap points barely visible
- ✓ Group-specific overlap statistics displayed

---

#### FR7: Console Output
- **Priority**: P1 (High)
- **Description**: Print formatted statistical information
- **Requirements**:
  - Progress message at start
  - Formatted statistics tables with separators
  - True vs. sample parameter comparison
  - Overlap analysis summary
  - Completion confirmation message
  - Validation results (performance, overlap range)

**Output Structure:**
```
================================================================================
               GAUSSIAN OVERLAP DATASET GENERATOR
================================================================================

[1/4] Generating synthetic dataset...
      [OK] Generated X points

[2/4] Calculating statistics...
      [OK] Computed means, covariances

[3/4] Detecting overlap regions...
      [OK] Found Y points in overlap (Z%)

[4/4] Creating visualization...

================================================================================
                    STATISTICAL SUMMARY
================================================================================
[Per-group statistics...]

================================================================================
                         OVERLAP ANALYSIS
================================================================================
[Overlap statistics...]

================================================================================
                       EXECUTION SUMMARY
================================================================================
Execution Time: X.XXX seconds
[Validation results...]
```

**Acceptance Criteria:**
- ✓ Clear progress indicators
- ✓ Formatted with box-drawing characters
- ✓ Human-readable output
- ✓ Validation pass/fail indicators

---

#### FR8: Interactive Display
- **Priority**: P1 (High)
- **Description**: Show matplotlib visualization
- **Requirements**:
  - Two-panel layout (1 row, 2 columns)
  - Figure size: 18x8 inches
  - Tight layout for optimal spacing
  - Save to file (gaussian_overlap_analysis.png)
  - High resolution: 300 DPI

**Layout:**
```
┌─────────────────────────┬─────────────────────────┐
│  Distribution View      │  Overlap View           │
│  (9x8 inches)           │  (9x8 inches)           │
│                         │                         │
│  - All points           │  - Highlighted overlap  │
│  - Means marked         │  - Faded non-overlap    │
│  - Confidence ellipses  │  - Convex hull          │
│  - Statistics box       │  - Group counts         │
└─────────────────────────┴─────────────────────────┘
```

**Acceptance Criteria:**
- ✓ Both panels visible side-by-side
- ✓ High resolution output (300 DPI)
- ✓ Saved to file automatically
- ✓ Consistent axis limits across panels

---

## 4. Non-Functional Requirements

### 4.1 Performance (NFR1)

**Requirements:**
- Generate and visualize n=10,000 points in < 5 seconds
- Support population sizes from 100 to 100,000
- Minimal memory footprint (< 500MB for n=10,000)
- Linear time complexity: O(n)

**Performance Targets:**

| Population Size | Target Time | Memory Usage |
|----------------|-------------|--------------|
| 100            | < 0.5s      | < 50 MB      |
| 1,000          | < 1.0s      | < 100 MB     |
| 10,000         | < 5.0s      | < 200 MB     |
| 100,000        | < 10.0s     | < 500 MB     |

**Bottlenecks:**
- PDF calculation: O(n) per distribution, O(3n) total
- Convex hull: O(k log k) where k = overlap points
- Visualization rendering: O(n)

**Optimization Strategies:**
- Vectorized numpy operations
- Efficient scipy PDF calculations
- Matplotlib batch rendering

---

### 4.2 Code Quality (NFR2)

**Requirements:**
- PEP 8 compliant Python code
- Clear variable naming and comments
- Modular function design
- Error handling for edge cases
- Type hints where beneficial

**Code Standards:**
- Line length: ≤ 100 characters
- Docstrings: Google style
- Comments: Explain "why", not "what"
- Function length: ≤ 50 lines (guideline)

**Modularity:**
```
data_generation.py    → FR1, FR2
statistics_1.py       → FR3, FR4
visualization.py      → FR5, FR6
main.py              → FR7, FR8
```

---

### 4.3 Reliability (NFR3)

**Requirements:**
- Reproducible results with fixed random seed
- Consistent overlap percentage across runs
- Robust convex hull calculation with fallback
- Graceful handling of edge cases

**Edge Cases:**
- n not divisible by 3 → Adjust to nearest multiple
- Very small n (< 9) → Warning message
- Singular covariance → Use pseudo-inverse
- Convex hull failure → Skip polygon drawing

**Error Handling:**
```python
if n % 3 != 0:
    n = (n // 3) * 3
    print(f"Adjusted to {n}")

try:
    hull = ConvexHull(overlap_data)
except:
    print("Warning: Could not compute convex hull")
```

---

### 4.4 Usability (NFR4)

**Requirements:**
- Simple command-line interface
- Clear prompts and instructions
- Human-readable output formatting
- Self-documenting visualizations
- Minimal setup required

**CLI Design:**
```bash
# Default
python main.py

# Custom population
python main.py 15000

# Help
python main.py --help  (future enhancement)
```

**User Feedback:**
- Progress messages during execution
- Validation results at end
- Clear error messages
- Output file location

---

### 4.5 Maintainability (NFR5)

**Requirements:**
- Single-file implementation per module
- Minimal dependencies (numpy, matplotlib, scipy)
- Documented algorithms and formulas
- Easy parameter tuning via constants
- Version control friendly

**Dependencies:**
```python
numpy>=1.19.0      # Core computations
scipy>=1.5.0       # PDF, convex hull
matplotlib>=3.3.0  # Visualization
```

**Configuration:**
All parameters in one place (data_generation.py):
```python
RADIUS = 2.0
SHARED_VAR = 3.85
THRESHOLD_PERCENT = 0.20
SEED = 42
```

---

## 5. Technical Specifications

### 5.1 Technology Stack

**Language:** Python 3.7+

**Core Libraries:**
- **numpy**: Random number generation, array operations, linear algebra
- **matplotlib**: Visualization and plotting
- **scipy.stats**: Multivariate normal PDF calculations
- **scipy.spatial**: Convex hull computation

**Development Tools:**
- Git for version control
- pytest for testing (optional)
- Black for code formatting (optional)

---

### 5.2 Input Specifications

**User Input:**
- Population size (n): Integer
- Command-line argument: `sys.argv[1]`

**Constraints:**
- n must be divisible by 3
- Recommended range: 100 ≤ n ≤ 100,000
- Default: n = 10,000

**Validation:**
```python
if len(sys.argv) > 1:
    n = int(sys.argv[1])
    if n < 100 or n > 100000:
        print("Warning: Recommended range 100-100,000")
else:
    n = 10000  # Default

if n % 3 != 0:
    n = (n // 3) * 3
    print(f"Adjusted to {n}")
```

---

### 5.3 Output Specifications

**Console Output:**
- Plain text with box-drawing characters (=, -)
- Monospace-friendly formatting
- 80-character width for separators
- Progress indicators: [1/4], [2/4], etc.
- Status markers: [OK], [PASS], [WARN]

**Visual Output:**
- Format: PNG
- Resolution: 300 DPI
- Color space: RGB
- Dimensions: 5400×2400 pixels (18×8 inches @ 300 DPI)
- File size: ~2-3 MB for n=10,000

**Data Output (Future):**
- CSV export option
- JSON metadata
- NumPy .npz format

---

### 5.4 Algorithm Design

#### Overlap Detection Algorithm (Detailed)

```python
def detect_overlap_region(data, labels, stats):
    """
    PDF-based overlap detection.

    Theory:
    - Points in overlap have high PDF under multiple distributions
    - Minimum PDF captures "worst case" classification
    - Threshold ensures ~30-35% overlap
    """
    n_points = len(data)

    # Step 1: Create distributions
    distributions = []
    for group_name in ['Group 1', 'Group 2', 'Group 3']:
        mean = stats[group_name]['true_mean']
        cov = stats[group_name]['true_cov']
        dist = multivariate_normal(mean=mean, cov=cov)
        distributions.append(dist)

    # Step 2: Calculate PDFs for all points
    pdfs = np.zeros((n_points, 3))
    for i, dist in enumerate(distributions):
        pdfs[:, i] = dist.pdf(data)  # Vectorized!

    # Step 3: Minimum PDF per point
    min_pdfs = np.min(pdfs, axis=1)

    # Step 4: Calculate threshold
    center = np.mean([stats[gn]['true_mean']
                      for gn in ['Group 1', 'Group 2', 'Group 3']],
                     axis=0)
    center_pdfs = np.array([dist.pdf(center) for dist in distributions])
    center_min = np.min(center_pdfs)
    threshold = 0.20 * center_min

    # Step 5: Classify
    overlap_mask = min_pdfs > threshold

    return {
        'overlap_mask': overlap_mask,
        'threshold': threshold,
        'center_point': center,
        'center_min_pdf': center_min,
        # ... additional statistics
    }
```

**Complexity:**
- Time: O(n) for PDF calculations
- Space: O(n) for PDF storage
- Efficient vectorization via numpy/scipy

---

#### Confidence Ellipse Drawing

```python
def plot_confidence_ellipse(ax, mean, cov, n_std=2):
    """
    Draw 2D confidence ellipse.

    Theory:
    - Eigenvalues = variances along principal axes
    - Eigenvectors = rotation matrix
    - n_std=2 → approximately 95% confidence for 2D normal
    """
    # Eigendecomposition
    eigenvalues, eigenvectors = np.linalg.eig(cov)

    # Rotation angle
    angle = np.degrees(np.arctan2(eigenvectors[1, 0],
                                   eigenvectors[0, 0]))

    # Ellipse dimensions
    width = 2 * n_std * np.sqrt(eigenvalues[0])
    height = 2 * n_std * np.sqrt(eigenvalues[1])

    # Create and add ellipse
    ellipse = Ellipse(xy=mean, width=width, height=height,
                     angle=angle, ...)
    ax.add_patch(ellipse)
```

**Mathematical Background:**
For 2D normal: X ~ N(μ, Σ)
- Mahalanobis distance: D² = (x-μ)ᵀ Σ⁻¹ (x-μ)
- D² ~ χ²(2) distribution
- χ²(2, 0.95) ≈ 5.99 → contour at 2.45 std devs
- We use 2 std devs as approximation (~95%)

---

## 6. User Stories

### US1: Generate Test Dataset
**As a** data scientist
**I want to** generate a synthetic dataset with overlapping distributions
**So that** I can test my clustering algorithm on ambiguous cases

**Acceptance Criteria:**
- ✓ Can specify population size via command line
- ✓ Receives dataset with three distinct groups
- ✓ Approximately 30-35% of points are in overlap region
- ✓ Results are reproducible with same seed
- ✓ Data accessible as numpy arrays

**Example Usage:**
```python
dataset = generate_gaussian_dataset(n=10000, seed=42)
X = dataset['data']
y = dataset['labels']

# Test clustering algorithm
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=3, random_state=42)
y_pred = kmeans.fit_predict(X)

# Evaluate on overlap vs non-overlap points
overlap_mask = overlap_info['overlap_mask']
accuracy_overlap = accuracy_score(y[overlap_mask], y_pred[overlap_mask])
accuracy_non_overlap = accuracy_score(y[~overlap_mask], y_pred[~overlap_mask])
```

---

### US2: Visualize Distribution Overlap
**As a** statistics educator
**I want to** see visual representations of overlapping Gaussians
**So that** I can explain mixture models to students

**Acceptance Criteria:**
- ✓ Clear color coding for each distribution
- ✓ Confidence ellipses show distribution spread
- ✓ Overlap region is clearly highlighted
- ✓ Professional quality suitable for presentations
- ✓ High-resolution output (300 DPI)

**Teaching Points:**
- Equilateral triangle = symmetric design
- Confidence ellipses = 95% confidence regions
- Overlap region = classification ambiguity
- PDF-based detection = principled approach

---

### US3: Verify Statistical Properties
**As a** researcher
**I want to** see statistical summaries of each distribution
**So that** I can verify the data matches expected parameters

**Acceptance Criteria:**
- ✓ True vs. sample means are displayed
- ✓ Standard deviations are calculated
- ✓ Covariance matrices are shown
- ✓ Overlap percentages are reported
- ✓ Validation checks indicate pass/fail

**Verification Checklist:**
- Sample means ≈ true means (within sampling error)
- Sample std devs ≈ 1.962 (within 10%)
- Overlap percentage: 30-35%
- Equal group sizes: n/3 each
- Performance: < 5 seconds for n=10,000

---

## 7. Design Specifications

### 7.1 Color Scheme

**Primary Colors:**
- **Group 1**: Red (#FF0000) with dark red edges (#8B0000)
- **Group 2**: Blue (#0000FF) with dark blue edges (#00008B)
- **Group 3**: Green (#008000) with dark green edges (#006400)

**Accent Colors:**
- **Overlap Region**: Yellow (#FFFF00) fill with orange (#FFA500) edges
- **Convex Hull**: Orange (#FFA500) boundary
- **Mean Markers**: Black with white edges
- **Background**: White (#FFFFFF)
- **Grid**: Light gray (alpha=0.3)

**Color Accessibility:**
- High contrast for visibility
- Colorblind-friendly (red-blue-green is distinguishable for most types)
- Suitable for both screen and print

---

### 7.2 Typography

**Title Font:**
- Weight: Bold
- Size: 14pt
- Family: Default sans-serif

**Axis Labels:**
- Weight: Bold
- Size: 12pt
- Labels: 'X', 'Y'

**Legend:**
- Weight: Regular
- Size: 8-9pt
- Position: Upper right

**Statistics Box:**
- Family: Monospace
- Size: 9pt
- Alignment: Left

**Text Boxes (Mean Labels):**
- Weight: Bold
- Size: 9pt
- Background: White with alpha=0.8
- Border: Rounded rectangle

---

### 7.3 Layout

**Figure Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│                  Gaussian Overlap Analysis                   │
│  ┌──────────────────────┬──────────────────────┐            │
│  │ Distribution View    │ Overlap View         │            │
│  │                      │                      │            │
│  │ ╔═══════════╗        │ ╔═══════════╗        │            │
│  │ ║ Stats Box ║        │ ║ Overlap   ║        │            │
│  │ ╚═══════════╝        │ ║ Stats Box ║        │            │
│  │                      │ ╚═══════════╝        │            │
│  │  ● ● ●  ⃝           │    . . .  ⃝          │            │
│  │   ● ●    Group 1     │     . .   Overlap    │            │
│  │  ● ● ●  (Red)        │    . . .  (Yellow)   │            │
│  │                      │                      │            │
│  │      X̄₁              │                      │            │
│  │    Mean              │                      │            │
│  │                      │                      │            │
│  │  ╭─────────╮         │  ╭─────────╮         │            │
│  │  │ Legend  │         │  │ Legend  │         │            │
│  │  ╰─────────╯         │  ╰─────────╯         │            │
│  │                      │                      │            │
│  └──────────────────────┴──────────────────────┘            │
│                 X axis (both panels)                         │
└─────────────────────────────────────────────────────────────┘
```

**Dimensions:**
- Total figure: 18×8 inches (5400×2400 pixels @ 300 DPI)
- Left panel: 9×8 inches
- Right panel: 9×8 inches
- Margins: Tight layout (automatic)

**Alignment:**
- Axis limits: Matched across panels
- Grid: Aligned on both panels
- Equal aspect ratio: Enforced

---

## 8. Constraints and Assumptions

### 8.1 Constraints

**Technical Constraints:**
- Python 3.7+ environment required
- Must have display for interactive plotting (or headless backend)
- Population size should be divisible by 3
- Memory limitations for very large n (>1,000,000)
- Requires numpy, scipy, matplotlib

**Design Constraints:**
- Must use equilateral triangle arrangement (not modifiable)
- Shared covariance matrix (not per-group)
- Fixed color scheme (for consistency)
- PDF-based overlap (not distance-based)

**Performance Constraints:**
- < 5 seconds for n=10,000 (hard requirement)
- < 500 MB memory for n=10,000 (soft requirement)
- Linear time complexity O(n) preferred

---

### 8.2 Assumptions

**User Assumptions:**
- Users have basic Python knowledge
- Required libraries are installed
- Users understand Gaussian distributions
- Display supports matplotlib backend

**Data Assumptions:**
- Points are i.i.d. (independent, identically distributed)
- True parameters are exactly specified
- Random seed ensures reproducibility
- Overlap percentage is deterministic (given seed)

**Environment Assumptions:**
- Sufficient disk space for output image (~3 MB)
- Write permissions in current directory
- No firewall blocking matplotlib display
- Console supports UTF-8 (or ASCII fallback)

---

## 9. Future Enhancements

### 9.1 Phase 2 Features (Out of Current Scope)

**File I/O:**
- [ ] Save visualization to multiple formats (PNG, PDF, SVG)
- [ ] Export data to CSV with headers
- [ ] Save metadata to JSON
- [ ] Load existing datasets

**Command-Line Interface:**
- [ ] Argument parser with `--help`
- [ ] Custom parameters: `--radius`, `--variance`
- [ ] Output directory specification
- [ ] Verbosity control: `--quiet`, `--verbose`

**Configuration:**
- [ ] Config file support (YAML/JSON)
- [ ] Preset configurations (easy/medium/hard)
- [ ] Custom color schemes
- [ ] Adjustable overlap threshold

---

### 9.2 Phase 3 Features (Advanced)

**Extended Functionality:**
- [ ] Variable number of distributions (2-10)
- [ ] Custom distribution arrangements (grid, random)
- [ ] Non-shared covariances
- [ ] Correlated distributions (non-diagonal Σ)

**3D Support:**
- [ ] 3D Gaussian distributions
- [ ] 3D visualization (interactive)
- [ ] Projection to 2D planes

**Interactive Features:**
- [ ] GUI with sliders for parameters
- [ ] Animation of distribution evolution
- [ ] Real-time overlap adjustment
- [ ] Interactive point selection

**Integration:**
- [ ] sklearn pipeline compatibility
- [ ] Pandas DataFrame output
- [ ] TensorFlow/PyTorch dataset format
- [ ] Jupyter notebook widgets

**Batch Operations:**
- [ ] Generate multiple datasets
- [ ] Parameter sweeps
- [ ] Statistical analysis across runs
- [ ] Automated benchmarking

---

## 10. Testing Requirements

### 10.1 Unit Tests

**Data Generation:**
- [ ] Test equal distribution (n/3 each)
- [ ] Test seed reproducibility
- [ ] Test parameter validation
- [ ] Test edge cases (n=3, n=9)

**Statistical Calculations:**
- [ ] Test MLE mean estimator accuracy
- [ ] Test covariance calculation
- [ ] Test overlap detection consistency
- [ ] Test PDF calculations

**Visualization:**
- [ ] Test figure creation
- [ ] Test file saving
- [ ] Test ellipse calculations
- [ ] Test convex hull robustness

---

### 10.2 Integration Tests

**End-to-End:**
- [ ] Full pipeline execution
- [ ] Console output formatting
- [ ] File generation
- [ ] Multiple population sizes

**Performance:**
- [ ] Benchmark n=10,000 (< 5s)
- [ ] Benchmark n=100,000 (< 10s)
- [ ] Memory profiling
- [ ] Scalability testing

---

### 10.3 Validation Tests

**Statistical Validation:**
- [ ] Overlap percentage in 30-35% range
- [ ] Sample statistics approximate true values
- [ ] Equal group sizes maintained
- [ ] Reproducibility across runs

**Visual Validation:**
- [ ] Manual inspection of plots
- [ ] Color scheme correctness
- [ ] Label readability
- [ ] Resolution quality

---

## 11. Acceptance Criteria

### 11.1 Feature Completeness

The product is considered complete when:

**Data Generation:**
- ✓ Generates three pure Gaussian distributions
- ✓ Uses equilateral triangle arrangement
- ✓ Applies shared covariance matrix [[3.85, 0], [0, 3.85]]
- ✓ Equal distribution: n/3 points per group

**Statistical Analysis:**
- ✓ Calculates sample means, std devs, covariances
- ✓ Displays true vs. sample parameter comparison
- ✓ Uses MLE estimators with Bessel's correction

**Overlap Detection:**
- ✓ Implements PDF-based method
- ✓ Uses 20% threshold of center min PDF
- ✓ Achieves 30-35% overlap consistently
- ✓ Reports per-group overlap statistics

**Visualization:**
- ✓ Two-panel layout (18×8 inches)
- ✓ Distribution view with confidence ellipses
- ✓ Overlap view with convex hull
- ✓ Clear labeling and legends
- ✓ High resolution (300 DPI)

**Console Output:**
- ✓ Progress messages for each stage
- ✓ Formatted statistics tables
- ✓ Validation results
- ✓ Execution time reporting

**Performance:**
- ✓ Executes in < 5 seconds for n=10,000
- ✓ Handles 100 to 100,000 points
- ✓ Memory usage < 500 MB

**Quality:**
- ✓ PEP 8 compliant code
- ✓ Documented functions
- ✓ Modular design
- ✓ Error handling

**Usability:**
- ✓ Simple CLI interface
- ✓ Clear error messages
- ✓ Reproducible results (seed=42)
- ✓ Minimal dependencies

---

### 11.2 Validation Checklist

Run the following validation:

```bash
# Test 1: Default execution
python main.py
# Expected: 10,000 points, 30-35% overlap, < 5s

# Test 2: Custom population
python main.py 3000
# Expected: 3,000 points, 30-35% overlap, < 2s

# Test 3: Large dataset
python main.py 30000
# Expected: 30,000 points, 30-35% overlap, < 8s

# Test 4: Edge case
python main.py 100
# Expected: Adjusted to 99, warning displayed
```

**Success Criteria:**
- All tests produce output image
- Overlap percentage: 30-35% in all tests
- Performance targets met
- No errors or warnings (except edge cases)

---

### 11.3 Sign-Off

**Stakeholder Approval:**
- [ ] Product owner review
- [ ] Technical lead review
- [ ] QA testing complete
- [ ] Documentation complete

**Deliverables:**
- [ ] Source code (4 Python files)
- [ ] README.md (comprehensive)
- [ ] PRD.md (this document)
- [ ] Sample output visualization
- [ ] Usage examples

**Deployment:**
- [ ] Code pushed to repository
- [ ] Tagged version release
- [ ] Dependencies documented
- [ ] Installation instructions verified

---

## Revision History

| Version | Date       | Author    | Changes                              |
|---------|------------|-----------|--------------------------------------|
| 1.0     | Oct 2024   | Koby Lev  | Initial PRD - Complete specification |

---

## Appendix

### A. Mathematical Formulas

**Multivariate Normal PDF:**
```
f(x|μ,Σ) = (2π)^(-k/2) |Σ|^(-1/2) exp(-½(x-μ)ᵀΣ⁻¹(x-μ))
```
where k=2 (2D), μ=mean, Σ=covariance

**Mahalanobis Distance:**
```
D(x) = √((x-μ)ᵀ Σ⁻¹ (x-μ))
```

**Equilateral Triangle Vertices:**
```
Vertex 1: (R, 0)
Vertex 2: (R cos(120°), R sin(120°))
Vertex 3: (R cos(240°), R sin(240°))
```
where R=2.0

---

### B. References

- Product concept based on Gaussian Mixture Model (GMM) theory
- Overlap detection inspired by Bayes decision theory
- Visualization design follows Tufte principles
- Implementation uses numpy/scipy best practices

---

**End of PRD**
