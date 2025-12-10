from pydantic import BaseModel, EmailStr
from typing import Optional
from .models import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: UserRole
    company_id: Optional[int] = None


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: UserRole
    company_id: Optional[int]

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


from typing import Optional
from .models import JobStatus


class JobCreate(BaseModel):
    title: str
    description: Optional[str] = None
    company_id: int


class JobOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: JobStatus
    company_id: int
    created_by_id: int

    class Config:
        from_attributes = True


from datetime import datetime
from .models import ApplicationStage

class ApplicationOut(BaseModel):
    id: int
    candidate_id: int
    job_id: int
    stage: ApplicationStage
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
class ApplicationStageUpdate(BaseModel):
    new_stage: ApplicationStage