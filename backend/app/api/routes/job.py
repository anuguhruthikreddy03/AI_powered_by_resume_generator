from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.job import JobCreate, JobResponse
from app.services.job_service import create_job

router = APIRouter()

@router.post("/", response_model=JobResponse)
def create_job_api(job: JobCreate, db: Session = Depends(get_db)):
    return create_job(db, job)