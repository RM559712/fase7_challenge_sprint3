# -----------------------------------------------
# SCRIPT: integrar_clima_ndvi_sp.py
# OBJETIVO: Integrar dados do INMET e NDVI por município de SP (2020–2023)
# AUTOR: Marco Franzoi
# -----------------------------------------------

import pandas as pd
import os
import sys

# -----------------------------------------------
# 1. CAMINHOS
# -----------------------------------------------

CAMINHO_INMET = '/workspace/fase7_challenge_sprint3/dados/INMET_SP_unificado.csv'
CAMINHO_ESTACOES_MUN = '/workspace/fase7_challenge_sprint3/dados/estacoes_com_municipio.csv'
CAMINHO_NDVI = '/workspace/fase7_challenge_sprint3/dados/ndvi_mensal_cana_20250526_2009.csv'
CAMINHO_SAIDA = '/workspace/fase7_challenge_sprint3/dados/clima_ndvi_integrado.csv'

# -----------------------------------------------
# 2. VERIFICAÇÃO DOS ARQUIVOS
# -----------------------------------------------

arquivos_requeridos = {
    'INMET': CAMINHO_INMET,
    'Estações': CAMINHO_ESTACOES_MUN,
    'NDVI': CAMINHO_NDVI
}

print("🔍 Verificando existência dos arquivos...")

for nome, caminho in arquivos_requeridos.items():
    if not os.path.isfile(caminho):
        print(f"❌ Arquivo '{nome}' não encontrado: {caminho}")
        sys.exit(1)

print("✅ Todos os arquivos foram encontrados.\n")

# -----------------------------------------------
# 3. LEITURA DOS ARQUIVOS
# -----------------------------------------------

print("📥 Lendo arquivos...")
df_clima = pd.read_csv(CAMINHO_INMET, sep=',', encoding='latin1')
df_estacoes = pd.read_csv(CAMINHO_ESTACOES_MUN)
df_ndvi = pd.read_csv(CAMINHO_NDVI)
print("✅ Leitura concluída.")

# -----------------------------------------------
# 4. TRATAMENTO DO INMET
# -----------------------------------------------

print("🔄 Tratando dados climáticos...")
df_clima.columns = df_clima.columns.str.strip().str.upper()

colunas_convertidas = {
    'PRECIPITAÇÃO TOTAL, HORÁRIO (MM)': 'CHUVA',
    'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)': 'TEMP_MED',
    'TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)': 'TEMP_MAX',
    'TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)': 'TEMP_MIN',
    'UMIDADE RELATIVA DO AR, HORARIA (%)': 'UMID_MED'
}

for col_original, col_novo in colunas_convertidas.items():
    if col_original in df_clima.columns:
        print(f"🔢 Convertendo coluna: {col_original} → {col_novo}")
        df_clima[col_novo] = (
            df_clima[col_original]
            .astype(str)
            .str.replace(",", ".", regex=False)
        )
        df_clima[col_novo] = pd.to_numeric(df_clima[col_novo], errors='coerce')

if 'DATA' not in df_clima.columns:
    print("❌ Coluna 'DATA' não encontrada.")
    sys.exit(1)

df_clima['DT_MEDICAO'] = pd.to_datetime(df_clima['DATA'], errors='coerce')
df_clima['ANO'] = df_clima['DT_MEDICAO'].dt.year
df_clima['MES'] = df_clima['DT_MEDICAO'].dt.month

df_clima = df_clima[df_clima['ANO'].between(2020, 2023)]
print(f"📊 Registros climáticos válidos (2020–2023): {len(df_clima)}")

# -----------------------------------------------
# 5. JUNÇÃO COM CD_MUN
# -----------------------------------------------

print("🔗 Associando CD_MUN às estações...")
df_clima = pd.merge(df_clima, df_estacoes[['CD_ESTACAO', 'CD_MUN']], on='CD_ESTACAO', how='left')
faltando = df_clima[df_clima['CD_MUN'].isnull()]
print(f"⚠️ Estações sem CD_MUN: {faltando['CD_ESTACAO'].nunique()}")
df_clima = df_clima.dropna(subset=['CD_MUN'])

# ✅ Corrige o problema do ".0" e zera à esquerda
df_clima['CD_MUN'] = df_clima['CD_MUN'].astype(str).str.replace('.0', '', regex=False).str.zfill(7)

# -----------------------------------------------
# 6. PREPARAÇÃO DO NDVI
# -----------------------------------------------

print("🧬 Tratando NDVI...")
df_ndvi['CD_MUN'] = df_ndvi['CD_MUN'].astype(str).str.zfill(7)

cd_mun_sp = df_clima['CD_MUN'].unique()
df_ndvi = df_ndvi[df_ndvi['CD_MUN'].isin(cd_mun_sp)]

df_ndvi.rename(columns={'mean': 'NDVI_MEDIO'}, inplace=True)
df_ndvi['ano'] = df_ndvi['ano'].astype(int)
df_ndvi['mes'] = df_ndvi['mes'].astype(int)

print(f"📈 NDVI filtrado para municípios SP: {df_ndvi['CD_MUN'].nunique()} municípios")

# -----------------------------------------------
# 7. JUNÇÃO FINAL CLIMA + NDVI
# -----------------------------------------------

print("🔀 Integrando dados climáticos com NDVI...")
df_merge = pd.merge(
    df_clima,
    df_ndvi[['CD_MUN', 'ano', 'mes', 'NDVI_MEDIO']],
    left_on=['CD_MUN', 'ANO', 'MES'],
    right_on=['CD_MUN', 'ano', 'mes'],
    how='inner'
)

print(f"✅ Registros integrados: {len(df_merge)}")

# -----------------------------------------------
# 8. SALVANDO RESULTADO FINAL
# -----------------------------------------------

df_merge.to_csv(CAMINHO_SAIDA, index=False)
print(f"\n💾 Arquivo salvo: {CAMINHO_SAIDA}")
print(f"📊 Total final de linhas: {len(df_merge)}")
