"""
Builds the Log_File_Analysis.ipynb notebook programmatically using nbformat.
Run this once to generate the notebook, then open in Jupyter.
"""
import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

# ============== TITLE ==============
cells.append(nbf.v4.new_markdown_cell("""# Log File Analysis using PySpark
### Big Data Analytics — Mini Project 6

**Author:** Easy Storage
**Date:** May 2026
**Tools:** PySpark, Pandas, Matplotlib, Jupyter Notebook (Anaconda)

---

## Project Overview

This project performs comprehensive analysis on Apache web server access logs using **PySpark** to demonstrate big data processing techniques. We go beyond the basic requirements by adding three novelty features:

**Core Tasks (Required):**
1. Load server log data
2. Count number of requests
3. Find most frequent IP
4. Filter error logs

**Novelty Additions (Bonus):**
5. **Time-series traffic analysis** — hourly/daily request patterns with visualization
6. **Anomaly / suspicious IP detection** — security-focused threat hunting
7. **Bot vs Human traffic split** — User-Agent classification

---
"""))

# ============== STEP 1: SETUP ==============
cells.append(nbf.v4.new_markdown_cell("## 1. Setup — Import Libraries & Initialize Spark Session"))
cells.append(nbf.v4.new_code_cell("""import os
import re
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, regexp_extract, count, desc, when, hour, to_timestamp,
    dayofweek, date_format, sum as _sum, lit, length
)
from pyspark.sql.types import IntegerType

# Initialize Spark Session
spark = (
    SparkSession.builder
    .appName("LogFileAnalysis")
    .master("local[*]")
    .config("spark.sql.shuffle.partitions", "4")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")
print("Spark Version:", spark.version)
print("Spark Session created successfully!")"""))

# ============== STEP 2: LOAD DATA ==============
cells.append(nbf.v4.new_markdown_cell("""## 2. Task 1 — Load Server Log Data

Apache logs follow the **Combined Log Format**:
```
IP - - [timestamp] "METHOD /url HTTP/1.1" status size "referrer" "user-agent"
```

We load the raw log file as a text DataFrame, then parse each field using **regex extraction** — a classic Big Data pattern for semi-structured data."""))

cells.append(nbf.v4.new_code_cell("""# Load raw logs as a single-column DataFrame
LOG_PATH = "access.log"
raw_logs = spark.read.text(LOG_PATH)
print(f"Total raw lines loaded: {raw_logs.count():,}")
raw_logs.show(3, truncate=80)"""))

cells.append(nbf.v4.new_code_cell("""# Apache Combined Log Format regex
LOG_PATTERN = (
    r'^(\\S+) \\S+ \\S+ \\[([^\\]]+)\\] '
    r'"(\\S+) (\\S+) (\\S+)" '
    r'(\\d{3}) (\\d+) "([^"]*)" "([^"]*)"'
)

logs = raw_logs.select(
    regexp_extract("value", LOG_PATTERN, 1).alias("ip"),
    regexp_extract("value", LOG_PATTERN, 2).alias("timestamp_str"),
    regexp_extract("value", LOG_PATTERN, 3).alias("method"),
    regexp_extract("value", LOG_PATTERN, 4).alias("url"),
    regexp_extract("value", LOG_PATTERN, 5).alias("protocol"),
    regexp_extract("value", LOG_PATTERN, 6).cast(IntegerType()).alias("status"),
    regexp_extract("value", LOG_PATTERN, 7).cast(IntegerType()).alias("size"),
    regexp_extract("value", LOG_PATTERN, 8).alias("referrer"),
    regexp_extract("value", LOG_PATTERN, 9).alias("user_agent"),
)

# Convert timestamp string to proper TimestampType
logs = logs.withColumn(
    "timestamp",
    to_timestamp(col("timestamp_str"), "dd/MMM/yyyy:HH:mm:ss Z")
)

# Drop rows where parsing failed
logs = logs.filter(col("ip") != "")
logs.cache()
print(f"Total parsed log records: {logs.count():,}")
logs.printSchema()
logs.show(5, truncate=40)"""))

# ============== STEP 3: COUNT REQUESTS ==============
cells.append(nbf.v4.new_markdown_cell("## 3. Task 2 — Count Number of Requests"))
cells.append(nbf.v4.new_code_cell("""total_requests = logs.count()
print(f"Total HTTP requests in log file: {total_requests:,}")

# Breakdown by HTTP method
print("\\nRequests by HTTP Method:")
logs.groupBy("method").count().orderBy(desc("count")).show()

# Breakdown by status code
print("Requests by Status Code:")
logs.groupBy("status").count().orderBy(desc("count")).show()"""))

# ============== STEP 4: TOP IPs ==============
cells.append(nbf.v4.new_markdown_cell("## 4. Task 3 — Find Most Frequent IP Addresses"))
cells.append(nbf.v4.new_code_cell("""top_ips = (
    logs.groupBy("ip")
    .agg(count("*").alias("request_count"))
    .orderBy(desc("request_count"))
)
print("Top 10 Most Frequent IPs:")
top_ips.show(10, truncate=False)

most_frequent_ip = top_ips.first()
print(f"\\nMost frequent IP: {most_frequent_ip['ip']} with {most_frequent_ip['request_count']:,} requests")"""))

# ============== STEP 5: ERROR LOGS ==============
cells.append(nbf.v4.new_markdown_cell("""## 5. Task 4 — Filter Error Logs

HTTP status codes in the **4xx range** indicate client errors (e.g., 404 Not Found, 403 Forbidden) and **5xx range** indicate server errors (e.g., 500 Internal Server Error)."""))
cells.append(nbf.v4.new_code_cell("""error_logs = logs.filter((col("status") >= 400) & (col("status") < 600))
total_errors = error_logs.count()
error_rate = (total_errors / total_requests) * 100
print(f"Total error responses: {total_errors:,}")
print(f"Error rate: {error_rate:.2f}% of all requests\\n")

print("Error breakdown by status code:")
error_logs.groupBy("status").count().orderBy(desc("count")).show()

print("Sample error log entries:")
error_logs.select("ip", "method", "url", "status", "timestamp").show(10, truncate=False)"""))

# ============== NOVELTY 1: TIME-SERIES ==============
cells.append(nbf.v4.new_markdown_cell("""---
## 6. Novelty Feature #1 — Time-Series Traffic Analysis

Identifying peak traffic hours helps with **capacity planning, scaling decisions, and detecting DDoS patterns**."""))
cells.append(nbf.v4.new_code_cell("""import matplotlib.pyplot as plt

# Requests per hour of day
hourly = (
    logs.withColumn("hour", hour("timestamp"))
    .groupBy("hour")
    .agg(count("*").alias("requests"))
    .orderBy("hour")
    .toPandas()
)

# Requests per day
daily = (
    logs.withColumn("day", date_format("timestamp", "yyyy-MM-dd"))
    .groupBy("day")
    .agg(count("*").alias("requests"))
    .orderBy("day")
    .toPandas()
)

print("Hourly traffic distribution:")
print(hourly.to_string(index=False))
print(f"\\nPeak traffic hour: {int(hourly.loc[hourly['requests'].idxmax(),'hour']):02d}:00 with {int(hourly['requests'].max()):,} requests")"""))

cells.append(nbf.v4.new_code_cell("""fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Hourly chart
axes[0].bar(hourly["hour"], hourly["requests"], color="#3b82f6", edgecolor="black")
axes[0].set_title("Requests per Hour of Day", fontsize=13, fontweight="bold")
axes[0].set_xlabel("Hour (0-23)")
axes[0].set_ylabel("Number of Requests")
axes[0].set_xticks(range(0, 24))
axes[0].grid(axis="y", alpha=0.3)

# Daily chart
axes[1].plot(daily["day"], daily["requests"], marker="o", color="#ef4444", linewidth=2)
axes[1].set_title("Requests per Day", fontsize=13, fontweight="bold")
axes[1].set_xlabel("Date")
axes[1].set_ylabel("Number of Requests")
axes[1].tick_params(axis="x", rotation=45)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig("chart_traffic_timeseries.png", dpi=110, bbox_inches="tight")
plt.show()
print("Chart saved: chart_traffic_timeseries.png")"""))

# ============== NOVELTY 2: ANOMALY DETECTION ==============
cells.append(nbf.v4.new_markdown_cell("""---
## 7. Novelty Feature #2 — Anomaly & Suspicious IP Detection

We flag an IP as **suspicious** if it exhibits attack-like behavior:
- More than **3% error rate** AND at least 10 total requests
- Attempts to access sensitive paths (`/wp-admin`, `/.env`, `/admin`, `/phpmyadmin`, etc.)"""))

cells.append(nbf.v4.new_code_cell("""# Per-IP statistics
ip_stats = (
    logs.groupBy("ip")
    .agg(
        count("*").alias("total_requests"),
        _sum(when((col("status") >= 400) & (col("status") < 600), 1).otherwise(0)).alias("error_count"),
        _sum(when(col("status") == 404, 1).otherwise(0)).alias("notfound_count"),
        _sum(when(col("status") == 403, 1).otherwise(0)).alias("forbidden_count"),
    )
    .withColumn("error_rate_pct", (col("error_count") / col("total_requests") * 100))
)

# Suspicious = high error rate + meaningful traffic
suspicious_ips = (
    ip_stats.filter((col("error_rate_pct") > 30) & (col("total_requests") >= 10))
    .orderBy(desc("error_rate_pct"))
)
print("SUSPICIOUS IPs DETECTED (high error rate, possible attack):")
suspicious_ips.show(20, truncate=False)"""))

cells.append(nbf.v4.new_code_cell("""# Detect IPs hitting sensitive/admin paths
ATTACK_PATHS = ["/wp-admin", "/.env", "/config.php", "/wp-login.php",
                "/phpmyadmin", "/.git/config", "/admin"]
attack_filter = col("url").isin(ATTACK_PATHS) | col("url").startswith("/admin")

attackers = (
    logs.filter(attack_filter)
    .groupBy("ip")
    .agg(count("*").alias("attack_attempts"))
    .orderBy(desc("attack_attempts"))
)
print("IPs probing sensitive paths (likely scanners/attackers):")
attackers.show(20, truncate=False)"""))

# ============== NOVELTY 3: BOT VS HUMAN ==============
cells.append(nbf.v4.new_markdown_cell("""---
## 8. Novelty Feature #3 — Bot vs Human Traffic Split

We classify traffic by analyzing the **User-Agent** string. Known bot signatures: `bot`, `crawler`, `spider`, `curl`, `wget`, `python-requests`, `Googlebot`, `bingbot`, etc."""))

cells.append(nbf.v4.new_code_cell("""bot_pattern = r"(?i)bot|crawler|spider|curl|wget|python-requests|facebookexternalhit|twitterbot"

classified = logs.withColumn(
    "traffic_type",
    when(col("user_agent").rlike(bot_pattern), "Bot").otherwise("Human")
)

split = (
    classified.groupBy("traffic_type")
    .agg(count("*").alias("requests"))
    .toPandas()
)
print("Bot vs Human Traffic Split:")
print(split.to_string(index=False))

# Pie chart visualization
fig, ax = plt.subplots(figsize=(7, 7))
colors = ["#10b981", "#f59e0b"]
ax.pie(split["requests"], labels=split["traffic_type"], autopct="%1.1f%%",
       startangle=90, colors=colors, textprops={"fontsize": 12, "fontweight": "bold"})
ax.set_title("Bot vs Human Traffic Distribution", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("chart_bot_vs_human.png", dpi=110, bbox_inches="tight")
plt.show()
print("Chart saved: chart_bot_vs_human.png")"""))

cells.append(nbf.v4.new_code_cell("""# Top bot user agents
print("Top 10 Bot User-Agents:")
(classified.filter(col("traffic_type") == "Bot")
    .groupBy("user_agent")
    .agg(count("*").alias("requests"))
    .orderBy(desc("requests"))
    .show(10, truncate=80))"""))

# ============== STATUS CODE CHART ==============
cells.append(nbf.v4.new_markdown_cell("## 9. Bonus Visualization — Status Code Distribution"))
cells.append(nbf.v4.new_code_cell("""status_dist = (
    logs.groupBy("status").agg(count("*").alias("count"))
    .orderBy("status").toPandas()
)

fig, ax = plt.subplots(figsize=(10, 5))
colors_map = {200: "#10b981", 301: "#3b82f6", 304: "#6366f1",
              401: "#f59e0b", 403: "#f97316", 404: "#ef4444", 500: "#7c2d12"}
bar_colors = [colors_map.get(s, "#94a3b8") for s in status_dist["status"]]
ax.bar(status_dist["status"].astype(str), status_dist["count"],
       color=bar_colors, edgecolor="black")
ax.set_title("HTTP Status Code Distribution", fontsize=13, fontweight="bold")
ax.set_xlabel("Status Code")
ax.set_ylabel("Request Count")
ax.grid(axis="y", alpha=0.3)
for i, v in enumerate(status_dist["count"]):
    ax.text(i, v + max(status_dist["count"]) * 0.01, str(v), ha="center", fontweight="bold")
plt.tight_layout()
plt.savefig("chart_status_codes.png", dpi=110, bbox_inches="tight")
plt.show()
print("Chart saved: chart_status_codes.png")"""))

# ============== CONCLUSION ==============
cells.append(nbf.v4.new_markdown_cell("""---
## 10. Conclusion & Key Insights

### Summary of Findings

| Metric | Value |
|--------|-------|
| Total Requests | (shown above) |
| Total Errors (4xx + 5xx) | (shown above) |
| Most Frequent IP | (shown above) |
| Peak Traffic Hour | (shown above) |
| Suspicious IPs Detected | (shown above) |
| Bot Traffic Share | (shown above) |

### Business Insights
- **Capacity Planning**: Peak hours identify when server resources must be scaled up.
- **Security**: Suspicious IP detection + sensitive-path probing reveal active reconnaissance attempts that should be blocked at the WAF/firewall level.
- **SEO & Traffic Quality**: Bot vs human split tells us whether crawler traffic is dominating actual user engagement — important when interpreting analytics.
- **Reliability**: Error-rate trends per IP/per hour highlight outages or misconfigured endpoints.

### Why PySpark?
PySpark was chosen over plain Pandas because log files in production can reach **GBs to TBs per day**. The DataFrame API + Catalyst optimizer + lazy evaluation + distributed execution scale linearly — the same code runs on a laptop here and on a cluster in production.

---
**Stop Spark session:**"""))

cells.append(nbf.v4.new_code_cell("""spark.stop()
print("Spark session stopped. Project complete!")"""))

nb["cells"] = cells

# write notebook
with open("Log_File_Analysis.ipynb", "w") as f:
    nbf.write(nb, f)
print("Notebook written: Log_File_Analysis.ipynb")
