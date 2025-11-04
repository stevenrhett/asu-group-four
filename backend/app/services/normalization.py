import re
from typing import Iterable, List

_SKILL_ALIASES = {
    "js": "javascript",
    "py": "python",
    "node.js": "nodejs",
    "node": "nodejs",
    "c sharp": "c#",
    "c++": "c++",
    "nlp": "nlp",
    "ml": "machine learning",
}


def _dedupe_preserve_order(items: Iterable[str]) -> List[str]:
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def normalize_skill(skill: str) -> str:
    cleaned = skill.strip().lower()
    if not cleaned:
        return ""
    cleaned = cleaned.replace("_", " ")
    return _SKILL_ALIASES.get(cleaned, cleaned)


def normalize_skills(skills: Iterable[str]) -> List[str]:
    normalized = [normalize_skill(skill) for skill in skills]
    normalized = [skill for skill in normalized if skill]
    return _dedupe_preserve_order(normalized)


def normalize_title(title: str) -> str:
    return re.sub(r"\s+", " ", title.strip().lower())


def normalize_text_chunks(*chunks: str) -> str:
    joined = " ".join(chunk.strip() for chunk in chunks if chunk and chunk.strip())
    return re.sub(r"\s+", " ", joined).strip()


def tokenize(text: str) -> List[str]:
    return re.findall(r"[a-z0-9]+", text.lower())

