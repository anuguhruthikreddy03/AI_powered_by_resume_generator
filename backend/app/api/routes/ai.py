from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# ✅ Import services
from app.services.groq_service import generate_ai_resume, groq_completion

router = APIRouter()   # ❗ NO prefix here


# -------------------------
# ✅ REQUEST MODELS
# -------------------------
class GenerateRequest(BaseModel):
    name: str = ""
    skills: str = ""
    projects: str = ""
    experience: str = ""
    education: str = ""
    certifications: str = ""
    achievements: str = ""
    job_description: str = ""
    template: str = "Professional"


class ImproveRequest(BaseModel):
    resume: str
    feedback: str


class SuggestRequest(BaseModel):
    resume: str


# -------------------------
# 🚀 GENERATE RESUME
# -------------------------
@router.post("/generate")
def generate_resume(data: GenerateRequest):
    try:
        resume = generate_ai_resume(data.dict())

        if not resume:
            raise HTTPException(status_code=500, detail="Empty resume generated")

        return {"resume": resume}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------
# ✨ IMPROVE RESUME (USER FEEDBACK)
# -------------------------
@router.post("/improve")
def improve_resume(data: ImproveRequest):
    try:
        prompt = f"""
Improve this resume based on feedback.

RESUME:
{data.resume}

FEEDBACK:
{data.feedback}

Return only improved resume.
"""

        result = groq_completion(prompt)

        return {"improved_resume": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------
# 🧠 AI SUGGESTIONS
# -------------------------
@router.post("/suggest")
def suggest_resume(data: SuggestRequest):
    try:
        prompt = f"""
You are a resume reviewer.

Analyze this resume and give:

1. Missing skills
2. Weak sections
3. ATS improvements
4. Better bullet points

Resume:
{data.resume}

ONLY bullet points.
"""

        result = groq_completion(prompt)

        return {"suggestions": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))