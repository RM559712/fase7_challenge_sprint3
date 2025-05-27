## Etapa 1 – Coleta de Dados de Produtividade Histórica

Nesta primeira etapa da Sprint 3, o foco foi a **pesquisa e consolidação de bases públicas** com dados históricos de produtividade agrícola.

### 🔍 Fontes de dados consultadas:
- **IBGE (Instituto Brasileiro de Geografia e Estatística)** – SIDRA
- **CONAB (Companhia Nacional de Abastecimento)** – (não utilizada diretamente nesta Sprint)
- **MAPA** e **CEPEA/USP** – considerados, mas sem dados diretos no escopo desta Sprint

### 🌱 Cultura selecionada:
- **Cana-de-açúcar**  
  Mantivemos a mesma cultura agrícola analisada nas Sprints anteriores, garantindo consistência na abordagem.

### 🗂 Informações coletadas:
- **Produtividade média (toneladas por hectare)** por município
- **Ano agrícola:** 2020, 2021, 2022, 2023
- **Códigos e nomes dos municípios** para integrar com outras bases (NDVI, clima)
- **Condições regionais:** contextualizadas na Etapa 4 (interpretação crítica)

---

### ⚙️ Organização dos scripts utilizados nesta etapa

Para padronizar os dados de produtividade histórica da cana-de-açúcar e transformá-los em um formato compatível com análise de séries temporais e integração com NDVI, desenvolvemos os seguintes scripts:

#### 🔧 `convert_full_csv_to_long_final.py`
- Responsável por converter a base original da produtividade (formato wide, com colunas por ano) para o formato **long**, com uma linha por município por ano.
- O script:
  - Renomeia colunas com nomes padronizados dos anos
  - Trata valores ausentes e inválidos (ex: '-', 'X', '..')
  - Converte dados para ponto flutuante (`float`)
  - Padroniza o código do município para 7 dígitos
  - Exporta o resultado com o nome `canadeacucar_long_final_<timestamp>.csv`

#### 🧪 Validação
- Verificamos se os dados estavam coerentes em relação a anos, municípios e formato
- O dataset final serviu de base para a etapa seguinte de correlação com NDVI e variáveis climáticas

Este processo garantiu que os dados estivessem prontos para unificação e análise estatística, mantendo qualidade e estrutura adequada para regressão, correlação e visualizações futuras.
