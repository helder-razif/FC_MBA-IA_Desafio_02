import subprocess
import re
from datetime import datetime
from dotenv import load_dotenv
from langsmith import Client

load_dotenv()
client = Client()

def run_pytest_notas():
    """Executa pytest e extrai notas dos 6 testes"""
    result = subprocess.run(["pytest", "tests/test_prompts.py", "-v", "--tb=no"], capture_output=True, text=True)
    
    tests = [
        'test_prompt_has_system_prompt',
        'test_prompt_has_role_definition',
        'test_prompt_mentions_format',
        'test_prompt_has_few_shot_examples',
        'test_prompt_no_todos',
        'test_minimum_techniques'
    ]
    notas_testes = {}
    
    for test in tests:
        notas_testes[test] = 1.0 if test in result.stdout else 0.0
    
    passed = all(nota == 1.0 for nota in notas_testes.values())
    return passed, notas_testes

def run_evaluate_notas():
    """Executa evaluate.py e extrai notas das 4 métricas"""
    result = subprocess.run(["python", "src/evaluate.py"], capture_output=True, text=True)
    
    # Extrai scores do output
    notas_metricas = {}
    patterns = {
        'tone_score': r'Tone Score: ([\d.]+)',
        'acceptance_criteria_score': r'Acceptance Criteria Score: ([\d.]+)',
        'user_story_format_score': r'User Story Format Score: ([\d.]+)',
        'completeness_score': r'Completeness Score: ([\d.]+)'
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, result.stdout)
        if match:
            notas_metricas[key] = float(match.group(1))
        else:
            notas_metricas[key] = 0.0
    
    all_metrics_ok = all(nota >= 0.9 for nota in notas_metricas.values())
    return all_metrics_ok, notas_metricas

def main():
    tests_ok, notas_testes = run_pytest_notas()
    metrics_ok, notas_metricas = run_evaluate_notas()
    
    print("\n" + "=" * 70)
    print("AVALIAÇÃO COMPLETA - 10 ITENS COM NOTAS")
    print("=" * 70)
    
    print("\n📋 TESTES INDIVIDUAIS (6 itens):")
    for test, nota in notas_testes.items():
        status = "✓" if nota == 1.0 else "✗"
        print(f"- {test}: {nota:.1f} {status}")
    
    print("\n📈 MÉTRICAS INDIVIDUAIS (4 itens):")
    for metric, nota in notas_metricas.items():
        status = "✓" if nota >= 0.9 else "✗"
        print(f"- {metric}: {nota:.2f} {status}")
    
    todas_notas = list(notas_testes.values()) + list(notas_metricas.values())
    media_geral = sum(todas_notas) / len(todas_notas) if todas_notas else 0.0
    
    print("\n" + "=" * 70)
    print(f"Média Geral (10 itens): {media_geral:.2f}")
    status = tests_ok and metrics_ok
    print(f"Status: {'APROVADO ✓ - Todas as métricas atingiram o mínimo de 0.9' if status else 'FALHOU - Métricas abaixo do mínimo de 0.9'}")
    print("=" * 70)

if __name__ == "__main__":
    main()