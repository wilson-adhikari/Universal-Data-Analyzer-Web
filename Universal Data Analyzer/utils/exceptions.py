"""Custom Exceptions Module"""

class DataAnalyzerException(Exception):
    """Base exception for Data Analyzer"""
    pass

class DataLoadingException(DataAnalyzerException):
    """Exception raised during data loading"""
    pass

class DataValidationException(DataAnalyzerException):
    """Exception raised during data validation"""
    pass

class DataCleaningException(DataAnalyzerException):
    """Exception raised during data cleaning"""
    pass

class AnalysisException(DataAnalyzerException):
    """Exception raised during analysis"""
    pass

class VisualizationException(DataAnalyzerException):
    """Exception raised during visualization"""
    pass

class ReportGenerationException(DataAnalyzerException):
    """Exception raised during report generation"""
    pass
