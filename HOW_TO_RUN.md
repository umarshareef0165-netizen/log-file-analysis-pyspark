# How to Run This Project — Step by Step (Anaconda + Jupyter)

> **Total time:** ~5-10 minutes (assuming Anaconda already installed)

---

## STEP 1 — Install dependencies (one time only)

Open **Anaconda Prompt** and run:

```bash
pip install pyspark pandas matplotlib jupyter python-docx
```

> Note: Java 8 or 11 must be installed for PySpark. If you don't have it:
> Windows: download from https://adoptium.net/ → install → done.

---

## STEP 2 — Generate the dataset

Navigate to the project folder in Anaconda Prompt:

```bash
cd path\to\log-file-analysis
python generate_logs.py
```

Output:
```
Generated 5000 log lines into access.log
```

You should now see `access.log` (~700 KB) in the folder.

---

## STEP 3 — Build the Word documentation (one-time)

```bash
python build_docx.py
```

This converts the project documentation into `Documentation.docx`.

---

## STEP 4 — Open the Jupyter Notebook

```bash
jupyter notebook
```

Browser opens. Click **Log_File_Analysis.ipynb**.

---

## STEP 5 — Run all cells

In Jupyter menu: **Cell → Run All**

Or press `Shift + Enter` on each cell sequentially.

You'll see:
- Spark session starting (~5 seconds)
- 5,000 records parsed
- Tables for total requests, top IPs, errors
- Charts rendered inline (traffic time-series, status codes, bot vs human pie)
- Suspicious IPs detected
- All 3 PNG charts saved to the project folder

---

## STEP 6 — Take screenshots for submission

Capture screenshots of:
1. Spark session initialization output
2. Total requests count + method/status breakdown
3. Top 10 IPs table
4. Error logs filter output
5. Traffic time-series chart (hourly + daily)
6. Suspicious IPs table
7. Attack-path probing table
8. Bot vs Human pie chart
9. Status code distribution chart

> Tip: Use Windows `Snipping Tool` (Win + Shift + S) for quick crops.

---

## STEP 7 — Record the video (1-2 minutes)

Use **OBS Studio** (free) or Windows built-in **Game Bar** (Win + G):
- Follow the script in `Video_Script.md`
- Show the notebook running cell by cell
- Highlight the 3 novelty features
- Export as MP4

---

## STEP 8 — Upload to GitHub

```bash
git init
git add .
git commit -m "Log File Analysis using PySpark — Big Data Analytics Mini Project 6"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/log-file-analysis.git
git push -u origin main
```

> Don't forget to update the `[GitHub link]` placeholder in `LinkedIn_Post.md`.

---

## STEP 9 — Post on LinkedIn

Copy text from `LinkedIn_Post.md` (Version 1 recommended).
Upload the video.
Put the GitHub link in the FIRST COMMENT (not in post body — better algorithm reach).
Tag your professor / group partner.

---

## STEP 10 — Submit

Share GitHub repo link + LinkedIn post URL with your group/instructor.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `JAVA_HOME not set` | Install Java 8/11 from adoptium.net, set `JAVA_HOME` env variable |
| `findspark not found` | `pip install findspark` (only needed if PySpark doesn't auto-import) |
| Notebook kernel crashes | Restart kernel; reduce dataset size in `generate_logs.py` (change `NUM_LINES = 1000`) |
| Charts not showing | Add `%matplotlib inline` at the top of the notebook (Jupyter usually does this automatically) |
| `regexp_extract` returns empty | Verify the log file format — open `access.log` and confirm Combined Log Format |

---

**You're done! Good luck with the submission.**
