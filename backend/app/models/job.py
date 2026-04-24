from sqlalchemy import Column, Integer, Text
from app.config.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text)