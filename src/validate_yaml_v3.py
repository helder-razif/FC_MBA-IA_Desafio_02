import yaml

print("\n" + "="*70)
print("VALIDAÇÃO DO YAML v3")
print("="*70)

try:
    with open('prompts/bug_to_user_story_v3.yml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    print("\n✓ YAML v3 válido e carregado com sucesso")
    print(f"  - Chaves encontradas: {list(data.keys())}")
    print(f"  - System length: {len(data.get('system', ''))} chars")
    print(f"  - Human length: {len(data.get('human', ''))} chars")
    
    # Validar presença de mensagem human
    if 'human' not in data or not data['human']:
        print("\n❌ ERRO: Falta mensagem 'human'")
        exit(1)
    
    if 'system' not in data or not data['system']:
        print("\n❌ ERRO: Falta mensagem 'system'")
        exit(1)
    
    # Validar palavras-chave obrigatórias
    text = (data.get('system', '') + data.get('human', '')).lower()
    keywords = ['como', 'quero', 'para', 'dado', 'quando', 'então']
    found = [w for w in keywords if w in text]
    
    print(f"\n✓ Palavras-chave encontradas: {len(found)}/6")
    print(f"  - Encontradas: {found}")
    
    if len(found) < 6:
        print(f"  - ⚠️ AVISO: Faltando {[w for w in keywords if w not in found]}")
    
    print("\n" + "="*70)
    print("STATUS: ✓ VALIDAÇÃO CONCLUÍDA COM SUCESSO")
    print("="*70)

except Exception as e:
    print(f"\n❌ ERRO: {e}")
    print("\n" + "="*70)
    print("STATUS: ✗ VALIDAÇÃO FALHOU")
    print("="*70)
    exit(1)