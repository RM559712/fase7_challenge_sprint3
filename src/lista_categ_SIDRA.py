import requests

def listar_categorias_classificacao(cod_classificacao="112"):
    url = f"https://apisidra.ibge.gov.br/classifications/{cod_classificacao}/categories"

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erro ao acessar a API: {response.status_code}")
        return

    data = response.json()

    print(f"✅ Categorias da classificação {cod_classificacao}:\n")
    for item in data:
        print(f"{item['nome']} → {item['id']}")
    
    return {item["nome"]: item["id"] for item in data}

# Rodar
if __name__ == "__main__":
    categorias = listar_categorias_classificacao("112")
