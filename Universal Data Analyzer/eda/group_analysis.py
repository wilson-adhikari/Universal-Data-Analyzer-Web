import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logger = logging.getLogger(__name__)

class GroupAnalyzer:
    """Perform group-based analysis"""
    
    @staticmethod
    def group_statistics(df: pd.DataFrame, groupby_col: str, agg_cols: list = None,
                        agg_funcs: list = None) -> pd.DataFrame:
        """Generate group statistics"""
        if agg_cols is None:
            agg_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if agg_funcs is None:
            agg_funcs = ['mean', 'sum', 'count', 'std']
        
        grouped = df.groupby(groupby_col)[agg_cols].agg(agg_funcs)
        
        logger.info(f"Generated group statistics for {groupby_col}")
        return grouped
    
    @staticmethod
    def plot_grouped_bar(df: pd.DataFrame, groupby_col: str, value_col: str,
                        agg_func: str = 'mean', figsize: tuple = (12, 6)) -> tuple:
        """Plot grouped bar chart"""
        try:
            grouped = df.groupby(groupby_col)[value_col].agg(agg_func).reset_index()
            
            fig, ax = plt.subplots(figsize=figsize)
            bars = ax.bar(grouped[groupby_col], grouped[value_col], color='steelblue', edgecolor='black')
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.2f}', ha='center', va='bottom', fontweight='bold')
            
            ax.set_xlabel(groupby_col, fontsize=12, fontweight='bold')
            ax.set_ylabel(value_col, fontsize=12, fontweight='bold')
            ax.set_title(f"{value_col} by {groupby_col} ({agg_func})", fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            logger.info(f"Created grouped bar plot for {groupby_col}")
            return fig, ax
        
        except Exception as e:
            logger.error(f"Error creating grouped bar plot: {str(e)}")
            raise
    
    @staticmethod
    def plot_grouped_line(df: pd.DataFrame, x_col: str, y_col: str, color_col: str,
                         figsize: tuple = (12, 6)) -> tuple:
        """Plot grouped line chart"""
        try:
            fig, ax = plt.subplots(figsize=figsize)
            
            # Get unique values in color column
            groups = df[color_col].unique()
            colors = sns.color_palette('husl', len(groups))
            
            for idx, group in enumerate(groups):
                group_data = df[df[color_col] == group].sort_values(x_col)
                ax.plot(group_data[x_col], group_data[y_col], marker='o',
                       label=str(group), linewidth=2, markersize=6, color=colors[idx])
            
            ax.set_xlabel(x_col, fontsize=12, fontweight='bold')
            ax.set_ylabel(y_col, fontsize=12, fontweight='bold')
            ax.set_title(f"{y_col} over {x_col} by {color_col}", fontsize=14, fontweight='bold')
            ax.legend(title=color_col, loc='best')
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            logger.info(f"Created grouped line plot")
            return fig, ax
        
        except Exception as e:
            logger.error(f"Error creating grouped line plot: {str(e)}")
            raise
    
    @staticmethod
    def plot_pivot_heatmap(df: pd.DataFrame, index_col: str, columns_col: str,
                          values_col: str, aggfunc: str = 'mean',
                          figsize: tuple = (12, 8)) -> tuple:
        """Create pivot table and plot as heatmap"""
        try:
            pivot = df.pivot_table(index=index_col, columns=columns_col,
                                  values=values_col, aggfunc=aggfunc)
            
            fig, ax = plt.subplots(figsize=figsize)
            sns.heatmap(pivot, annot=True, fmt='.2f', cmap='YlGnBu',
                       ax=ax, cbar_kws={'label': values_col})
            
            ax.set_title(f"{values_col} by {index_col} and {columns_col} ({aggfunc})",
                        fontsize=14, fontweight='bold', pad=20)
            plt.tight_layout()
            logger.info(f"Created pivot heatmap")
            return fig, ax
        
        except Exception as e:
            logger.error(f"Error creating pivot heatmap: {str(e)}")
            raise
    
    @staticmethod
    def plot_boxplot_groups(df: pd.DataFrame, groupby_col: str, value_col: str,
                           figsize: tuple = (12, 6)) -> tuple:
        """Create grouped box plots"""
        try:
            fig, ax = plt.subplots(figsize=figsize)
            sns.boxplot(x=groupby_col, y=value_col, data=df, ax=ax, palette='Set2')
            
            ax.set_xlabel(groupby_col, fontsize=12, fontweight='bold')
            ax.set_ylabel(value_col, fontsize=12, fontweight='bold')
            ax.set_title(f"Distribution of {value_col} by {groupby_col}",
                        fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            logger.info(f"Created boxplot groups for {groupby_col}")
            return fig, ax
        
        except Exception as e:
            logger.error(f"Error creating boxplot groups: {str(e)}")
            raise
           