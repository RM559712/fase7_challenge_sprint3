# -----------------------------------------------
# SCRIPT: validar_outliers_dados.py
# OBJETIVO: Detectar e tratar valores ausentes ou outliers
#           nos dados climáticos + NDVI integrados
# AUTOR: Marco Franzoi
# -----------------------------------------------

import pandas as pd
from pathlib import Path

# -----------------------------------------------
# 1. CAMINHOS
# -----------------------------------------------

CAMINHO_INPUT = Path("/workspace/fase7_challenge_sprint3/dados/clima_ndvi_integrado.csv")
CAMINHO_OUTPUT = Path("/workspace/fase7_challenge_sprint3/dados/clima_ndvi_sem_outliers.csv")

# -----------------------------------------------
# 2. LEITURA DOS DADOS
# -----------------------------------------------

print("📥 Lendo dados...")
df = pd.read_csv(CAMINHO_INPUT)

print(f"✅ Total de registros originais: {len(df)}")

# -----------------------------------------------
# 3. TRATAMENTO DE VALORES AUSENTES
# -----------------------------------------------

# Remove linhas com campos críticos nulos
colunas_criticas = ['NDVI_MEDIO', 'TEMP_MED', 'TEMP_MAX', 'TEMP_MIN', 'CHUVA', 'UMID_MED']
colunas_presentes = [col for col in colunas_criticas if col in df.columns]

df = df.dropna(subset=colunas_presentes)

print(f"✅ Registros após remoção de ausentes: {len(df)}")

# -----------------------------------------------
# 4. DETECÇÃO E REMOÇÃO DE OUTLIERS
# -----------------------------------------------

def remover_outliers(df, coluna, min_val, max_val):
    original = len(df)
    df = df[(df[coluna] >= min_val) & (df[coluna] <= max_val)]
    print(f"🧪 {coluna}: removidos {original - len(df)} registros fora de [{min_val}, {max_val}]")
    return df

# Faixas aceitáveis (ajustável conforme necessidade)
limites = {
    'NDVI_MEDIO': (0.05, 1.0),     # NDVI varia de 0 a 1 (descarta negativos ou > 1.0)
    'TEMP_MED': (-10, 45),         # Temperatura média esperada
    'TEMP_MIN': (-15, 40),
    'TEMP_MAX': (-5, 50),
    'CHUVA': (0, 300),             # Precipitação diária normal
    'UMID_MED': (0, 100),          # Umidade relativa %
}

# Aplica filtros de outliers
for col, (min_v, max_v) in limites.items():
    if col in df.columns:
        df = remover_outliers(df, col, min_v, max_v)

# -----------------------------------------------
# 5. SALVA RESULTADO FINAL
# -----------------------------------------------

df.to_csv(CAMINHO_OUTPUT, index=False)
print(f"\n✅ Dados limpos salvos em: {CAMINHO_OUTPUT}")
print(f"📊 Total de registros finais: {len(df)}")
