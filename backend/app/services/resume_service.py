from app.database import SessionLocal
from app.models.resume import Resume
from app.services.groq_service import generate_ai_resume


# -------------------------
# CLEAN FIELD
# -------------------------
def clean_field(value):
    if not value:
        return ""
    return str(value).strip()


# -------------------------
# GENERATE BASIC RESUME (fallback)
# -------------------------
def generate_resume(data: dict):

    name = clean_field(data.get("name"))
    skills = clean_field(data.get("skills"))
    projects = clean_field(data.get("projects"))
    experience = clean_field(data.get("experience"))
    education = clean_field(data.get("education"))
    certifications = clean_field(data.get("certifications"))
    achievements = clean_field(data.get("achievements"))

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
""".strip()


# -------------------------
# AI RESUME GENERATION
# -------------------------
def generate_ai_resume_service(data: dict):
    try:
        return generate_ai_resume(data)
    except Exception as e:
        print("🔥 AI ERROR:", str(e))
        return generate_resume(data)  # fallback


# -------------------------
# SAVE RESUME
# -------------------------
def save_resume(data: dict):
    db = SessionLocal()

    try:
        new_resume = Resume(
            content=data.get("content", ""),
            template=data.get("template", "Professional")
        )

        db.add(new_resume)
        db.commit()

    except Exception as e:
        db.rollback()
        print("🔥 ERROR SAVING RESUME:", str(e))

    finally:
        db.close()


# -------------------------
# GET ALL RESUMES
# -------------------------
def get_all_resumes():
    db = SessionLocal()

    try:
        resumes = db.query(Resume).all()

        result = []

        for r in resumes:
            result.append({
                "id": r.id,
                "content": r.content,
                "template": r.template
            })

        return result

    except Exception as e:
        print("🔥 ERROR FETCHING RESUMES:", str(e))
        return []

    finally:
        db.close()


# -------------------------
# DELETE RESUME
# -------------------------
def delete_resume(resume_id: int):
    db = SessionLocal()

    try:
        resume = db.query(Resume).filter(Resume.id == resume_id).first()

        if resume:
            db.delete(resume)
            db.commit()

        return {"message": "Deleted successfully"}

    except Exception as e:
        db.rollback()
        return {"error": str(e)}

    finally:
        db.close()