from fastapi import APIRouter
from pydantic import BaseModel
from app.services.skill_service import match_skills

router = APIRouter()


# -------------------------
# REQUEST MODEL
# -------------------------
class SkillRequest(BaseModel):
    skills: str
    job_description: str


# -------------------------
# ATS SCORE CALCULATION
# -------------------------
def calculate_ats_score(matched, missing):
    total = len(matched) + len(missing)

    if total == 0:
        return 0

    return int((len(matched) / total) * 100)


# -------------------------
# SUMMARY GENERATOR
# -------------------------
def generate_summary(score: int):

    if score >= 80:
        return "Excellent match! Your resume is highly aligned with the job role."
    elif score >= 60:
        return "Good match. Consider improving a few missing skills."
    elif score >= 40:
        return "Average match. You need to upskill in key areas."
    else:
        return "Low match. Significant skill gaps detected. Improve your profile."


# -------------------------
# MAIN ANALYSIS API
# -------------------------
@router.post("/skills")
def analyze_skills(data: SkillRequest):

    # 🔹 Get skill matching
    result = match_skills(
        data.skills,
        data.job_description
    )

    matched = result.get("matched_skills", [])
    missing = result.get("missing_skills", [])

    # 🔹 Calculate ATS Score
    score = calculate_ats_score(matched, missing)

    # 🔹 Final response
    return {
        "ats_score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "matched_count": len(matched),
        "missing_count": len(missing),
        "total_required_skills": len(matched) + len(missing),
        "summary": generate_summary(score)
    }