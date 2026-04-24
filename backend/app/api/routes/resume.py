from fastapi import APIRouter
from app.services.resume_service import save_resume, get_all_resumes

router = APIRouter()

@router.post("/save")
def save(data: dict):
    save_resume(data)
    return {"message": "Saved successfully"}

@router.get("/all")
def get_all():
    return get_all_resumes()