"""Test Data Ingestion Module"""
import pytest
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from ingestion.csv_loader import CSVLoader
from ingestion.schema_detector import SchemaDetector

class TestCSVLoader:
    """Test CSV loading functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.loader = CSVLoader()
        self.test_csv = Path(__file__).parent.parent.parent / "data" / "samples" / "test.csv"
    
    def test_csv_loader_initialization(self):
        """Test CSV loader initialization"""
        assert self.loader is not None
        assert self.loader.encoding == 'utf-8'
    
    def test_separator_detection(self):
        """Test separator detection"""
        import io
        for sep in [',', ';', '\t', '|']:
            assert self.loader.detect_separator(io.BytesIO(f"a{sep}b\n".encode())) == sep

class TestSchemaDetector:
    """Test schema detection"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.detector = SchemaDetector()
        self.df = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'salary': [50000.0, 60000.0, 75000.0, 80000.0, 95000.0],
            'date': pd.date_range('2023-01-01', periods=5)
        })
    
    def test_schema_detection(self):
        """Test schema detection"""
        schema = self.detector.detect_schema(self.df)
        
        assert 'columns' in schema
        assert len(schema['columns']) == 4
        assert 'id' in schema['columns']
    
    def test_data_quality_report(self):
        """Test data quality report generation"""
        report = self.detector.get_data_quality_report(self.df)
        
        assert report['total_rows'] == 5
        assert report['total_columns'] == 4
        assert report['total_missing'] == 0
    
    def test_primary_key_inference(self):
        """Test primary key inference"""
        primary_key = self.detector.infer_primary_key(self.df)
        
        assert primary_key == 'id'

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
