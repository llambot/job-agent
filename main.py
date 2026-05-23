"""
main.py
The daily job agent orchestrator.
Run this every morning via cron or GitHub Actions.

Usage:
  python main.py                  # full daily run
  python main.py --test           # dry run, no emails sent
  python main.py --rank-only      # scrape + rank, no cover letters
  python main.py --cover <job_id> # generate cover letter for a specific job
"""

import json
import argparse
from pathlib import Path
from datetime import date

from job_scraper import scrape_all
# claude_engine removed — scoring done by Gemini in enrich_jobs.py
# cover letters, PDFs, and email handled server-side at jobs.lambot.co

# Optional: only import gmail if credentials exist
GMAIL_READY = (Path(__file__).parent / "credentials.json").exists()
if GMAIL_READY:
    from gmail_sender import send_email


def run_daily(dry_run: bool = False, rank_only: bool = False):
    """Full morning pipeline: scrape, rank, save results."""
    print(f"\n{'='*60}")
    print(f"  LAURIE'S JOB AGENT — {date.today()}")
    print(f"{'='*60}\n")

    # Step 1: Scrape
    print("STEP 1: Scraping jobs...")
    new_jobs = scrape_all()

    if not new_jobs:
        print("No new jobs found today. Check back tomorrow.")
        return []

    # Step 2: Pass jobs through — scoring done by Gemini in enrich_jobs.py
    print(f"\nSTEP 2: {len(new_jobs)} jobs scraped — Gemini will score during enrichment")
    ranked = new_jobs

    # Save top jobs to JSON for the app
    output_file = Path(__file__).parent / "today_jobs.json"
    with open(output_file, "w", encoding='utf-8') as f:
        all_jobs = sorted(ranked, key=lambda x: x.get('claude_score') or x.get('fit_score') or 0, reverse=True)[:30]
        json.dump(all_jobs, f, indent=2, ensure_ascii=True, default=str)

    print(f"\nSTEP 3: Top {len(ranked)} jobs saved to {output_file}")

    # Print summary
    print("\n" + "="*60)
    print("TODAY'S TOP JOBS")
    print("="*60)
    for i, job in enumerate(ranked[:10], 1):
        canada = " 🍁" if job.get("canada_flag") or job.get("is_canadian") else ""
        remote = " [remote]" if job.get("remote") or job.get("is_remote") else ""
        print(f"\n#{i} {job.get('title', 'N/A')} @ {job.get('company', 'N/A')}")
        print(f"   {job.get('location', 'N/A')} | {job.get('est_salary', 'N/A')}")

    return ranked


def apply_to_job(job_id: str, dry_run: bool = True):
    """
    Cover letter generation, PDF, and email sending
    are all handled server-side at jobs.lambot.co
    Use the app at jobs.lambot.co to apply to jobs.
    """
    print("Application pipeline moved to jobs.lambot.co")
    print(f"To apply to job {job_id}, open the app and click 'Write cover letter'")


def main():
    parser = argparse.ArgumentParser(description="Laurie's Job Agent")
    parser.add_argument("--test",      action="store_true", help="Dry run — no emails sent")
    parser.add_argument("--rank-only", action="store_true", help="Scrape and rank only")
    parser.add_argument("--cover",     type=str,            help="Generate cover letter for job ID")
    args = parser.parse_args()

    if args.cover:
        apply_to_job(args.cover, dry_run=args.test)
    else:
        run_daily(dry_run=args.test, rank_only=args.rank_only)


if __name__ == "__main__":
    main()
