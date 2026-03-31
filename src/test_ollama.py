import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

def main():
    print("Iniciando teste de integração LangChain + Ollama (gemma2:9b)...")

    llm = ChatOllama(
        base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
        model=os.getenv("OLLAMA_MODEL", "gemma2:9b"),
        temperature=0,
    )

    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content="Say hello in one sentence.")
    ]

    try:
        response = llm.invoke(messages)
        print(response.content)
        print("\nTeste concluído com sucesso.")
    except Exception as e:
        print(f"\nFalha ao conectar com o Ollama: {e}")

if __name__ == "__main__":
    main()