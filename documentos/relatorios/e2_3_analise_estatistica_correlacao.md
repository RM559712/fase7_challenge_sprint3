## Etapa 3 – Sugestões de Análise Estatística e Correlação

Nesta etapa, realizamos as análises estatísticas propostas para investigar a relação entre o **NDVI médio** e a **produtividade agrícola real** da cana-de-açúcar entre os anos de 2020 e 2023, no estado de São Paulo.

---

### 📊 Testes de correlação aplicados

Foram aplicadas duas técnicas estatísticas para medir a correlação entre as variáveis:

- **Correlação de Pearson (linear):** r = **-0.302**, p = 0.00043  
  → Interpretação: **fraca correlação negativa**

- **Correlação de Spearman (monótona):** r = **-0.456**, p < 0.00001  
  → Interpretação: **moderada correlação negativa**

---

### 📐 Regressão linear simples

Também foi ajustado um modelo de regressão linear simples para avaliar a capacidade do NDVI em prever a produtividade agrícola:

- **Equação da regressão:**  
  `Produtividade = -8.46 * NDVI + 68393.12`

- **Coeficiente de determinação (R²):**  
  `0.091` → O modelo explica apenas **9,1% da variância da produtividade**

---

### 🧭 Análise por município

Executamos uma correlação de Spearman individual por município para identificar padrões regionais:

- **Total de municípios analisados:** 26

#### 🟢 Top 5 correlação positiva:
- Avaré (SP): **0.95**
- Bebedouro (SP): **0.87**
- Rancharia (SP): 0.60
- José Bonifácio (SP): 0.45
- Bragança Paulista (SP): 0.45

#### 🔴 Top 5 correlação negativa:
- Itapira (SP): **-0.80**
- Bauru (SP): -0.80
- São Simão (SP): -0.77
- Cachoeira Paulista (SP): -0.77
- São Luiz do Paraitinga (SP): -0.77

---

### 📈 Gráficos produzidos

#### 1. Correlação de Spearman por município:
![Gráfico de correlação por município](../graficos/e3_correlacao_por_municipio.png)

#### 2. Distribuição da produtividade por ano:
![Boxplot produtividade por ano](../graficos/e3_grafico_box_ano.png)

#### 3. Dispersão NDVI × produtividade com linha de tendência:
![Dispersão NDVI vs Produtividade](../graficos/e3_grafico_dispersion_ndvi_produtividade.png)

---

### ✅ Conclusão

Embora o NDVI mostre alguma correlação com a produtividade em certos municípios, ele não é um preditor confiável de forma isolada para todo o estado. O modelo linear simples apresenta limitações claras, mas os resultados fornecem uma base sólida para futuras melhorias com variáveis adicionais ou modelos mais robustos.
