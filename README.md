FlowTrack ATS – Job Application Tracking System API

Backend project by Akhila Priya Nookarapu for a modern Applicant Tracking System (ATS) supporting:

User roles: Candidate, Recruiter, Hiring Manager

Job postings & job applications

Multi-stage application workflow
(Applied → Screening → Interview → Offer → Hired/Rejected)

Full application history tracking (who changed what and when)

JWT authentication + Role-Based Access Control (RBAC)

Repository: https://github.com/Akhila-priya-Nookarapu/ATS-Backend

🚀 Architecture Overview

This is a backend-only project built using FastAPI, SQLite, and SQLAlchemy ORM.

Major Components
Component	Description
FastAPI App (app/main.py)	Initializes the server & loads routers
Database (app/database.py)	Creates engine, session & Base ORM
Models (app/models.py)	User, Company, Job, Application, ApplicationHistory
Auth (app/auth.py)	JWT Tokens, password hashing, role validation
Routers	/auth, /jobs, /applications, /history
Services	Business logic (application workflow, history tracking, email placeholder)
🔁 Application Workflow
1️⃣ Candidate registers & logs in

POST /auth/register

POST /auth/login → returns JWT Access Token

2️⃣ Recruiter creates a job

POST /jobs/

3️⃣ Candidate applies to a job

POST /applications/?job_id={id}

4️⃣ Recruiter updates application stage

Example:

PATCH /applications/1/stage?new_stage=Screening

5️⃣ Every stage change is recorded

Stored in ApplicationHistory:

old_stage

new_stage

changed_by_id

changed_at

6️⃣ History endpoints

Recruiter: GET /history/application/{id}

Candidate: GET /history/me/{id}

🔄 Application State Machine (Workflow Diagram)
[Applied] ─> [Screening] ─> [Interview] ─> [Offer] ─> [Hired]
       └──────────────────────────────────────────────┐
        └────────────────────────────────────────────> [Rejected]

🧩 Role-Based Access Control (RBAC)
Endpoint	Candidate	Recruiter	Hiring Manager
Register/Login	✅	✅	✅
Create Job	❌	✅	✅
Apply to Job	✅	❌	❌
View Applications for Job	❌	✅	✅
Change Application Stage	❌	✅	❌
View Own Applications	✅	❌	❌
View Full History	❌	✅	❌
🗄️ Database Schema (ERD)

Add your image to the repository (already uploaded).
Now display it in README:

## 📌 Database Schema (ERD)
![ERD](./erd.png)


It will render like this:

🛠️ Setup Instructions (Development Environment)
1️⃣ Clone the repository
git clone https://github.com/Akhila-priya-Nookarapu/ATS-Backend
cd ATS-Backend

2️⃣ Create virtual environment
python -m venv venv

3️⃣ Activate environment

Windows:

venv\Scripts\activate

4️⃣ Install dependencies
pip install -r requirements.txt

5️⃣ Run the FastAPI server
uvicorn app.main:app --reload

6️⃣ Open API Docs

http://127.0.0.1:8000/docs

🧪 Postman Collection

Include your exported .json here:

postman_collection.json

🎥 Demo Video (3–5 minutes)

Your demo should cover:

Candidate login

Recruiter creating a job

Candidate applying

Recruiter moving the application through stages

View history timeline
