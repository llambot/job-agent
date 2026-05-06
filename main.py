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

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import date

from job_scraper import scrape_all, get_todays_jobs, save_claude_ranking, mark_job_status
from claude_engine import rank_all_jobs, generate_cover_letter, research_company
from pdf_generator import generate_pdf

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

    # Step 2: Rank with Claude
    print(f"\nSTEP 2: Ranking {len(new_jobs)} jobs with Claude...")
    ranked = rank_all_jobs(new_jobs)

    # Save rankings to DB
    for job in ranked:
        save_claude_ranking(
            job_id=job["id"],
            score=job.get("claude_score", 0),
            summary=job.get("claude_summary", "")
        )

    # Save top jobs to JSON for the app
    output_file = Path(__file__).parent / "today_jobs.json"
    with open(output_file, "w", encoding='utf-8') as f:
        all_jobs = sorted(ranked, key=lambda x: x.get('claude_score') or 0, reverse=True)[:30]
        json.dump(all_jobs, f, indent=2, ensure_ascii=True, default=str)

    print(f"\nSTEP 3: Top {len(ranked)} jobs saved to {output_file}")

    # Print summary
    print("\n" + "="*60)
    print("TODAY'S TOP JOBS")
    print("="*60)
    for i, job in enumerate(ranked[:10], 1):
        canada = " 🍁" if job.get("canada_flag") or job.get("is_canadian") else ""
        remote = " [remote]" if job.get("remote") or job.get("is_remote") else ""
        print(f"\n#{i} [{job['claude_score']}/100] {job.get('match_label', '')}{canada}{remote}")
        print(f"   {job.get('title', 'N/A')} @ {job.get('company', 'N/A')}")
        print(f"   {job.get('location', 'N/A')} | {job.get('est_salary', 'N/A')}")
        print(f"   {job.get('claude_summary', '')}")

    return ranked


def apply_to_job(job_id: str, dry_run: bool = True):
    """Generate cover letter and send application for a specific job."""
    # Load today's jobs
    jobs_file = Path(__file__).parent / "today_jobs.json"
    if not jobs_file.exists():
        print("No jobs file found. Run main.py first.")
        return

    with open(jobs_file) as f:
        jobs = json.load(f)

    job = next((j for j in jobs if str(j.get("id")) == str(job_id)), None)
    if not job:
        print(f"Job {job_id} not found.")
        return

    print(f"\nApplying to: {job['title']} @ {job['company']}")

    # Research company
    print("Researching company...")
    company_info = research_company(job["company"], job["title"])

    # Generate cover letter
    print("Generating cover letter...")
    extra = f"Company context: {company_info.get('description', '')}"
    letter = generate_cover_letter(job, extra_context=extra)
    print("\n--- COVER LETTER PREVIEW ---")
    print(letter)
    print("----------------------------\n")

    # Generate PDF
    print("Compiling PDF...")
    try:
        pdf_path = generate_pdf(
            cover_letter_text=letter,
            company_name=job["company"],
            job_title=job["title"],
            filename_hint=f"{job['company']}_{job['title']}"
        )
    except RuntimeError as e:
        print(f"PDF generation failed: {e}")
        pdf_path = None

    # Send email
    if not GMAIL_READY:
        print("\nGmail not configured yet. PDF and letter generated — send manually.")
        return

    to_email = input("Enter hiring manager email (or press Enter to skip): ").strip()
    if not to_email:
        print("No email provided. Application saved but not sent.")
        return

    result = send_email(
        to_email=to_email,
        to_name="Hiring Manager",
        company=job["company"],
        job_title=job["title"],
        cover_letter_text=letter,
        pdf_path=pdf_path,
        dry_run=dry_run,
    )
    mark_job_status(job_id, "applied")
    print(f"\nApplication status: {result['status']}")


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
