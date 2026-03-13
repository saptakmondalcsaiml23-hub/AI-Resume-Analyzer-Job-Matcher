# AI Resume Analyzer and Job Matcher

An AI-powered career assistant for developers. Upload a resume PDF, compare it with a job description, and get:

- Extracted technical skills
- Resume-to-job similarity score
- Skill gap analysis
- Resume improvement suggestions (LLM-backed with fallback heuristics)

## Tech Stack

- Frontend: React + Tailwind CSS + Vite
- Backend: FastAPI (Python)
- Database: PostgreSQL (SQLAlchemy ORM)
- AI/NLP:
	- Rule-based NLP skill extraction
	- TF-IDF + cosine similarity scoring
	- Optional LLM suggestions via OpenAI API

## Core Features

- Resume upload and PDF text parsing
- AI skill extraction from resume text
- Job description similarity scoring
- Skill gap detection (missing skills)
- AI-generated resume improvement suggestions
- Dashboard showing skill match percentage and insights

## Project Structure

```
.
├── backend
│   ├── app
│   │   ├── api
│   │   │   └── routes.py
│   │   ├── core
│   │   │   └── config.py
│   │   ├── db
│   │   │   ├── database.py
│   │   │   └── models.py
│   │   ├── services
│   │   │   ├── llm_suggestions.py
│   │   │   ├── matcher.py
│   │   │   ├── pdf_parser.py
│   │   │   └── skill_extractor.py
│   │   ├── main.py
│   │   └── schemas.py
│   ├── .env.example
│   ├── Dockerfile
│   └── requirements.txt
├── frontend
│   ├── src
│   │   ├── api.js
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── Dockerfile
│   ├── package.json
│   └── tailwind.config.js
├── .env.example
├── docker-compose.yml
└── README.md
```

## How the AI Works

1. Resume text extraction:
	 - Parses PDF pages and concatenates text.

2. Skill extraction:
	 - Uses an NLP-style keyword/pattern matcher across common engineering and AI skills.

3. Similarity score:
	 - Computes cosine similarity over TF-IDF vectors for resume vs job description.
	 - Match percentage is the cosine score scaled to 0-100.

4. Skill gap analysis:
	 - Extracts job skills and compares them against resume skills.
	 - Returns matched skills and missing skills.

5. Resume suggestions:
	 - If OpenAI API key exists: requests tailored LLM advice.
	 - If not: returns strong deterministic heuristic suggestions.

## Prerequisites

- Docker + Docker Compose
or
- Python 3.11+
- Node.js 20+
- PostgreSQL 16+

## Quick Start with Docker

1. Copy root env file:

```bash
cp .env.example .env
```

2. (Optional) Add your OpenAI key in `.env`:

```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
```

3. Start everything:

```bash
docker compose up --build
```

4. Open apps:

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API docs: http://localhost:8000/docs

## Local Development (Without Docker)

### 1) Start PostgreSQL

Create a database named `resume_matcher` and ensure credentials match backend env settings.

### 2) Backend setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3) Frontend setup

```bash
cd frontend
npm install
npm run dev
```

Frontend expects backend at `http://localhost:8000/api` by default.

## API Endpoints

### Health

- `GET /api/health`

### Upload Resume

- `POST /api/upload-resume`
- Form field: `file` (PDF)

Sample response:

```json
{
	"resume_id": 1,
	"filename": "resume.pdf",
	"extracted_skills": ["python", "fastapi", "postgresql"],
	"text_preview": "Experienced engineer with ..."
}
```

### List Resumes

- `GET /api/resumes`

### Match Job

- `POST /api/match-job`

Sample request:

```json
{
	"resume_id": 1,
	"job_title": "Backend AI Engineer",
	"job_description": "Looking for Python, FastAPI, PostgreSQL, NLP and Docker experience ..."
}
```

Sample response:

```json
{
	"match_id": 4,
	"resume_id": 1,
	"job_title": "Backend AI Engineer",
	"match_percentage": 74.28,
	"extracted_resume_skills": ["docker", "fastapi", "python"],
	"required_job_skills": ["docker", "nlp", "postgresql", "python"],
	"matched_skills": ["docker", "python"],
	"missing_skills": ["nlp", "postgresql"],
	"suggestions": [
		"Add project bullets showing hands-on use of: nlp, postgresql.",
		"Strengthen experience bullets with measurable impact tied to the top required skills."
	]
}
```

## Environment Variables

Backend env (`backend/.env`):

- `APP_ENV` (default: `development`)
- `DATABASE_URL` (PostgreSQL SQLAlchemy URL)
- `CORS_ORIGINS` (comma-separated URLs)
- `OPENAI_API_KEY` (optional)
- `OPENAI_MODEL` (default: `gpt-4o-mini`)
- `MAX_UPLOAD_SIZE_MB` (default: `5`)

## Roadmap Ideas

- Better resume section parsing (experience/projects/skills)
- Embedding-based semantic similarity
- Authentication and user profiles
- Match history analytics
- Exportable improvement report
