import pandas as pd
from pathlib import Path
from datetime import datetime

# Diretório onde estão os arquivos
data_dir = Path("../dados")

# Lista os arquivos no padrão esperado
arquivos = list(data_dir.glob("canadeacucar_long_final_*.csv"))
if not arquivos:
    raise FileNotFoundError("❌ Nenhum arquivo 'canadeacucar_long_final_*.csv' encontrado em ../dados")

# Ordena pelos nomes e pega o mais recente
arquivo_mais_novo = sorted(arquivos)[-1]
print(f"📄 Usando arquivo mais recente: {arquivo_mais_novo.name}")

# Lê o arquivo
df = pd.read_csv(arquivo_mais_novo, sep=";")

# Padroniza código de município
df["Cod Municipio"] = df["Cod Municipio"].astype(str).str.zfill(7)

# Expande para 12 meses
df_expanded = df.loc[df.index.repeat(12)].copy()
df_expanded["Mes"] = df_expanded.groupby(["Ano", "Cod Municipio"]).cumcount() + 1

# Interpolação mensal
df_expanded["Produtividade (ton/ha)"] = df_expanded["Produtividade (ton/ha)"] / 12

# Cria coluna Ano-Mes
df_expanded["Ano-Mes"] = pd.to_datetime(
    df_expanded["Ano"].astype(str) + "-" + df_expanded["Mes"].astype(str).str.zfill(2)
)

# Reorganiza colunas
df_final = df_expanded[
    ["Ano", "Mes", "Ano-Mes", "Cod Municipio", "Nome Municipio", "Produtividade (ton/ha)"]
]

# Salva com timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
output_path = data_dir / f"produtividade_cana_mensal_{timestamp}.csv"
df_final.to_csv(output_path, sep=";", index=False)

print(f"✅ Arquivo salvo: {output_path.name}")
