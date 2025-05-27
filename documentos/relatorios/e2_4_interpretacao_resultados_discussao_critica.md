## Etapa 4 – Interpretação dos Resultados e Discussão Crítica

---

### 1. O NDVI foi um bom preditor da produtividade?

De forma geral, **o NDVI não se mostrou um preditor confiável** da produtividade agrícola da cana-de-açúcar quando utilizado isoladamente.  
Os testes estatísticos revelaram:

- **Correlação de Pearson:** -0.302 → fraca
- **Correlação de Spearman:** -0.456 → moderada (negativa)
- **Regressão linear simples (R²):** 0.091 → o modelo explica apenas 9,1% da variação da produtividade

---

### 2. Em que situações o modelo teve melhor ou pior desempenho?

#### 🟢 Melhor desempenho:
- Municípios como **Avaré** e **Bebedouro** apresentaram **forte correlação positiva**, indicando que em certas regiões o NDVI pode estar mais alinhado com a produtividade real.

#### 🔴 Pior desempenho:
- Municípios como **Itapira**, **Bauru** e **São Simão** tiveram correlação negativa forte, mostrando que NDVI alto não necessariamente significou produtividade alta — o que pode indicar presença de outras variáveis críticas não modeladas.

---

### 3. Fatores externos que podem ter influenciado os resultados

- **Eventos climáticos:**  
  Geadas, estiagens e chuvas irregulares registradas em SP durante os anos de 2021 e 2022 não foram modeladas diretamente, mas certamente impactaram a produtividade agrícola.

- **Pragas e doenças agrícolas:**  
  A ausência de dados fitossanitários impede avaliar o impacto de infestações ou doenças sobre os rendimentos.

- **Pandemia de COVID-19:**  
  Durante 2020 e 2021, o Brasil — e especialmente o estado de São Paulo — sofreu com os efeitos da pandemia, que podem ter influenciado negativamente a produtividade agrícola devido a:
  - Redução da força de trabalho no campo
  - Dificuldade logística de insumos e transporte
  - Possíveis atrasos ou falhas no manejo da cultura

- **Qualidade das imagens NDVI:**  
  O modelo utilizou a coleção **MODIS/061/MOD13Q1** com 250m de resolução, o que pode ter causado **mistura de pixels agrícolas com vegetação nativa ou áreas urbanas**, distorcendo o NDVI médio por município.

---

### 4. Sugestões de melhorias para o modelo de IA

- ✅ **Incluir novos dados climáticos e ambientais** como:
  - Precipitação acumulada
  - Temperatura média
  - Umidade do solo
  - Índices como EVI ou evapotranspiração

- ✅ **Melhorar o tratamento das imagens**:
  - Utilizar imagens Sentinel-2 com 10m de resolução
  - Aplicar filtros para remoção de nuvens e correção atmosférica

- ✅ **Ajustar o período de coleta do NDVI**:
  - Ao invés da média mensal, usar o **NDVI máximo da safra**
  - Ou aplicar uma **média acumulada entre meses críticos da cultura**

---

### 5. Limitações da análise

- **Tamanho da amostra:**  
  A análise foi baseada em apenas **132 registros válidos**, o que limita a robustez estatística.

- **Qualidade das bases públicas:**  
  Estações do INMET com falhas de cobertura e inconsistências em alguns arquivos CSV demandaram pré-processamento manual.

- **Modelo estatístico simples:**  
  Foi utilizada **regressão linear simples**, o que não captura relações complexas entre múltiplas variáveis.

---

### ✅ Conclusão

Mesmo com as limitações, esta Sprint cumpriu seu papel de **validar criticamente a proposta de modelo de IA aplicada à agricultura de precisão**, destacando caminhos promissores para futuras melhorias e demonstrando na prática a importância do rigor estatístico na modelagem preditiva.
