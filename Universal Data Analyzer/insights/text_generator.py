"""
Insight Generator Module - Generates text-based insights
"""
import pandas as pd
from typing import List
import logging

logger = logging.getLogger(__name__)


class InsightGenerator:
    """Generate text-based insights from data"""
    
    @staticmethod
    def generate_insights(df: pd.DataFrame) -> List[str]:
        """
        Generate insights from dataframe
        
        Args:
            df: Input dataframe
        
        Returns:
            List of insight strings
        """
        insights = []
        
        # Basic insights
        insights.append(f"Dataset contains {len(df)} rows and {len(df.columns)} columns")
        
        # Missing values insight
        missing_total = df.isnull().sum().sum()
        if missing_total > 0:
            missing_pct = (missing_total / (len(df) * len(df.columns)) * 100)
            insights.append(f"Dataset has {missing_pct:.1f}% missing values ({missing_total} total)")
        
        # Duplicate rows
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            insights.append(f"Found {duplicates} duplicate rows ({duplicates/len(df)*100:.1f}% of data)")
        
        # Numeric column insights
        numeric_cols = df.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            mean_val = df[col].mean()
            std_val = df[col].std()
            
            if std_val > 0:
                cv = (std_val / mean_val) * 100  # Coefficient of variation
                if cv > 100:
                    insights.append(f"Column '{col}' has high variability (CV: {cv:.1f}%)")
            
            # Skewness
            skew = df[col].skew()
            if abs(skew) > 1:
                skew_type = "positively" if skew > 0 else "negatively"
                insights.append(f"Column '{col}' is {skew_type} skewed (skewness: {skew:.2f})")
        
        # Categorical insights
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        for col in categorical_cols:
            unique_vals = df[col].nunique()
            if unique_vals < 10:
                top_val = df[col].value_counts().index[0]
                top_count = df[col].value_counts().values[0]
                insights.append(f"Column '{col}': Most common value is '{top_val}' ({top_count} occurrences)")
        
        logger.info(f"Generated {len(insights)} insights")
        return insights
    
    @staticmethod
    def generate_statistical_summary(df: pd.DataFrame) -> str:
        """Generate summary text"""
        summary = f"Statistical Summary:\n"
        summary += f"- Shape: {df.shape[0]} rows × {df.shape[1]} columns\n"
        summary += f"- Memory: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB\n"
        summary += f"- Numeric columns: {len(df.select_dtypes(include=['number']).columns)}\n"
        summary += f"- Categorical columns: {len(df.select_dtypes(include=['object', 'category']).columns)}\n"
        
        return summary