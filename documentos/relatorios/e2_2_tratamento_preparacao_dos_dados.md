## Etapa 2 – Tratamento e Preparação dos Dados

Nesta etapa, o objetivo foi organizar e padronizar os dados para viabilizar análises estatísticas comparáveis entre produtividade real e NDVI médio, com foco na cultura da cana-de-açúcar no estado de São Paulo.

---

### 📐 Estruturação dos dados

Foram organizadas colunas compatíveis para posterior unificação:
- **Produtividade agrícola real** (toneladas por hectare)
- **NDVI médio mensal por município**
- **Ano e mês como base temporal comum**

---

### 🧭 Ajustes e padronizações realizadas

- Conversão de todos os códigos de município para **7 dígitos (formato IBGE)**
- Conversão dos dados de **NDVI e produtividade para tipo numérico (float)**
- Alinhamento da escala temporal entre os datasets:
  - Todos os dados utilizados estão no intervalo de **2020 a 2023**
- Remoção de registros com valores ausentes ou inválidos
- Garantia de consistência por meio de validações cruzadas entre os datasets

---

### 🛰️ Integração com Google Earth Engine (NDVI via MODIS)

Um dos principais diferenciais técnicos desta etapa foi a **integração com o Earth Engine (GEE)** para coleta do NDVI mensal médio por município. Para isso:

#### 🔧 Script utilizado:
- **`extrair_nvdi_mensal.py`**
  - Inicializa o GEE com autenticação por projeto
  - Utiliza a coleção **MODIS/061/MOD13Q1** com resolução de 250m
  - Reduz as imagens por **média mensal de NDVI por município**
  - Exporta o resultado como arquivo `.csv` para integração local
  - Dados organizados com `ano`, `mês`, `CD_MUN` e `NDVI_MEDIO`

Essa abordagem garantiu maior qualidade, periodicidade padronizada e alinhamento espacial com os dados públicos de produtividade.

---

### ⚙️ Unificação e preparação final dos dados

Para consolidar os dados em um único arquivo integrado, foram utilizados os seguintes scripts:

#### 🔧 `mapear_estacoes_inmet.py`
- Extraiu metadados (nome, código, latitude, longitude) das estações meteorológicas do INMET

#### 🔧 `map_estacao_metereologica_ibge.py`
- Realizou o cruzamento espacial das estações com os municípios do shapefile do IBGE, associando cada estação ao código `CD_MUN`

#### 🔧 `integrar_clima_ndvi_sp.py`
- Unificou os dados do INMET com o NDVI mensal por município
- Validou o cruzamento por ano e mês
- Exportou o resultado como `clima_ndvi_integrado.csv`

#### 🔧 `integrar_produtividade_com_clima_ndvi.py`
- Realizou a junção final com a produtividade agrícola, resultando em:
  - **NDVI médio**
  - **Clima médio (chuva, temperatura, umidade)**
  - **Produtividade agrícola real**

---

### ✅ Resultado

Ao final da Etapa 2, os dados foram tratados, padronizados e integrados com sucesso em um único dataset, prontos para análises estatísticas e visualizações avançadas.
