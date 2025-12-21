import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)
class SummaryStats:
    
    @staticmethod
    def get_summary(df: pd.DataFrame) -> pd.DataFrame:
        """
        Get comprehensive summary statistics
        
        Args:
            df: Input dataframe
        
        Returns:
            pd.DataFrame: Summary statistics
        """
        numeric_df = df.select_dtypes(include=['number'])
        summary = numeric_df.describe().T
        
        # Add additional statistics
        summary['skewness'] = numeric_df.skew()
        summary['kurtosis'] = numeric_df.kurtosis()
        summary['variance'] = numeric_df.var()
        summary['median'] = numeric_df.median()
        summary['mode'] = numeric_df.mode().iloc[0] if len(numeric_df.mode()) > 0 else np.nan
        
        logger.info(f"Generated summary statistics for {len(summary)} columns")
        return summary
    @staticmethod
    def get_categorical_summary(df: pd.DataFrame) -> pd.DataFrame:
        """
        Get summary statistics for categorical columns
        """
        categorical_df = df.select_dtypes(include=['object', 'category'])
        summary_list = []
        
        for col in categorical_df.columns:
            value_counts = categorical_df[col].value_counts(dropna=False)
            top_value = value_counts.idxmax()
            top_freq = value_counts.max()
            unique_count = categorical_df[col].nunique(dropna=False)
            missing_count = categorical_df[col].isnull().sum()
            
            summary_list.append({
                'column': col,
                'unique_values': unique_count,
                'top_value': top_value,
                'top_frequency': top_freq,
                'missing_values': missing_count
            })
        
        summary_df = pd.DataFrame(summary_list)
        logger.info(f"Generated categorical summary for {len(summary_df)} columns")
        return summary_df
    @staticmethod
    def get_overall_summary(df: pd.DataFrame) -> pd.DataFrame:
        """
        Get overall summary including both numeric and categorical statistics
        """
        numeric_summary = SummaryStats.get_summary(df)
        categorical_summary = SummaryStats.get_categorical_summary(df)
        
        overall_summary = {
            'numeric_summary': numeric_summary,
            'categorical_summary': categorical_summary
        }
        
        logger.info("Generated overall summary statistics")
        return overall_summary