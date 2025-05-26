import pandas as pd
from pathlib import Path
from datetime import datetime

# Caminho do arquivo original
input_path = Path("/workspace/fase7_challenge_sprint3/dados/canadeacucar_2020_2023_temp_cleaned.csv")

# Leitura do arquivo com separador e encoding BR
df = pd.read_csv(input_path, sep=";", encoding="utf-8")

# Renomeia as colunas dos anos para facilitar o tratamento
col_renames = {
    "Ano 2020 em Hectares": "2020",
    "Ano 2021 em Hectares": "2021",
    "Ano 2022 em Hectares": "2022",
    "Ano 2023 em Hectares": "2023",
}
df.rename(columns=col_renames, inplace=True)

# Lista das colunas de produtividade
year_cols = ["2020", "2021", "2022", "2023"]

# Limpeza dos valores: trata símbolos especiais e converte para float
for col in year_cols:
    df[col] = (
        df[col]
        .replace({"-": "0", "X": None, "..": None, "...": None})
        .replace(r"^[A-WYZ]$", None, regex=True)  # Remove letras A-Z (exceto X já tratado)
        .astype(str)
        .str.replace(",", ".", regex=False)       # Converte decimal BR para ponto
    )
    df[col] = pd.to_numeric(df[col], errors="coerce")  # Converte para float

# Padroniza o código do município com 7 dígitos
df["Cod Municipio"] = df["Cod Municipio"].astype(str).str.zfill(7)

# Transforma o dataframe de wide para long
df_long = df.melt(
    id_vars=["Cod Municipio", "Nome Municipio"],
    value_vars=year_cols,
    var_name="Ano",
    value_name="Produtividade (ton/ha)"
)

# Ajusta tipos e ordena
df_long["Ano"] = df_long["Ano"].astype(int)
df_long = df_long[["Ano", "Cod Municipio", "Nome Municipio", "Produtividade (ton/ha)"]]
df_long.sort_values(by=["Cod Municipio", "Ano"], inplace=True)

# Gera timestamp e salva arquivo
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
output_path = Path(f"/workspace/fase7_challenge_sprint3/dados/canadeacucar_long_final_{timestamp}.csv")
df_long.to_csv(output_path, sep=";", index=False)

print(f"✅ Arquivo salvo: {output_path}")
