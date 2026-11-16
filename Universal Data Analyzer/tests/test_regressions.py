"""Regression tests for defects listed in docs/audit/TECHNICAL_DEBT.md (IDs in test names)."""
import importlib
import io
import json
import sqlite3
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

APP_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(APP_DIR))

from cleaning.missing_values import MissingValueHandler
from cleaning.outliers import OutlierHandler
from eda.correlations import CorrelationAnalyzer
from eda.summary_stats import SummaryStats
from ingestion.csv_loader import CSVLoader
from insights.text_generator import InsightGenerator
from reporting.report_builder import ReportBuilder

NUMERIC_DF = pd.DataFrame({"g": ["a", "b", "a", "b"], "x": [1.0, 2.0, 3.0, 4.0]})


def _open_page(page, df, monkeypatch, tmp_path):
    """Run main.py headlessly with df loaded and the given sidebar page selected."""
    monkeypatch.chdir(tmp_path)  # setup_logger writes logs/ relative to the cwd
    at = AppTest.from_file(str(APP_DIR / "main.py"), default_timeout=30)
    at.session_state["df"] = df
    at.session_state["original_df"] = df
    at.session_state["data_loaded"] = True
    at.run()
    at.sidebar.radio[0].set_value(page).run()
    return at


# ---- P0 ----

def test_p0_1_pyarrow_is_pinned():
    lines = (APP_DIR / "requirements.txt").read_text().lower().splitlines()
    assert any(line.startswith("pyarrow==") for line in lines)


def test_p0_2_and_p0_3_readme_documents_python_and_run_command():
    readme = (APP_DIR.parent / "README.md").read_text(encoding="utf-8")
    assert "3.11" in readme
    assert "streamlit run main.py" in readme


# ---- P1 ----

def test_p1_1_handle_outliers_checkbox_does_not_crash(monkeypatch, tmp_path):
    at = _open_page("Data Cleaning", NUMERIC_DF, monkeypatch, tmp_path)
    [c for c in at.checkbox if c.label == "Handle Outliers"][0].check().run()
    assert not at.exception


def test_p1_2_group_analysis_button_does_not_crash(monkeypatch, tmp_path):
    at = _open_page("EDA", NUMERIC_DF, monkeypatch, tmp_path)
    [b for b in at.button if b.label == "Perform Group Analysis"][0].click().run()
    assert not at.exception


def test_p1_3_no_sql_button_or_sql_claim(monkeypatch, tmp_path):
    at = _open_page("Home", NUMERIC_DF, monkeypatch, tmp_path)
    assert not any("SQL" in m.value for m in at.markdown)
    at.sidebar.radio[0].set_value("Data Ingestion").run()
    assert not any("SQL" in b.label for b in at.button)


def test_p1_5_html_report_escapes_user_text():
    df = pd.DataFrame({"<script>alert(1)</script>": [1, 2]})
    html = ReportBuilder.build_html_report(df, title="<script>alert(2)</script>")
    assert "<script>" not in html


def test_p1_6_database_queries_module_imports():
    importlib.import_module("database.queries")


# ---- P2 ----

def test_p2_2_no_correlation_above_threshold_returns_empty_frame():
    df = pd.DataFrame({"X": [1, 2, 3, 4, 5, 6], "Y": [1, -1, 1, -1, 1, -1]})
    result = CorrelationAnalyzer.get_correlation_values(df, threshold=0.99)
    assert result.empty
    assert list(result.columns) == ["Variable1", "Variable2", "Correlation"]


def test_p2_2_strong_correlation_is_still_reported():
    df = pd.DataFrame({"X": [1, 2, 3, 4], "Y": [2, 4, 6, 8]})
    result = CorrelationAnalyzer.get_correlation_values(df, threshold=0.9)
    assert len(result) == 1


def test_p2_3_summary_of_text_only_frame_is_empty_not_a_crash():
    df = pd.DataFrame({"a": ["x", "y"], "b": ["p", "q"]})
    assert SummaryStats.get_summary(df).empty


def test_p2_3_eda_page_renders_for_text_only_data(monkeypatch, tmp_path):
    df = pd.DataFrame({"a": ["x", "y"], "b": ["p", "q"]})
    at = _open_page("EDA", df, monkeypatch, tmp_path)
    assert not at.exception


def test_p2_4_all_null_text_column_does_not_crash_insights():
    df = pd.DataFrame({"t": pd.Series([None, None, None], dtype=object), "n": [1, 2, 3]})
    InsightGenerator.generate_insights(df)


def test_p2_4_no_cv_insight_when_mean_is_zero():
    df = pd.DataFrame({"n": [-1.0, 1.0, -2.0, 2.0]})
    assert not any("CV" in i for i in InsightGenerator.generate_insights(df))


def test_p2_5_zscore_default_threshold_keeps_normal_data():
    df = pd.DataFrame({"v": np.random.default_rng(0).normal(size=1000)})
    out = OutlierHandler.remove_outliers(df, "v", method="zscore")
    assert len(df) - len(out) < 20  # |z|>=3 removes ~0.3%; the old 1.5 removed ~13%


def test_p2_5_explicit_threshold_and_iqr_default_unchanged():
    df = pd.DataFrame({"v": np.random.default_rng(0).normal(size=1000)})
    assert len(df) - len(OutlierHandler.remove_outliers(df, "v", method="zscore", threshold=1.5)) > 100
    with_outlier = pd.DataFrame({"v": [1.0, 2.0, 3.0, 4.0, 5.0, 1000.0]})
    assert len(OutlierHandler.remove_outliers(with_outlier, "v")) == 5


@pytest.mark.parametrize("sep", [";", "\t", "|", ","])
def test_p2_6_csv_separator_is_detected_for_paths_and_uploads(sep, tmp_path):
    text = sep.join(["a", "b"]) + "\n" + sep.join(["1", "2"]) + "\n"
    path = tmp_path / "data.csv"
    path.write_text(text)
    assert list(CSVLoader().load(path).columns) == ["a", "b"]
    # Streamlit passes an in-memory file object, not a path
    assert list(CSVLoader().load(io.BytesIO(text.encode())).columns) == ["a", "b"]


def test_p2_6_single_column_csv_still_loads():
    df = CSVLoader().load(io.BytesIO(b"a\n1\n2\n"))
    assert list(df.columns) == ["a"] and len(df) == 2


def test_p2_8_plotly_declared_and_plot_export_works(tmp_path):
    lines = (APP_DIR / "requirements.txt").read_text().lower().splitlines()
    assert any(line.startswith("plotly==") for line in lines)
    import plotly.graph_objects as go
    from reporting.export_plots import PlotExporter

    out = tmp_path / "plot.html"
    PlotExporter.export_plot_to_html(go.Figure(), str(out))
    assert out.exists()


def test_p2_9_sql_loader_raises_instead_of_returning_empty_frame(tmp_path):
    from ingestion.sql_loader import load_sql_table

    db = tmp_path / "t.db"
    with sqlite3.connect(db) as con:
        con.execute("CREATE TABLE t (a INTEGER)")
        con.executemany("INSERT INTO t VALUES (?)", [(1,), (2,)])
    con.close()
    url = f"sqlite:///{db.as_posix()}"
    assert len(load_sql_table(url, "t")) == 2
    with pytest.raises(ValueError):
        load_sql_table(url, "no_such_table")


def test_p2_10_export_to_json_supports_non_records_orient(tmp_path):
    from reporting.export_data import DataExporter

    df = pd.DataFrame({"a": [1, 3], "b": [2, 4]})
    split = tmp_path / "split.json"
    DataExporter.export_to_json(df, str(split), orient="split")
    assert json.loads(split.read_text())["data"] == [[1, 2], [3, 4]]
    records = tmp_path / "records.jsonl"
    DataExporter.export_to_json(df, str(records))  # default stays JSON lines
    assert [json.loads(line) for line in records.read_text().splitlines()] == [
        {"a": 1, "b": 2}, {"a": 3, "b": 4}]


def test_p2_11_unknown_missing_value_strategy_raises():
    with pytest.raises(ValueError):
        MissingValueHandler().handle(pd.DataFrame({"a": [1, None]}), strategy="bogus")


def test_p2_11_fill_directions_use_no_deprecated_fillna_method():
    df = pd.DataFrame({"a": [1.0, None, 3.0]})
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert MissingValueHandler().handle(df, strategy="forward_fill")["a"].tolist() == [1.0, 1.0, 3.0]
        assert MissingValueHandler().handle(df, strategy="backward_fill")["a"].tolist() == [1.0, 3.0, 3.0]


# ---- Round 2 ----

@pytest.fixture
def sqlite_url(tmp_path):
    db = tmp_path / "inj.db"
    con = sqlite3.connect(db)
    con.execute("CREATE TABLE users (a INTEGER)")
    con.execute("CREATE TABLE secret (b INTEGER)")
    con.executemany("INSERT INTO users VALUES (?)", [(1,), (2,)])
    con.execute("INSERT INTO secret VALUES (99)")
    con.commit()
    con.close()
    return f"sqlite:///{db.as_posix()}"


def test_p2_1_engine_rejects_injected_table_name(sqlite_url):
    from database.engine import DatabaseEngine

    db = DatabaseEngine(sqlite_url)
    try:
        assert len(db.load_table("users", limit=1)) == 1
        assert len(db.load_table("users")) == 2
        with pytest.raises(ValueError):
            db.load_table("users UNION SELECT b FROM secret")
        with pytest.raises(ValueError):
            db.load_table("users", limit="1 UNION SELECT b FROM secret")
    finally:
        db.close()


def test_p2_1_query_builder_rejects_injected_names(sqlite_url):
    import sqlalchemy
    from database.queries import QueryBuilder

    engine = sqlalchemy.create_engine(sqlite_url)
    try:
        qb = QueryBuilder(engine)
        assert len(qb.select_all("users", limit=1)) == 1
        assert list(qb.select_columns("users", ["a"]).columns) == ["a"]
        with pytest.raises(ValueError):
            qb.select_all("users UNION SELECT b FROM secret")
        with pytest.raises(ValueError):
            qb.select_columns("users", ["a FROM users UNION SELECT b"])
        with pytest.raises(ValueError):
            qb.select_columns("users UNION SELECT b FROM secret", ["a"])
    finally:
        engine.dispose()


def test_p2_7_insights_are_not_called_ai(monkeypatch, tmp_path):
    at = _open_page("Home", NUMERIC_DF, monkeypatch, tmp_path)
    assert not any("AI" in m.value for m in at.markdown)
    at.sidebar.radio[0].set_value("Insights").run()
    assert not any("AI" in m.value for m in at.markdown)
    assert any("rule-based" in m.value for m in at.markdown)


def test_p2_12_logger_handlers_not_duplicated_and_log_dir_is_fixed(monkeypatch, tmp_path):
    import logging
    from utils.helpers import setup_logger

    monkeypatch.chdir(tmp_path)
    logger = setup_logger("p2_12_test")
    assert setup_logger("p2_12_test") is logger
    assert len(logger.handlers) == 2
    file_handler = [h for h in logger.handlers if isinstance(h, logging.FileHandler)][0]
    assert Path(file_handler.baseFilename).parent == APP_DIR / "logs"
    assert not (tmp_path / "logs").exists()


def test_p2_14_and_p1_7_readme_is_accurate():
    readme = (APP_DIR.parent / "README.md").read_text(encoding="utf-8")
    assert "logging.json" not in readme
    assert "data/" not in readme
    assert "Interactive visualizations" not in readme
    assert "Smart chart recommendations" not in readme
    assert "--server.address localhost" in readme
    assert "no login" in readme


def test_png_jpeg_plot_export_removed_because_kaleido_is_not_a_dependency():
    from reporting.export_plots import PlotExporter

    assert not hasattr(PlotExporter, "export_plot_to_png")
    assert not hasattr(PlotExporter, "export_plot_to_jpeg")


def test_p3_3_load_config_finds_default_config_from_any_cwd(monkeypatch, tmp_path):
    from utils.helpers import load_config

    monkeypatch.chdir(tmp_path)
    assert "analysis_rules" in load_config()


def test_p3_11_non_64bit_numeric_columns_are_treated_as_numeric():
    from ingestion.schema_detector import SchemaDetector
    from visualization.chart_selector import ChartSelector

    df = pd.DataFrame({"x": pd.Series(range(30), dtype="int32"), "y": pd.Series([1.5] * 30, dtype="float32")})
    schema = SchemaDetector.detect_schema(df)
    assert "statistics" in schema["columns"]["x"] and "statistics" in schema["columns"]["y"]
    assert "histogram" in ChartSelector.recommend_charts(df, "x")
