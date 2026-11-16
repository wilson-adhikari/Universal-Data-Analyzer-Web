# Universal Data Analyzer 📊

Universal Data Analyzer is a modular, extensible Python project designed to perform **automatic data ingestion, cleaning, exploratory data analysis (EDA), visualization, and reporting** on virtually any dataset.

The goal is simple:  
👉 *Give any dataset → Get structured insights, charts, and reports.*

This project is built with **real-world data analyst workflows** in mind and follows clean software engineering principles.

---

## 🚀 Features

- Load data from CSV and Excel files (SQL helper modules exist but are not wired into the app)
- Handle missing values, duplicates, and outliers
- Generate descriptive statistics and correlations
- Static charts (scatter, line, bar, histogram, box, violin, KDE)
- Rule-based text insights
- Export cleaned data (CSV, Excel) and an HTML report
- Fully modular & testable architecture

---

## 🧠 Why This Project?

Most data analysis projects are **dataset-specific**.  
This one is **dataset-agnostic**.

It demonstrates:
- Strong Python fundamentals
- Data analysis expertise
- Clean project structure
- Scalable design
- Real production-style thinking

This is exactly the kind of project recruiters like to see.

---

## 🏗 Project Structure

```text
universal_data_analyzer/
│
├── main.py                  # Entry point
│
├── config/                  # Configurations
│   ├── default.json
│   └── loging.json
│
├── ingestion/               # Data loading
│   ├── csv_loader.py
│   ├── excel_loader.py
│   ├── sql_loader.py
│   └── schema_detector.py
│
├── cleaning/                # Data cleaning logic
│   ├── missing_values.py
│   ├── outliers.py
│   ├── duplicates.py
│   └── type_casting.py
│
├── eda/                     # Exploratory Data Analysis
│   ├── summary_stats.py
│   ├── distributions.py
│   ├── correlations.py
│   └── group_analysis.py
│
├── visualization/           # Visualization engine
│   ├── chart_selector.py
│   ├── plot_factory.py
│   └── style.py
│
├── insights/                # Auto-generated insights
│   ├── text_generator.py
│   └── thresholds.py
│
├── reporting/               # Exporting results
│   ├── export_data.py
│   ├── export_plots.py
│   └── report_builder.py
│
├── database/                # Database utilities
│   ├── engine.py
│   └── queries.py
│
├── utils/                   # Helpers & validators
│   ├── validators.py
│   ├── helpers.py
│   └── exceptions.py
│
├── tests/                   # Unit tests
│
├── logs/
│   └── app.log
│
└── requirements.txt
```
## Installation

Requires **Python 3.11** (the version this project is tested on). The pinned `numpy==1.24.3` and `pandas==2.0.3` do not install on Python 3.12 or newer. Python 3.9 and 3.10 are untested.

```
git clone https://github.com/wilson-adhikari/Universal-Data-Analyzer-Web.git
cd "Universal-Data-Analyzer-Web/Universal Data Analyzer"
python -m venv .venv
.venv\Scripts\activate          # Windows; on macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

## Run

From the `Universal Data Analyzer` folder (its name contains spaces, so quote the path):

```
streamlit run main.py --server.address localhost
```

Then open http://localhost:8501 in your browser.

**Security:** the app has no login. `--server.address localhost` keeps it reachable from your own machine only. Do not run it without that flag or expose it to a network.

