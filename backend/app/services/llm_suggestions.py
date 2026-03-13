import re

from openai import OpenAI

from app.core.config import get_settings
from app.services.matcher import MatchResult, heuristic_resume_suggestions


def _parse_bullets(text: str) -> list[str]:
    parsed: list[str] = []
    seen: set[str] = set()

    for line in text.splitlines():
        cleaned = re.sub(r"^\s*(?:[-*]|\d+[.)])\s*", "", line).strip()
        if not cleaned:
            continue
        key = cleaned.lower()
        if key in seen:
            continue
        seen.add(key)
        parsed.append(cleaned)

    return parsed[:5]


def generate_resume_suggestions(
    resume_text: str,
    job_description: str,
    match_result: MatchResult,
) -> list[str]:
    fallback = heuristic_resume_suggestions(match_result)
    settings = get_settings()

    if not settings.openai_api_key:
        return fallback

    client = OpenAI(api_key=settings.openai_api_key)

    prompt = (
        "You are an expert technical resume coach. Provide 5 concise resume improvements as bullet points. "
        "Each suggestion must be actionable and tailored to the target role.\n\n"
        f"Job Description:\n{job_description}\n\n"
        f"Current Resume Text:\n{resume_text[:3500]}\n\n"
        f"Missing Skills: {', '.join(match_result.missing_skills) if match_result.missing_skills else 'None'}"
    )

    try:
        response = client.chat.completions.create(
            model=settings.openai_model,
            temperature=0.3,
            messages=[
                {"role": "system", "content": "Return only bullet point suggestions."},
                {"role": "user", "content": prompt},
            ],
        )
        content = response.choices[0].message.content or ""
        parsed = _parse_bullets(content)
        return parsed if parsed else fallback
    except Exception:
        return fallback
