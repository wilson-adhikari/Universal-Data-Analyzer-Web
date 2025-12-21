import pandas as pd
from typing import Dict, Any
import logging
from datetime import datetime
logger = logging.getLogger(__name__)

class DataExporter:
    """Export data to various formats"""
    
    @staticmethod
    def export_to_csv(df: pd.DataFrame, file_path: str, index: bool = False) -> None:
        """
        Export DataFrame to CSV file
        
        Args:
            df: Input dataframe
            file_path: Path to save the CSV file
            index: Whether to write row names (index)
        """
        try:
            df.to_csv(file_path, index=index)
            logger.info(f"Data exported successfully to {file_path}")
        except Exception as e:
            logger.error(f"Failed to export data to CSV: {e}")
            raise

    @staticmethod
    def export_to_json(df: pd.DataFrame, file_path: str, orient: str = 'records') -> None:
        """
        Export DataFrame to JSON file
        
        Args:
            df: Input dataframe
            file_path: Path to save the JSON file
            orient: String indicating the format of the JSON output
        """
        try:
            df.to_json(file_path, orient=orient, lines=True)
            logger.info(f"Data exported successfully to {file_path}")
        except Exception as e:
            logger.error(f"Failed to export data to JSON: {e}")
            raise
    @staticmethod
    def export_to_excel(df: pd.DataFrame, file_path: str, index: bool = False) -> None:
        """
        Export DataFrame to Excel file
        
        Args:
            df: Input dataframe
            file_path: Path to save the Excel file
            index: Whether to write row names (index)
        """
        try:
            df.to_excel(file_path, index=index)
            logger.info(f"Data exported successfully to {file_path}")
        except Exception as e:
            logger.error(f"Failed to export data to Excel: {e}")
            raise