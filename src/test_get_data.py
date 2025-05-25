import os
import requests
import pandas as pd

CULTURAS = {
    "6872": "cana-de-açúcar",
    "7452": "milho (em grão)",
    "7581": "soja (em grão)",
    "6612": "arroz (em casca)",
    "6450": "algodão herbáceo (em caroço)",
    "6469": "feijão (em grão) 1ª safra",
    "6470": "feijão (em grão) 2ª safra",
    "6471": "feijão (em grão) 3ª safra",
    "7583": "sorgo (em grão)",
    "7593": "trigo (em grão)"
}

def montar_url(codigo_cultura, anos, usar_classificacao=True):
    base = f"https://apisidra.ibge.gov.br/values/t/1612/n2/all/v/214/p/{anos}"
    if usar_classificacao:
        return f"{base}/c112/{codigo_cultura}"
    return base

def baixar_dados_ibge(codigo_cultura, anos):
    nome_cultura = CULTURAS.get(codigo_cultura, "desconhecida")

    # 1ª tentativa: com filtro da classificação
    url = montar_url(codigo_cultura, anos, usar_classificacao=True)
    print(f"🔄 Tentando com classificação: {url}")
    response = requests.get(url)

    if response.status_code != 200:
        print(f"⚠️ Erro {response.status_code} com filtro. Tentando sem classificação...")

        # 2ª tentativa: sem filtro (filtro por pandas depois)
        url = montar_url(codigo_cultura, anos, usar_classificacao=False)
        print(f"🔄 Tentando sem classificação: {url}")
        response = requests.get(url)

        if response.status_code != 200:
            print(f"❌ Erro crítico ao acessar a API do SIDRA: {response.status_code}")
            return

    data = response.json()

    if len(data) <= 1:
        print("⚠️ Nenhum dado retornado pela API.")
        return

    df = pd.DataFrame(data[1:])  # pula cabeçalho

    # Se vier tudo, filtrar por nome da cultura
    if "D4C" in df.columns and df["D4C"].nunique() > 1:
        df = df[df["D4C"] == codigo_cultura]

    if df.empty:
        print("⚠️ Nenhum dado encontrado para essa cultura nesse período.")
        return

    safe_name = nome_cultura.replace(" ", "_").replace("ã", "a").replace("ç", "c").lower()
    filename = f"produtividade_{safe_name}_{anos.replace('-', '_')}.csv"
    output_path = os.path.join("..", "dados", filename)
    df.to_csv(output_path, index=False, encoding='utf-8')

    print(f"\n✅ Dados salvos em: {output_path}")
    print(f"📈 Total de registros: {len(df)}")

# Execução interativa
if __name__ == "__main__":
    print("\n🌾 Códigos disponíveis:")
    for cod, nome in CULTURAS.items():
        print(f" {cod} → {nome}")

    cod_cultura = input("\nDigite o código da cultura (ex: 6872): ").strip()
    anos = input("Digite o período (ex: 2020-2023): ").strip()
    if not anos:
        anos = "2020-2023"

    baixar_dados_ibge(cod_cultura, anos)
