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

## 📁 Estrutura de Pastas

FASE7_CHALLENGE_SPRINT3/
├── assets/
│ ├── graficos/ # Gráficos gerados pela análise
│ └── images/ # Imagens auxiliares (ex: logo)
├── config/ # Arquivos JSON de configuração
├── document/
│ └── relatorios/ # Relatório técnico (PDF e DOCX)
├── scripts/ # Scripts utilitários
├── src/ # Código-fonte da análise
├── requirements.txt # Bibliotecas Python utilizadas
└── README.md # Este arquivo

### 📈 Resultados e Entregáveis

- 📊 **Gráficos de correlação**  
  Localizados em: `assets/graficos/`  
  - Gráfico de dispersão entre NDVI e produtividade real  
  - Linha de tendência da regressão linear  
  - Gráficos por safra ou por região (se aplicável)

- 📝 **Relatório Técnico Final**  
  Local: `document/relatorios/relatorio_sprint3.pdf`  
  Conteúdo:
  - Metodologia de coleta de dados
  - Técnicas estatísticas utilizadas
  - Análise dos gráficos
  - Discussão crítica dos resultados
  - Referências bibliográficas

- 💻 **Código-fonte da análise**  
  Local: `src/analise_ndvi_cana.py`  
  Funcionalidades:
  - Leitura dos dados
  - Análise estatística (correlação e regressão)
  - Geração de gráficos e exportação

- 📦 **Repositório GitHub**  
  Contém o projeto completo, com documentação, código e relatório para reprodutibilidade.

---

### 📚 Referências

- [IBGE – sidra.ibge.gov.br](https://sidra.ibge.gov.br)
- [CONAB – conab.gov.br](https://www.conab.gov.br)
- [MAPA – gov.br/agricultura](https://www.gov.br/agricultura)
- [CEPEA/USP – cepea.esalq.usp.br](https://www.cepea.esalq.usp.br)

---

### 📋 Licença

Desenvolvido pelo **Grupo 46** para o projeto da Fase 7  
(*Enterprise Challenge - Sprint 3 - Ingredion*) da [FIAP](https://fiap.com.br).

Este projeto está licenciado sob a licença  
[Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1).
