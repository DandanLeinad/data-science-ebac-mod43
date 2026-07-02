# LoL Win Predictor

Projeto final do Módulo 43 (Case 03) — modelo de classificação binária que prevê o vencedor de uma partida ranqueada de League of Legends a partir do estado do jogo no minuto 10, desenvolvido para a Riot Games.

**📊 Apresentação completa:** <https://CHANGE-ME.github.io/projeto-final-mod43/>

## O que tem neste repositório

| Caminho | Conteúdo |
|---|---|
| `lol_match_winner_prediction.ipynb` | Notebook completo: EDA, feature engineering, treino e comparação de 5 modelos, tuning, threshold e interpretabilidade |
| `data/raw/` | Dataset original (9.879 partidas, 40 colunas) |
| `models/` | Modelos treinados e serializados (`.pkl`) |
| `reports/figures/` | Visualizações geradas pelo notebook |
| `src/lol_match_winner_predictor/` | App Streamlit (simulador interativo) |
| `docs/` | Fonte da apresentação (site estático gerado com [Zensical](https://zensical.org)) |

## Modelo final

**Regressão Logística** tunada via `GridSearchCV` (`C=0.01`, `penalty='l1'`, `solver='saga'`) — AUC-ROC de 0,8065 (teste) / 0,8117 (validação cruzada, 5-fold). Threshold operacional: 0,32 (otimizado para F1-Score).

Detalhes completos, incluindo o achado mais interessante do projeto, estão na [apresentação](https://CHANGE-ME.github.io/projeto-final-mod43/04-resultados/).

## Rodando o simulador localmente

Requer [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run python -m lol_match_winner_predictor.main
```

## Rodando a apresentação localmente

```bash
cd docs
pip install zensical
zensical serve -o
```

---

Projeto Final · Módulo 43 · EBAC
