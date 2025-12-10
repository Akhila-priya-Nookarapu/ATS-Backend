from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Job, UserRole
from ..schemas import JobCreate, JobOut
from ..auth import require_role, get_current_user
from ..models import User

router = APIRouter(prefix="/jobs", tags=["Jobs"])


# -----------------------------
# CREATE JOB (Recruiter only)
# -----------------------------

@router.post("/", response_model=JobOut)
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.RECRUITER))
):
    new_job = Job(
        title=job.title,
        description=job.description,
        company_id=job.company_id,
        created_by_id=current_user.id
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job


# -----------------------------
# GET ALL JOBS (Public)
# -----------------------------

@router.get("/", response_model=list[JobOut])
def list_jobs(db: Session = Depends(get_db)):
    return db.query(Job).all()


# -----------------------------
# UPDATE JOB (Recruiter only)
# -----------------------------

@router.put("/{job_id}", response_model=JobOut)
def update_job(
    job_id: int,
    updated: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.RECRUITER))
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(404, "Job not found")

    if job.created_by_id != current_user.id:
        raise HTTPException(403, "You cannot edit a job you did not create")

    job.title = updated.title
    job.description = updated.description
    job.company_id = updated.company_id

    db.commit()
    db.refresh(job)
    return job


# -----------------------------
# DELETE JOB (Recruiter only)
# -----------------------------

@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.RECRUITER))
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(404, "Job not found")

    if job.created_by_id != current_user.id:
        raise HTTPException(403, "You cannot delete another recruiter's job")

    db.delete(job)
    db.commit()
    return {"message": "Job deleted"}
