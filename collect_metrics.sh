#!/bin/bash

# Script to collect metrics from Java projects using CK tool
# Usage: ./collect_metrics.sh <path-to-java-project> <output-directory>

set -e

# Check if parameters are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <path-to-java-project> <output-directory>"
    exit 1
fi

PROJECT_PATH="$1"
OUTPUT_DIR="$2"
PROJECT_NAME=$(basename "$PROJECT_PATH")

# Check if CK tool exists
CK_JAR="./tools/ck-tool/ck.jar"
if [ ! -f "$CK_JAR" ]; then
    echo "Error: CK tool not found at $CK_JAR"
    echo "Please download it from https://github.com/mauricioaniche/ck"
    exit 1
fi

echo "Analyzing project: $PROJECT_NAME"
echo "Project path: $PROJECT_PATH"
echo "Output directory: $OUTPUT_DIR"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Run CK tool
echo "Running CK analysis..."
java -jar "$CK_JAR" "$PROJECT_PATH" true 0 false "$OUTPUT_DIR/${PROJECT_NAME}-metrics.csv"

echo "Analysis complete. Results saved to $OUTPUT_DIR/${PROJECT_NAME}-metrics.csv"
echo "----------------------------------------"