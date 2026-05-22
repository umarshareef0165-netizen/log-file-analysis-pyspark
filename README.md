# Log File Analysis using PySpark

> **Big Data Analytics — Mini Project 6**
> Comprehensive Apache web server log analysis using distributed processing with PySpark.

---

## Project Overview

This project parses raw Apache access logs (Combined Log Format) and runs analytical queries using **PySpark DataFrames**. It demonstrates how big data tools handle semi-structured text data at scale — the same code runs on a laptop or on a multi-node cluster.

## Tasks Implemented

### Core Tasks (Project Requirements)
1. **Load server log data** — regex-based parsing of Apache Combined Log Format
2. **Count number of requests** — total requests + breakdown by HTTP method
3. **Find most frequent IP** — top 10 IPs ranked by request count
4. **Filter error logs** — all 4xx and 5xx responses with sample entries

### Novelty Features (Bonus — makes this project unique)
5. **Time-series Traffic Analysis** — hourly and daily traffic patterns with bar/line charts
6. **Anomaly & Suspicious IP Detection** — flags IPs with abnormal error rates and probes to sensitive paths like `/wp-admin`, `/.env`, `/admin`
7. **Bot vs Human Traffic Split** — User-Agent classification with pie chart visualization

---

## Tech Stack

| Component | Purpose |
|-----------|---------|
| **PySpark 3.x** | Distributed data processing |
| **Pandas** | Final aggregation conversion for plotting |
| **Matplotlib** | Visualizations (bar, line, pie charts) |
| **Jupyter Notebook** | Interactive analysis environment |
| **Anaconda** | Python distribution |

---

## Project Structure

```
log-file-analysis/
├── access.log                       # Synthetic Apache log dataset (5,000 records)
├── generate_logs.py                 # Script to regenerate the dataset
├── Log_File_Analysis.ipynb          # Main PySpark notebook
├── build_notebook.py                # Script that builds the notebook
├── chart_traffic_timeseries.png     # Hourly + daily traffic chart
├── chart_bot_vs_human.png           # Bot vs human pie chart
├── chart_status_codes.png           # Status code distribution
├── Documentation.docx               # Short documentation
└── README.md                        # This file
```

---

## How to Run

### 1. Install dependencies
```bash
pip install pyspark pandas matplotlib jupyter
```

### 2. Generate the dataset (already included)
```bash
python generate_logs.py
```
This creates `access.log` with 5,000 realistic Apache log records.

### 3. Launch Jupyter
```bash
jupyter notebook Log_File_Analysis.ipynb
```

### 4. Run all cells
`Cell -> Run All` — the notebook executes end-to-end and renders all charts inline.

---

## Sample Output Highlights

- **Total Requests:** ~5,000
- **Most Frequent IP:** Top 5 heavy users identified
- **Error Rate:** ~12-18% of requests (404, 403, 500, etc.)
- **Peak Traffic Hour:** 11:00 AM – 1:00 PM window
- **Suspicious IPs:** 3 attacker IPs flagged via probing of `/wp-admin`, `/.env`
- **Bot Traffic Share:** ~25-30% (Googlebot, bingbot, curl, python-requests, etc.)

---

## Why PySpark over Pandas?

A production web server can produce **hundreds of GB of logs per day**. Pandas loads everything into memory — it would crash. PySpark uses:
- **Lazy evaluation** — only computes what's needed
- **Distributed execution** — splits work across CPU cores / cluster nodes
- **Catalyst optimizer** — automatically optimizes query plans
- **Same DataFrame API** — code runs unchanged from laptop to cluster

---

## Submitted By

**Easy Storage**
Big Data Analytics — Spring 2026
Submission Date: 20 May 2026

---

## License

MIT — feel free to fork and extend.
