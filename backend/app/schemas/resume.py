from pydantic import BaseModel

class ResumeCreate(BaseModel):
    user_id: int
    skills: str
    projects: str
    experience: str

class ResumeResponse(BaseModel):
    id: int
    user_id: int
    skills: str
    projects: str
    experience: str
    version: int

    class Config:
        from_attributes = True