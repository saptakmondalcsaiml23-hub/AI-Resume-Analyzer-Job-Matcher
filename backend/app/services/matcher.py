from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.services.skill_extractor import extract_skills


@dataclass(slots=True)
class MatchResult:
    similarity_score: float
    resume_skills: list[str]
    job_skills: list[str]
    matched_skills: list[str]
    missing_skills: list[str]


def compute_cosine_similarity(resume_text: str, job_description: str) -> float:
    clean_resume = (resume_text or "").strip()
    clean_job = (job_description or "").strip()
    if not clean_resume or not clean_job:
        return 0.0

    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform([clean_resume, clean_job])
    score = float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])
    return round(max(0.0, min(score * 100, 100.0)), 2)


def build_match_result(
    resume_text: str,
    job_description: str,
    resume_skills: list[str] | None = None,
) -> MatchResult:
    current_resume_skills = resume_skills or extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    resume_skill_set = {skill.lower() for skill in current_resume_skills}
    job_skill_set = {skill.lower() for skill in job_skills}

    matched_lower = sorted(resume_skill_set & job_skill_set)
    missing_lower = sorted(job_skill_set - resume_skill_set)

    matched_skills = [skill for skill in job_skills if skill.lower() in matched_lower]
    missing_skills = [skill for skill in job_skills if skill.lower() in missing_lower]

    return MatchResult(
        similarity_score=compute_cosine_similarity(resume_text, job_description),
        resume_skills=sorted(current_resume_skills),
        job_skills=sorted(job_skills),
        matched_skills=matched_skills,
        missing_skills=missing_skills,
    )


def heuristic_resume_suggestions(match_result: MatchResult) -> list[str]:
    suggestions: list[str] = []

    if match_result.missing_skills:
        missing = ", ".join(match_result.missing_skills[:5])
        suggestions.append(f"Add project bullets showing hands-on use of: {missing}.")

    if match_result.similarity_score < 40:
        suggestions.append(
            "Rewrite your summary to mirror the job description using role-specific keywords and outcomes."
        )
    elif match_result.similarity_score < 70:
        suggestions.append(
            "Strengthen experience bullets with measurable impact tied to the top required skills."
        )

    suggestions.append("Prioritize recent and relevant projects near the top of the resume.")
    suggestions.append("Quantify achievements with numbers such as latency reduction, revenue impact, or model accuracy.")
    suggestions.append("Keep each bullet outcome-focused using an action + impact format.")

    return suggestions[:5]
