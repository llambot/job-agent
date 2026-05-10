"""
claude_engine.py
Uses the Anthropic API to:
1. Rank jobs against Laurie's profile (score 0-100 + summary)
2. Generate cover letters in Laurie's voice using her LaTeX template
"""

import os
import re
import json
import anthropic
from profile import PROFILE_SUMMARY, PROFILE

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
MODEL  = "claude-sonnet-4-6"


# ─────────────────────────────────────────────────────────────────────────────
# JOB RANKING
# ─────────────────────────────────────────────────────────────────────────────

RANKING_SYSTEM = """
You are a job-matching assistant for Laurie Lambot, PhD.
You rank job postings on a 0-100 fit score against her profile.
You are ruthlessly honest — only high-scoring jobs are worth her time.

Scoring criteria:
- Uses her PhD (neuroscience, biomedical, research): up to 40 pts
- Salary meets or exceeds $90k USD equivalent: up to 15 pts
- Remote or Colorado in-person: up to 10 pts
- Canadian employer (especially Quebec): up to 15 pts
- Intellectual challenge / pride-worthy work: up to 10 pts
- Her clinical/EMT background adds value: up to 10 pts (bonus)
- Well paid non-neuro role she would excel at (medical device, CAD, science writting, policy, BD): score normally, no cap, mark as surprise, mark emoji as 🤡

Automatic score cap at 40 if the role does not require or value a PhD.
Automatic 0 if the role is clearly below $60k or purely administrative.

Respond ONLY in this exact JSON format (no markdown, no preamble):
{
  "score": <integer 0-100>,
  "match_label": "<one of: Perfect fit | Strong match | Good fit | Weak match | Not suitable>",
  "why": "<2-3 sentences explaining the score in plain language>",
  "canada_flag": <true|false>,
  "remote": <true|false>,
  "estimated_salary": "<salary range from posting or 'Not specified'>",
  "emoji": "<✨ if score>=70, 🍁 if Canadian, 🤡 if well-paid non-neuro surprise role, combine if needed, empty string otherwise>"
}
"""

def rank_job(job: dict) -> dict:
    """Score a job posting. Returns dict with score, label, why, flags."""
    title    = job.get("title", "")
    company  = job.get("company", "")
    location = job.get("location", "")
    desc = str(job.get("description", "") or "").encode('ascii', 'ignore').decode()[:3000]

    prompt = f"""
Here is Laurie's profile:
{PROFILE_SUMMARY}

Here is the job posting:
Title: {title}
Company: {company}
Location: {location}
Description:
{desc}

Score this job for Laurie.
"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=400,
        system=RANKING_SYSTEM,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Fallback if Claude adds extra text
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            return json.loads(match.group())
        return {"score": 0, "match_label": "Error", "why": raw, "canada_flag": False, "remote": False, "estimated_salary": "N/A"}


def rank_all_jobs(jobs: list[dict]) -> list[dict]:
    """Rank a list of jobs and return sorted by score descending."""
    results = []
    for job in jobs:
        print(f"  Ranking: {job.get('title')} @ {job.get('company')} ...")
        ranking = rank_job(job)
        job["claude_score"]   = ranking.get("score", 0)
        job["claude_summary"] = ranking.get("why", "")
        job["match_label"]    = ranking.get("match_label", "")
        job["canada_flag"]    = ranking.get("canada_flag", False)
        job["remote"]         = ranking.get("remote", False)
        job["est_salary"]     = ranking.get("estimated_salary", "N/A")
        results.append(job)

    results.sort(key=lambda x: x["claude_score"], reverse=True)
    return results[:15]  # top 15 only


# ─────────────────────────────────────────────────────────────────────────────
# COVER LETTER GENERATION
# ─────────────────────────────────────────────────────────────────────────────

COVER_LETTER_SYSTEM = f"""
You are writing a cover letter AS Laurie Lambot, PhD.
You know her deeply — her research, her voice, her values.

ABSOLUTE RULES (never break these):
1. Never use em dashes ( — ) anywhere. Use commas or periods instead.
2. Always include lambot.co naturally somewhere in the letter.
3. Sign off: Warm regards,\\n\\nLaurie Lambot, PhD
   (For Canadian/French companies use: Chaleureusement, or Avec plaisir,)
4. Lead with the PhD for science jobs. Use the EMT/firefighter background as a memorable, human twist.
   Use "volunteer medic-firefighter" if it fits naturally. Never force it.
5. Write in prose. No bullet points in the body. If including an "I offer:" list, use it sparingly.
6. Sound like a thoughtful European scientist, not an American corporate applicant.
7. Be direct and confident. No groveling, no excessive enthusiasm.
8. Reference specific website projects (lambot.co/project/...) when genuinely relevant.
9. Maximum 400 words for the body. Tight, focused, no filler.
10. Do NOT start sentences with "I" more than twice in a row.

Her profile for reference:
{PROFILE_SUMMARY}

Her key projects (use URLs when relevant):
- Chapter 2 (multimodal recording platform, 400+ neurons): lambot.co/project/chapter2/
- Chapter 5 (Modendo, deep brain imaging, investor pitch): lambot.co/project/chapter5/
- HAT (cranial implant design): lambot.co/project/hat/
- Alzheimer's model (Neuron 2017): human iPSC neurons in mouse brain

Testimonials to reference if very relevant:
- Jason MacLean (UChicago): "The breadth of her work is highly unusual and demonstrates a tremendous intellect."
- Tim Morrissey (Drive Capital): "Laurie is not just a scientist; she's a leader who understands how to translate innovative research into commercially viable products."
"""

def generate_cover_letter(job: dict, extra_context: str = "") -> str:
    """Generate a cover letter for a specific job. Returns plain text."""
    title    = job.get("title", "")
    company  = job.get("company", "")
    location = job.get("location", "")
    desc     = (job.get("description", "") or "")[:3000]
    is_canada = job.get("is_canadian") or job.get("canada_flag", False)
    canada_note = "\nThis is a Canadian company. Use a French closing if appropriate (Chaleureusement or Avec plaisir)." if is_canada else ""

    prompt = f"""
Write a cover letter for Laurie applying to:

Title: {title}
Company: {company}
Location: {location}
Job description:
{desc}
{canada_note}
{extra_context}

Start with the city and date on the first line, then the company address block, then the opening.
The tone should feel like Laurie wrote it herself on a good day: precise, warm, honest, European.
"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=1200,
        system=COVER_LETTER_SYSTEM,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text.strip()


def refine_cover_letter(original: str, instruction: str) -> str:
    """Refine an existing cover letter based on Laurie's feedback."""
    prompt = f"""
Here is the current cover letter:
---
{original}
---

Laurie's instruction: {instruction}

Rewrite the cover letter applying this change while keeping all style rules.
Return only the full rewritten letter.
"""
    response = client.messages.create(
        model=MODEL,
        max_tokens=1200,
        system=COVER_LETTER_SYSTEM,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text.strip()


# ─────────────────────────────────────────────────────────────────────────────
# COMPANY RESEARCH
# ─────────────────────────────────────────────────────────────────────────────

def research_company(company_name: str, job_title: str) -> dict:
    """
    Research a company using Claude's web search tool.
    Returns dict with: description, recent_news, recent_pubs, why_laurie
    """
    prompt = f"""
Research the company "{company_name}" for a job application by Laurie Lambot, PhD.
She is applying for: {job_title}

Find and return:
1. A 2-3 sentence company description (what they do, where, stage)
2. 2-3 recent news items (last 6 months) with title and date
3. 2 recent publications or research projects if it's a science company
4. 3 specific reasons why Laurie's background is a strong match

Return ONLY this JSON:
{{
  "description": "...",
  "founded": "...",
  "size": "...",
  "funding": "...",
  "hq": "...",
  "news": [
    {{"title": "...", "date": "...", "source": "..."}},
    {{"title": "...", "date": "...", "source": "..."}}
  ],
  "publications": [
    {{"journal": "...", "title": "...", "date": "..."}}
  ],
  "why_laurie": [
    "...",
    "...",
    "..."
  ]
}}
"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract text from response (may include tool use blocks)
    text = ""
    for block in response.content:
        if hasattr(block, "text"):
            text += block.text

    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception:
        pass

    return {
        "description": f"{company_name} is a research-focused organization.",
        "founded": "N/A", "size": "N/A", "funding": "N/A", "hq": "N/A",
        "news": [], "publications": [],
        "why_laurie": ["Strong PhD match", "Remote-friendly", "Research focus"]
    }


if __name__ == "__main__":
    # Quick test
    test_job = {
        "title": "Senior Research Scientist — Computational Neuroscience",
        "company": "Aifred Health",
        "location": "Montreal, QC — Remote",
        "description": "We are looking for a senior neuroscientist with a PhD and 10+ years experience to lead our clinical research team developing AI tools for depression treatment.",
        "is_canadian": True,
    }
    print("Testing ranking...")
    result = rank_job(test_job)
    print(json.dumps(result, indent=2))

    print("\nTesting cover letter...")
    letter = generate_cover_letter(test_job)
    print(letter[:500])
