# -----------------------------------------------
# SCRIPT: integrar_clima_ndvi_sp_2020_2023.py
# OBJETIVO: Relacionar os dados climáticos INMET com os valores mensais de NDVI
#           por município de São Paulo entre 2020 e 2023.
# AUTOR: Marco Franzoi + ChatGPT
# -----------------------------------------------

import pandas as pd
import os
import sys

# -----------------------------------------------
# 1. CAMINHOS DOS ARQUIVOS DE ENTRADA E SAÍDA
# -----------------------------------------------

CAMINHO_INMET = '/workspace/fase7_challenge_sprint3/dados/INMET_SP_unificado.csv'
CAMINHO_ESTACOES_MUN = '/workspace/fase7_challenge_sprint3/dados/estacoes_com_municipio.csv'
CAMINHO_NDVI = '/workspace/fase7_challenge_sprint3/dados/ndvi_mensal_cana_20250526_2009.csv'
CAMINHO_SAIDA = '/workspace/fase7_challenge_sprint3/dados/clima_ndvi_integrado.csv'

# -----------------------------------------------
# 2. VERIFICAÇÃO DOS ARQUIVOS DE ENTRADA
# -----------------------------------------------

arquivos_requeridos = {
    'INMET': CAMINHO_INMET,
    'Estações com Município': CAMINHO_ESTACOES_MUN,
    'NDVI': CAMINHO_NDVI
}

print("🔍 Verificando existência dos arquivos...")

for nome, caminho in arquivos_requeridos.items():
    if not os.path.isfile(caminho):
        print(f"❌ ERRO: Arquivo '{nome}' não encontrado em: {caminho}")
        sys.exit(1)

print("✅ Todos os arquivos foram encontrados.\n")

# -----------------------------------------------
# 3. LEITURA DOS DADOS
# -----------------------------------------------

df_clima = pd.read_csv(CAMINHO_INMET)
df_estacoes = pd.read_csv(CAMINHO_ESTACOES_MUN)
df_ndvi = pd.read_csv(CAMINHO_NDVI)

# -----------------------------------------------
# 4. ASSOCIA CD_MUN A CADA LINHA DO INMET
# -----------------------------------------------

df_clima = pd.merge(df_clima, df_estacoes[['CD_ESTACAO', 'CD_MUN']], on='CD_ESTACAO', how='left')

faltando = df_clima[df_clima['CD_MUN'].isnull()]
print(f"⚠️ Estações sem CD_MUN: {faltando['CD_ESTACAO'].nunique()}")

df_clima = df_clima.dropna(subset=['CD_MUN'])

# -----------------------------------------------
# 5. EXTRAI ANO E MÊS DA DATA DE MEDIÇÃO
# -----------------------------------------------

df_clima['DT_MEDICAO'] = pd.to_datetime(df_clima['DT_MEDICAO'], dayfirst=True, errors='coerce')
df_clima['ANO'] = df_clima['DT_MEDICAO'].dt.year
df_clima['MES'] = df_clima['DT_MEDICAO'].dt.month

df_clima = df_clima[df_clima['ANO'].between(2020, 2023)]

# -----------------------------------------------
# 6. PREPARAÇÃO DO NDVI
# -----------------------------------------------

df_ndvi['CD_MUN'] = df_ndvi['CD_MUN'].astype(str)
df_clima['CD_MUN'] = df_clima['CD_MUN'].astype(str)

cd_mun_sp = df_clima['CD_MUN'].unique()
df_ndvi = df_ndvi[df_ndvi['CD_MUN'].isin(cd_mun_sp)]

df_ndvi.rename(columns={'mean': 'NDVI_MEDIO'}, inplace=True)
df_ndvi['ano'] = df_ndvi['ano'].astype(int)
df_ndvi['mes'] = df_ndvi['mes'].astype(int)

# -----------------------------------------------
# 7. JUNÇÃO DOS DADOS POR MUNICÍPIO + ANO + MÊS
# -----------------------------------------------

df_merge = pd.merge(
    df_clima,
    df_ndvi[['CD_MUN', 'ano', 'mes', 'NDVI_MEDIO']],
    left_on=['CD_MUN', 'ANO', 'MES'],
    right_on=['CD_MUN', 'ano', 'mes'],
    how='inner'
)

# -----------------------------------------------
# 8. EXPORTAÇÃO DO RESULTADO FINAL
# -----------------------------------------------

df_merge.to_csv(CAMINHO_SAIDA, index=False)
print(f"\n✅ Arquivo final salvo: {CAMINHO_SAIDA}")
print(f"📊 Total de registros integrados: {len(df_merge)}")
