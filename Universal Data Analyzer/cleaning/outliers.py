"""Outliers Handler Module"""
import pandas as pd
import numpy as np
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class OutlierHandler:
    """Handle outliers in numerical data"""
    
    @staticmethod
    def remove_outliers(df: pd.DataFrame, column: str, method: str = 'iqr', threshold: Optional[float] = None) -> pd.DataFrame:
        """Remove outliers using specified method"""
        df = df.copy()
        if threshold is None:
            threshold = 1.5 if method == 'iqr' else 3.0
        
        if method == 'iqr':
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            
            before = len(df)
            df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
            after = len(df)
            
            logger.info(f"IQR method removed {before - after} outliers from {column}")
        
        elif method == 'zscore':
            z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
            before = len(df)
            df = df[z_scores < threshold]
            after = len(df)
            
            logger.info(f"Z-score method removed {before - after} outliers from {column}")
        
        return df
    
    @staticmethod
    def detect_outliers(df: pd.DataFrame, column: str, method: str = 'iqr') -> pd.DataFrame:
        """Detect outliers without removing"""
        if method == 'iqr':
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            
            outliers = df[(df[column] < (Q1 - 1.5 * IQR)) | (df[column] > (Q3 + 1.5 * IQR))]
        
        elif method == 'zscore':
            z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
            outliers = df[z_scores > 3]
        
        logger.info(f"Detected {len(outliers)} outliers in {column}")
        return outliers
    
    @staticmethod
    def get_outlier_report(df: pd.DataFrame) -> dict:
        """Generate outlier report for all numeric columns"""
        numeric_cols = df.select_dtypes(include=['number']).columns
        report = {}
        
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            outlier_count = len(df[(df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))])
            report[col] = {
                'outlier_count': outlier_count,
                'outlier_percentage': (outlier_count / len(df) * 100) if len(df) > 0 else 0,
                'lower_bound': Q1 - 1.5 * IQR,
                'upper_bound': Q3 + 1.5 * IQR
            }
        
        return report