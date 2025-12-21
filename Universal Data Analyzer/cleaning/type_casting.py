"""Type Casting Module"""
import pandas as pd
import numpy as np
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class TypeCaster:
    """Handle type conversion for columns"""
    
    def cast(self, series: pd.Series, target_type: str) -> pd.Series:
        """Cast series to target type"""
        try:
            if target_type == 'int':
                return pd.to_numeric(series, errors='coerce').astype('Int64')
            
            elif target_type == 'float':
                return pd.to_numeric(series, errors='coerce').astype('float64')
            
            elif target_type == 'string':
                return series.astype('string')
            
            elif target_type == 'datetime':
                return pd.to_datetime(series, errors='coerce')
            
            elif target_type == 'bool':
                return series.astype('bool')
            
            elif target_type == 'category':
                return series.astype('category')
            
            else:
                logger.warning(f"Unknown target type: {target_type}")
                return series
        
        except Exception as e:
            logger.error(f"Error casting to {target_type}: {str(e)}")
            raise
    
    @staticmethod
    def auto_detect_types(df: pd.DataFrame) -> pd.DataFrame:
        """Auto-detect and cast appropriate types"""
        df = df.copy()
        
        for col in df.columns:
            try:
                numeric = pd.to_numeric(df[col], errors='coerce')
                if numeric.notna().sum() / len(df) > 0.8:
                    if numeric.dtype == 'int64':
                        df[col] = numeric.astype('Int64')
                    else:
                        df[col] = numeric
                    continue
            except:
                pass
            
            try:
                datetime = pd.to_datetime(df[col], errors='coerce')
                if datetime.notna().sum() / len(df) > 0.8:
                    df[col] = datetime
                    continue
            except:
                pass
        
        logger.info("Auto-detected and casted types")
        return df
    
    @staticmethod
    def get_type_report(df: pd.DataFrame) -> pd.DataFrame:
        """Generate type information report"""
        type_report = pd.DataFrame({
            'Column': df.columns,
            'Data_Type': df.dtypes.values,
            'Non_Null_Count': df.count().values,
            'Null_Count': df.isnull().sum().values,
            'Unique_Count': df.nunique().values
        })
        
        return type_report
