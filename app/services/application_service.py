from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models import (
    Application,
    ApplicationHistory,
    ApplicationStage,
    Job,
    JobStatus,
    User,
)


class ApplicationService:

    @staticmethod
    def apply_to_job(db: Session, candidate: User, job_id: int) -> Application:
        # 1) Check job exists
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found",
            )

        # 2) Check job is open
        if job.status != JobStatus.OPEN:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Job is not open for applications.",
            )

        # 3) Check candidate hasn't already applied
        existing = (
            db.query(Application)
            .filter(
                Application.candidate_id == candidate.id,
                Application.job_id == job_id,
            )
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already applied to this job.",
            )

        # 4) Create application
        application = Application(
            candidate_id=candidate.id,
            job_id=job_id,
            stage=ApplicationStage.APPLIED,
        )
        db.add(application)
        db.flush()  # get application.id

        # 5) Create history record (no old_stage for first time)
        history = ApplicationHistory(
            application_id=application.id,
            old_stage=None,
            new_stage=ApplicationStage.APPLIED,
            changed_by_id=candidate.id,
        )
        db.add(history)

        # 6) Save
        db.commit()
        db.refresh(application)
        return application

    @staticmethod
    def update_stage(
        db: Session,
        recruiter: User,
        application_id: int,
        new_stage: ApplicationStage,
    ):
        # 1) Find application
        application = db.query(Application).filter(Application.id == application_id).first()
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found",
            )

        old_stage = application.stage

        # 2) Update stage
        application.stage = new_stage

        # 3) Add history record
        history = ApplicationHistory(
            application_id=application.id,
            old_stage=old_stage,
            new_stage=new_stage,
            changed_by_id=recruiter.id,
        )
        db.add(history)

        # 4) Save
        db.commit()
        db.refresh(application)

        # Can return application or empty dict (you used {})
        return {}
