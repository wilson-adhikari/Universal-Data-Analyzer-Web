"""Utility Validators Module"""
import pandas as pd
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

class DataValidator:
    """Validate data integrity and quality"""
    
    @staticmethod
    def validate_dataframe(df: pd.DataFrame) -> Tuple[bool, list]:
        """Validate dataframe"""
        issues = []
        
        if df is None:
            issues.append("DataFrame is None")
            return False, issues
        
        if len(df) == 0:
            issues.append("DataFrame is empty (0 rows)")
        
        if len(df.columns) == 0:
            issues.append("DataFrame has no columns")
        
        for col in df.columns:
            if df[col].isnull().all():
                issues.append(f"Column '{col}' contains only NaN values")
        
        if len(df.columns) != len(df.columns.unique()):
            issues.append("DataFrame has duplicate column names")
        
        logger.info(f"Validation complete: {len(issues)} issues found")
        return len(issues) == 0, issues
    
    @staticmethod
    def check_data_quality(df: pd.DataFrame) -> dict:
        """Generate data quality score"""
        total_cells = len(df) * len(df.columns)
        missing_cells = df.isnull().sum().sum()
        duplicate_rows = df.duplicated().sum()
        
        quality_score = 100
        
        if total_cells > 0:
            missing_pct = (missing_cells / total_cells) * 100
            quality_score -= min(missing_pct * 0.5, 30)
        
        if len(df) > 0:
            dup_pct = (duplicate_rows / len(df)) * 100
            quality_score -= min(dup_pct * 0.5, 20)
        
        return {
            'quality_score': max(0, quality_score),
            'missing_percentage': (missing_cells / total_cells * 100) if total_cells > 0 else 0,
            'duplicate_rows': int(duplicate_rows),
            'total_cells': total_cells,
            'missing_cells': int(missing_cells)
        }
