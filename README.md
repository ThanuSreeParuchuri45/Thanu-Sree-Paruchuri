# Class Size and Software Maintainability Study

An empirical investigation into the effect of class size (measured in Lines of Code, LoC) on software maintainability in Java projects using CK metrics.

## Overview

This repository contains the data, analysis, and findings from our empirical study examining the relationship between Java class size and maintainability metrics. We analyzed five popular Java projects on GitHub using the CK metrics tool to measure complexity (WMC) and coupling (CBO) in relation to class size.

## Key Findings

- Strong positive correlation between class size (LoC) and complexity (WMC) across all projects (r = 0.65-0.82)
- Moderate positive correlation between class size and coupling (CBO) across all projects (r = 0.53-0.67)
- 80% of classes with LoC > 500 had WMC > 30 and CBO > 15, indicating reduced maintainability
- Larger classes consistently showed poorer maintainability characteristics

## Repository Structure

- `/data`: Raw and processed metrics from the analyzed projects
- `/src`: Analysis scripts and data processing code
- `/report`: Full empirical study report and figures
- `/tools`: Instructions and scripts for the CK metrics tool

## Getting Started

### Prerequisites

- Java 8 or higher
- Python 3.7 or higher
- Required Python packages: pandas, matplotlib, seaborn, numpy

### Setup

1. Clone the repository:
```
git clone https://github.com/yourusername/class-size-maintainability.git
cd class-size-maintainability
```

2. Install Python dependencies:
```
pip install -r requirements.txt
```

3. Download the CK metrics tool following instructions in `/tools/ck-tool/README.md`

### Running the Analysis

1. Collect metrics from a Java project:
```
bash src/data_collection/collect_metrics.sh <path-to-java-project> <output-directory>
```

2. Analyze the metrics and generate visualizations:
```
python src/analysis/analyze_metrics.py --input data/raw/ --output data/processed/
python src/visualization/generate_plots.py --input data/processed/ --output report/figures/
```

## Projects Analyzed

1. **Snailclimb/JavaGuide** - Java learning guide (153,206 LoC)
2. **iluwatar/java-design-patterns** - Design patterns in Java (28,281 LoC)
3. **doocs/advanced-java** - Java interview guide (29,161 LoC) 
4. **macrozheng/mall** - E-commerce system (57,643 LoC)
5. **spring-projects/spring-boot** - Spring Boot framework (151,778 LoC)

## Contributors

- [Your Name]
- [Team Member Names]

## License

This project is licensed under the MIT License - see the LICENSE file for details.s