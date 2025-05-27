# -----------------------------------------------
# SCRIPT: integrar_produtividade_com_clima_ndvi.py
# OBJETIVO: Integrar produtividade da cana com dados de NDVI e clima
#           por município e ano (2020 a 2023)
# AUTOR: Marco Franzoi
# -----------------------------------------------

import pandas as pd
from pathlib import Path
import glob

# -----------------------------------------------
# 1. CAMINHOS DOS ARQUIVOS
# -----------------------------------------------

CAMINHO_CLIMA_NDVI = Path("/workspace/fase7_challenge_sprint3/dados/clima_ndvi_integrado.csv")
PASTA_PRODUTIVIDADE = Path("/workspace/fase7_challenge_sprint3/dados")
CAMINHO_SAIDA = Path("/workspace/fase7_challenge_sprint3/dados/produtividade_clima_ndvi.csv")

# -----------------------------------------------
# 2. IDENTIFICA O ARQUIVO MAIS RECENTE DE PRODUTIVIDADE
# -----------------------------------------------

arquivos_prod = sorted(
    glob.glob(str(PASTA_PRODUTIVIDADE / "canadeacucar_long_final_*.csv")),
    reverse=True
)

if not arquivos_prod:
    print("❌ Nenhum arquivo de produtividade encontrado com padrão 'canadeacucar_long_final_*.csv'")
    exit(1)

CAMINHO_PRODUTIVIDADE = arquivos_prod[0]
print(f"📄 Usando arquivo de produtividade: {CAMINHO_PRODUTIVIDADE}")

# -----------------------------------------------
# 3. LEITURA DOS DADOS
# -----------------------------------------------

df_prod = pd.read_csv(CAMINHO_PRODUTIVIDADE, sep=";", encoding="utf-8-sig")
df_clima = pd.read_csv(CAMINHO_CLIMA_NDVI, dtype={"CD_MUN": str})  # <- corrigido aqui

# Padroniza tipos
df_prod["Cod Municipio"] = df_prod["Cod Municipio"].astype(str).str.zfill(7)
df_clima["CD_MUN"] = df_clima["CD_MUN"].astype(str).str.zfill(7)

# -----------------------------------------------
# 4. AGREGA MÉDIAS MENSAIS → ANUAL POR MUNICÍPIO
# -----------------------------------------------

colunas_meteorologicas = ["NDVI_MEDIO", "TEMP_MED", "CHUVA", "UMID_MED"]
colunas_existentes = [col for col in colunas_meteorologicas if col in df_clima.columns]

df_agg = df_clima.groupby(["CD_MUN", "ANO"], as_index=False)[colunas_existentes].mean()

# -----------------------------------------------
# 5. MERGE COM PRODUTIVIDADE
# -----------------------------------------------

print("🔗 Integrando produtividade com médias climáticas e NDVI...")
df_merge = pd.merge(
    df_prod,
    df_agg,
    left_on=["Cod Municipio", "Ano"],
    right_on=["CD_MUN", "ANO"],
    how="inner"
)

print(f"✅ Registros integrados: {len(df_merge)}")

# -----------------------------------------------
# 6. SALVA RESULTADO FINAL
# -----------------------------------------------

df_merge.to_csv(CAMINHO_SAIDA, sep=";", index=False, encoding="utf-8-sig")
print(f"\n💾 Arquivo salvo: {CAMINHO_SAIDA}")
print(f"📊 Total de linhas: {len(df_merge)}")
