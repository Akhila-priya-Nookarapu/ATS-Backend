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

import redis
import json

# -----------------------------
# CONNECT TO REDIS MESSAGE QUEUE
# -----------------------------
redis_client = redis.StrictRedis(host="127.0.0.1", port=6379, db=0)


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

        # 5) Create history record
        history = ApplicationHistory(
            application_id=application.id,
            old_stage=None,
            new_stage=ApplicationStage.APPLIED,
            changed_by_id=candidate.id,
        )
        db.add(history)

        db.commit()
        db.refresh(application)

        # -----------------------------
        # 6) PUSH EMAIL TASK TO REDIS
        # -----------------------------
        task = {
            "email": candidate.email,
            "subject": "Application Received",
            "message": f"Your application for Job ID {job_id} has been received."
        }
        redis_client.lpush("email_queue", json.dumps(task))

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
        application.stage = new_stage

        # 2) Save history
        history = ApplicationHistory(
            application_id=application.id,
            old_stage=old_stage,
            new_stage=new_stage,
            changed_by_id=recruiter.id,
        )
        db.add(history)
        db.commit()
        db.refresh(application)

        # -----------------------------
        # 3) SEND EMAIL NOTIFICATION
        # -----------------------------
        task = {
            "email": f"candidate-{application.candidate_id}@example.com",
            "subject": "Application Status Updated",
            "message": f"Your application stage changed from {old_stage} to {new_stage}."
        }

        redis_client.lpush("email_queue", json.dumps(task))

        return {}
