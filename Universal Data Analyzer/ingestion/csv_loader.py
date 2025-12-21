"""CSV Data Loader Module"""
import pandas as pd
from typing import Union
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class CSVLoader:
    """Load and validate CSV files"""
    
    def __init__(self, encoding='utf-8', sep=None):
        self.encoding = encoding
        self.sep = sep
    
    def load(self, filepath: Union[str, Path], **kwargs) -> pd.DataFrame:
        """Load CSV file with automatic separator detection"""
        try:
            if self.sep is None:
                df = pd.read_csv(filepath, encoding=self.encoding, **kwargs)
            else:
                df = pd.read_csv(filepath, sep=self.sep, encoding=self.encoding, **kwargs)
            
            logger.info(f"Successfully loaded CSV: {len(df)} rows, {len(df.columns)} columns")
            return df
        
        except Exception as e:
            logger.error(f"Error loading CSV: {str(e)}")
            raise
    
    def detect_separator(self, filepath: Union[str, Path]) -> str:
        """Detect CSV separator"""
        with open(filepath, 'r', encoding=self.encoding) as f:
            first_line = f.readline()
        
        separators = [',', ';', '\t', '|']
        for sep in separators:
            if sep in first_line:
                logger.info(f"Detected separator: '{sep}'")
                return sep
        
        return ','
