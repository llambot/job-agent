"""
job_scraper.py
Scrapes LinkedIn, Indeed, and Google Jobs using python-jobspy.
Deduplicates results and saves to SQLite.
"""

import json
import time
import sqlite3
from datetime import datetime, date
from pathlib import Path

# ── Try to import jobspy (install if missing) ──────────────────────────────
try:
    from jobspy import scrape_jobs
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-jobspy", "-q"])
    from jobspy import scrape_jobs

import pandas as pd

DB_PATH = Path(__file__).parent / "jobs.db"

# ── Search queries tailored to Laurie's profile ────────────────────────────
SEARCH_QUERIES = [
    # Core neuroscience / research scientist
    {"query": "neuroscience research scientist", "location": "Remote"},
    {"query": "computational neuroscience scientist", "location": "Remote"},
    {"query": "senior research scientist neuroscience", "location": "Remote"},
    # Biotech / pharma / neurotech
    {"query": "neuroscience biotech scientist remote", "location": "Remote"},
    {"query": "clinical research scientist neurology", "location": "Remote"},
    {"query": "medical science liaison neuroscience", "location": "Remote"},
    {"query": "neurotech research scientist", "location": "Remote"},
    # Digital health / AI in health
    {"query": "digital health neuroscience scientist", "location": "Remote"},
    {"query": "AI healthcare neuroscience PhD", "location": "Remote"},
    # Colorado in-person
    {"query": "neuroscience scientist", "location": "Colorado"},
    {"query": "research scientist biomedical Colorado", "location": "Colorado"},
    # Canada bonus
    {"query": "neuroscience research scientist", "location": "Canada"},
    {"query": "neurotech scientist remote", "location": "Canada"},
    {"query": "clinical neuroscience scientist", "location": "Montreal"},
    {"query": "neuroscience PhD scientist", "location": "Toronto"},
]

SOURCES = ["linkedin", "indeed", "google"]


def init_db():
    """Create the SQLite database and jobs table if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id              TEXT PRIMARY KEY,
            title           TEXT,
            company         TEXT,
            location        TEXT,
            description     TEXT,
            job_url         TEXT,
            source          TEXT,
            date_posted     TEXT,
            salary_min      REAL,
            salary_max      REAL,
            is_remote       INTEGER,
            is_canadian     INTEGER,
            claude_score    REAL,
            claude_summary  TEXT,
            status          TEXT DEFAULT 'new',
            scraped_at      TEXT
        )
    """)
    conn.commit()
    conn.close()


def already_seen(job_id: str) -> bool:
    SKIP_DUPLICATE_CHECK = True
        if SKIP_DUPLICATE_CHECK:
        return FALSE
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM jobs WHERE id = ?", (job_id,))
    result = cur.fetchone()
    conn.close()
    return result is not None


def save_job(job: dict):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT OR IGNORE INTO jobs
        (id, title, company, location, description, job_url, source,
         date_posted, salary_min, salary_max, is_remote, is_canadian, scraped_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        job["id"],
        job.get("title", ""),
        job.get("company", ""),
        job.get("location", ""),
        job.get("description", ""),
        job.get("job_url", ""),
        job.get("source", ""),
        str(job.get("date_posted", "")),
        job.get("min_amount"),
        job.get("max_amount"),
        1 if job.get("is_remote") else 0,
        1 if _is_canadian(job) else 0,
        datetime.now().isoformat(),
    ))
    conn.commit()
    conn.close()


def _is_canadian(job: dict) -> bool:
    location = str(job.get("location", "")).lower()
    company  = str(job.get("company", "")).lower()
    canadian_markers = ["canada", "ontario", "quebec", "british columbia",
                        "alberta", "toronto", "montreal", "vancouver",
                        "ottawa", "calgary", " on,", " bc,", " qc,", " ab,"]
    return any(m in location or m in company for m in canadian_markers)


def scrape_all() -> list[dict]:
    """Run all search queries and return new jobs as a list of dicts."""
    init_db()
    new_jobs = []
    seen_urls = set()

    for query_config in SEARCH_QUERIES:
        print(f"  Searching: '{query_config['query']}' in {query_config['location']}")
        time.sleep(3)
        try:
            df = scrape_jobs(
                site_name=SOURCES,
                search_term=query_config["query"],
                location=query_config["location"],
                results_wanted=20,
		hours_old=720,     # 30 days to catch more jobs
		country_indeed="USA",
		job_type="fulltime",
            )
        except Exception as e:
            print(f"    Warning: scrape failed for this query — {e}")
            continue

        if df is None or df.empty:
            continue

        for _, row in df.iterrows():
            job = row.to_dict()
            job_url = str(job.get("job_url", ""))
            job_id  = job.get("id", job_url)  # use URL as fallback ID

            # Skip duplicates within this run or already in DB
            if job_url in seen_urls or already_seen(str(job_id)):
                continue

            # Skip jobs with no description (useless to rank)
            if not job.get("description"):
                continue

            seen_urls.add(job_url)
            job["id"] = str(job_id)
            save_job(job)
            new_jobs.append(job)

    print(f"\n  Found {len(new_jobs)} new jobs today.")
    return new_jobs


def get_todays_jobs(limit: int = 50) -> list[dict]:
    """Retrieve today's unranked jobs from the database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    today = date.today().isoformat()
    cur.execute("""
        SELECT * FROM jobs
        WHERE scraped_at LIKE ?
        AND status = 'new'
        ORDER BY is_canadian DESC, scraped_at DESC
        LIMIT ?
    """, (f"{today}%", limit))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def mark_job_status(job_id: str, status: str):
    """Update a job's status: 'new', 'ranked', 'selected', 'applied', 'passed'."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE jobs SET status = ? WHERE id = ?", (status, job_id))
    conn.commit()
    conn.close()


def save_claude_ranking(job_id: str, score: float, summary: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "UPDATE jobs SET claude_score = ?, claude_summary = ?, status = 'ranked' WHERE id = ?",
        (score, summary, job_id)
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    print("Running job scraper...")
    jobs = scrape_all()
    print(f"Done. {len(jobs)} new jobs saved to {DB_PATH}")
