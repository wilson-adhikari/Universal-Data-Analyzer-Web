# Feature Traceability

Each claim from the README (R) and the in-app Home page (H) is traced to code and to evidence from the audit runs. Paths are relative to `Universal Data Analyzer/`.

**Statuses:**
- **Fully implemented:** works in the UI on the happy path.
- **Partially implemented:** works, but with gaps or not reachable from the UI.
- **Not implemented**
- **Broken:** crashes or fails to import.
- **Experimental:** code exists but nothing calls it.
- **Unverified:** not executed during the audit.

## Declared features

| # | Claim | Source | Status | Evidence |
|---|---|---|---|---|
| 1 | Load CSV | R:14, H | **Partially implemented** | The loader works (ingestion/csv_loader.py:16-29) and the UI uploader is wired up (main.py:135-155). The claimed "automatic separator detection" is not wired: `load()` never calls `detect_separator()` (csv_loader.py:19-20, 31-42), so a probe `;`-separated CSV loaded as one column `['a;b']`. The UI upload path itself was not clicked (AppTest cannot drive uploads), so that path is Unverified. |
| 2 | Load Excel | R:14, H | **Fully implemented** (loader); UI upload Unverified | excel_loader.py:15-24 loaded a probe .xlsx. The UI is wired at main.py:157-175. There is no sheet picker in the UI even though `list_sheets` exists (excel_loader.py:26). |
| 3 | Load from SQL databases (MySQL, PostgreSQL, SQLite) | R:14, H:93,111 | **Not implemented** in the UI | The button only sets `upload_mode="sql"` (main.py:129-130). There is no `sql` branch (main.py:135-175), and AppTest showed no input widgets after the click. The backend helpers work for SQLite (`DatabaseEngine.load_table`, `get_tables`), but they are SQL-injectable (database/engine.py:25-27). `ingestion/sql_loader.py:19-21` swallows errors and returns an empty DataFrame. No MySQL/PostgreSQL drivers are in requirements. |
| 4 | Automatically detect schema and data types | R:15 | **Experimental** | `SchemaDetector` (ingestion/schema_detector.py) works and is tested, but it is imported and never used in the UI (main.py:13). Its stats only cover `int64`/`float64` (line 29), so an int32 column returned `statistics=None`. `TypeCaster.auto_detect_types` (cleaning/type_casting.py:42) is also unused. |
| 5 | Handle missing values | R:16, H | **Fully implemented** | Verified in AppTest: the mean strategy took missing values from 1 to 0 (main.py:224-230; cleaning/missing_values.py). Gaps: an unknown strategy is a silent no-op (lines 39-42), `fillna(method=…)` is deprecated (lines 34,37), and `constant` is not offered in the UI. |
| 6 | Handle duplicates | R:16, H | **Fully implemented** | main.py:233-240; cleaning/duplicates.py:11-19. Rendered without error. |
| 7 | Handle outliers | R:16, H | **Broken** | main.py:244 `from app.cleaning.outliers import …`. AppTest gave `ModuleNotFoundError: No module named 'app'`. The module itself works, but z-score reuses `threshold=1.5` (cleaning/outliers.py:13,34), which removed 129 of 1000 normal points (about 13%). |
| 8 | Type casting | H | **Fully implemented** | main.py:256-271; cleaning/type_casting.py:12-39. |
| 9 | Descriptive statistics | R:17, H | **Partially implemented** | EDA Summary tab renders (main.py:289-293). `SummaryStats.get_summary` raises `ValueError: Cannot describe a DataFrame without columns` when there are no numeric columns (eda/summary_stats.py:19-20), so the EDA page crashes for text-only datasets. `get_categorical_summary` is not shown in the UI. |
| 10 | Distributions | H | **Fully implemented** | main.py:295-303; eda/distributions.py:13-37. Box, violin, QQ and multi-distribution plots exist but are not exposed. |
| 11 | Correlations | R:17, H | **Partially implemented** | The heatmap renders (main.py:305-314). `get_correlation_values` raises `KeyError: 'Correlation'` when no pair exceeds the threshold (eda/correlations.py:52), which shows up as a failing test. It is not used in the UI. |
| 12 | Group analysis | H (EDA tab) | **Broken** | main.py:324 `GroupAnalyzer()` is never imported. AppTest gave `NameError: name 'GroupAnalyzer' is not defined`. The module eda/group_analysis.py itself imports fine. |
| 13 | Smart chart recommendations based on data types | R:18, H:96 | **Experimental** | `ChartSelector` (visualization/chart_selector.py) is imported (main.py:20) but never called. It recommends `heatmap`, `distribution`, `pie` and `donut`, which `PlotFactory.create_plot` does not implement. Unknown types silently fall back to scatter (plot_factory.py:89-94). |
| 14 | Interactive visualizations | R:19 | **Not implemented** | All charts are static matplotlib (`st.pyplot`). Plotly is referenced only in reporting/export_plots.py and is not installed. With a categorical x, scatter/line/bar/histogram/box/violin rendered; kde errors ("no numeric data to plot"). |
| 15 | AI-generated text insights | H:97, main.py:366 | **Partially implemented** (rule-based, not AI) | insights/text_generator.py:15-68 uses fixed heuristics, and the Insights page rendered 3 insights. It crashes with `IndexError` on an all-null text column (line 63), and gives `CV: inf%` when the mean is 0 (line 48). `insights/thresholds.py` is empty, and `config/default.json` thresholds are unused. |
| 16 | Export cleaned data | R:20, H | **Fully implemented** (CSV, Excel) | main.py:388-399. AppTest clicks succeeded. The download button appears only after a first click on a separate button, which is a UX wart. `reporting/export_data.py` is unused, and its `export_to_json` fails for any `orient` other than `records` (line 38). |
| 17 | Export plots | R:20 | **Broken / Not implemented** | reporting/export_plots.py:2 imports plotly (not in requirements) and annotates `px.Figure`. It is not wired into the UI, and the app's matplotlib figures could not be passed to it anyway. |
| 18 | Export reports (HTML) | R:20, H | **Partially implemented** | report_builder.py:13-119 builds HTML and the AppTest click succeeded. Column names and title are **not HTML-escaped** (lines 29,46,84). The report has no charts, insights or correlations. PDF (weasyprint/reportlab in requirements) is not implemented. |
| 19 | Fully modular & testable architecture | R:21 | **Partially implemented** | Modules are cleanly separated. However, there are no packages or `__init__.py` files, tests cannot import the code (`app.` prefix), there are 8 tests (1 tautological, 2 failing), and there is no CI. |
| 20 | Configuration (default.json, logging.json) | R tree | **Not implemented** | Neither file is loaded anywhere. `load_config` path is wrong (utils/helpers.py:33). |
| 21 | Database utilities / query builder | R tree | **Broken** | database/queries.py is truncated at line 80-81, giving `IndentationError` on import. |
| 22 | Data validation | (module) | **Experimental** | `DataValidator` (utils/validators.py) is imported (main.py:24) but never called. |
| 23 | Visualization style module | R tree | **Not implemented** | visualization/style.py is 0 bytes. |

## Counts

| Status | Features |
|---|---|
| Fully implemented | 6: #2, #5, #6, #8, #10, #16 |
| Partially implemented | 6: #1, #9, #11, #15, #18, #19 |
| Broken | 4: #7, #12, #17, #21 |
| Not implemented | 5: #3 UI, #14, #20, #23, plus PDF reports |
| Experimental (unused code) | 3: #4, #13, #22 |
| Unverified | Real browser file upload; MySQL/PostgreSQL connectivity |
