# Repository Audit: Universal-Data-Analyzer-Web

- **Audit date:** 2026-11-05
- **Commit audited:** `1557139` (HEAD of default branch, 4 commits total)
- **Auditor:** Claude Code (automated code-level audit)
- **Scope:** every tracked source, config, test and doc file. Source code was not changed.

## 1. Summary

This is a **single-page Streamlit app** (`Universal Data Analyzer/main.py`) backed by about 20 small helper modules written with pandas, matplotlib and seaborn. It is not a "framework" and has no web backend, API, accounts or persistence. The name says "Web" only because Streamlit serves the UI over HTTP.

**Verdict:**
- It runs, but only after a dependency workaround.
- Core CSV and Excel loading, basic cleaning, statistics, charts, rule-based insights and CSV/Excel/HTML export work on the happy path.
- Two UI features crash: outlier removal and group analysis.
- SQL ingestion has no UI.
- One module has a syntax error.
- Both test files fail to import.
- There is no CI.
- **It is not fit to offer to customers in its current state.**

## 2. What exists

| Item | Finding |
|---|---|
| Layout | All code lives in the folder `Universal Data Analyzer/`, whose name contains spaces. There are no `__init__.py` files, no `pyproject.toml`/`setup.py`, and no packaging. Imports rely on `sys.path.insert` (main.py:9). |
| Entry point | `main.py`, a Streamlit script. The README has no run command. The real command is `streamlit run main.py`. |
| Size | About 2,400 lines of Python: main.py has 430 lines and the rest are modules. `visualization/style.py` and `insights/thresholds.py` are empty (0 bytes). |
| Dependencies | `requirements.txt` has 18 exact pins from 2023 (streamlit 1.28.1, pandas 2.0.3, numpy 1.24.3, …). Runtime and dev tools are mixed together. Six runtime deps are never imported: weasyprint, reportlab, jinja2, pydantic, scikit-learn, python-dotenv. `plotly` is imported (reporting/export_plots.py:2) but is not listed. |
| Config | `config/default.json` and `config/loging.json` (misspelled) are **never loaded**. `utils/helpers.py:33` `load_config` defaults to the non-existent `app/config/default.json` and nothing calls it. |
| Tests | `tests/test_cleaning.py` (which actually tests ingestion) and `tests/test_eda.py`, 8 tests in total. Both import a non-existent `app.` package. |
| CI | None: there is no `.github/`, no workflow, and no lint config. |
| Git history | 4 commits, all dated 2025-12-21, by a single author. All code arrived in one web upload ("Add files via upload"), so there is no development history. |
| Committed artefacts | 19 `__pycache__/*.pyc` files (cpython-313 and 314) and `logs/app.log` are tracked even though `.gitignore` excludes them. |
| Licence | MIT, © 2025 wilson adhikari. All pinned deps are permissive (BSD/MIT/Apache/PSF-style). There are no third-party code copies and no NOTICE file. |

## 3. Execution record (what was actually run)

Environment: Windows 11, Python **3.11.0** (`py -3.11`). Python 3.15 is also installed but cannot install numpy 1.24.3.

The venv was created at `D:\tmp-audit-uda-web\venv` instead of the requested scratchpad on C:, because **C: had 0.5 GB free** and the first install failed with `OSError: [Errno 28] No space left on device`.

| # | Command | Result |
|---|---|---|
| 1 | `py -3.11 -m venv venv` then `pip install --no-cache-dir -r "Universal Data Analyzer/requirements.txt"` | Exit 0. pip resolved **pyarrow 26.0.1** as a transitive dependency of streamlit. |
| 2 | `python -c "import streamlit"` | **FAIL:** `ImportError: pyarrow requires NumPy 2.0 or newer, found 1.24.3`. **A clean install cannot start the app.** |
| 3 | Venv-only workaround: `pip install "pyarrow<15"` (gives 14.0.2) | `import streamlit` OK. No repo file was changed. |
| 4 | Import every module | 23 of 25 import OK. `database.queries`: **IndentationError** at line 80 (file truncated mid-function). `reporting.export_plots`: **ModuleNotFoundError: plotly**. |
| 5 | `pytest tests` (from repo dir) | **2 collection errors**: `ModuleNotFoundError: No module named 'app'`. 0 tests ran. |
| 6 | Same tests run from an out-of-repo copy of the folder renamed `app/` (import shim only) | **6 passed, 2 failed.** `test_categorical_summary` has a wrong assertion. `test_correlation_values` hits `KeyError: 'Correlation'`, a real bug in eda/correlations.py:52. |
| 7 | `streamlit run main.py --server.headless true --server.port 8599` | Server started. `/_stcore/health` returned `ok` and `GET /` returned 200. It binds to all interfaces (a "Network URL" was printed). |
| 8 | Headless UI drive with `streamlit.testing.v1.AppTest`, using a 50-row synthetic DataFrame injected into session state (AppTest cannot drive `file_uploader`) | Home, Cleaning (missing values → mean), EDA tabs, Visualization (scatter/line/bar/histogram/box/violin), Insights, and all 3 Export buttons render with no exception. **Outliers checkbox → `No module named 'app'`. Group Analysis button → `NameError: GroupAnalyzer`. SQL button → no input widgets appear. kde with a categorical x → error shown.** |
| 9 | Direct module probes (scripts in `D:\tmp-audit-uda-web\run\`) | See FEATURE_TRACEABILITY.md and TECHNICAL_DEBT.md. Highlights: a semicolon CSV loads as 1 column, the HTML report does not escape column names, `DatabaseEngine.load_table` accepts injected SQL, and insights crash on an all-null text column. |

**Not executed:**
- A real browser upload of CSV/Excel through the UI. The loaders were exercised directly instead.
- Any MySQL/PostgreSQL connection.
- PNG/JPEG plot export (plotly is absent).
- `pip-audit`/CVE scanning.
- flake8/black.
- Testing on Python 3.12+.
- Testing on Linux/macOS.

After all runs, `git status --short --ignored` showed the repo clean. Logs were written to the run directory, not to the tracked `logs/app.log`.

## 4. Security findings

| Severity | Finding | Evidence |
|---|---|---|
| High (for a hosted product) | **No authentication.** Streamlit binds 0.0.0.0, and any network peer can upload files (default limit 200 MB) and use CPU. That is acceptable only for local, single-user use. | main.py (no auth layer); run #7 output |
| Medium | **HTML injection in the generated report.** The title, column names and dtypes are interpolated into HTML without escaping. A crafted CSV header such as `<script>…</script>` ends up as live script in `report.html`, which users download and share. | reporting/report_builder.py:29,46,84; probe confirmed the column name is not escaped |
| Medium (latent) | **SQL injection.** Table and column names and `LIMIT` are concatenated into SQL with f-strings. The probe ran `users UNION SELECT 99, sqlite_version()` successfully. This is not reachable from the UI today, but it will be once SQL ingestion is exposed. | database/engine.py:25-27; database/queries.py:42,67 |
| Low | Error messages are shown verbatim to the user (`st.error(str(e))`), which can leak paths and DB details. | main.py:154,174,271,357 |
| Low | Old pins: streamlit 1.28.1 (2023) and jinja2 3.1.2 have published advisories in later releases. Not verified with a scanner, so run `pip-audit`. | requirements.txt |
| Info | `config/default.json:27` holds the placeholder DSN `postgresql://user:password@localhost…`. This is not a real secret, but it models storing credentials in committed config. No real secrets, keys or tokens were found. | grep over the repo |
| Info | `unsafe_allow_html=True` is used only with static strings, so it is safe as written. | main.py:39-52,86,116 |

## 5. Documentation accuracy

- No AI citation artefacts (`[web:…]`, `[cite…]`) were found.
- The README clone URL and `cd` point to `Universal-Data-Analyzer`, not this repo (`-Web`), and the folder is actually `Universal Data Analyzer/` (README.md:109-110).
- The README tree shows `universal_data_analyzer/`, `config/logging.json` and `data/raw|processed|samples`. The real names are `Universal Data Analyzer/` and `config/loging.json`, and `data/` does not exist.
- The README has no run command and no Python-version requirement. numpy 1.24.3 requires Python ≤ 3.11.
- "Interactive visualizations" (README.md:19): charts are static matplotlib images.
- "Smart chart recommendations" (README.md:18): `ChartSelector` is imported but never called.
- "Export … plots" (README.md:20): there is no plot export in the UI, and the module is broken.
- The UI promises "AI-generated text insights" (main.py:97,366). They are fixed rules (row count, % missing, CV>100%, |skew|>1, top category). Customer-facing copy must not call this AI.
- The UI promises SQL (MySQL, PostgreSQL, SQLite) support (main.py:111). There is no SQL UI, and no MySQL/PostgreSQL drivers are in requirements.
- The README describes itself in portfolio terms ("This is exactly the kind of project recruiters like to see", README.md:37), which does not suit a product page.

## 6. Customer readiness

**Not ready.** It fails the release gates in CLAUDE.md §12:
- It does not install cleanly.
- The tests do not run and there is no CI.
- Two advertised features crash and one is absent.
- The README is inaccurate.
- It has no auth, entitlement or licensing integration.
- The report has an injection issue.

It could serve as a local single-user demo after milestone M1 in REBUILD_PLAN.md.
