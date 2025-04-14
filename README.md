# CK Metrics Tool Setup

This directory contains instructions for setting up and using the CK metrics tool for Java code analysis.

## About CK

CK is a tool for calculating class-level software metrics in Java projects. It calculates the following metrics:

- Lines of Code (LOC)
- Weighted Methods per Class (WMC)
- Depth of Inheritance Tree (DIT)
- Number of Children (NOC)
- Coupling Between Objects (CBO)
- Response for a Class (RFC)
- Lack of Cohesion of Methods (LCOM)

## Installation

1. Download the latest release of CK from the official repository:
   https://github.com/mauricioaniche/ck/releases

2. Save the downloaded JAR file as `ck.jar` in this directory.

## Usage

### Using the Provided Script

We've provided a convenient script to run CK on Java projects:

```bash
bash ../../src/data_collection/collect_metrics.sh  
```

### Manual Usage

Alternatively, you can run CK directly:

```bash
java -jar ck.jar  true 0 false /-metrics.csv
```

Parameters:
- `<path-to-java-project>`: Path to the Java project
- `true`: Use JDT AST for parsing
- `0`: Maximum files to parse (0 = unlimited)
- `false`: Disable metrics calculation for inner classes
- `<output-directory>/<project-name>-metrics.csv`: Output file path

## Output Format

The tool generates a CSV file with the following columns:

- `file`: Java file path
- `class`: Full class name
- `type`: Class type (class or interface)
- `loc`: Lines of code
- `wmc`: Weighted methods per class
- `cbo`: Coupling between objects
- And other CK metrics

## References

- CK GitHub Repository: https://github.com/mauricioaniche/ck
- Original CK Metrics Paper: Chidamber, S. R., & Kemerer, C. F. (1994). A Metrics Suite for Object-Oriented Design. IEEE Transactions on Software Engineering.