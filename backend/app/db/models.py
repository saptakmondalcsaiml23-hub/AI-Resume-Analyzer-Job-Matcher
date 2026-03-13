from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    extracted_skills: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    matches: Mapped[list["JobMatch"]] = relationship(
        back_populates="resume",
        cascade="all, delete-orphan",
    )


class JobMatch(Base):
    __tablename__ = "job_matches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resume_analyses.id", ondelete="CASCADE"), nullable=False)
    job_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    job_description: Mapped[str] = mapped_column(Text, nullable=False)
    matched_skills: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    missing_skills: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    similarity_score: Mapped[float] = mapped_column(Float, nullable=False)
    improvement_suggestions: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    resume: Mapped[ResumeAnalysis] = relationship(back_populates="matches")
