"""
pdf_generator.py
Takes a cover letter text and compiles it using Laurie's LaTeX template.
Outputs a polished PDF with her background, signature, and branding.
"""

import os
import re
import shutil
import subprocess
import tempfile
from datetime import date
from pathlib import Path

ASSETS_DIR = Path(__file__).parent / "assets"
TEX_TEMPLATE = ASSETS_DIR / "french_letter.tex"
BACKGROUND   = ASSETS_DIR / "CoverLetterBackground.pdf"
SIGNATURE    = ASSETS_DIR / "signeTeal.png"
OUTPUT_DIR   = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def _escape_latex(text: str) -> str:
    """Escape special LaTeX characters in plain text."""
    replacements = [
        ("\\", r"\textbackslash{}"),
        ("&",  r"\&"),
        ("%",  r"\%"),
        ("$",  r"\$"),
        ("#",  r"\#"),
        ("_",  r"\_"),
        ("{",  r"\{"),
        ("}",  r"\}"),
        ("~",  r"\textasciitilde{}"),
        ("^",  r"\textasciicircum{}"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def _format_body(cover_letter_text: str) -> str:
    """
    Convert plain text cover letter to LaTeX body.
    - Paragraphs separated by blank lines become \\n\\n in LaTeX
    - Lines starting with "- " or "• " become itemize items
    - URLs become \\href
    """
    lines = cover_letter_text.split("\n")
    latex_lines = []
    in_itemize = False

    for line in lines:
        stripped = line.strip()

        # Detect bullet points
        if stripped.startswith(("- ", "• ")):
            if not in_itemize:
                latex_lines.append(r"\begin{itemize}")
                in_itemize = True
            item = _escape_latex(stripped[2:])
            latex_lines.append(f"    \\item {item}")
            continue

        # Close itemize if we were in one
        if in_itemize and not stripped.startswith(("- ", "• ")):
            latex_lines.append(r"\end{itemize}")
            in_itemize = False

        # Empty line = paragraph break
        if not stripped:
            latex_lines.append("")
            continue

        # Skip the closing line (we handle it separately)
        if stripped.startswith(("Warm regards", "Chaleureusement", "Avec plaisir", "Respectfully")):
            continue

        # Skip "Laurie Lambot, PhD" at end (handled in closing)
        if stripped == "Laurie Lambot, PhD":
            continue

        latex_lines.append(_escape_latex(stripped))

    if in_itemize:
        latex_lines.append(r"\end{itemize}")

    return "\n\n".join(latex_lines)


def _detect_closing(cover_letter_text: str) -> str:
    """Extract the closing salutation from the letter."""
    for line in cover_letter_text.split("\n"):
        stripped = line.strip()
        for closing in ["Chaleureusement", "Avec plaisir", "Warm regards", "Respectfully", "Best regards"]:
            if stripped.startswith(closing):
                return closing + ","
    return "Warm regards,"


def _extract_address_block(cover_letter_text: str) -> tuple[str, str, str]:
    """
    Extract company name, address, and opening greeting from letter text.
    Returns (company_block, opening_line, body_start_index)
    """
    lines = cover_letter_text.strip().split("\n")

    # Find "Dear..." line
    opening_line = "Dear Hiring Manager,"
    body_lines = []
    company_lines = []
    found_dear = False

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.lower().startswith("dear"):
            opening_line = stripped
            body_lines = lines[i+1:]
            found_dear = True
        elif not found_dear and stripped and not stripped.startswith(("Boulder", "4 Tall", "May", "laurie")):
            company_lines.append(stripped)

    company_block = " \\\\\n".join(company_lines[:4]) if company_lines else "Hiring Manager \\\\\nRemote Position"
    body = "\n".join(body_lines)
    return company_block, opening_line, body


def generate_pdf(
    cover_letter_text: str,
    company_name: str,
    job_title: str,
    filename_hint: str = "cover_letter"
) -> Path:
    """
    Compile a PDF cover letter using Laurie's LaTeX template.
    Returns the path to the generated PDF.
    """

    # Check for pdflatex
    if not shutil.which("pdflatex"):
        raise RuntimeError(
            "pdflatex is not installed. Install texlive:\n"
            "  sudo apt-get install texlive-latex-base texlive-fonts-recommended\n"
            "  or: brew install --cask mactex"
        )

    # Parse the letter
    company_block, opening_line, body_text = _extract_address_block(cover_letter_text)
    body_latex  = _format_body(body_text)
    closing     = _detect_closing(cover_letter_text)
    today_str   = date.today().strftime("%B %d, %Y")

    # Read template
    template = TEX_TEMPLATE.read_text(encoding="utf-8")

    # Replace dynamic fields
    template = template.replace(
        "December 9th, 2025", today_str
    ).replace(
        r"""Hiring Manager \\
Intertwine Associates LLC \\
Remote Position""",
        company_block
    ).replace(
        r"\opening{\vspace{12mm}Dear Hiring Manager,}",
        f"\\opening{{\\vspace{{12mm}}{opening_line}}}"
    )

    # Replace body: everything between \opening{...} and \closing{...}
    body_placeholder_start = template.find(r"\vspace{5mm}I am writing")
    body_placeholder_end   = template.find(r"\closing{")

    if body_placeholder_start != -1 and body_placeholder_end != -1:
        template = (
            template[:body_placeholder_start] +
            f"\n\\vspace{{5mm}}{body_latex}\n\n" +
            template[body_placeholder_end:]
        )

    # Replace closing
    template = template.replace(
        r"\hspace*{-30mm}Respectfully,",
        f"\\hspace*{{-30mm}}{closing}"
    )

    # Compile in a temp directory with assets
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Copy assets to temp dir (pdflatex needs them local)
        shutil.copy(BACKGROUND, tmpdir / "CoverLetterBackground.pdf")
        shutil.copy(SIGNATURE,  tmpdir / "signeTeal.png")

        # Write the .tex file
        tex_file = tmpdir / "cover_letter.tex"
        tex_file.write_text(template, encoding="utf-8")

        # Run pdflatex (twice for proper layout)
        for _ in range(2):
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "cover_letter.tex"],
                cwd=tmpdir,
                capture_output=True,
                text=True
            )

        pdf_tmp = tmpdir / "cover_letter.pdf"
        if not pdf_tmp.exists():
            error_log = (tmpdir / "cover_letter.log").read_text() if (tmpdir / "cover_letter.log").exists() else result.stderr
            raise RuntimeError(f"pdflatex failed. Log:\n{error_log[-2000:]}")

        # Save to output directory
        safe_name = re.sub(r'[^\w\-]', '_', filename_hint.lower())[:40]
        out_path = OUTPUT_DIR / f"{safe_name}_{date.today().isoformat()}.pdf"
        shutil.copy(pdf_tmp, out_path)

    print(f"  PDF generated: {out_path}")
    return out_path


if __name__ == "__main__":
    # Quick test with a sample letter
    sample_letter = """
Aifred Health
1000 De La Gauchetière West
Montreal, QC H3B 4W5

Dear Dr. Tremblay,

With a PhD in Neuroscience from ULB and 15 years of research experience, I am writing to express my strong interest in the Senior Research Scientist role at Aifred Health.

My background in computational neuroscience and translational research maps directly onto what you are building. At the University of Chicago, I designed imaging platforms capturing the activity of 400+ neurons simultaneously, integrating machine learning pipelines for real-time analysis (lambot.co/project/chapter2/). That work required the same kind of methodological rigor and clinical relevance that your AI-guided treatment platform demands.

What you may not find in many applicants is the clinical layer I bring. As a volunteer medic-firefighter and EMT working in an emergency department, I see patients. That shapes how I think about therapeutic endpoints in ways that pure bench science does not.

I am a native French speaker planning a relocation to Quebec, which makes Aifred not just an employer but a natural next step in my life.

Chaleureusement,

Laurie Lambot, PhD
"""
    pdf = generate_pdf(sample_letter, "Aifred Health", "Senior Research Scientist", "aifred_health")
    print(f"Test PDF: {pdf}")
