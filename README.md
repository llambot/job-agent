# Laurie's Job Agent

A personal AI-powered job search agent that finds, ranks, and applies to science jobs every morning.

## What it does

1. Scrapes LinkedIn, Indeed, and Google Jobs daily
2. Claude ranks each job against your PhD profile (0-100 score)
3. You select which jobs to pursue via the mobile app
4. Claude writes a cover letter in your voice using your LaTeX template
5. Emails the application via your Gmail account

---

## Setup (one time)

### 1. Clone and install

```bash
git clone https://github.com/YOUR_USERNAME/job-agent.git
cd job-agent
pip install -r requirements.txt
```

### 2. Install LaTeX (for PDF generation)

```bash
# macOS
brew install --cask mactex

# Ubuntu / GitHub Actions
sudo apt-get install texlive texlive-latex-extra texlive-fonts-recommended
```

### 3. Set your Anthropic API key

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

Or add it to a `.env` file:
```
ANTHROPIC_API_KEY=sk-ant-...
```

### 4. Set up Gmail API (one time)

1. Go to https://console.cloud.google.com/
2. Create a new project → Enable Gmail API
3. APIs & Services > Credentials > Create OAuth 2.0 Client ID (Desktop app)
4. Download JSON → save as `credentials.json` in this folder
5. Run once to authenticate:
   ```bash
   python gmail_sender.py
   ```
   This opens a browser, you log in, and `token.pickle` is saved.

### 5. Run manually

```bash
python main.py                  # full daily run
python main.py --test           # dry run, no emails
python main.py --rank-only      # scrape + rank only
python main.py --cover JOB_ID   # apply to specific job
```

### 6. Schedule via GitHub Actions (free, runs while laptop is off)

1. Push this folder to a private GitHub repo
2. Add your `ANTHROPIC_API_KEY` as a repo secret:
   Settings > Secrets > Actions > New secret
3. Add Gmail token as a secret:
   ```bash
   base64 token.pickle | pbcopy   # macOS
   ```
   Paste as `GMAIL_TOKEN_B64` secret
4. The workflow in `.github/workflows/daily_agent.yml` runs at 7 AM MT daily

---

## File structure

```
job_agent/
├── main.py              # Daily orchestrator
├── profile.py           # YOUR PROFILE — edit this
├── job_scraper.py       # LinkedIn + Indeed + Google Jobs
├── claude_engine.py     # Ranking + cover letter generation
├── pdf_generator.py     # LaTeX PDF compiler
├── gmail_sender.py      # Gmail API sender
├── requirements.txt
├── jobs.db              # SQLite database (auto-created)
├── today_jobs.json      # Today's ranked jobs (for the app)
├── assets/
│   ├── french_letter.tex
│   ├── CoverLetterBackground.pdf
│   └── signeTeal.png
├── output/              # Generated PDFs
└── .github/
    └── workflows/
        └── daily_agent.yml
```

---

## Updating your profile

Edit `profile.py` — this is the single source of truth Claude uses for everything.
Any change here automatically applies to all future rankings and cover letters.

---

## Calendar integration (Phase 5)

When you get interview requests, the agent will:
- Parse the email for date/time
- Add it to a dedicated Google Calendar ("Job Interviews")
- Create a prep session the evening before
- Generate a briefing note about the company and role

---

## Cost estimate

| Component | Cost |
|---|---|
| Job scraping (jobspy) | Free |
| Claude API (ranking 50 jobs/day + 5 cover letters/week) | ~$0.30/month |
| GitHub Actions | Free |
| Gmail API | Free |
| **Total** | **~$0.30/month** |
