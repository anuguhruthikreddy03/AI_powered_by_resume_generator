from sqlalchemy import Column, Integer, Text, String
from app.database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    template = Column(String, default="Professional")