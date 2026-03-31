from __future__ import annotations

from pathlib import Path

import pytest
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROMPT_FILE = PROJECT_ROOT / "prompts" / "bug_to_user_story_v2.yml"


@pytest.fixture(scope="module")
def prompt_data():
    assert PROMPT_FILE.exists(), f"Prompt file not found: {PROMPT_FILE}"
    with PROMPT_FILE.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert isinstance(data, dict), "Prompt YAML must be a dictionary"
    return data


def test_prompt_has_system_prompt(prompt_data):
    system_prompt = str(prompt_data.get("system_prompt", "")).strip()
    assert system_prompt, "system_prompt must not be empty"


def test_prompt_has_role_definition(prompt_data):
    text = str(prompt_data.get("system_prompt", "")).lower()
    assert any(
        phrase in text for phrase in ["you are", "as an", "role", "assistant", "expert"]
    ), "system_prompt must define a role"


def test_prompt_mentions_format(prompt_data):
    text = str(prompt_data.get("system_prompt", "")).lower() + " " + str(
        prompt_data.get("user_prompt", "")
    ).lower()
    assert any(
        phrase in text for phrase in ["user story", "acceptance criteria", "format", "template"]
    ), "Prompt must mention the expected output format"


def test_prompt_has_few_shot_examples(prompt_data):
    text = str(prompt_data.get("system_prompt", "")) + "\n" + str(prompt_data.get("user_prompt", ""))
    examples = text.lower().count("example") + text.lower().count("exemplo")
    assert examples >= 2, "Prompt must contain at least two examples"


def test_prompt_no_todos(prompt_data):
    combined = f"{prompt_data.get('system_prompt', '')}\n{prompt_data.get('user_prompt', '')}"
    forbidden = ["todo", "tbd", "to be done", "fill later", "[insert"]
    assert not any(token in combined.lower() for token in forbidden), "Prompt contains unfinished placeholders"


def test_minimum_techniques(prompt_data):
    text = f"{prompt_data.get('system_prompt', '')}\n{prompt_data.get('user_prompt', '')}".lower()
    techniques = {
        "few_shot": any(key in text for key in ["example", "exemplo", "few-shot"]),
        "role_prompting": any(key in text for key in ["you are", "role", "expert", "as an"]),
        "skeleton": any(key in text for key in ["step 1", "step 2", "structure", "outline"]),
        "cot": any(key in text for key in ["think step by step", "step by step", "reason"]),
        "react": "react" in text,
        "tree_of_thought": "tree of thought" in text,
    }
    assert sum(techniques.values()) >= 2, "Prompt must apply at least two techniques"