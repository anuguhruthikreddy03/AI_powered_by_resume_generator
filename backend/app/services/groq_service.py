from groq import Groq
import os
from dotenv import load_dotenv
from pathlib import Path
import re

# -------------------------
# IMPORT SKILL MATCHING
# -------------------------
from app.services.skill_service import match_skills

# -------------------------
# LOAD ENV
# -------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# -------------------------
# GENERIC LLM FUNCTION
# -------------------------
def groq_completion(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="qwen/qwen3-32b"
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"ERROR: {str(e)}"


# -------------------------
# CLEAN FIELD
# -------------------------
def clean_field(value):
    if not value:
        return ""
    return str(value).strip()


# -------------------------
# MAIN RESUME GENERATOR
# -------------------------
def generate_ai_resume(data: dict):

    # -------------------------
    # CLEAN INPUT DATA
    # -------------------------
    name = clean_field(data.get("name"))
    skills = clean_field(data.get("skills"))
    projects = clean_field(data.get("projects"))
    experience = clean_field(data.get("experience"))
    education = clean_field(data.get("education"))
    certifications = clean_field(data.get("certifications"))
    achievements = clean_field(data.get("achievements"))
    job_description = clean_field(data.get("job_description"))

    template = data.get("template", "Professional")

    # -------------------------
    # TEMPLATE STYLE
    # -------------------------
    TEMPLATE_STYLE = {
        "Professional": "formal corporate resume with structured sections",
        "Modern": "clean modern resume with bullet points",
        "Minimal": "simple concise resume"
    }

    style = TEMPLATE_STYLE.get(template, "professional resume")

    # -------------------------
    # SKILL MATCHING
    # -------------------------
    result = match_skills(skills, job_description)

    matched = ", ".join(result.get("matched_skills", []))
    missing = ", ".join(result.get("missing_skills", []))

    # -------------------------
    # PROMPT
    # -------------------------
    prompt = f"""
You are an expert ATS resume writer.

Generate a HIGHLY PROFESSIONAL resume.

STRICT RULES:
- Output ONLY final resume
- No explanation
- No thinking text
- No markdown symbols (**)

STYLE:
{style}

OPTIMIZATION:
- Highlight matched skills: {matched}
- Try to include missing skills if relevant: {missing}

FORMAT:
PROFESSIONAL SUMMARY
SKILLS
EXPERIENCE
PROJECTS
EDUCATION
CERTIFICATIONS
ACHIEVEMENTS

DATA:
Name: {name}
Skills: {skills}
Projects: {projects}
Experience: {experience}
Education: {education}
Certifications: {certifications}
Achievements: {achievements}
"""

    try:
        # -------------------------
        # USE GENERIC FUNCTION
        # -------------------------
        text = groq_completion(prompt)

        # -------------------------
        # CLEAN OUTPUT
        # -------------------------
        text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
        text = text.replace("**", "")
        text = text.replace("\\n", "\n")

        return text.strip()

    except Exception as e:
        print("🔥 GROQ ERROR:", str(e))

        # -------------------------
        # FALLBACK RESPONSE
        # -------------------------
        return f"""
PROFESSIONAL SUMMARY:
Motivated candidate with skills in {skills}.

SKILLS:
{skills}

EXPERIENCE:
{experience or "Not Provided"}

PROJECTS:
{projects or "Not Provided"}

EDUCATION:
{education or "Not Provided"}

CERTIFICATIONS:
{certifications or "Not Provided"}

ACHIEVEMENTS:
{achievements or "Not Provided"}
"""