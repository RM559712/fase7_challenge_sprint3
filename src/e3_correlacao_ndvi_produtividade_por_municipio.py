# -----------------------------------------------
# SCRIPT: e3_correlacao_ndvi_produtividade_por_municipio.py
# OBJETIVO: Calcular correlação de Spearman entre NDVI e produtividade por município
# AUTOR: Marco Franzoi
# -----------------------------------------------

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
from pathlib import Path

# -----------------------------------------------
# 1. CAMINHOS
# -----------------------------------------------

CAMINHO_DADOS = "/workspace/fase7_challenge_sprint3/dados/produtividade_clima_ndvi.csv"
PASTA_GRAFICOS = Path("/workspace/fase7_challenge_sprint3/graficos")
PASTA_GRAFICOS.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------
# 2. LEITURA E PREPARAÇÃO
# -----------------------------------------------

print("📥 Lendo dados...")
df = pd.read_csv(CAMINHO_DADOS, sep=";")
df.columns = df.columns.str.strip()

col_ndvi = "NDVI_MEDIO"
col_prod = "Produtividade (ton/ha)"
col_mun = "Nome Municipio"

df = df.dropna(subset=[col_ndvi, col_prod, col_mun])
print(f"✅ Total de registros válidos: {len(df)}")

# -----------------------------------------------
# 3. CÁLCULO DE CORRELAÇÃO POR MUNICÍPIO
# -----------------------------------------------

print("📊 Calculando correlação de Spearman por município...")

resultados = []

for municipio, grupo in df.groupby(col_mun):
    if len(grupo) >= 2:
        r, p = spearmanr(grupo[col_ndvi], grupo[col_prod])
        resultados.append({
            "Nome Municipio": municipio,
            "Spearman": r,
            "P-valor": p,
            "Total Anos": len(grupo)
        })

df_corr = pd.DataFrame(resultados).dropna().sort_values("Spearman", ascending=False)

print(f"📈 Municípios analisados: {len(df_corr)}")

# -----------------------------------------------
# 4. EXIBIÇÃO DOS EXTREMOS
# -----------------------------------------------

print("\n🏅 Top 5 correlação positiva:")
print(df_corr.head(5)[["Nome Municipio", "Spearman"]])

print("\n🚨 Top 5 correlação negativa:")
print(df_corr.tail(5)[["Nome Municipio", "Spearman"]])

# -----------------------------------------------
# 5. GRÁFICO
# -----------------------------------------------

top_grafico = df_corr.sort_values("Spearman")
plt.figure(figsize=(12, 6))
sns.barplot(data=top_grafico, x="Spearman", y="Nome Municipio", palette="coolwarm")
plt.title("Correlação de Spearman NDVI x Produtividade por Município")
plt.xlabel("Coeficiente de Spearman")
plt.ylabel("Município")
plt.grid(True)
plt.tight_layout()

saida_grafico = PASTA_GRAFICOS / "e3_correlacao_por_municipio.png"
plt.savefig(saida_grafico)
print(f"\n📸 Gráfico salvo: {saida_grafico}")
