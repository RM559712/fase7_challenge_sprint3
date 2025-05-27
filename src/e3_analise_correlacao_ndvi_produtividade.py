# -----------------------------------------------
# SCRIPT: e3_analise_correlacao_ndvi_produtividade.py
# OBJETIVO: Calcular correlações e regressão entre NDVI e produtividade
# AUTOR: Marco Franzoi
# -----------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from pathlib import Path

# -----------------------------------------------
# 1. CAMINHOS
# -----------------------------------------------

CAMINHO_DADOS = "/workspace/fase7_challenge_sprint3/dados/produtividade_clima_ndvi.csv"
PASTA_GRAFICOS = Path("/workspace/fase7_challenge_sprint3/graficos")
PASTA_GRAFICOS.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------
# 2. LEITURA DOS DADOS
# -----------------------------------------------

print("📥 Lendo dados...")
df = pd.read_csv(CAMINHO_DADOS, sep=";")
df.columns = df.columns.str.strip()

col_ndvi = "NDVI_MEDIO"
col_prod = "Produtividade (ton/ha)"

df = df.dropna(subset=[col_ndvi, col_prod])
print(f"✅ Total de registros válidos: {len(df)}")

# -----------------------------------------------
# 3. CORRELAÇÃO
# -----------------------------------------------

print("\n📊 Correlação entre NDVI médio e produtividade:")

pearson_corr, p_pearson = pearsonr(df[col_ndvi], df[col_prod])
print(f"🔹 Pearson: r = {pearson_corr:.3f}, p = {p_pearson:.5f}")

spearman_corr, p_spearman = spearmanr(df[col_ndvi], df[col_prod])
print(f"🔸 Spearman: r = {spearman_corr:.3f}, p = {p_spearman:.5f}")

def interpreta(r):
    if abs(r) >= 0.7:
        return "forte"
    elif abs(r) >= 0.4:
        return "moderada"
    else:
        return "fraca"

print(f"📈 Interpretação Pearson: {interpreta(pearson_corr)}")
print(f"📈 Interpretação Spearman: {interpreta(spearman_corr)}")

# -----------------------------------------------
# 4. REGRESSÃO LINEAR
# -----------------------------------------------

print("\n📐 Regressão linear simples NDVI → Produtividade...")
X = df[[col_ndvi]]
y = df[col_prod]

modelo = LinearRegression()
modelo.fit(X, y)

y_pred = modelo.predict(X)
r2 = r2_score(y, y_pred)

print(f"🔺 Equação: produtividade = {modelo.coef_[0]:.2f} * NDVI + {modelo.intercept_:.2f}")
print(f"🔹 R² (coef. de determinação): {r2:.3f}")

# -----------------------------------------------
# 5. GRÁFICO DE DISPERSÃO
# -----------------------------------------------

plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x=col_ndvi, y=col_prod)
plt.plot(df[col_ndvi], y_pred, color="red", label="Regressão Linear")
plt.title("NDVI vs Produtividade")
plt.xlabel("NDVI Médio")
plt.ylabel("Produtividade (ton/ha)")
plt.legend()
plt.grid(True)
plt.tight_layout()
grafico_disp = PASTA_GRAFICOS / "e3_grafico_dispersion_ndvi_produtividade.png"
plt.savefig(grafico_disp)
print(f"📸 Gráfico salvo: {grafico_disp}")

# -----------------------------------------------
# 6. GRÁFICO BOX PLOT POR ANO
# -----------------------------------------------

plt.figure(figsize=(10, 5))
sns.boxplot(data=df, x="Ano", y=col_prod)
plt.title("Distribuição da produtividade por ano")
plt.grid(True)
plt.tight_layout()
grafico_box = PASTA_GRAFICOS / "e3_grafico_box_ano.png"
plt.savefig(grafico_box)
print(f"📸 Gráfico salvo: {grafico_box}")
