import pandas as pd
from typing import Dict
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ReportBuilder:
    """Build comprehensive analysis reports"""
    
    @staticmethod
    def build_html_report(df: pd.DataFrame, title: str = "Data Analysis Report") -> str:
        """
        Build HTML report
        
        Args:
            df: Input dataframe
            title: Report title
        
        Returns:
            HTML string
        """
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
                .header {{ background-color: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
                .section {{ background-color: white; padding: 20px; margin: 20px 0; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
                .section h2 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background-color: #3498db; color: white; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                .metric {{ display: inline-block; background-color: #ecf0f1; padding: 15px; margin: 10px; border-radius: 5px; text-align: center; }}
                .metric-value {{ font-size: 24px; font-weight: bold; color: #2c3e50; }}
                .metric-label {{ color: #7f8c8d; margin-top: 5px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{title}</h1>
                <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="section">
                <h2>📊 Dataset Overview</h2>
                <div class="metric">
                    <div class="metric-value">{len(df)}</div>
                    <div class="metric-label">Total Rows</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{len(df.columns)}</div>
                    <div class="metric-label">Total Columns</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB</div>
                    <div class="metric-label">Memory Usage</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{df.isnull().sum().sum()}</div>
                    <div class="metric-label">Missing Values</div>
                </div>
            </div>
            
            <div class="section">
                <h2>📋 Column Information</h2>
                <table>
                    <tr>
                        <th>Column Name</th>
                        <th>Data Type</th>
                        <th>Non-Null Count</th>
                        <th>Unique Values</th>
                    </tr>
        """
        
        for col in df.columns:
            html += f"""
                    <tr>
                        <td>{col}</td>
                        <td>{df[col].dtype}</td>
                        <td>{df[col].count()}</td>
                        <td>{df[col].nunique()}</td>
                    </tr>
            """
        
        html += """
                </table>
            </div>
            
            <div class="section">
                <h2>📈 Statistical Summary</h2>
        """
        
        # Add numeric summary
        numeric_summary = df.describe().T.to_html()
        html += numeric_summary
        
        html += """
            </div>
            
            <div class="section">
                <h2>📝 Data Sample</h2>
        """
        
        html += df.head(10).to_html()
        
        html += """
            </div>
        </body>
        </html>
        """
        
        logger.info("Built HTML report")
        return html
    
    @staticmethod
    def save_html_report(df: pd.DataFrame, filepath: str) -> None:
        """Save HTML report to file"""
        html = ReportBuilder.build_html_report(df)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        logger.info(f"Saved HTML report to {filepath}")