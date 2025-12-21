"""
Universal Data Analyzer - Main Application Entry Point
"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from ingestion.csv_loader import CSVLoader
from ingestion.excel_loader import ExcelLoader
from ingestion.schema_detector import SchemaDetector
from cleaning.missing_values import MissingValueHandler
from cleaning.duplicates import DuplicateHandler
from cleaning.type_casting import TypeCaster    
from eda.summary_stats import SummaryStats
from eda.distributions import DistributionAnalyzer
from eda.correlations import CorrelationAnalyzer
from visualization.chart_selector import ChartSelector
from visualization.plot_factory import PlotFactory
from insights.text_generator import InsightGenerator
from reporting.report_builder import ReportBuilder
from utils.validators import DataValidator
from utils.helpers import setup_logger

# Configure page
st.set_page_config(
    page_title="Universal Data Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Setup logger
logger = setup_logger("streamlit_app")

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .section-header {
        font-size: 24px;
        font-weight: bold;
        margin-top: 2rem;
        margin-bottom: 1rem;
        color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if "df" not in st.session_state:
        st.session_state.df = None
    if "original_df" not in st.session_state:
        st.session_state.original_df = None
    if "data_loaded" not in st.session_state:
        st.session_state.data_loaded = False
    if "cleaning_applied" not in st.session_state:
        st.session_state.cleaning_applied = False

def render_header():
    """Render application header"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("📊 Universal Data Analyzer")
    st.markdown("---")

def render_sidebar():
    """Render sidebar navigation"""
    with st.sidebar:
        st.header("Navigation")
        page = st.radio(
            "Select Analysis Step:",
            ["Home", "Data Ingestion", "Data Cleaning", "EDA", "Visualization", "Insights", "Export Report"]
        )
        st.markdown("---")
        st.info("💡 Follow the steps sequentially for best results")
        return page

def render_home():
    """Render home page"""
    st.markdown("<div class='section-header'>Welcome to Universal Data Analyzer</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Features
        - **Data Ingestion**: Load CSV, Excel, SQL databases
        - **Data Cleaning**: Handle missing values, duplicates, outliers
        - **EDA**: Summary statistics, distributions, correlations
        - **Visualization**: Automatic chart recommendations
        - **Insights**: AI-generated text insights
        - **Reporting**: Export comprehensive reports
        """)
    
    with col2:
        st.markdown("""
        ### How to Use
        1. Load your data (CSV, Excel, or SQL)
        2. Review and clean the data
        3. Perform exploratory data analysis
        4. Generate visualizations
        5. Extract insights
        6. Export detailed report
        
        **Supported Formats**: CSV, Excel, SQL (MySQL, PostgreSQL, SQLite)
        """)

def render_data_ingestion():
    """Render data ingestion page"""
    st.markdown("<div class='section-header'>Step 1: Data Ingestion</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📁 Load CSV", use_container_width=True):
            st.session_state.upload_mode = "csv"
    
    with col2:
        if st.button("📊 Load Excel", use_container_width=True):
            st.session_state.upload_mode = "excel"
    
    with col3:
        if st.button("🗄️ Load from SQL", use_container_width=True):
            st.session_state.upload_mode = "sql"
    
    if "upload_mode" in st.session_state:
        st.markdown("---")
        
        if st.session_state.upload_mode == "csv":
            uploaded_file = st.file_uploader("Choose CSV file", type="csv")
            if uploaded_file:
                try:
                    loader = CSVLoader()
                    df = loader.load(uploaded_file)
                    
                    st.session_state.original_df = df.copy()
                    st.session_state.df = df
                    st.session_state.data_loaded = True
                    
                    st.success(f"✅ Loaded CSV with {len(df)} rows and {len(df.columns)} columns")
                    
                    with st.expander("View Data Preview"):
                        st.dataframe(df.head(10), use_container_width=True)
                        st.write(f"**Shape**: {df.shape}")
                        st.write(f"**Memory Usage**: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
                
                except Exception as e:
                    st.error(f"Error loading CSV: {str(e)}")
                    logger.error(f"CSV loading error: {str(e)}")
        
        elif st.session_state.upload_mode == "excel":
            uploaded_file = st.file_uploader("Choose Excel file", type=["xls", "xlsx"])
            if uploaded_file:
                try:
                    loader = ExcelLoader()
                    df = loader.load(uploaded_file)
                    
                    st.session_state.original_df = df.copy()
                    st.session_state.df = df
                    st.session_state.data_loaded = True
                    
                    st.success(f"✅ Loaded Excel with {len(df)} rows and {len(df.columns)} columns")
                    
                    with st.expander("View Data Preview"):
                        st.dataframe(df.head(10), use_container_width=True)
                
                except Exception as e:
                    st.error(f"Error loading Excel: {str(e)}")
                    logger.error(f"Excel loading error: {str(e)}")
    
    if st.session_state.data_loaded:
        st.markdown("---")
        st.success("✅ Data loaded successfully! Proceed to Data Cleaning.")

def render_data_cleaning():
    """Render data cleaning page"""
    if not st.session_state.data_loaded:
        st.warning("⚠️ Please load data first in the Data Ingestion step")
        return
    
    st.markdown("<div class='section-header'>Step 2: Data Cleaning</div>", unsafe_allow_html=True)
    
    df = st.session_state.df
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Rows", len(df))
    with col2:
        st.metric("Total Columns", len(df.columns))
    with col3:
        st.metric("Missing Values", df.isnull().sum().sum())
    
    st.markdown("---")
    
    with st.expander("🔍 Data Quality Report", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Missing Values")
            missing = df.isnull().sum()
            missing = missing[missing > 0]
            if len(missing) > 0:
                st.bar_chart(missing)
            else:
                st.success("No missing values found!")
        
        with col2:
            st.subheader("Data Types")
            st.write(df.dtypes.value_counts())
    
    st.markdown("---")
    st.subheader("Cleaning Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.checkbox("Handle Missing Values"):
            handler = MissingValueHandler()
            strategy = st.selectbox("Strategy", ["drop", "mean", "median", "forward_fill", "backward_fill"])
            if st.button("Apply Missing Value Handler"):
                df = handler.handle(df, strategy=strategy)
                st.session_state.df = df
                st.success(f"✅ Applied {strategy} strategy")
    
    with col2:
        if st.checkbox("Remove Duplicates"):
            handler = DuplicateHandler()
            subset = st.multiselect("Columns to check (empty = all)", df.columns.tolist())
            if st.button("Remove Duplicates"):
                initial_rows = len(df)
                df = handler.remove(df, subset=subset if subset else None)
                st.session_state.df = df
                st.success(f"✅ Removed {initial_rows - len(df)} duplicate rows")
    
    with col3:
        if st.checkbox("Handle Outliers"):
            from app.cleaning.outliers import OutlierHandler
            handler = OutlierHandler()
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            col = st.selectbox("Select column", numeric_cols)
            method = st.selectbox("Method", ["iqr", "zscore"])
            if st.button("Remove Outliers"):
                initial_rows = len(df)
                df = handler.remove_outliers(df, col, method=method)
                st.session_state.df = df
                st.success(f"✅ Removed {initial_rows - len(df)} outliers")
    
    st.markdown("---")
    st.subheader("Type Casting")
    caster = TypeCaster()
    
    col1, col2 = st.columns(2)
    with col1:
        column = st.selectbox("Select column", df.columns.tolist())
    with col2:
        target_type = st.selectbox("Target type", ["int", "float", "string", "datetime"])
    
    if st.button("Cast Type"):
        try:
            df[column] = caster.cast(df[column], target_type)
            st.session_state.df = df
            st.success(f"✅ Casted {column} to {target_type}")
        except Exception as e:
            st.error(f"Error casting type: {str(e)}")
    
    st.markdown("---")
    with st.expander("Preview Cleaned Data"):
        st.dataframe(df.head(15), use_container_width=True)

def render_eda():
    """Render EDA page"""
    if not st.session_state.data_loaded:
        st.warning("⚠️ Please load data first")
        return
    
    st.markdown("<div class='section-header'>Step 3: Exploratory Data Analysis</div>", unsafe_allow_html=True)
    
    df = st.session_state.df
    
    tab1, tab2, tab3, tab4 = st.tabs(["Summary Stats", "Distributions", "Correlations", "Group Analysis"])
    
    with tab1:
        st.subheader("Summary Statistics")
        stats = SummaryStats()
        summary = stats.get_summary(df)
        st.dataframe(summary, use_container_width=True)
    
    with tab2:
        st.subheader("Distribution Analysis")
        dist = DistributionAnalyzer()
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        selected_col = st.selectbox("Select numeric column", numeric_cols)
        
        if selected_col:
            fig, ax = dist.plot_distribution(df, selected_col)
            st.pyplot(fig)
    
    with tab3:
        st.subheader("Correlation Analysis")
        corr = CorrelationAnalyzer()
        numeric_df = df.select_dtypes(include=['number'])
        
        if len(numeric_df.columns) > 1:
            fig, ax = corr.plot_correlation_matrix(numeric_df)
            st.pyplot(fig)
        else:
            st.warning("Need at least 2 numeric columns for correlation analysis")
    
    with tab4:
        st.subheader("Group Analysis")
        groupby_col = st.selectbox("Group by column", df.columns.tolist())
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        agg_col = st.selectbox("Aggregate column", numeric_cols)
        agg_func = st.selectbox("Aggregation function", ["mean", "sum", "count", "std", "min", "max"])
        
        if st.button("Perform Group Analysis"):
            analyzer = GroupAnalyzer()
            fig, ax = analyzer.plot_grouped_bar(df, groupby_col, agg_col, agg_func)
            st.pyplot(fig)


def render_visualization():
    """Render visualization page"""
    if not st.session_state.data_loaded:
        st.warning("⚠️ Please load data first")
        return
    
    st.markdown("<div class='section-header'>Step 4: Visualization</div>", unsafe_allow_html=True)
    
    df = st.session_state.df
    
    col1, col2 = st.columns(2)
    
    with col1:
        x_col = st.selectbox("X-axis column", df.columns.tolist())
    with col2:
        y_col = st.selectbox("Y-axis column", df.select_dtypes(include=['number']).columns.tolist())
    
    chart_type = st.selectbox(
        "Chart Type",
        ["scatter", "line", "bar", "histogram", "box", "violin", "kde"]
    )
    
    if st.button("Generate Chart"):
        try:
            factory = PlotFactory()
            fig, ax = factory.create_plot(df, x_col, y_col, chart_type)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Error generating chart: {str(e)}")


def render_insights():
    """Render insights page"""
    if not st.session_state.data_loaded:
        st.warning("⚠️ Please load data first")
        return
    
    st.markdown("<div class='section-header'>Step 5: AI-Generated Insights</div>", unsafe_allow_html=True)
    
    df = st.session_state.df
    
    generator = InsightGenerator()
    insights = generator.generate_insights(df)
    
    for i, insight in enumerate(insights, 1):
        st.info(f"💡 **Insight {i}**: {insight}")

def render_export():
    """Render export page"""
    if not st.session_state.data_loaded:
        st.warning("⚠️ Please load data first")
        return
    
    st.markdown("<div class='section-header'>Step 6: Export Report</div>", unsafe_allow_html=True)
    
    df = st.session_state.df
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export as CSV", use_container_width=True):
            csv = df.to_csv(index=False)
            st.download_button("Download CSV", csv, "data.csv", "text/csv")
    
    with col2:
        if st.button("📊 Export as Excel", use_container_width=True):
            from io import BytesIO
            buffer = BytesIO()
            df.to_excel(buffer, index=False)
            buffer.seek(0)
            st.download_button("Download Excel", buffer, "data.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    with col3:
        if st.button("📋 Generate HTML Report", use_container_width=True):
            builder = ReportBuilder()
            html = builder.build_html_report(df)
            st.download_button("Download HTML Report", html, "report.html", "text/html")

def main():
    """Main application function"""
    initialize_session_state()
    render_header()
    
    page = render_sidebar()
    
    if page == "Home":
        render_home()
    elif page == "Data Ingestion":
        render_data_ingestion()
    elif page == "Data Cleaning":
        render_data_cleaning()
    elif page == "EDA":
        render_eda()
    elif page == "Visualization":
        render_visualization()
    elif page == "Insights":
        render_insights()
    elif page == "Export Report":
        render_export()

if __name__ == "__main__":
    main()
