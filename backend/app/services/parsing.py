from dataclasses import dataclass
from pathlib import Path
from typing import List, Set
import re

from docx import Document as DocxDocument
from pypdf import PdfReader


class ResumeParsingError(Exception):
    """Raised when a resume cannot be parsed."""


SUPPORTED_EXTENSIONS = {".pdf", ".docx"}
SKILL_KEYWORDS: Set[str] = {
    "python",
    "java",
    "sql",
    "mongodb",
    "fastapi",
    "react",
    "aws",
    "docker",
    "kubernetes",
    "c++",
    "c#",
    "javascript",
    "typescript",
    "node",
    "git",
    "ci/cd",
    "ml",
    "machine learning",
    "nlp",
}
TITLE_KEYWORDS = [
    "engineer",
    "developer",
    "manager",
    "scientist",
    "analyst",
    "consultant",
    "architect",
    "specialist",
    "lead",
    "intern",
    "designer",
]


@dataclass
class ParsedResume:
    raw_text: str
    skills: List[str]
    titles: List[str]


def _extract_text_from_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    chunks: List[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        if text:
            chunks.append(text)
    return "\n".join(chunks).strip()


def _extract_text_from_docx(path: Path) -> str:
    doc = DocxDocument(str(path))
    paragraphs = [paragraph.text for paragraph in doc.paragraphs if paragraph.text]
    return "\n".join(paragraphs).strip()


def _extract_text_from_plain(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore").strip()


def _normalise_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _parse_skills(raw_text: str) -> List[str]:
    text_lower = raw_text.lower()
    found = {skill for skill in SKILL_KEYWORDS if skill in text_lower}
    ordered = sorted(found)
    return ordered


def _clean_title(line: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9\s/\-&]", "", line)
    return _normalise_text(cleaned)


def _parse_titles(raw_text: str) -> List[str]:
    candidates = set()
    for line in raw_text.splitlines():
        lower_line = line.lower()
        if any(keyword in lower_line for keyword in TITLE_KEYWORDS):
            cleaned = _clean_title(line)
            if cleaned:
                candidates.add(cleaned)
    return sorted(candidates)


def parse_resume(path: Path) -> ParsedResume:
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ResumeParsingError(f"Unsupported resume format: {suffix or 'unknown'}")

    if suffix == ".pdf":
        raw_text = _extract_text_from_pdf(path)
    elif suffix == ".docx":
        raw_text = _extract_text_from_docx(path)
    else:
        raw_text = _extract_text_from_plain(path)

    raw_text_original = raw_text.strip()
    normalised_text = _normalise_text(raw_text_original)
    if not normalised_text:
        raise ResumeParsingError("Unable to extract text from resume")

    skills = _parse_skills(normalised_text)
    titles = _parse_titles(raw_text_original)
    return ParsedResume(raw_text=normalised_text, skills=skills, titles=titles)
