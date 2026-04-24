from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user

router = APIRouter()

@router.post("/", response_model=UserResponse)
def create_user_api(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)