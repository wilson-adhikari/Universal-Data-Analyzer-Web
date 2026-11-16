import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from typing import List
import logging
logger = logging.getLogger(__name__)
class PlotExporter:
    """Export plots to various formats"""
    
    @staticmethod
    def export_plot_to_html(fig: go.Figure, file_path: str) -> None:
        """
        Export plot to HTML file
        
        Args:
            fig: Plotly figure object
            file_path: Path to save the HTML file
        """
        try:
            pio.write_html(fig, file=file_path)
            logger.info(f"Plot exported successfully to {file_path}")
        except Exception as e:
            logger.error(f"Failed to export plot to HTML: {e}")
            raise
