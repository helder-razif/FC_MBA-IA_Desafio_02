import sys
from pathlib import Path
from dotenv import load_dotenv
from langsmith import Client
from utils import load_yaml, print_section_header, check_env_vars

load_dotenv()

OUT = Path("prompts/bug_to_user_story_v1.yml")
PROMPT_ID = "leonanluppi/bug_to_user_story_v1"

def main():
    print_section_header("PULL LANGSMITH HUB")
    if not check_env_vars(["LANGSMITH_API_KEY"]):
        print("❌ LANGSMITH_API_KEY necessário.")
        return 1

    try:
        prompt = Client().pull_prompt(PROMPT_ID)
        OUT.parent.mkdir(parents=True, exist_ok=True)
        data = prompt.model_dump() if hasattr(prompt, "model_dump") else (prompt.dict() if hasattr(prompt, "dict") else str(prompt))
        OUT.write_text(str(data), encoding="utf-8")
        print(f"✅ Hub OK.")
        print(f"✅ {OUT.name} pronto: {OUT}")
        return 0
    except Exception as e:
        print(f"❌ Erro: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())