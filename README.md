# Universal Data Analyzer 📊

Universal Data Analyzer is a modular, extensible Python project designed to perform **automatic data ingestion, cleaning, exploratory data analysis (EDA), visualization, and reporting** on virtually any dataset.

The goal is simple:  
👉 *Give any dataset → Get structured insights, charts, and reports.*

This project is built with **real-world data analyst workflows** in mind and follows clean software engineering principles.

---

## 🚀 Features

- Load data from CSV, Excel, and SQL databases
- Automatically detect schema and data types
- Handle missing values, duplicates, and outliers
- Generate descriptive statistics and correlations
- Smart chart recommendations based on data types
- Interactive visualizations
- Export cleaned data, plots, and reports
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
│   └── logging.json
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
├── data/
│   ├── raw/
│   ├── processed/
│   └── samples/
│
├── logs/
│   └── app.log
│
├── requirements.txt
├── README.md
└── .gitignore
```
## Installation
```
git clone https://github.com/wilson-adhikari/Universal-Data-Analyzer.git
cd Universal-Data-Analyzer
pip install -r requirements.txt

```

