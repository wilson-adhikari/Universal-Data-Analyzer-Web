"""Helper Functions Module"""
import logging
import logging.config
import json
from pathlib import Path
import os

def setup_logger(name: str, log_level=logging.INFO) -> logging.Logger:
    """Setup logger with file and stream handlers"""
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    fh = logging.FileHandler(log_dir / "app.log")
    fh.setLevel(logging.DEBUG)
    
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger

def load_config(config_file: str = "app/config/default.json") -> dict:
    """Load configuration from JSON file"""
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        return {}

def ensure_directory(directory: str) -> None:
    """Ensure directory exists"""
    Path(directory).mkdir(parents=True, exist_ok=True)

def format_large_number(num: float) -> str:
    """Format large numbers with K, M, B suffix"""
    if num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.1f}B"
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    else:
        return f"{num:.0f}"

def get_file_size(filepath: str) -> str:
    """Get file size in human-readable format"""
    size = os.path.getsize(filepath)
    
    if size >= 1_000_000:
        return f"{size / 1_000_000:.2f} MB"
    elif size >= 1_000:
        return f"{size / 1_000:.2f} KB"
    else:
        return f"{size} B"

def sanitize_column_name(col_name: str) -> str:
    """Sanitize column name"""
    col_name = col_name.strip()
    col_name = col_name.replace(' ', '_')
    col_name = ''.join(c if c.isalnum() or c == '_' else '' for c in col_name)
    return col_name.lower()
def describe_chart_type(chart_type: str) -> str:
    """Return description for chart type"""
    descriptions = {
            'bar': 'Bar chart - Compare categories with rectangular bars',
            'line': 'Line chart - Show trends over time with lines',
            'scatter': 'Scatter plot - Show relationships between two variables',
            'pie': 'Pie chart - Show proportions of a whole',
            'histogram': 'Histogram - Show distribution of numerical data',
            'box': 'Box plot - Show data spread and outliers',
            'heatmap': 'Heatmap - Show data density with colors',
            'area': 'Area chart - Show cumulative totals over time',
            'bubble': 'Bubble chart - Show relationships with size variation',
            'radar': 'Radar chart - Show multivariate data in a circular format',
            'treemap': 'Treemap - Show hierarchical data as nested rectangles',
            'waterfall': 'Waterfall chart - Show cumulative effect of sequential values',
            'funnel': 'Funnel chart - Show stages in a process',
            'gauge': 'Gauge chart - Show progress towards a goal',
            'donut': 'Donut chart - Shows proportions with center hole'
        }
        
    return descriptions.get(chart_type, 'Unknown chart type')