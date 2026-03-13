import re

SKILL_PATTERNS: dict[str, list[str]] = {
    "python": [r"\bpython\b"],
    "java": [r"\bjava\b"],
    "c": [r"\bc\b"],
    "c++": [r"\bc\+\+\b"],
    "c#": [r"\bc#\b", r"\bcsharp\b"],
    "javascript": [r"\bjavascript\b"],
    "typescript": [r"\btypescript\b"],
    "react": [r"\breact(?:\.js)?\b"],
    "next.js": [r"\bnext(?:\.js)?\b"],
    "node.js": [r"\bnode(?:\.js|js)?\b"],
    "fastapi": [r"\bfastapi\b"],
    "flask": [r"\bflask\b"],
    "django": [r"\bdjango\b"],
    "sql": [r"\bsql\b"],
    "postgresql": [r"\bpostgres(?:ql)?\b"],
    "mysql": [r"\bmysql\b"],
    "sqlite": [r"\bsqlite\b"],
    "mongodb": [r"\bmongo(?:db)?\b"],
    "redis": [r"\bredis\b"],
    "docker": [r"\bdocker\b"],
    "kubernetes": [r"\bkubernetes\b", r"\bk8s\b"],
    "aws": [r"\baws\b", r"\bamazon web services\b"],
    "azure": [r"\bazure\b"],
    "gcp": [r"\bgcp\b", r"\bgoogle cloud\b"],
    "git": [r"\bgit\b"],
    "linux": [r"\blinux\b"],
    "rest api": [r"\brest(?:ful)?\b", r"\bapi\b"],
    "graphql": [r"\bgraphql\b"],
    "machine learning": [r"\bmachine learning\b", r"\bml\b"],
    "deep learning": [r"\bdeep learning\b"],
    "nlp": [r"\bnlp\b", r"\bnatural language processing\b"],
    "llm": [r"\bllm\b", r"\blarge language model\b"],
    "openai": [r"\bopenai\b"],
    "hugging face": [r"\bhugging\s*face\b"],
    "tensorflow": [r"\btensorflow\b"],
    "pytorch": [r"\bpytorch\b"],
    "scikit-learn": [r"\bscikit[-\s]?learn\b", r"\bsklearn\b"],
    "pandas": [r"\bpandas\b"],
    "numpy": [r"\bnumpy\b"],
    "tailwind css": [r"\btailwind\b"],
    "html": [r"\bhtml\b"],
    "css": [r"\bcss\b"],
}


def extract_skills(text: str) -> list[str]:
    if not text:
        return []

    lowered = text.lower()
    found_skills: list[str] = []

    for skill, patterns in SKILL_PATTERNS.items():
        if any(re.search(pattern, lowered, flags=re.IGNORECASE) for pattern in patterns):
            found_skills.append(skill)

    return sorted(found_skills)
