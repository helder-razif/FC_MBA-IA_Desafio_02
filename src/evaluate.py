from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from statistics import mean
from typing import Dict, List

import yaml
from dotenv import load_dotenv
import ollama

from dataset import get_dataset
from metrics import evaluate_output

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROMPT_FILE = PROJECT_ROOT / "prompts" / "bug_to_user_story_v2.yml"

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434").strip()
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma2:9b").strip()
PREFERRED_PROVIDER = os.getenv("LLM_PROVIDER", "ollama").strip().lower()


def load_prompt_from_yaml() -> Dict[str, str]:
    if not PROMPT_FILE.exists():
        raise FileNotFoundError(f"Arquivo de prompt não encontrado: {PROMPT_FILE}")

    with PROMPT_FILE.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    system_prompt = (data.get("system_prompt") or "").strip()
    user_prompt = (data.get("user_prompt") or "").strip()

    if not system_prompt or not user_prompt:
        raise ValueError(
            "O YAML precisa conter system_prompt e user_prompt preenchidos."
        )

    return {"system_prompt": system_prompt, "user_prompt": user_prompt}


def build_messages(prompt_data: Dict[str, str], bug_description: str) -> List[Dict[str, str]]:
    system_prompt = prompt_data["system_prompt"]
    user_prompt = prompt_data["user_prompt"].replace("{bug_description}", bug_description)

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def invoke_ollama(messages: List[Dict[str, str]]) -> str:
    if PREFERRED_PROVIDER != "ollama":
        raise ValueError(
            f"Este evaluate.py foi preparado para LLM_PROVIDER=ollama. Valor atual: {PREFERRED_PROVIDER}"
        )

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=messages,
        options={"temperature": 0},
    )

    return response["message"]["content"]


def evaluate_single_example(prompt_data: Dict[str, str], example: Dict[str, str]) -> Dict[str, object]:
    messages = build_messages(prompt_data, example["description"])
    output_text = invoke_ollama(messages)
    scores = evaluate_output(output_text)

    return {
        "id": example["bug_id"],
        "title": example["bug_id"],
        "input": example["description"],
        "expected_user_story": example.get("expected_output", ""),
        "output": output_text,
        "scores": scores,
    }


def summarize_scores(results: List[Dict[str, object]]) -> Dict[str, float]:
    tone_scores = [r["scores"]["tone_score"]["score"] for r in results]
    acceptance_scores = [r["scores"]["acceptance_criteria_score"]["score"] for r in results]
    user_story_scores = [r["scores"]["user_story_format_score"]["score"] for r in results]
    completeness_scores = [r["scores"]["completeness_score"]["score"] for r in results]

    summary = {
        "tone_score": round(mean(tone_scores), 2) if tone_scores else 0.0,
        "acceptance_criteria_score": round(mean(acceptance_scores), 2) if acceptance_scores else 0.0,
        "user_story_format_score": round(mean(user_story_scores), 2) if user_story_scores else 0.0,
        "completeness_score": round(mean(completeness_scores), 2) if completeness_scores else 0.0,
    }

    summary["global_average"] = round(
        mean(
            [
                summary["tone_score"],
                summary["acceptance_criteria_score"],
                summary["user_story_format_score"],
                summary["completeness_score"],
            ]
        ),
        2,
    )
    return summary


def print_example_result(result: Dict[str, object]) -> None:
    print(f"Prompt: {result['id']} - {result['title']}")
    print(f"- Tone Score: {result['scores']['tone_score']['score']}")
    print(f"- Acceptance Criteria Score: {result['scores']['acceptance_criteria_score']['score']}")
    print(f"- User Story Format Score: {result['scores']['user_story_format_score']['score']}")
    print(f"- Completeness Score: {result['scores']['completeness_score']['score']}")
    print("-" * 40)


def print_summary(summary: Dict[str, float]) -> None:
    print("Resumo consolidado")
    print("=" * 40)
    print(f"- Tone Score: {summary['tone_score']}")
    print(f"- Acceptance Criteria Score: {summary['acceptance_criteria_score']}")
    print(f"- User Story Format Score: {summary['user_story_format_score']}")
    print(f"- Completeness Score: {summary['completeness_score']}")
    print(f"- Média geral: {summary['global_average']}")
    print("=" * 40)

    status = (
        "APROVADO"
        if min(
            summary["tone_score"],
            summary["acceptance_criteria_score"],
            summary["user_story_format_score"],
            summary["completeness_score"],
        ) >= 0.9
        else "FALHOU"
    )
    print(f"Status: {status}")


def run_evaluation() -> None:
    dataset = get_dataset()
    examples = dataset["examples"]
    prompt_data = load_prompt_from_yaml()

    experiment_name = f"desafio2-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    print("Executando avaliação dos prompts...")
    print("=" * 40)
    print(f"Prompt local: {PROMPT_FILE}")
    print(f"Experimento: {experiment_name}")
    print(f"Casos no dataset: {len(examples)}")
    print(f"Provider: {PREFERRED_PROVIDER}")
    print(f"Modelo: {OLLAMA_MODEL}")
    print("=" * 40)

    results = []
    for example in examples:
        result = evaluate_single_example(prompt_data, example)
        results.append(result)
        print_example_result(result)

    summary = summarize_scores(results)
    print_summary(summary)


if __name__ == "__main__":
    run_evaluation()