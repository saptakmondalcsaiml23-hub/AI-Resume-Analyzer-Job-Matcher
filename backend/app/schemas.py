from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ResumeSummary(BaseModel):
    id: int
    filename: str
    extracted_skills: list[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ResumeUploadResponse(BaseModel):
    resume_id: int
    filename: str
    extracted_skills: list[str]
    text_preview: str


class AnalyzeRequest(BaseModel):
    resume_id: int
    job_title: str | None = None
    job_description: str = Field(min_length=20)


class AnalyzeResponse(BaseModel):
    match_id: int
    resume_id: int
    job_title: str | None
    match_percentage: float
    extracted_resume_skills: list[str]
    required_job_skills: list[str]
    matched_skills: list[str]
    missing_skills: list[str]
    suggestions: list[str]
