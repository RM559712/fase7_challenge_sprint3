# -----------------------------------------------
# SCRIPT: unificar_inmet_sp.py
# OBJETIVO: Unificar os arquivos INMET_*_SP_*.CSV
#           em um único arquivo consolidado com dados
#           diários de 2020 a 2023 para o estado de São Paulo.
# AUTOR: Marco Franzoi
# -----------------------------------------------

import os
import glob
import pandas as pd

# -----------------------------------------------
# 1. CONFIGURAÇÃO DOS CAMINHOS
# -----------------------------------------------

CAMINHO_DADOS = '/workspace/fase7_challenge_sprint3/dados/download_manual/inmet/'
CAMINHO_SAIDA = '/workspace/fase7_challenge_sprint3/dados/INMET_SP_unificado.csv'

# -----------------------------------------------
# 2. BUSCA DE ARQUIVOS VÁLIDOS
# -----------------------------------------------

# Seleciona todos os arquivos INMET para SP (com cabeçalho já removido)
arquivos = [
    f for f in glob.glob(os.path.join(CAMINHO_DADOS, '**', 'INMET_*_SP_*.CSV'), recursive=True)
    if os.path.isfile(f)
]

if not arquivos:
    print("❌ Nenhum arquivo encontrado com padrão INMET_*_SP_*.CSV.")
    exit(1)

print(f"📁 Total de arquivos encontrados: {len(arquivos)}")

# -----------------------------------------------
# 3. LEITURA E CONSOLIDAÇÃO DOS DADOS
# -----------------------------------------------

dfs = []
for caminho in arquivos:
    try:
        df = pd.read_csv(caminho, sep=';', encoding='latin1')

        if df.empty:
            print(f"⚠️ Arquivo vazio: {os.path.basename(caminho)} — ignorado.")
            continue

        # Tenta extrair o código da estação do nome do arquivo
        nome = os.path.basename(caminho)
        partes = nome.split('_')
        cd_estacao = partes[3] if len(partes) >= 4 else 'DESCONHECIDA'

        df['CD_ESTACAO'] = cd_estacao
        df['ARQUIVO_ORIGEM'] = nome
        dfs.append(df)

        print(f"✅ Processado: {nome} ({len(df)} registros)")

    except Exception as e:
        print(f"❌ Erro ao ler {os.path.basename(caminho)}: {e}")

# -----------------------------------------------
# 4. UNIFICAÇÃO FINAL E EXPORTAÇÃO
# -----------------------------------------------

if dfs:
    df_final = pd.concat(dfs, ignore_index=True)
    df_final.columns = [col.strip().upper() for col in df_final.columns]  # padroniza colunas
    df_final.to_csv(CAMINHO_SAIDA, index=False)
    print(f"\n✅ Arquivo consolidado salvo em: {CAMINHO_SAIDA}")
    print(f"📊 Total de registros: {len(df_final)}")
else:
    print("🚫 Nenhum dado foi consolidado. Verifique os arquivos de origem.")
