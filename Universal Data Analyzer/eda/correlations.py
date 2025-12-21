import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logger = logging.getLogger(__name__)

class CorrelationAnalyzer:
    """Analyze correlations between variables"""
    
    @staticmethod
    def plot_correlation_matrix(df: pd.DataFrame, method: str = 'pearson',
                               figsize: tuple = (12, 10)) -> tuple:
        """Plot correlation heatmap using seaborn"""
        try:
            fig, ax = plt.subplots(figsize=figsize)
            corr_matrix = df.corr(method=method)
            
            # Create heatmap
            sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdBu_r', 
                       center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8},
                       ax=ax, vmin=-1, vmax=1)
            
            ax.set_title(f"Correlation Matrix ({method})", fontsize=14, fontweight='bold', pad=20)
            plt.tight_layout()
            logger.info(f"Created correlation matrix plot using {method} method")
            return fig, ax
        
        except Exception as e:
            logger.error(f"Error creating correlation matrix: {str(e)}")
            raise
    
    @staticmethod
    def get_correlation_values(df: pd.DataFrame, method: str = 'pearson',
                              threshold: float = 0.7) -> pd.DataFrame:
        """Get strong correlations above threshold"""
        try:
            corr_matrix = df.corr(method=method)
            
            corr_pairs = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_value = corr_matrix.iloc[i, j]
                    if abs(corr_value) >= threshold:
                        corr_pairs.append({
                            'Variable1': corr_matrix.columns[i],
                            'Variable2': corr_matrix.columns[j],
                            'Correlation': round(corr_value, 4)
                        })
            
            result = pd.DataFrame(corr_pairs).sort_values('Correlation', key=abs, ascending=False)
            logger.info(f"Found {len(result)} correlations above threshold {threshold}")
            return result
        
        except Exception as e:
            logger.error(f"Error getting correlation values: {str(e)}")
            raise
    
    @staticmethod
    def plot_scatter_with_regression(df: pd.DataFrame, x_col: str, y_col: str,
                                    figsize: tuple = (12, 6)) -> tuple:
        """Plot scatter plot with regression line"""
        try:
            fig, ax = plt.subplots(figsize=figsize)
            sns.regplot(x=x_col, y=y_col, data=df, ax=ax,
                       scatter_kws={'alpha': 0.6, 's': 50, 'color': 'steelblue'},
                       line_kws={'color': 'red', 'linewidth': 2})
            
            ax.set_xlabel(x_col, fontsize=12, fontweight='bold')
            ax.set_ylabel(y_col, fontsize=12, fontweight='bold')
            ax.set_title(f"{x_col} vs {y_col} (Linear Regression)", fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            logger.info(f"Created regression plot for {x_col} vs {y_col}")
            return fig, ax
        
        except Exception as e:
            logger.error(f"Error creating regression plot: {str(e)}")
            raise
    
    @staticmethod
    def plot_pairplot(df: pd.DataFrame, columns: list = None,
                     figsize: tuple = (12, 12)) -> object:
        """Create pairplot for exploratory analysis"""
        try:
            if columns:
                df_subset = df[columns]
            else:
                df_subset = df.select_dtypes(include=[np.number])
            
            pairplot = sns.pairplot(df_subset, diag_kind='hist', 
                                   plot_kws={'alpha': 0.6, 's': 30},
                                   diag_kws={'bins': 20, 'edgecolor': 'black'})
            
            logger.info(f"Created pairplot for {len(df_subset.columns)} columns")
            return pairplot
        
        except Exception as e:
            logger.error(f"Error creating pairplot: {str(e)}")
            raise
    @staticmethod
    def plot_heatmap(df: pd.DataFrame, x_col: str, y_col: str,
                     figsize: tuple = (12, 8), bins: int = 30) -> tuple:
        """Plot heatmap for two continuous variables"""
        try:
            fig, ax = plt.subplots(figsize=figsize)
            hb = ax.hexbin(df[x_col], df[y_col], gridsize=bins, cmap='Blues', mincnt=1)
            cb = fig.colorbar(hb, ax=ax)
            cb.set_label('Counts')
            
            ax.set_xlabel(x_col, fontsize=12, fontweight='bold')
            ax.set_ylabel(y_col, fontsize=12, fontweight='bold')
            ax.set_title(f"Heatmap of {x_col} vs {y_col}", fontsize=14, fontweight='bold')
            plt.tight_layout()
            logger.info(f"Created heatmap for {x_col} vs {y_col}")
            return fig, ax
        
        except Exception as e:
            logger.error(f"Error creating heatmap: {str(e)}")
            raise
        