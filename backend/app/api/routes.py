from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.database import get_db
from app.db.models import JobMatch, ResumeAnalysis
from app.schemas import AnalyzeRequest, AnalyzeResponse, ResumeSummary, ResumeUploadResponse
from app.services.llm_suggestions import generate_resume_suggestions
from app.services.matcher import build_match_result
from app.services.pdf_parser import PDFExtractionError, extract_text_from_pdf
from app.services.skill_extractor import extract_skills

router = APIRouter(tags=["Resume Matcher"])


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/resumes", response_model=list[ResumeSummary])
def list_resumes(db: Session = Depends(get_db)) -> list[ResumeSummary]:
    records = db.query(ResumeAnalysis).order_by(ResumeAnalysis.created_at.desc()).all()
    return [ResumeSummary.model_validate(record) for record in records]


@router.post(
    "/upload-resume",
    response_model=ResumeUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> ResumeUploadResponse:
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF resume.")

    payload = await file.read()
    settings = get_settings()
    max_upload_bytes = settings.max_upload_size_mb * 1024 * 1024
    if len(payload) > max_upload_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Max size is {settings.max_upload_size_mb} MB.",
        )

    try:
        resume_text = extract_text_from_pdf(payload)
    except PDFExtractionError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    extracted_skills = extract_skills(resume_text)

    resume_record = ResumeAnalysis(
        filename=file.filename,
        raw_text=resume_text,
        extracted_skills=extracted_skills,
    )
    db.add(resume_record)
    db.commit()
    db.refresh(resume_record)

    preview = " ".join(resume_text.split())[:280]
    return ResumeUploadResponse(
        resume_id=resume_record.id,
        filename=resume_record.filename,
        extracted_skills=resume_record.extracted_skills,
        text_preview=preview,
    )


@router.post("/match-job", response_model=AnalyzeResponse)
def match_job(
    payload: AnalyzeRequest,
    db: Session = Depends(get_db),
) -> AnalyzeResponse:
    resume_record = db.get(ResumeAnalysis, payload.resume_id)
    if not resume_record:
        raise HTTPException(status_code=404, detail="Resume not found.")

    match_result = build_match_result(
        resume_text=resume_record.raw_text,
        job_description=payload.job_description,
        resume_skills=resume_record.extracted_skills,
    )
    suggestions = generate_resume_suggestions(
        resume_text=resume_record.raw_text,
        job_description=payload.job_description,
        match_result=match_result,
    )

    job_match_record = JobMatch(
        resume_id=resume_record.id,
        job_title=payload.job_title,
        job_description=payload.job_description,
        matched_skills=match_result.matched_skills,
        missing_skills=match_result.missing_skills,
        similarity_score=match_result.similarity_score,
        improvement_suggestions="\n".join(suggestions),
    )
    db.add(job_match_record)
    db.commit()
    db.refresh(job_match_record)

    return AnalyzeResponse(
        match_id=job_match_record.id,
        resume_id=resume_record.id,
        job_title=payload.job_title,
        match_percentage=match_result.similarity_score,
        extracted_resume_skills=match_result.resume_skills,
        required_job_skills=match_result.job_skills,
        matched_skills=match_result.matched_skills,
        missing_skills=match_result.missing_skills,
        suggestions=suggestions,
    )
