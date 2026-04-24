from sqlalchemy.orm import Session
from app.models.job import Job
from app.services.ai_service import call_llm
import re


# -------------------------
# DB FUNCTION (KEEP THIS)
# -------------------------
def create_job(db: Session, job_data):
    job = Job(**job_data.dict())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


# -------------------------
# 🔥 AI FUNCTION (IMPROVED)
# -------------------------
def extract_skills_from_jd(jd_text: str):

    prompt = f"""
You are an AI system.

Extract ONLY technical skills from the job description.

STRICT RULES:
- Return only Python list
- No explanation
- No sentences

JD:
{jd_text}
"""

    response = call_llm(prompt)

    try:
        # safer than raw eval
        skills = eval(response)
    except:
        # fallback extraction (if AI breaks format)
        skills = re.findall(r'\b[A-Za-z]+\b', response)

    return list(set(skills))