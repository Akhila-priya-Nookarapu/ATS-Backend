from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth import get_current_user, require_role
from ..models import UserRole, ApplicationHistory

router = APIRouter(prefix="/history", tags=["Application History"])


# -----------------------------
# VIEW HISTORY FOR ONE APPLICATION
# -----------------------------
@router.get("/application/{application_id}")
def get_history_for_application(
    application_id: int,
    db: Session = Depends(get_db),
    recruiter = Depends(require_role(UserRole.RECRUITER))
):
    history = db.query(ApplicationHistory).filter(
        ApplicationHistory.application_id == application_id
    ).all()

    return history


# -----------------------------
# CANDIDATE VIEW OWN APPLICATION HISTORY
# -----------------------------
@router.get("/me/{application_id}")
def get_my_history(
    application_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    history = db.query(ApplicationHistory).filter(
        ApplicationHistory.application_id == application_id
    ).all()

    # SECURITY CHECK
    if not history:
        return []

    # Ensure candidate owns this application
    app_user_id = history[0].application.candidate_id

    if app_user_id != user.id:
        return {"detail": "Not your application"}

    return history
