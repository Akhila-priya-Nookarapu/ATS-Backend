# FlowTrack ATS – Job Application Tracking System API

Backend project by **Akhila Priya Nookarapu** for an **Applicant Tracking System (ATS)** with:

- User roles (Candidate, Recruiter, Hiring Manager)
- Job posting and job applications
- Application workflow stages (Applied → Screening → Interview → Offer → Hired/Rejected)
- Application history tracking (who changed what and when)
- JWT-based authentication & basic Role-Based Access Control (RBAC)

> Repository: https://github.com/Akhila-priya-Nookarapu/ATS-Backend

---

## Architecture Overview

This project is a **FastAPI** backend using **SQLite + SQLAlchemy ORM**.

### Main Components

- **FastAPI app**: `app/main.py`
  - Mounts routers: `auth_router`, `jobs_router`, `applications_router`, `history_router` (if you have it)
  - Health endpoint: `GET /health`
- **Database layer**: `app/database.py`
  - Uses SQLite database: e.g. `ats.db`
  - `SessionLocal` and `Base` defined here
- **Models**: `app/models.py`
  - `User` – Candidate / Recruiter / Hiring Manager
  - `Company`
  - `Job`
  - `Application`
  - `ApplicationHistory`
- **Auth & Security**: `app/auth.py`
  - Password hashing with `passlib[bcrypt]`
  - JWT creation & verification with `python-jose`
  - `get_current_user` dependency
  - `require_role(...)` for RBAC
- **Routers**:
  - `app/routers/auth_router.py`
  - `app/routers/jobs_router.py`
  - `app/routers/applications_router.py`
  - `app/routers/history_router.py` (if you created one)
- **Services**:
  - `app/services/application_service.py` – contains logic for applying to jobs and updating stages

---

## Application Workflow

1. **Candidate registers and logs in**
   - `POST /auth/register`
   - `POST /auth/login` → returns `access_token`
2. **Recruiter creates a job**
   - `POST /jobs/` (recruiter only)
3. **Candidate applies to job**
   - `POST /applications/?job_id={job_id}`
4. **Recruiter reviews and updates stage**
   - `PATCH /applications/{application_id}/stage?new_stage=Screening`
   - Possible stages:
     - `Applied`
     - `Screening`
     - `Interview`
     - `Offer`
     - `Hired`
     - `Rejected`
5. **History is recorded**
   - Each change is stored in `ApplicationHistory`:
     - `old_stage`
     - `new_stage`
     - `changed_by_id`
     - `changed_at`
6. **History can be viewed**
   - Recruiter: `GET /history/application/{application_id}`
   - Candidate: `GET /history/me/{application_id}`

---

## State Transition Diagram (Workflow)

Valid state transitions (example):

```text
[Applied] ─> [Screening] ─> [Interview] ─> [Offer] ─> [Hired]
       └──────────────────────────────┐
        └───────────────────────────> [Rejected]
