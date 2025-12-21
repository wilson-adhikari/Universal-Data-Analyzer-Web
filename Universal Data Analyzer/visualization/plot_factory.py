import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

class PlotFactory:
    """Factory for creating various plots using matplotlib and seaborn"""
    
    @staticmethod
    def create_plot(df: pd.DataFrame, x_col: str, y_col: str, 
                   chart_type: str = 'scatter', figsize: Tuple[int, int] = (12, 6)) -> Tuple:
        """
        Create plot based on type
        
        Args:
            df: DataFrame
            x_col: X-axis column
            y_col: Y-axis column
            chart_type: Type of chart (scatter, line, bar, histogram, box, violin, kde)
            figsize: Figure size (width, height)
        
        Returns:
            Tuple of (figure, axes)
        """
        try:
            fig, ax = plt.subplots(figsize=figsize)
            
            if chart_type == 'scatter':
                ax.scatter(df[x_col], df[y_col], alpha=0.6, s=50, edgecolors='k', linewidth=0.5)
                ax.set_xlabel(x_col, fontsize=12, fontweight='bold')
                ax.set_ylabel(y_col, fontsize=12, fontweight='bold')
                ax.set_title(f"{x_col} vs {y_col}", fontsize=14, fontweight='bold')
            
            elif chart_type == 'line':
                ax.plot(df[x_col], df[y_col], marker='o', linewidth=2, markersize=6)
                ax.set_xlabel(x_col, fontsize=12, fontweight='bold')
                ax.set_ylabel(y_col, fontsize=12, fontweight='bold')
                ax.set_title(f"{x_col} vs {y_col}", fontsize=14, fontweight='bold')
                ax.grid(True, alpha=0.3)
            
            elif chart_type == 'bar':
                # Group by x_col and aggregate y_col
                grouped = df.groupby(x_col)[y_col].mean()
                ax.bar(range(len(grouped)), grouped.values, color='steelblue', edgecolor='black')
                ax.set_xticks(range(len(grouped)))
                ax.set_xticklabels(grouped.index, rotation=45, ha='right')
                ax.set_xlabel(x_col, fontsize=12, fontweight='bold')
                ax.set_ylabel(y_col, fontsize=12, fontweight='bold')
                ax.set_title(f"{y_col} by {x_col}", fontsize=14, fontweight='bold')
            
            elif chart_type == 'histogram':
                ax.hist(df[x_col].dropna(), bins=30, color='steelblue', edgecolor='black', alpha=0.7)
                ax.set_xlabel(x_col, fontsize=12, fontweight='bold')
                ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
                ax.set_title(f"Distribution of {x_col}", fontsize=14, fontweight='bold')
                ax.grid(True, alpha=0.3, axis='y')
            
            elif chart_type == 'box':
                # Box plot requires categorical x and numeric y
                if df[x_col].dtype == 'object':
                    sns.boxplot(x=x_col, y=y_col, data=df, ax=ax, palette='Set2')
                else:
                    ax.boxplot(df[y_col].dropna())
                    ax.set_ylabel(y_col, fontsize=12, fontweight='bold')
                    ax.set_title(f"Box Plot of {y_col}", fontsize=14, fontweight='bold')
            
            elif chart_type == 'violin':
                if df[x_col].dtype == 'object':
                    sns.violinplot(x=x_col, y=y_col, data=df, ax=ax, palette='Set2')
                else:
                    sns.violinplot(y=y_col, data=df, ax=ax, palette='Set2')
                ax.set_title(f"Violin Plot of {y_col}", fontsize=14, fontweight='bold')
            
            elif chart_type == 'kde':
                # Kernel Density Estimation
                df[x_col].dropna().plot(kind='kde', ax=ax, color='steelblue', linewidth=2)
                ax.set_xlabel(x_col, fontsize=12, fontweight='bold')
                ax.set_ylabel('Density', fontsize=12, fontweight='bold')
                ax.set_title(f"KDE of {x_col}", fontsize=14, fontweight='bold')
                ax.grid(True, alpha=0.3)
            
            else:
                # Default to scatter
                ax.scatter(df[x_col], df[y_col], alpha=0.6, s=50)
                ax.set_xlabel(x_col, fontsize=12, fontweight='bold')
                ax.set_ylabel(y_col, fontsize=12, fontweight='bold')
                ax.set_title(f"{x_col} vs {y_col}", fontsize=14, fontweight='bold')
            
            plt.tight_layout()
            logger.info(f"Created {chart_type} plot for {x_col} vs {y_col}")
            return fig, ax
        
        except Exception as e:
            logger.error(f"Error creating plot: {str(e)}")
            raise
    
    @staticmethod
    def create_pie_chart(df: pd.DataFrame, labels_col: str, values_col: str,
                        figsize: Tuple[int, int] = (10, 8)) -> Tuple:
        """Create pie chart"""
        try:
            fig, ax = plt.subplots(figsize=figsize)
            grouped = df.groupby(labels_col)[values_col].sum()
            colors = sns.color_palette('husl', len(grouped))
            ax.pie(grouped.values, labels=grouped.index, autopct='%1.1f%%',
                   colors=colors, startangle=90)
            ax.set_title(f"Distribution of {labels_col}", fontsize=14, fontweight='bold')
            plt.tight_layout()
            logger.info(f"Created pie chart for {labels_col}")
            return fig, ax
        
        except Exception as e:
            logger.error(f"Error creating pie chart: {str(e)}")
            raise
    
    @staticmethod
    def create_subplots(df: pd.DataFrame, columns: list, chart_type: str = 'histogram',
                       figsize: Tuple[int, int] = (15, 10)) -> Tuple:
        """Create subplots for multiple columns"""
        try:
            n_cols = len(columns)
            n_rows = (n_cols + 1) // 2
            
            fig, axes = plt.subplots(n_rows, 2, figsize=figsize)
            axes = axes.flatten()
            
            for idx, col in enumerate(columns):
                ax = axes[idx]
                
                if chart_type == 'histogram':
                    ax.hist(df[col].dropna(), bins=20, color='steelblue', edgecolor='black', alpha=0.7)
                    ax.set_title(f"Distribution of {col}", fontweight='bold')
                    ax.set_xlabel('Value')
                    ax.set_ylabel('Frequency')
                
                elif chart_type == 'box':
                    ax.boxplot(df[col].dropna())
                    ax.set_title(f"Box Plot of {col}", fontweight='bold')
                    ax.set_ylabel('Value')
                
                elif chart_type == 'kde':
                    df[col].dropna().plot(kind='kde', ax=ax, color='steelblue', linewidth=2)
                    ax.set_title(f"KDE of {col}", fontweight='bold')
                    ax.set_ylabel('Density')
            
            # Hide unused subplots
            for idx in range(len(columns), len(axes)):
                axes[idx].axis('off')
            
            plt.tight_layout()
            logger.info(f"Created subplots for {len(columns)} columns")
            return fig, axes
        
        except Exception as e:
            logger.error(f"Error creating subplots: {str(e)}")
            raise
    
    @staticmethod
    def create_regression_plot(df: pd.DataFrame, x_col: str, y_col: str,
                              figsize: Tuple[int, int] = (12, 6)) -> Tuple:
        """Create scatter plot with regression line"""
        try:
            fig, ax = plt.subplots(figsize=figsize)
            sns.regplot(x=x_col, y=y_col, data=df, ax=ax, scatter_kws={'alpha': 0.6, 's': 50},
                       line_kws={'color': 'red', 'linewidth': 2})
            ax.set_xlabel(x_col, fontsize=12, fontweight='bold')
            ax.set_ylabel(y_col, fontsize=12, fontweight='bold')
            ax.set_title(f"{x_col} vs {y_col} (with regression)", fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            logger.info(f"Created regression plot for {x_col} vs {y_col}")
            return fig, ax
        
        except Exception as e:
            logger.error(f"Error creating regression plot: {str(e)}")
            raise
