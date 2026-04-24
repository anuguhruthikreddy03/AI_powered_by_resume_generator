from fastapi import FastAPI
from app.api.routes import ai, analysis, resume

app = FastAPI()

app.include_router(ai.router, prefix="/ai", tags=["AI"])
app.include_router(analysis.router, prefix="/analysis")
app.include_router(resume.router, prefix="/resume")