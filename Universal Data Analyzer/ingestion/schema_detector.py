"""Schema Detection Module"""
import pandas as pd
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class SchemaDetector:
    """Detect and analyze data schema"""
    
    @staticmethod
    def detect_schema(df: pd.DataFrame) -> Dict:
        """Detect data types and schema"""
        schema = {
            'columns': {},
            'primary_key': None,
            'statistics': {}
        }
        
        for col in df.columns:
            dtype = str(df[col].dtype)
            schema['columns'][col] = {
                'type': dtype,
                'null_count': int(df[col].isnull().sum()),
                'unique_values': int(df[col].nunique()),
                'sample_values': df[col].dropna().unique()[:5].tolist()
            }
            
            if pd.api.types.is_numeric_dtype(df[col]) and not pd.api.types.is_bool_dtype(df[col]):
                schema['columns'][col]['statistics'] = {
                    'min': float(df[col].min()),
                    'max': float(df[col].max()),
                    'mean': float(df[col].mean()),
                    'std': float(df[col].std())
                }
        
        logger.info(f"Detected schema for {len(schema['columns'])} columns")
        return schema
    
    @staticmethod
    def infer_primary_key(df: pd.DataFrame) -> str:
        """Infer primary key column"""
        for col in df.columns:
            if df[col].nunique() == len(df) and df[col].isnull().sum() == 0:
                logger.info(f"Inferred primary key: {col}")
                return col
        return None
    
    @staticmethod
    def get_data_quality_report(df: pd.DataFrame) -> Dict:
        """Generate data quality report"""
        report = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'total_missing': int(df.isnull().sum().sum()),
            'missing_percentage': float((df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100)),
            'duplicate_rows': int(df.duplicated().sum()),
            'numeric_columns': len(df.select_dtypes(include=['number']).columns),
            'categorical_columns': len(df.select_dtypes(include=['object']).columns),
            'datetime_columns': len(df.select_dtypes(include=['datetime64']).columns),
            'memory_usage_mb': float(df.memory_usage(deep=True).sum() / 1024**2)
        }
        
        return report