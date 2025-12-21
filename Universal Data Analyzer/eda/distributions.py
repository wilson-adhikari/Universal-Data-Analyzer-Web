import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import logging

logger = logging.getLogger(__name__)

class DistributionAnalyzer:
    """Analyze data distributions with matplotlib and seaborn"""
    
    @staticmethod
    def plot_distribution(df: pd.DataFrame, column: str, bins: int = 30,
                         figsize: tuple = (12, 6)) -> tuple:
        """Plot distribution histogram with KDE"""
        try:
            fig, ax = plt.subplots(figsize=figsize)
            
            # Histogram with KDE
            ax.hist(df[column].dropna(), bins=bins, color='steelblue', 
                   edgecolor='black', alpha=0.7, density=True)
            
            # Add KDE curve
            df[column].dropna().plot(kind='kde', ax=ax, color='red', linewidth=2, secondary_y=False)
            
            ax.set_xlabel(column, fontsize=12, fontweight='bold')
            ax.set_ylabel('Density', fontsize=12, fontweight='bold')
            ax.set_title(f"Distribution of {column}", fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
            
            plt.tight_layout()
            logger.info(f"Created distribution plot for {column}")
            return fig, ax
        
        except Exception as e:
            logger.error(f"Error creating distribution plot: {str(e)}")
            raise
    
    @staticmethod
    def plot_box(df: pd.DataFrame, column: str, figsize: tuple = (12, 6)) -> tuple:
        """Plot box plot"""
        try:
            fig, ax = plt.subplots(figsize=figsize)
            sns.boxplot(y=column, data=df, ax=ax, color='lightblue', width=0.5)
            ax.set_ylabel(column, fontsize=12, fontweight='bold')
            ax.set_title(f"Box Plot of {column}", fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
            plt.tight_layout()
            logger.info(f"Created box plot for {column}")
            return fig, ax
        
        except Exception as e:
            logger.error(f"Error creating box plot: {str(e)}")
            raise
    
    @staticmethod
    def plot_violin(df: pd.DataFrame, column: str, group_by: str = None,
                   figsize: tuple = (12, 6)) -> tuple:
        """Plot violin plot"""
        try:
            fig, ax = plt.subplots(figsize=figsize)
            
            if group_by and group_by in df.columns:
                sns.violinplot(x=group_by, y=column, data=df, ax=ax, palette='Set2')
                ax.set_xlabel(group_by, fontsize=12, fontweight='bold')
            else:
                sns.violinplot(y=column, data=df, ax=ax, color='lightblue')
            
            ax.set_ylabel(column, fontsize=12, fontweight='bold')
            ax.set_title(f"Violin Plot of {column}", fontsize=14, fontweight='bold')
            plt.tight_layout()
            logger.info(f"Created violin plot for {column}")
            return fig, ax
        
        except Exception as e:
            logger.error(f"Error creating violin plot: {str(e)}")
            raise
    
    @staticmethod
    def plot_qq(df: pd.DataFrame, column: str, figsize: tuple = (10, 8)) -> tuple:
        """Plot Q-Q plot for normality check"""
        try:
            fig, ax = plt.subplots(figsize=figsize)
            data = df[column].dropna()
            stats.probplot(data, dist="norm", plot=ax)
            ax.set_title(f"Q-Q Plot for {column}", fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            logger.info(f"Created Q-Q plot for {column}")
            return fig, ax
        
        except Exception as e:
            logger.error(f"Error creating Q-Q plot: {str(e)}")
            raise
    
    @staticmethod
    def plot_multiple_distributions(df: pd.DataFrame, columns: list,
                                   figsize: tuple = (15, 10)) -> tuple:
        """Plot distributions for multiple numeric columns"""
        try:
            n_cols = len(columns)
            n_rows = (n_cols + 1) // 2
            
            fig, axes = plt.subplots(n_rows, 2, figsize=figsize)
            axes = axes.flatten()
            
            for idx, col in enumerate(columns):
                ax = axes[idx]
                ax.hist(df[col].dropna(), bins=20, color='steelblue', 
                       edgecolor='black', alpha=0.7)
                ax.set_title(f"Distribution of {col}", fontweight='bold')
                ax.set_xlabel('Value')
                ax.set_ylabel('Frequency')
                ax.grid(True, alpha=0.3, axis='y')
            
            # Hide unused subplots
            for idx in range(len(columns), len(axes)):
                axes[idx].axis('off')
            
            plt.tight_layout()
            logger.info(f"Created distribution plots for {len(columns)} columns")
            return fig, axes
        
        except Exception as e:
            logger.error(f"Error creating distribution plots: {str(e)}")
            raise
