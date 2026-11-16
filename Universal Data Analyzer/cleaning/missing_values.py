"""Missing Values Handler Module"""
import pandas as pd
import numpy as np
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

class MissingValueHandler:
    """Handle missing values in dataframes"""
    
    def handle(self, df: pd.DataFrame, strategy: str = 'drop', subset: Optional[List[str]] = None) -> pd.DataFrame:
        """Handle missing values using specified strategy"""
        df = df.copy()
        
        if subset is None:
            subset = df.columns.tolist()
        
        logger.info(f"Applying {strategy} strategy to {len(subset)} columns")
        
        if strategy == 'drop':
            df = df.dropna(subset=subset)
            logger.info(f"Dropped rows with missing values: {df.shape}")
        
        elif strategy == 'mean':
            numeric_cols = df[subset].select_dtypes(include=['number']).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        
        elif strategy == 'median':
            numeric_cols = df[subset].select_dtypes(include=['number']).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        
        elif strategy == 'forward_fill':
            df[subset] = df[subset].ffill()
        
        elif strategy == 'backward_fill':
            df[subset] = df[subset].bfill()
        
        elif strategy == 'constant':
            df[subset] = df[subset].fillna(0)

        else:
            raise ValueError(f"Unknown missing value strategy: {strategy}")
        
        logger.info(f"Missing values after handling: {df.isnull().sum().sum()}")
        return df
    
    @staticmethod
    def get_missing_value_report(df: pd.DataFrame) -> pd.DataFrame:
        """Generate missing value report"""
        missing_report = pd.DataFrame({
            'Column': df.columns,
            'Missing_Count': df.isnull().sum().values,
            'Missing_Percentage': (df.isnull().sum().values / len(df) * 100).round(2)
        })
        
        return missing_report[missing_report['Missing_Count'] > 0].sort_values('Missing_Count', ascending=False)
