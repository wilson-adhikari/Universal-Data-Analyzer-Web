"""Chart Selector Module"""
import pandas as pd
from typing import List
import logging

logger = logging.getLogger(__name__)

class ChartSelector:
    """Recommend appropriate charts based on data"""
    
    @staticmethod
    def recommend_charts(df: pd.DataFrame, column: str = None) -> List[str]:
        """Recommend charts based on data characteristics"""
        recommendations = []
        
        if column is None:
            numeric_cols = len(df.select_dtypes(include=['number']).columns)
            categorical_cols = len(df.select_dtypes(include=['object', 'category']).columns)
            
            if numeric_cols >= 2:
                recommendations.extend(['scatter', 'line', 'heatmap'])
            
            if categorical_cols >= 1 and numeric_cols >= 1:
                recommendations.extend(['bar', 'box', 'violin'])
            
            if numeric_cols >= 1:
                recommendations.extend(['histogram', 'kde', 'distribution'])
        
        else:
            if pd.api.types.is_numeric_dtype(df[column]) and not pd.api.types.is_bool_dtype(df[column]):
                if df[column].nunique() < 20:
                    recommendations = ['bar', 'histogram', 'box', 'violin']
                else:
                    recommendations = ['histogram', 'kde', 'box', 'violin', 'scatter']
            
            else:
                recommendations = ['bar', 'pie', 'donut']
        
        logger.info(f"Recommended charts: {recommendations}")
        return recommendations
    
    @staticmethod
    def get_chart_description(chart_type: str) -> str:
        """Get description of chart type"""
        descriptions = {
            'scatter': 'Scatter plot - Shows relationship between two numeric variables',
            'line': 'Line chart - Shows trends over time or ordered data',
            'bar': 'Bar chart - Compares categorical values',
            'histogram': 'Histogram - Shows distribution of numeric data',
            'box': 'Box plot - Shows quartiles and outliers',
            'violin': 'Violin plot - Shows full distribution shape',
            'heatmap': 'Heatmap - Shows correlations or patterns in 2D data',
            'pie': 'Pie chart - Shows proportions of categories',
            'kde': 'KDE plot - Smooth distribution curve',
            'donut': 'Donut chart - Shows proportions with center hole'
        }
        
        return descriptions.get(chart_type, 'Unknown chart type')