import os
from pathlib import Path

# Diretório base contendo os subdiretórios por ano
base_path = Path("/workspace/fase7_challenge_sprint3/dados/download_manual/inmet")

total = 0
corrigidos = 0

print("🔍 Procurando arquivos com aspas simples no nome...")

# Percorre todos os subdiretórios (2020, 2021, etc.)
for ano_dir in base_path.iterdir():
    if ano_dir.is_dir():
        for nome_arquivo in os.listdir(ano_dir):
            total += 1
            if nome_arquivo.startswith("'") and nome_arquivo.endswith("'"):
                caminho_antigo = ano_dir / nome_arquivo
                nome_corrigido = nome_arquivo.strip("'")
                caminho_novo = ano_dir / nome_corrigido
                os.rename(caminho_antigo, caminho_novo)
                corrigidos += 1
                print(f"✅ Corrigido: {nome_arquivo} ➜ {nome_corrigido}")

print("\n📊 RESUMO FINAL:")
print(f"📁 Total de arquivos analisados: {total}")
print(f"🔧 Arquivos corrigidos: {corrigidos}")
print(f"➖ Sem necessidade de correção: {total - corrigidos}")
