from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class MetricResult:
    score: float
    passed: bool
    detail: str

    def to_dict(self) -> Dict[str, object]:
        return {
            "score": round(self.score, 2),
            "passed": self.passed,
            "detail": self.detail,
        }


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def _count_matches(patterns: List[str], text: str) -> int:
    return sum(1 for pattern in patterns if re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE))


def tone_score(text: str) -> Dict[str, object]:
    """
    Avalia se a resposta tem tom profissional, claro e orientado a produto.
    Heurística simples: presença de linguagem de user story, ações e clareza.
    """
    normalized = _normalize(text)

    positive_markers = [
        "as a",
        "i want",
        "so that",
        "acceptance criteria",
        "user story",
        "notes",
    ]
    score = sum(1 for marker in positive_markers if marker in normalized) / len(positive_markers)

    return MetricResult(
        score=score,
        passed=score >= 0.9,
        detail=f"Positive tone/structure markers found: {sum(1 for marker in positive_markers if marker in normalized)}/{len(positive_markers)}",
    ).to_dict()


def user_story_format_score(text: str) -> Dict[str, object]:
    """
    Verifica se há uma user story válida no formato:
    As a ... I want ... so that ...
    """
    normalized = _normalize(text)

    pattern = r"as a\s+.+?\s+i want\s+.+?\s+so that\s+.+"
    matched = bool(re.search(pattern, normalized, flags=re.IGNORECASE | re.DOTALL))

    return MetricResult(
        score=1.0 if matched else 0.0,
        passed=matched,
        detail="User story pattern detected" if matched else "User story pattern not detected",
    ).to_dict()


def acceptance_criteria_score(text: str) -> Dict[str, object]:
    """
    Avalia a presença e qualidade do bloco de Acceptance Criteria.
    Não força um formato engessado, mas valoriza:
    - seção explícita
    - pelo menos 3 critérios
    - evidência de Given/When/Then
    """
    normalized = _normalize(text)

    has_section = "acceptance criteria" in normalized
    bullet_lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip().startswith(("-", "*", "•", "1.", "2.", "3.", "4.", "5."))
    ]

    given_hits = len(re.findall(r"\bgiven\b", normalized, flags=re.IGNORECASE))
    when_hits = len(re.findall(r"\bwhen\b", normalized, flags=re.IGNORECASE))
    then_hits = len(re.findall(r"\bthen\b", normalized, flags=re.IGNORECASE))

    structure_score = 0.0
    if has_section:
        structure_score += 0.35
    if len(bullet_lines) >= 3:
        structure_score += 0.35
    if given_hits >= 1 and when_hits >= 1 and then_hits >= 1:
        structure_score += 0.30

    score = min(1.0, structure_score)

    detail_parts = []
    detail_parts.append("section=yes" if has_section else "section=no")
    detail_parts.append(f"bullets={len(bullet_lines)}")
    detail_parts.append(f"given={given_hits},when={when_hits},then={then_hits}")

    return MetricResult(
        score=score,
        passed=score >= 0.9,
        detail="; ".join(detail_parts),
    ).to_dict()


def completeness_score(text: str) -> Dict[str, object]:
    """
    Verifica se a resposta está completa:
    - user story
    - acceptance criteria
    - notes
    """
    normalized = _normalize(text)

    required_sections = [
        "as a",
        "i want",
        "so that",
        "acceptance criteria",
        "notes",
    ]

    hits = sum(1 for section in required_sections if section in normalized)
    base_score = hits / len(required_sections)

    # Penaliza respostas muito curtas
    if len(normalized) < 120:
        base_score *= 0.8

    # Bonifica estrutura visivelmente organizada
    if text.count("\n") >= 4:
        base_score = min(1.0, base_score + 0.1)

    return MetricResult(
        score=base_score,
        passed=base_score >= 0.9,
        detail=f"Sections found: {hits}/{len(required_sections)}",
    ).to_dict()


def evaluate_output(text: str) -> Dict[str, Dict[str, object]]:
    """
    Retorna os 4 scores esperados pelo desafio.
    """
    return {
        "tone_score": tone_score(text),
        "acceptance_criteria_score": acceptance_criteria_score(text),
        "user_story_format_score": user_story_format_score(text),
        "completeness_score": completeness_score(text),
    }