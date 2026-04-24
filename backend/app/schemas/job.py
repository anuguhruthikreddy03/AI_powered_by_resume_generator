from pydantic import BaseModel

class JobCreate(BaseModel):
    description: str

class JobResponse(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True