from groq import Groq
import os
from dotenv import load_dotenv
from pathlib import Path
import json
import re

# -------------------------
# LOAD ENV
# -------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None


# -------------------------
# CLEAN TEXT
# -------------------------
def clean(text):
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    text = text.replace("**", "")
    return text.strip()


# -------------------------
# SAFE JSON PARSE
# -------------------------
def safe_json(text):
    try:
        return json.loads(text)
    except:
        # extract JSON from messy output
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                return []
        return []


# -------------------------
# EXTRACT SKILLS (LLM)
# -------------------------
def extract_skills(text):

    # fallback if no API key
    if not client:
        return set()

    prompt = f"""
Extract ONLY technical skills.

STRICT RULES:
- Output JSON list ONLY
- No explanation
- No sentences
- Normalize (ML → Machine Learning)

Example:
["python", "machine learning", "numpy"]

TEXT:
{text}
"""

    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="qwen/qwen3-32b"
        )

        result = clean(response.choices[0].message.content)
        skills = safe_json(result)

        return set([s.lower().strip() for s in skills if s])

    except Exception:
        return set()


# -------------------------
# MATCH SKILLS (OPTIMIZED)
# -------------------------
def match_skills(user_skills, job_description):

    # 🔥 Only LLM for JD (important optimization)
    jd = extract_skills(job_description)

    # 🔥 User skills → simple clean (fast)
    user = set([s.strip().lower() for s in user_skills.split(",") if s.strip()])

    # synonym normalization
    SYNONYMS = {
        "ml": "machine learning",
        "dl": "deep learning",
        "ai": "artificial intelligence"
    }

    expanded_user = set()

    for s in user:
        expanded_user.add(s)
        if s in SYNONYMS:
            expanded_user.add(SYNONYMS[s])

    matched = expanded_user & jd
    missing = jd - expanded_user

    return {
        "matched_skills": sorted(list(matched)),
        "missing_skills": sorted(list(missing))
    }