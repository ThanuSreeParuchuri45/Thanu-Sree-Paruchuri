#!/usr/bin/env python3
"""
Script to generate visualizations from the processed metrics data.
Creates scatter plots showing relationships between LoC and maintainability metrics.
"""

import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def setup_plot_style():
    """Set up the plot style for better visualizations"""
    sns.set(style="whitegrid")
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.labelsize'] = 14
    plt.rcParams['axes.titlesize'] = 16
    plt.rcParams['xtick.labelsize'] = 12
    plt.rcParams['ytick.labelsize'] = 12
    plt.rcParams['legend.fontsize'] = 12

def create_scatter_plot(df, x_col, y_col, output_path, title, xlabel, ylabel):
    """Create a scatter plot with regression line"""
    plt.figure()
    
    # Create scatter plot
    ax = sns.scatterplot(data=df, x=x_col, y=y_col, hue='project', alpha=0.6)
    
    # Add regression line
    sns.regplot(data=df, x=x_col, y=y_col, scatter=False, ax=ax, color='black')
    
    # Calculate correlation
    correlation = df[x_col].corr(df[y_col])
    
    # Add correlation text
    plt.text(0.05, 0.95, f'Correlation (r): {correlation:.2f}', 
             transform=ax.transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.5))
    
    # Set plot labels and title
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    # Add grid
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Handle legend
    plt.legend(title='Project', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Tight layout
    plt.tight_layout()
    
    # Save figure
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Created scatter plot: {output_path}")

def create_project_specific_plots(df, output_dir):
    """Create scatter plots for each project"""
    projects = df['project'].unique()
    
    for project in projects:
        project_df = df[df['project'] == project]
        
        # WMC vs LoC
        create_scatter_plot(
            project_df, 'loc', 'wmc',
            os.path.join(output_dir, f'{project}-wmc-loc.png'),
            f'Complexity (WMC) vs. Class Size (LoC) for {project}',
            'Lines of Code (LoC)', 'Weighted Methods per Class (WMC)'
        )
        
        # CBO vs LoC
        create_scatter_plot(
            project_df, 'loc', 'cbo',
            os.path.join(output_dir, f'{project}-cbo-loc.png'),
            f'Coupling (CBO) vs. Class Size (LoC) for {project}',
            'Lines of Code (LoC)', 'Coupling Between Objects (CBO)'
        )

def create_correlation_bar_chart(correlation_df, output_dir):
    """Create bar charts summarizing correlations across projects"""
    plt.figure(figsize=(10, 6))
    
    # Create grouped bar chart
    x = np.arange(len(correlation_df))
    width = 0.35
    
    plt.bar(x - width/2, correlation_df['loc_wmc_correlation'], width, label='LoC-WMC')
    plt.bar(x + width/2, correlation_df['loc_cbo_correlation'], width, label='LoC-CBO')
    
    plt.xlabel('Project')
    plt.ylabel('Correlation Coefficient (r)')
    plt.title('Correlation between Class Size and Maintainability Metrics')
    plt.xticks(x, correlation_df['project'], rotation=45, ha='right')
    plt.legend()
    plt.ylim(0, 1)
    
    # Add grid
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Tight layout
    plt.tight_layout()
    
    # Save figure
    output_path = os.path.join(output_dir, 'correlation-summary.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Created correlation bar chart: {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Generate visualizations from metrics data')
    parser.add_argument('--input', required=True, help='Directory containing processed metrics data')
    parser.add_argument('--output', required=True, help='Output directory for visualizations')
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    
    # Set up plotting style
    setup_plot_style()
    
    # Load processed data
    combined_data_path = os.path.join(args.input, 'combined-metrics.csv')
    correlation_data_path = os.path.join(args.input, 'correlation-results.csv')
    
    if not os.path.exists(combined_data_path):
        print(f"Error: Combined metrics file not found at {combined_data_path}")
        return
    
    if not os.path.exists(correlation_data_path):
        print(f"Error: Correlation results file not found at {correlation_data_path}")
        return
    
    combined_df = pd.read_csv(combined_data_path)
    correlation_df = pd.read_csv(correlation_data_path)
    
    # Create overall scatter plots
    create_scatter_plot(
        combined_df, 'loc', 'wmc',
        os.path.join(args.output, 'wmc-loc-scatter.png'),
        'Complexity (WMC) vs. Class Size (LoC) Across Projects',
        'Lines of Code (LoC)', 'Weighted Methods per Class (WMC)'
    )
    
    create_scatter_plot(
        combined_df, 'loc', 'cbo',
        os.path.join(args.output, 'cbo-loc-scatter.png'),
        'Coupling (CBO) vs. Class Size (LoC) Across Projects',
        'Lines of Code (LoC)', 'Coupling Between Objects (CBO)'
    )
    
    # Create project-specific plots
    create_project_specific_plots(combined_df, args.output)
    
    # Create correlation summary
    create_correlation_bar_chart(correlation_df, args.output)
    
    print(f"All visualizations generated in {args.output}")

if __name__ == "__main__":
    main()