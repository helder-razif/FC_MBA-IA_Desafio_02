from langsmith import Client
from dotenv import load_dotenv

load_dotenv()
client = Client()

def extract_text_from_output(output):
    """Extrai texto real do output (pode ser dict, string ou AIMessage)"""
    if isinstance(output, dict):
        # Se for dict de mensagens, pega o último conteúdo
        if 'messages' in output and output['messages']:
            last_msg = output['messages'][-1]
            if isinstance(last_msg, dict):
                return last_msg.get('content', str(last_msg))
            else:
                return str(last_msg.content) if hasattr(last_msg, 'content') else str(last_msg)
        return str(output)
    elif isinstance(output, str):
        return output
    else:
        return str(output.content) if hasattr(output, 'content') else str(output)

def main():
    projects = list(client.list_projects(name_contains="bug-to-user-story-eval"))
    if not projects:
        print("❌ Nenhum projeto encontrado")
        return
    
    project = projects[-1]
    print(f"\n📊 Projeto: {project.name}\n")
    
    runs = list(client.list_runs(project_id=project.id, limit=3))
    
    print("=" * 80)
    print("3 PRIMEIROS OUTPUTS (DEBUG)")
    print("=" * 80)
    
    for i, run in enumerate(runs, 1):
        print(f"\n🔹 Run {i}:")
        
        # Input
        if run.inputs:
            bug_input = run.inputs.get('bug', run.inputs.get('bug_report', 'N/A'))
            print(f"Input Bug: {bug_input}")
        
        # Output extraído
        if run.outputs:
            raw_output = run.outputs.get('output', 'N/A')
            output_text = extract_text_from_output(raw_output)
            print(f"\nOutput (primeiros 300 chars):\n{output_text[:300]}...")
            
            # Análise das palavras-chave
            output_lower = output_text.lower()
            keywords = {
                "como": "como" in output_lower,
                "quero": "quero" in output_lower,
                "para": "para" in output_lower,
                "dado": "dado" in output_lower,
                "quando": "quando" in output_lower,
                "então": "então" in output_lower
            }
            print(f"\nPalavras-chave: {keywords}")
            print(f"✅ Encontradas: {sum(keywords.values())}/6")
        else:
            print("❌ Sem output")
        
        print("-" * 80)

if __name__ == "__main__":
    main()