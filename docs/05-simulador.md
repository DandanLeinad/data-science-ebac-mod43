---
title: Simulador
description: O app interativo que aplica o modelo em cenários simulados de partida.
---

# Simulador de Partida

Para tornar o modelo tangível — inclusive para quem não lê coeficiente de regressão — o projeto inclui um **app Streamlit** onde dá pra montar um cenário de partida no minuto 10 e ver a previsão do modelo em tempo real.

!!! info "Este site é estático"
    Como esta página vive no GitHub Pages, ela não roda Python — então o simulador não pode ser embutido aqui ao vivo. As instruções abaixo mostram como rodá-lo localmente. O código-fonte completo está no repositório.

## Como funciona

O app pede **12 indicadores** — ouro, experiência, kills, dragões, arautos e torres, para os dois times — e por trás dos panos:

1. Calcula automaticamente as 6 features de engenharia (`gold_dominance`, `xp_dominance`, `kill_advantage`, `elite_advantage`, entre outras);
2. Preenche as demais ~27 features (wards, CS, nível médio, first blood...) com a média do dataset de treino — já que, [como vimos](04-resultados.md), o modelo final não atribui peso a elas;
3. Aplica o `StandardScaler` e o modelo campeão (Regressão Logística tunada);
4. Mostra a probabilidade de vitória de cada time e a previsão final, usando o threshold de 0,32.

Um painel "O que realmente pesou nessa previsão?" expõe, de forma transparente, as 5 features que de fato movem a agulha — reforçando o achado da página anterior em vez de esconder essa complexidade do usuário.

## Rodando localmente

O projeto usa [uv](https://docs.astral.sh/uv/) para gerenciar dependências. A partir da raiz do repositório:

```bash
uv sync
uv run python -m lol_match_winner_predictor.main
```

Isso abre o simulador em `http://localhost:8501`.

<div class="grid cards" markdown>

-   :octicons-mark-github-16:{ .lg .middle } __Código-fonte__

    ---

    App, script de treino e utilitários de modelo.

    [:octicons-arrow-right-24: `src/lol_match_winner_predictor/`](https://github.com/CHANGE-ME/projeto-final-mod43/tree/main/src/lol_match_winner_predictor)

-   :material-notebook-outline:{ .lg .middle } __Notebook completo__

    ---

    Toda a análise que fundamenta este site e o simulador.

    [:octicons-arrow-right-24: `lol_match_winner_prediction.ipynb`](https://github.com/CHANGE-ME/projeto-final-mod43/blob/main/lol_match_winner_prediction.ipynb)

</div>

---

## Conclusão

Pra Bárbara Martinelli e a equipe de análise da Riot Games: o modelo entregue prevê o vencedor de uma partida ranqueada com **~81% de AUC-ROC** usando apenas o estado do jogo aos 10 minutos — e faz isso, na prática, olhando essencialmente para **uma coisa**: quem está na frente na economia (ouro e experiência). Dragões ajudam a desempatar cenários próximos; o resto do que acontece cedo no jogo (kills, wards, first blood) importa para o *resultado* da partida, mas seu efeito já está contido no placar de ouro e XP no momento em que o modelo olha para os dados.

Essa é, ao mesmo tempo, uma resposta ao desafio proposto e um insight de produto: se a Riot quiser simplificar um indicador de "quem está ganhando" para exibir ao vivo, `gold_dominance` sozinho já carrega quase toda a informação necessária.
