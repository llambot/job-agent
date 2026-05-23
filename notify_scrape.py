import json, smtplib, os
from email.mime.text import MIMEText
from datetime import date

jobs = json.load(open('today_jobs.json'))
password = os.environ.get('GMAIL_APP_PASSWORD', '')

lines = [f"🔍 Job Scraping Complete — {date.today()}", f"{len(jobs)} jobs found:\n"]
for i, j in enumerate(jobs, 1):
    title = j.get('title', '?')[:50]
    company = j.get('company', '?')[:30]
    loc = j.get('location', '?')[:30]
    salary = j.get('est_salary') or j.get('salary_range') or 'Not specified'
    posted = j.get('date_posted', '?')
    remote = '🌐' if j.get('is_remote') or j.get('remote') else '📍'
    canada = '🍁' if j.get('canada_flag') or 'canada' in str(loc).lower() else ''
    lines.append(f"{i}. {title} {canada}@ {company}")
    lines.append(f"   {remote} {loc} | 💰 {salary} | 📅 {posted}\n")
lines.append("jobs.lambot.co — enrichment at 6:20 AM MDT")

body = '\n'.join(lines)
msg = MIMEText(body)
msg['Subject'] = f"🔍 {len(jobs)} jobs scraped — {date.today()}"
msg['From'] = 'laurie@lambot.co'
msg['To'] = 'laurie@lambot.co'

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
        s.login('laurie@lambot.co', password)
        s.send_message(msg)
    print('Email sent!')
except Exception as e:
    print(f'Email failed: {e}')
