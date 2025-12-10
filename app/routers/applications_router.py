from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth import get_current_user, require_role
from ..models import UserRole, ApplicationStage, Job, Application
from ..services.application_service import ApplicationService
from ..schemas import ApplicationOut

router = APIRouter(prefix="/applications", tags=["Applications"])


# -----------------------------
# CANDIDATE APPLIES TO A JOB
# -----------------------------
@router.post("/", response_model=ApplicationOut)
def apply_to_job(
    job_id: int,
    db: Session = Depends(get_db),
    candidate = Depends(require_role(UserRole.CANDIDATE))
):
    return ApplicationService.apply_to_job(db, candidate, job_id)



# -----------------------------
# RECRUITER UPDATES APPLICATION STAGE
# -----------------------------
@router.patch("/{application_id}/stage")
def change_stage(
    application_id: int,
    new_stage: ApplicationStage = Query(..., description="New stage for the application"),
    db: Session = Depends(get_db),
    recruiter = Depends(require_role(UserRole.RECRUITER)),
):
    return ApplicationService.update_stage(db, recruiter, application_id, new_stage)



# -----------------------------
# VIEW APPLICATIONS FOR A JOB (Recruiter only)
# -----------------------------
@router.get("/job/{job_id}", response_model=list[ApplicationOut])
def list_applications_for_job(
    job_id: int,
    db: Session = Depends(get_db),
    recruiter = Depends(require_role(UserRole.RECRUITER))
):
    # 1. Check job exists
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # 2. Check job belongs to this recruiter
    if job.created_by_id != recruiter.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # 3. Return applications for this job only
    return db.query(Application).filter(Application.job_id == job_id).all()



# -----------------------------
# VIEW CANDIDATE'S OWN APPLICATIONS
# -----------------------------
@router.get("/me", response_model=list[ApplicationOut])
def list_my_applications(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return db.query(Application).filter(Application.candidate_id == user.id).all()


# -----------------------------
# GET ALL APPLICATIONS FOR RECRUITER WITH CANDIDATE DETAILS
# -----------------------------
@router.get("/recruiter/all")
def get_all_applications_for_recruiter(
    db: Session = Depends(get_db),
    recruiter = Depends(require_role(UserRole.RECRUITER))
):
    from ..models import Application, Job, User

    # Get jobs created by this recruiter
    jobs = db.query(Job).filter(Job.created_by_id == recruiter.id).all()
    job_ids = [job.id for job in jobs]

    if not job_ids:
        return []

    # Get applications for these jobs
    applications = (
        db.query(Application, User, Job)
        .join(User, Application.candidate_id == User.id)
        .join(Job, Application.job_id == Job.id)
        .filter(Application.job_id.in_(job_ids))
        .all()
    )

    result = []
    for app, user, job in applications:
        result.append({
            "application_id": app.id,
            "job_id": job.id,
            "job_title": job.title,
            "candidate_id": user.id,
            "candidate_name": user.full_name,
            "candidate_email": user.email,
            "stage": app.stage.value,
            "created_at": app.created_at,
            "updated_at": app.updated_at
        })

    return result
