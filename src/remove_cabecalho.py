import os

# Caminho base
base_path = "/workspace/fase7_challenge_sprint3/dados/download_manual/inmet"

def remover_linhas_iniciais():
    print("🧹 Removendo as 8 primeiras linhas dos arquivos INMET_*_SP_*.*\n")
    
    arquivos_processados = 0
    arquivos_pulados = 0

    for root, _, files in os.walk(base_path):
        for nome_arquivo in files:
            if nome_arquivo.startswith("INMET_") and "_SP_" in nome_arquivo:
                caminho_arquivo = os.path.join(root, nome_arquivo)

                try:
                    with open(caminho_arquivo, "r", encoding="latin1") as f:
                        linhas = f.readlines()

                    if len(linhas) <= 8:
                        print(f"⚠️ {nome_arquivo} — menos de 9 linhas, ignorado.")
                        arquivos_pulados += 1
                        continue

                    # Mantém da linha 9 em diante
                    conteudo_limpo = linhas[8:]

                    # Sobrescreve o arquivo apenas após validação
                    with open(caminho_arquivo, "w", encoding="latin1") as f:
                        f.writelines(conteudo_limpo)

                    print(f"✅ {nome_arquivo} — 8 primeiras linhas removidas.")
                    arquivos_processados += 1

                except Exception as e:
                    print(f"❌ Erro ao processar {nome_arquivo}: {e}")

    print("\n📊 RESUMO FINAL")
    print(f"✔️ Arquivos processados: {arquivos_processados}")
    print(f"➖ Arquivos ignorados: {arquivos_pulados}")

if __name__ == "__main__":
    remover_linhas_iniciais()
