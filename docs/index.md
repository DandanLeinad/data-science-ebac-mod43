---
title: LoL Win Predictor
description: Modelo de classificação para prever o vencedor de partidas ranqueadas de League of Legends aos 10 minutos de jogo.
---

# LoL Win Predictor

**Quem vai vencer, só com os dados do minuto 10?**

Projeto final do Módulo 43 (Case 03) — um modelo de classificação binária que prevê o vencedor de uma partida ranqueada de League of Legends a partir do estado do jogo por volta do **minuto 10**, para a Riot Games.

[:octicons-rocket-24: Ver o Simulador](05-simulador.md){ .md-button .md-button--primary }
[:octicons-mark-github-16: Repositório no GitHub](https://github.com/CHANGE-ME/projeto-final-mod43){ .md-button }

---

## Em números

<div class="grid cards" markdown>

- :material-chart-box-outline:{ .lg .middle } **0.807**

    ---

    AUC-ROC (cross-validation, 5 folds) do modelo campeão

- :material-scale-balance:{ .lg .middle } **9.879**

    ---

    Partidas ranqueadas analisadas, com o target quase perfeitamente balanceado (50,1% / 49,9%)

- :material-filter-variant:{ .lg .middle } **39 → 5**

    ---

    Das 39 features usadas no treino, o modelo tunado (L1) considerou apenas **5** realmente decisivas

- :material-target:{ .lg .middle } **0.32**

    ---

    Threshold de decisão operacional, otimizado para F1-Score (não o padrão 0.5)

</div>

---

## O que tem aqui

<div class="grid cards" markdown>

- :material-flag-outline:{ .lg .middle } **O Desafio**

    ---

    O briefing original da Bárbara Martinelli (Tech Lead, Riot Games) e os critérios do case.

    [:octicons-arrow-right-24: Ler o desafio](01-contexto.md)

- :material-database-search-outline:{ .lg .middle } **Dados & Exploração**

    ---

    De onde vêm os dados, como estão distribuídos, e o que a análise exploratória revelou.

    [:octicons-arrow-right-24: Explorar os dados](02-dados.md)

- :material-cog-outline:{ .lg .middle } **Modelagem**

    ---

    Limpeza, engenharia de features e a comparação entre 5 modelos de classificação.

    [:octicons-arrow-right-24: Ver a modelagem](03-modelagem.md)

- :material-trophy-outline:{ .lg .middle } **Modelo Final**

    ---

    O modelo campeão, suas métricas, e a descoberta mais interessante do projeto.

    [:octicons-arrow-right-24: Ver os resultados](04-resultados.md)

- :material-gamepad-variant-outline:{ .lg .middle } **Simulador**

    ---

    Um app interativo: monte um cenário de partida e veja a previsão em tempo real.

    [:octicons-arrow-right-24: Abrir o simulador](05-simulador.md)

- :material-notebook-outline:{ .lg .middle } **Notebook completo**

    ---

    Toda a análise, célula a célula, documentada e reprodutível.

    [:octicons-arrow-right-24: Ver no GitHub](https://github.com/CHANGE-ME/projeto-final-mod43/blob/main/lol_match_winner_prediction.ipynb)

</div>

!!! info "Stakeholder"
    Este projeto foi desenvolvido para **Bárbara Martinelli**, Tech Lead (fictícia) na Riot Games, como parte do Case 03 do Módulo 43 de Ciência de Dados.
