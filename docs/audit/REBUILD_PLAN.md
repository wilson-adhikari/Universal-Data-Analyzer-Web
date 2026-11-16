# Rebuild Plan (incremental, no rewrite)

**Principle:** keep the existing Streamlit app and module layout. Each milestone is small, reviewable and verified by commands that a person can rerun. Defect IDs refer to TECHNICAL_DEBT.md.

## M1: Make it install, run and test reliably

**Objective:** a fresh clone starts, and `pytest` runs green in CI.

1. **Dependencies (P0-1, P0-2, P3-2):**
   - Add `pyarrow<15` to requirements.txt, or move all pins to a coherent 2025 set on Python 3.12.
   - Split the file into `requirements.txt` (runtime) and `requirements-dev.txt` (pytest, black, flake8).
   - Drop the six unused dependencies.
   - Add `plotly` only if M3 keeps plot export.
2. **README (P0-3, P2-14):**
   - Document the Python version and the command `cd "Universal Data Analyzer" && streamlit run main.py`.
   - Fix the clone URL and the tree, and remove claims that are not true yet.
3. **Tests (P1-4, P3-7):**
   - Replace `from app.X` with `from X`.
   - Add `tests/conftest.py`, which inserts the source dir into `sys.path`. That is a one-line shim and does not need a package restructure.
   - Fix the categorical-summary assertion and delete the tautological test.
4. **Repo hygiene (P3-1):** `git rm --cached` the `__pycache__` files and `logs/app.log`.
5. **CI (P3-10):** add a GitHub Actions workflow that runs `pip install -r requirements.txt -r requirements-dev.txt && pytest`, plus `python -m compileall` so syntax errors like P1-6 are caught.

**Verification:**
- On a fresh venv, `pip install` succeeds and `import streamlit` works.
- `pytest` collects all tests and they pass.
- The CI run is green.

## M2: Fix defects in existing features

**Objective:** every UI path works without exceptions on representative data.

1. Fix the outliers import (main.py:244) and add the missing `GroupAnalyzer` import (P1-1, P1-2).
2. Add HTML escaping in report_builder.py with `html.escape` (P1-5).
3. Fix or delete the truncated `database/queries.py` (P1-6). Deleting it is preferable unless M3 needs it.
4. Data correctness:
   - Correlations with an empty result return an empty DataFrame (P2-2).
   - Guard the no-numeric-columns case in summary and EDA (P2-3).
   - Add guards in insights (P2-4).
   - Give z-score its own default threshold of 3 (P2-5).
   - Wire `detect_separator` into the CSV loader, or use `sep=None, engine="python"` (P2-6).
   - Raise on an unknown missing-value strategy and use `.ffill()`/`.bfill()` (P2-11).
   - Fix `export_to_json` (P2-10).
5. Make `setup_logger` idempotent and give it an absolute log path (P2-12).
6. Rename "AI-generated insights" to "Automated insights" (P2-7).
7. Add a regression test for each fix, plus one `streamlit.testing.v1.AppTest` smoke test per page. The audit's AppTest driver is a usable template for these.

**Verification:**
- The AppTest smoke suite passes for all 7 pages, including outliers and group analysis.
- The unit tests cover each P1 and P2 fix.

## M3: Expose modules that already exist

**Objective:** close the gap between the README and the UI, reusing code rather than writing new code.

1. **SQL ingestion (P1-3, P2-1, P2-9):**
   - Add a UI that takes a connection string and lists tables via `DatabaseEngine.get_tables()`.
   - Validate the chosen table against that list, and quote identifiers with SQLAlchemy `Table`/`select()` instead of f-strings.
   - Collapse `sql_loader.py` into `DatabaseEngine`.
   - Never persist credentials in config. Read them from the environment if needed.
2. Show the `SchemaDetector` and `DataValidator` quality report on the cleaning page.
3. Show `ChartSelector` recommendations on the Visualization page. Restrict them to the chart types that `PlotFactory` supports, or add those types.
4. Show the categorical summary and the remaining distribution and group plots in the EDA tabs.
5. Add an Excel sheet picker (`list_sheets`).
6. Either load `config/default.json` (with the file renamed to `logging.json`) or delete the config files and the empty `style.py`/`thresholds.py`.

**Verification:**
- Every README feature is "Fully implemented" in an updated FEATURE_TRACEABILITY.md.
- An SQLite test fixture passes end to end.
- An injection test against the table name is rejected.

## M4: Improvements (only after M1–M3; needs founder approval for scope)

- Add charts and insights to the HTML report. Choose a single PDF path, or drop the PDF claim.
- Interactive charts: switch the Visualization page to `st.plotly_chart`, which reuses plotly from export_plots, and then make plot export work.
- Hosting readiness (P1-7): add authentication in front of Streamlit (reverse proxy or the platform login), upload size limits, `--server.address 127.0.0.1` for local use, and a dependency scan (`pip-audit`) in CI (P2-13).
- Product integration per CLAUDE.md §7–8: server-side entitlement check before premium features, and a packaging and versioning decision (pyproject, release tags).
- Performance: cache figures and reports with `st.cache_data`, and add sampling for large files using `analysis_rules.sample_size`.

## Out of scope

Rewriting to another framework, a database-backed multi-user backend, or "AI" features. Each of these is a separate product decision for the founder.
