# Technical Debt and Defects

**Severity scale:**
- **P0:** blocks install or run.
- **P1:** an advertised feature crashes, a security issue, or tests unusable.
- **P2:** wrong results, latent risk or misleading behaviour.
- **P3:** hygiene.

Paths are relative to `Universal Data Analyzer/` unless noted. "Verified" means the defect was reproduced during this audit (see REPOSITORY_AUDIT.md §3).

## P0

| ID | Defect | Location | Impact | Verified |
|---|---|---|---|---|
| P0-1 | **FIXED 2026-11-15.** (`pyarrow==14.0.2` pinned; clean venv install then imports streamlit.) The transitive `pyarrow` is unpinned. A fresh install pulls pyarrow 26, which requires NumPy ≥ 2, while numpy is pinned to 1.24.3. | requirements.txt | `import streamlit` fails with `ImportError`, so **the app cannot start after a clean install**. Workaround: `pip install "pyarrow<15"`. | Yes |
| P0-2 | **FIXED 2026-11-15.** (Documented in README: Python 3.11; pins unchanged.) The numpy 1.24.3 and pandas 2.0.3 pins only build on Python ≤ 3.11, and this is undocumented. | requirements.txt; README | Installs fail on Python 3.12+, which is the default on most new machines. | Partially (3.15 was skipped and 3.11 used) |
| P0-3 | **FIXED 2026-11-15.** There are no run instructions. The README omits `streamlit run main.py` and the folder name contains spaces. | README.md:107-113 | A customer or new developer cannot start the app from the docs. | Yes |

## P1

| ID | Defect | Location | Impact | Verified |
|---|---|---|---|---|
| P1-1 | **FIXED 2026-11-15.** The outliers import uses the non-existent `app.` package. | main.py:244 | Ticking "Handle Outliers" crashes the cleaning page with `ModuleNotFoundError`. | Yes |
| P1-2 | **FIXED 2026-11-15.** `GroupAnalyzer` is used but never imported. | main.py:324 (missing import near line 19) | The EDA "Group Analysis" button raises `NameError`. | Yes |
| P1-3 | **FIXED 2026-11-15.** (Dead SQL button and SQL claims removed from the UI.) SQL ingestion is advertised but has no UI branch. | main.py:129-130, 135-175 | The "Load from SQL" button does nothing, which is a false claim to users. | Yes |
| P1-4 | **FIXED 2026-11-15.** Both test files import `app.*`, which does not exist. | tests/test_cleaning.py:9-10; tests/test_eda.py:10-11 | `pytest` collects 0 tests (2 errors), so there is no regression safety net. | Yes |
| P1-5 | **FIXED 2026-11-15.** The HTML report does not escape the title, column names or dtypes. | reporting/report_builder.py:29,46,84 | A crafted CSV header injects script into the downloaded `report.html`. | Yes |
| P1-6 | **FIXED 2026-11-15.** (Unfinished `select_where` stub removed; module imports.) `database/queries.py` is truncated mid-function. | database/queries.py:80-81 | `IndentationError` on import, so the query builder module is dead. | Yes |
| P1-7 | (OPEN, mitigated 2026-11-15: the README run command binds to localhost and warns that there is no login. Authentication is still missing.) There is no authentication, and Streamlit binds all interfaces by default. | main.py (whole app) | Unsafe to host for customers: anyone on the network can use it. Fine only for localhost use. | Yes (Network URL printed) |

## P2

| ID | Defect | Location | Impact | Verified |
|---|---|---|---|---|
| P2-1 | **FIXED 2026-11-15.** (Table and column names checked against the reflected schema; queries built with SQLAlchemy `select`, limit bound.) SQL is built with f-strings from table and column names and `limit`. | database/engine.py:25-27; database/queries.py:42,67 | SQL injection: `users UNION SELECT …` executed. This becomes reachable once SQL UI exists. | Yes |
| P2-2 | **FIXED 2026-11-15.** `get_correlation_values` raises `KeyError` when no pair passes the threshold. | eda/correlations.py:52 | Crash on weakly correlated data, and a failing test. | Yes |
| P2-3 | **FIXED 2026-11-15.** `get_summary` crashes when there are no numeric columns. | eda/summary_stats.py:19-20; main.py:292 | The EDA page errors on text-only datasets. | Yes |
| P2-4 | **FIXED 2026-11-15.** Insights crash on an all-null text column (`value_counts().index[0]`), and the coefficient of variation is computed when the mean is 0. | insights/text_generator.py:48,63-64 | Insights page `IndexError`, and a "CV: inf%" message. | Yes |
| P2-5 | **FIXED 2026-11-15.** The z-score outlier method reuses the IQR default `threshold=1.5`. | cleaning/outliers.py:13,34 | Removes about 13% of normally distributed rows (129 of 1000), so it silently destroys data. | Yes |
| P2-6 | **FIXED 2026-11-15.** The CSV loader claims automatic separator detection but never calls it. | ingestion/csv_loader.py:17-22 | `;`/tab files load as one column. | Yes |
| P2-7 | "AI-generated insights" are fixed rules. | main.py:97,366 | Misrepresents product capability (CLAUDE.md §3.5 sales rules). | Yes (code review) |
| P2-8 | **FIXED 2026-11-15.** (HTML export verified; the PNG/JPEG export methods were removed because they need the undeclared `kaleido`.) `plotly` is used but not declared, and `px.Figure` is an invalid annotation. | reporting/export_plots.py:2,11 | Plot export is unusable. | Yes (import fails) |
| P2-9 | **FIXED 2026-11-15.** `sql_loader` swallows all errors, `print`s, and returns an empty DataFrame. | ingestion/sql_loader.py:19-21 | Silent failure: users see "0 rows" instead of the error. | Yes |
| P2-10 | **FIXED 2026-11-15.** `export_to_json` always passes `lines=True`. | reporting/export_data.py:38 | Any `orient` other than `records` raises `ValueError`. | Yes |
| P2-11 | **FIXED 2026-11-15.** (Unknown strategy now raises; `ffill()`/`bfill()` behaviour verified on pandas 2.0.3 only.) `MissingValueHandler` silently ignores an unknown strategy and uses the deprecated `fillna(method=…)`. | cleaning/missing_values.py:34,37,39-42 | Silent no-op, and it breaks on pandas 3.0. | Yes (code) |
| P2-12 | **FIXED 2026-11-15.** (Logs now always go to `Universal Data Analyzer/logs/`.) `setup_logger` adds new handlers on every Streamlit rerun and writes `logs/` relative to the current working directory. | utils/helpers.py:8-31; main.py:36 | Log lines duplicate on every interaction, and log files appear wherever the app is launched. | Code review |
| P2-13 | (OPEN. Scanned 2026-11-15 with `pip-audit -r requirements.txt --no-deps`: 37 known vulnerabilities in 9 packages: streamlit, pyarrow, scikit-learn, python-dotenv, pydantic, jinja2, weasyprint, pytest, black. Fixing needs version upgrades.) Pins date from 2023 and have not been scanned. | requirements.txt | Possible known CVEs (streamlit, jinja2). Run `pip-audit`. | Not scanned |
| P2-14 | The README is inaccurate: wrong clone URL and folder, `logging.json` versus `loging.json`, a missing `data/` folder, and claims of "interactive" charts and chart recommendations. | README.md:14-21,44-106,109-110 | Misleading to customers and developers. | Yes |

## P3

| ID | Defect | Location | Impact |
|---|---|---|---|
| P3-1 | 19 `.pyc` files and `logs/app.log` are committed despite `.gitignore`. | `*/__pycache__/`, `logs/app.log` | Repo noise. |
| P3-2 | Six unused runtime dependencies (weasyprint, reportlab, jinja2, pydantic, scikit-learn, python-dotenv), and dev tools mixed with runtime dependencies. | requirements.txt | Slower install and a larger attack surface. weasyprint needs GTK on Windows. |
| P3-3 | Config files are never loaded. `load_config` points at `app/config/default.json`. | config/*.json; utils/helpers.py:33 | Thresholds are hard-coded, and the config is dead weight. |
| P3-4 | Empty modules. | visualization/style.py; insights/thresholds.py | Placeholder files that the README advertises. |
| P3-5 | Unused imports and classes: `SchemaDetector`, `ChartSelector`, `DataValidator`, `TypeCaster.auto_detect_types`, `DataExporter`, the `utils/exceptions.py` classes. | main.py:13,20,24 and modules | Dead code that inflates the apparent feature set. |
| P3-6 | No packaging (no `__init__.py`, no pyproject) and a source folder with spaces in its name. | `Universal Data Analyzer/` | Cannot be pip-installed and is awkward for tooling. |
| P3-7 | Test quality: the separator test is a tautology, and the categorical-summary assertion is wrong. | tests/test_cleaning.py:25-29; tests/test_eda.py:37-38 | False confidence. |
| P3-8 | Export uses a nested `st.button` → `st.download_button`, which takes 2 clicks, and recomputes the Excel/HTML on each rerun. | main.py:388-405 | UX friction. |
| P3-9 | Raw exception text is shown to users. | main.py:154,174,271,357 | Leaks internals, which is poor UX. |
| P3-10 | No CI, lint or format config, although black and flake8 are listed. | repo root | Nothing enforces quality. |
| P3-11 | **FIXED 2026-11-15.** `SchemaDetector` stats only handle `int64`/`float64`, and the chart selector checks the same narrow list. | ingestion/schema_detector.py:29; visualization/chart_selector.py:30 | Wrong results for int32, Int64 and float32 columns. |
