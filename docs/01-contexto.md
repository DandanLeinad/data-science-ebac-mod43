---
title: O Desafio
description: O briefing do case, direto da stakeholder.
---

# O Desafio

## O briefing

O desafio foi apresentado por **Bárbara Martinelli**, Tech Lead (fictícia) na Riot Games, como parte do Case 03 do Módulo 43:

!!! quote "Bárbara Martinelli — Tech Lead, Riot Games"
    Como vocês sabem, no LoL a dinâmica de jogo é extremamente complexa. Cada decisão, desde o first blood até a conquista de torres e dragões, influencia no resultado da partida.

    Nós temos uma base de dados que registra diversas partidas de League of Legends, contendo informações valiosas como o desempenho de cada equipe após o início do jogo — quem conseguiu o first blood, quem destruiu a primeira torre, quem matou mais dragões. Esses dados variam de partida para partida e têm um impacto direto no resultado final.

    O que queremos de vocês é que desenvolvam um modelo de classificação que consiga prever qual time vai vencer com base nesses dados de pós-início de partida. Para isso, vocês vão precisar escolher um modelo adequado e justificar suas escolhas.

    Já adianto que, por termos menos de 100 mil entradas de dados, uma rede neural pode ser um pouco exagerada aqui. Vamos focar em modelos mais simples, como regressão logística, naive bayes e árvores de decisão. Queremos que vocês comparem esses modelos usando métricas como ROC e AUC.

    Se tiverem mais tempo, sugiro testar com validação cruzada e, quem sabe, até brincar com métodos de ensemble. Lembrem-se de documentar bem cada etapa, justificar suas escolhas e usar visualizações para apresentar os resultados.

## O que foi pedido, em resumo

| Requisito | Como foi endereçado |
|---|---|
| Modelo de classificação binária | Vencedor previsto = time azul (`blueWins`) vs. time vermelho |
| Usar dados de **pós-início** de partida | Dataset captura o estado exato do jogo aos **10 minutos** |
| Modelos simples (sem rede neural) | Regressão Logística, Naive Bayes, Árvore de Decisão |
| Comparar com ROC / AUC | Curvas ROC + AUC-ROC como métrica principal em todos os modelos |
| Validação cruzada (bônus) | 5-fold `StratifiedKFold` em todos os modelos |
| Métodos de ensemble (bônus) | Random Forest e Gradient Boosting adicionados à comparação |
| Documentar e justificar escolhas | Notebook completo + esta apresentação |
| Visualizações | 16 visualizações, da EDA à interpretabilidade do modelo final |

## Interpretando o pedido

A Bárbara pediu modelos "simples" — e não pediu explicitamente o modelo com a maior acurácia possível a qualquer custo. Isso guiou duas decisões importantes do projeto:

1. **AUC-ROC como métrica principal**, exatamente como solicitado, em vez de acurácia isolada — importante porque o dataset é praticamente balanceado (então acurácia sozinha já seria razoável), mas AUC-ROC dá uma visão mais completa do trade-off entre acertos e erros em diferentes limiares de decisão.
2. **Transparência acima de complexidade**: o modelo escolhido no fim não é o mais sofisticado, e sim o mais simples entre os que empataram tecnicamente no topo — indo na linha do que a própria stakeholder sugeriu.

[:octicons-arrow-right-24: Ver os dados e a exploração](02-dados.md){ .md-button .md-button--primary }
