import subprocess
import re
from dotenv import load_dotenv
from langsmith import Client

load_dotenv()
client = Client()

def run_pytest_notas():
    print("\n🔍 Executando 6 testes obrigatórios...")
    result = subprocess.run(["pytest", "tests/test_prompts.py", "-v", "--tb=no"], capture_output=True, text=True)
    print(result.stdout)
    
    tests = ['test_prompt_has_system_prompt', 'test_prompt_has_role_definition', 'test_prompt_mentions_format', 
             'test_prompt_has_few_shot_examples', 'test_prompt_no_todos', 'test_minimum_techniques']
    notas_testes = {}
    
    print("\n📋 Notas Testes Individuais (1.0 = PASS):")
    for test in tests:
        if test in result.stdout:
            nota = 1.0
            status = "✅ APROVADO"
        else:
            nota = 0.0
            status = "❌ FALHOU"
        notas_testes[test] = nota
        print(f"- **{test}**: **{nota:.1f}** {status}")
    
    passed = all(nota == 1.0 for nota in notas_testes.values())
    return passed, notas_testes

def run_evaluate_notas():
    print("\n📊 Executando avaliação...")
    result = subprocess.run(["python", "src/evaluate.py"], capture_output=True, text=True)
    print(result.stdout)
    
    # Regex robusto para link dashboard
    dashboard_match = re.search(r"https://smith\.langchain\.com/public/[^/\s]+/t/", result.stdout)
    if dashboard_match:
        dashboard_url = dashboard_match.group(0)
        project_name = dashboard_url.split('/')[-2]
        print(f"🔗 Dashboard oficial: {dashboard_url}")
        
        # Fetch LLM runs para notas reais (20 exemplos)
        projects = list(client.list_projects(name_contains=project_name))
        if projects:
            project = projects[0]
            runs = list(client.list_runs(project_id=project.id, run_type="llm", limit=20))
            
            notas_metricas = {'tone_score': [], 'acceptance_criteria_score': [], 'user_story_format_score': [], 'completeness_score': []}
            for run in runs:
                output = run.outputs.get('output', '') if run.outputs else ''
                notas_metricas['tone_score'].append(1.0 if all(p in output.lower() for p in ["como", "quero", "para"]) else 0.0)
                notas_metricas['acceptance_criteria_score'].append(1.0 if all(c in output.lower() for c in ["dado", "quando", "então"]) else 0.0)
                notas_metricas['user_story_format_score'].append(1.0 if any(f in output.lower() for f in ["como usuário", "como [usuário]"]) else 0.0)
                notas_metricas['completeness_score'].append(1.0 if len(output) > 150 and len(output.splitlines()) > 5 else 0.0)
            
            print("\n📈 Notas Métricas Individuais (média de 20 runs LLM):")
            for key in notas_metricas:
                avg = sum(notas_metricas[key]) / len(notas_metricas[key]) if notas_metricas[key] else 0.0
                status = "✅ APROVADO" if avg >= 0.9 else "❌ PENDENTE"
                print(f"- **{key}**: **{avg:.3f}** {status}")
            
            all_metrics_ok = all(avg >= 0.9 for avgs in notas_metricas.values() for avg in [sum(avgs)/len(avgs)] if avgs)
            return all_metrics_ok, {key: sum(notas_metricas[key])/len(notas_metricas[key]) for key in notas_metricas if notas_metricas[key]}
    
    print("❌ Link dashboard não capturado")
    return False, {}

if __name__ == "__main__":
    tests_ok, notas_testes = run_pytest_notas()
    metrics_ok, notas_metricas = run_evaluate_notas()
    
    todas_notas = list(notas_testes.values()) + list(notas_metricas.values())
    media_geral = sum(todas_notas) / len(todas_notas) if todas_notas else 0.0
    
    status = tests_ok and metrics_ok
    print(f"\n🎯 **Média Geral (10 itens)**: **{media_geral:.3f}**")
    print(f"{'🎉 DESAFIO APROVADO (todas notas ≥0.9)' if status else '❌ PENDENTE (ver itens acima)'}")