from fastapi import FastAPI
from .database import Base, engine
from .routers import auth_router, jobs_router, applications_router
from .routers.application_history_router import router as history_router

app = FastAPI(title="ATS Backend System")

Base.metadata.create_all(bind=engine)

# Routers
app.include_router(auth_router.router)
app.include_router(jobs_router.router)
app.include_router(applications_router.router)
app.include_router(history_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
