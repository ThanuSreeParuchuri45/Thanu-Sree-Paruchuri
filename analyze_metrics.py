#!/usr/bin/env python3
"""
Script to analyze metrics collected from Java projects.
Calculates correlations between Lines of Code (LoC) and maintainability metrics.
"""

import os
import argparse
import pandas as pd
import numpy as np
import glob

def load_project_data(file_path):
    """Load metrics data from a CSV file"""
    df = pd.read_csv(file_path)
    
    # Select only relevant columns
    selected_columns = ['class', 'loc', 'wmc', 'cbo']
    
    # Check if columns exist in the dataframe
    available_columns = [col for col in selected_columns if col in df.columns]
    if len(available_columns) < len(selected_columns):
        missing = set(selected_columns) - set(available_columns)
        print(f"Warning: Missing columns in {file_path}: {missing}")
    
    # Filter out test classes
    df = df[~df['class'].str.contains('Test|test', na=False)]
    
    # Add project name based on file name
    project_name = os.path.basename(file_path).replace('-metrics.csv', '')
    df['project'] = project_name
    
    return df[available_columns + ['project']]

def calculate_correlations(df):
    """Calculate correlations between LoC and other metrics"""
    projects = df['project'].unique()
    correlation_results = []
    
    for project in projects:
        project_df = df[df['project'] == project]
        
        # Calculate correlations
        loc_wmc_corr = project_df['loc'].corr(project_df['wmc'])
        loc_cbo_corr = project_df['loc'].corr(project_df['cbo'])
        
        correlation_results.append({
            'project': project,
            'loc_wmc_correlation': loc_wmc_corr,
            'loc_cbo_correlation': loc_cbo_corr,
            'class_count': len(project_df),
            'avg_loc': project_df['loc'].mean(),
            'avg_wmc': project_df['wmc'].mean(),
            'avg_cbo': project_df['cbo'].mean()
        })
    
    return pd.DataFrame(correlation_results)

def main():
    parser = argparse.ArgumentParser(description='Analyze software metrics')
    parser.add_argument('--input', required=True, help='Directory containing metrics CSV files')
    parser.add_argument('--output', required=True, help='Output directory for processed data')
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    
    # Get all CSV files in the input directory
    csv_files = glob.glob(os.path.join(args.input, '*-metrics.csv'))
    
    if not csv_files:
        print(f"No metrics files found in {args.input}")
        return
    
    print(f"Found {len(csv_files)} metrics files")
    
    # Load and combine all project data
    dfs = []
    for file_path in csv_files:
        try:
            df = load_project_data(file_path)
            dfs.append(df)
            print(f"Loaded data from {file_path}: {len(df)} classes")
        except Exception as e:
            print(f"Error loading {file_path}: {str(e)}")
    
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Calculate correlations
    correlation_df = calculate_correlations(combined_df)
    
    # Save processed data
    combined_df.to_csv(os.path.join(args.output, 'combined-metrics.csv'), index=False)
    correlation_df.to_csv(os.path.join(args.output, 'correlation-results.csv'), index=False)
    
    print("\nResults Summary:")
    print(correlation_df[['project', 'loc_wmc_correlation', 'loc_cbo_correlation']])
    print(f"\nProcessed data saved to {args.output}")

if __name__ == "__main__":
    main()