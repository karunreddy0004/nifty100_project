# 📈 Nifty100 Investment Analytics Platform

A complete end-to-end financial analytics platform built using **Python**, **SQLite**, **FastAPI**, and **Streamlit** for analyzing Nifty100 companies.

---

# Project Overview

This project processes financial statement data, calculates investment ratios, performs valuation, generates reports, exposes REST APIs, and provides an interactive dashboard for investors.

---

# Features

- ETL pipeline for financial data
- Data validation framework
- 50+ Financial KPIs
- CAGR calculations
- Quality ranking engine
- Company screener
- Peer comparison engine
- Sector analysis
- Portfolio recommendation
- Investment score engine
- Cashflow intelligence
- Company pros & cons generation
- Company tearsheets
- Sector reports
- Portfolio reports
- Streamlit Dashboard
- FastAPI Backend (16+ Endpoints)
- Automated Testing using Pytest

---

# Technology Stack

- Python 3.13
- Pandas
- NumPy
- SQLite
- FastAPI
- Streamlit
- Pytest
- OpenPyXL
- Uvicorn

---

# Project Structure

```text
nifty100_project/

├── config/
├── data/
├── db/
├── docs/
├── output/
├── reports/
├── src/
│   ├── analytics/
│   ├── api/
│   ├── dashboard/
│   ├── etl/
│   ├── reports/
│   └── screener/
├── tests/
├── README.md
└── requirements.txt
```

---

# Project Workflow

```
Excel Files
      │
      ▼
ETL Pipeline
      │
      ▼
SQLite Database
      │
      ▼
Financial Ratio Engine
      │
      ▼
Ranking Engine
      │
      ▼
Screener
      │
      ▼
Portfolio Analysis
      │
      ▼
FastAPI
      │
      ▼
Streamlit Dashboard
```

---

# Main Modules

### Sprint 1

- ETL Pipeline
- Database Loader
- Data Validation

### Sprint 2

- Financial Ratio Engine
- CAGR
- KPI Calculations

### Sprint 3

- Screener
- Ranking Engine
- Peer Comparison

### Sprint 4

- Streamlit Dashboard
- Valuation Engine

### Sprint 5

- Cashflow Intelligence
- Company Reports
- Portfolio Reports

### Sprint 6

- FastAPI REST APIs
- Automated Testing
- Documentation

---

# FastAPI Endpoints

- Health
- Companies
- Documents
- Dashboard
- Stock Prices
- Analytics
- Portfolio
- Screener
- Risk
- Sectors
- Investment Scores
- Investor Reports
- Company Summary
- Valuation

---

# Dashboard Features

- Company Overview
- Financial Ratios
- Investment Scores
- Portfolio Analysis
- Screener
- Sector Analysis
- Charts
- Reports

---

# Testing

✔ 77 Automated Test Cases

```
77 Passed
0 Failed
```

Generated Report

```
reports/pytest_report.html
```

---

# Run Project

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Launch Streamlit

```bash
streamlit run src/dashboard/app.py
```

### Launch FastAPI

```bash
uvicorn src.api.main:app --reload
```

### Run Tests

```bash
python -m pytest tests -v
```

---

# Future Improvements

- Live NSE/BSE Data Integration
- AI Investment Recommendations
- User Authentication
- Portfolio Tracking
- Cloud Deployment
- Docker Support

---

# Author

**Karun Reddy**

Final Year B.Tech (CSE)

Python | Data Analytics | FastAPI | Streamlit | Machine Learning

GitHub:
https://github.com/karunreddy0004

LinkedIn:
(Add your LinkedIn profile)

---

# License

This project is developed for educational and portfolio purposes.