"""Excel Data Loader Module"""
import pandas as pd
from typing import Union
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class ExcelLoader:
    """Load and validate Excel files"""
    
    def __init__(self):
        pass
    
    def load(self, filepath: Union[str, Path], sheet_name=0, **kwargs) -> pd.DataFrame:
        """Load Excel file"""
        try:
            df = pd.read_excel(filepath, sheet_name=sheet_name, **kwargs)
            logger.info(f"Successfully loaded Excel: {len(df)} rows, {len(df.columns)} columns")
            return df
        
        except Exception as e:
            logger.error(f"Error loading Excel: {str(e)}")
            raise
    
    def list_sheets(self, filepath: Union[str, Path]) -> list:
        """Get list of sheet names"""
        try:
            xls = pd.ExcelFile(filepath)
            logger.info(f"Available sheets: {xls.sheet_names}")
            return xls.sheet_names
        
        except Exception as e:
            logger.error(f"Error listing sheets: {str(e)}")
            raise
    
    def load_all_sheets(self, filepath: Union[str, Path]) -> dict:
        """Load all sheets as dataframes"""
        try:
            xls = pd.ExcelFile(filepath)
            dfs = {sheet: pd.read_excel(filepath, sheet_name=sheet) for sheet in xls.sheet_names}
            logger.info(f"Loaded {len(dfs)} sheets")
            return dfs
        
        except Exception as e:
            logger.error(f"Error loading sheets: {str(e)}")
            raise
