# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href="https://www.fiap.com.br/">
  <img src="assets/images/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width="40%" height="40%">
</a>
</p>

---

# 🧠 Enterprise Challenge - Sprint 3 - Ingredion  
## Validação do Modelo de IA com Dados Reais de Produtividade Agrícola

---

## 👨‍👩 Grupo

Grupo de número **46** formado pelos integrantes mencionados abaixo.

### 👨‍🎓 Integrantes:
- [Ciro Henrique](https://www.linkedin.com/in/cirohenrique/) – *RM559040*
- [Marco Franzoi](https://www.linkedin.com/in/marcofranzoi/) – *RM559468*
- [Rodrigo Mazuco](https://www.linkedin.com/in/rodrigo-mazuco-16749b37/) – *RM559712*

### 👩‍🏫 Professores:
- **Tutor:** [Leonardo Ruiz Orabona](https://www.linkedin.com/in/leonardoorabona/)
- **Coordenador:** [André Godoi](https://www.linkedin.com/in/profandregodoi/)

---

## 📜 Descrição do Desafio

Nesta Sprint, o grupo teve como missão **validar o modelo de IA desenvolvido na Sprint 2**, comparando as previsões de produtividade agrícola baseadas em NDVI com **dados reais históricos** obtidos de fontes públicas como IBGE e CONAB.

Foram aplicadas técnicas estatísticas para medir a aderência entre as previsões do modelo e os dados reais, utilizando correlação, regressão e análise gráfica.

Referência do desafio: [Link para o enunciado](https://on.fiap.com.br/mod/assign/view.php?id=488636&c=13085)

---

## 🔬 Metodologia

1. **Coleta de Dados Reais**
   - Cultura analisada: **Cana-de-açúcar**
   - Fontes: IBGE, CONAB

2. **Tratamento de Dados**
   - Alinhamento temporal com os dados de NDVI
   - Normalização e organização por safra

3. **Análise Estatística**
   - Correlação de Pearson e Spearman
   - Regressão linear simples
   - Coeficiente de determinação (R²)

4. **Visualização**
   - Geração de gráficos de dispersão
   - Comparação entre NDVI médio e produtividade real

5. **Discussão Crítica**
   - Avaliação da confiabilidade do modelo
   - Sugestões de melhorias

---

# Informações Importantes - Dados SIDRA

Para o arquivo de dados coletado do SIDRA, foi percebido que entre os anos de 2020 a 2023 (Ultima data mais atualizada) 
haviam alguns municipios que não determinaram ou passaram suas informacoes para o IBGE. 
Segue abaixo um levantamento

📊 Análise de Dados Presentes e Faltantes 

- Ano 2020
-- Registros esperados - 5563
-- Registros presentes - 3302
-- Registros Faltantes - 2261

- Ano 2021
-- Registros esperados - 5563
-- Registros presentes - 3186
-- Registros Faltantes - 2377

- Ano 2022
-- Registros esperados - 5563
-- Registros presentes - 3172
-- Registros Faltantes - 2391

- Ano 2023
-- Registros esperados - 5563
-- Registros presentes - 3169
-- Registros Faltantes - 2394

<img src="assets/images/Percent_dados_Faltantes_SIDRA_CANA.png" alt="Percentual de Dados Faltantes por Ano (Cana-de-açucar)" border="0" width="40%" height="40%">

❌ Motivos dos dados faltantes (2.261 a 2.394 por ano):
'...': Valor não disponível (não pesquisado)
'..': Valor não se aplica (unidades diferentes)
'X': Valor inibido por sigilo estatístico
'-': Zero absoluto (registrado como ausente)
'A'–'Z': Faixas qualitativas que não representam um valor numérico direto