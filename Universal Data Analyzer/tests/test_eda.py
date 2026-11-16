"""Test EDA Module"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from eda.summary_stats import SummaryStats
from eda.correlations import CorrelationAnalyzer

class TestSummaryStats:
    """Test summary statistics"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.stats = SummaryStats()
        self.df = pd.DataFrame({
            'A': np.random.normal(100, 15, 100),
            'B': np.random.normal(50, 10, 100),
            'C': np.random.choice(['X', 'Y', 'Z'], 100)
        })
    
    def test_get_summary(self):
        """Test summary statistics generation"""
        summary = self.stats.get_summary(self.df[['A', 'B']])
        
        assert len(summary) == 2
        assert 'skewness' in summary.columns
        assert 'kurtosis' in summary.columns
    
    def test_categorical_summary(self):
        """Test categorical summary"""
        cat_summary = self.stats.get_categorical_summary(self.df)
        
        # The result is a table with one row per categorical column.
        assert 'C' in cat_summary['column'].values
        assert 'unique_values' in cat_summary.columns

class TestCorrelationAnalyzer:
    """Test correlation analysis"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.analyzer = CorrelationAnalyzer()
        self.df = pd.DataFrame({
            'X': np.random.normal(0, 1, 100),
            'Y': np.random.normal(0, 1, 100)
        })
    
    def test_correlation_values(self):
        """Test correlation value extraction"""
        corr_values = self.analyzer.get_correlation_values(self.df, threshold=0.5)
        
        assert isinstance(corr_values, pd.DataFrame)

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
