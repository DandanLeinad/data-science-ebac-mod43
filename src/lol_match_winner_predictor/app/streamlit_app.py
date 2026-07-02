"""
Simulador de Partida — LoL Win Predictor
Projeto Final | Módulo 43 | Case 03 — Riot Games (stakeholder: Bárbara Martinelli)

Rodar (a partir da raiz do projeto):
    uv run streamlit run src/lol_match_winner_predictor/app/streamlit_app.py
"""

import streamlit as st
from model_utils import (
    THRESHOLD,
    build_feature_vector,
    load_feature_reference,
    load_model_and_scaler,
    predict_proba_blue,
)

st.set_page_config(
    page_title="LoL Win Predictor — Simulador", page_icon="🎮", layout="centered"
)

model, scaler = load_model_and_scaler()
feature_names, feature_means, raw_stats = load_feature_reference()

# ---------------------------------------------------------------------------
# Cabeçalho
# ---------------------------------------------------------------------------
st.title("🎮 LoL Win Predictor")
st.caption(
    "Simulador de partida ranqueada de League of Legends — Projeto Final (Case 03 — Módulo 43)"
)
st.markdown(
    "Preencha o estado de uma partida por volta do **minuto 10** e veja "
    "a previsão do modelo para o vencedor."
)
st.space("small")

# ---------------------------------------------------------------------------
# Inputs — 6 pares Blue vs Red (12 indicadores) + First Blood
# ---------------------------------------------------------------------------
col_blue, col_red = st.columns(2, gap="large")

with col_blue:
    st.subheader(":material/sports_esports: Time Azul")
    blue_gold = st.number_input(
        "Ouro total",
        5000,
        30000,
        16500,
        step=100,
        key="bg",
        help="Ouro total acumulado pelo time até ~min 10",
    )
    blue_xp = st.number_input(
        "Experiência total",
        5000,
        25000,
        17900,
        step=100,
        key="bx",
        help="Experiência total acumulada pelo time até ~min 10",
    )
    blue_kills = st.number_input(
        "Abates (kills)",
        0,
        25,
        6,
        step=1,
        key="bk",
        help="Total de campeões abatidos pelo time",
    )
    blue_dragons = st.number_input(
        "Dragões abatidos",
        0,
        4,
        0,
        step=1,
        key="bd",
        help="Dragões capturados pelo time",
    )
    blue_heralds = st.number_input(
        "Arautos abatidos",
        0,
        2,
        0,
        step=1,
        key="bh",
        help="Arautos (Heralds) capturados pelo time",
    )
    blue_towers = st.number_input(
        "Torres destruídas",
        0,
        5,
        0,
        step=1,
        key="bt",
        help="Torres inimigas destruídas pelo time",
    )

with col_red:
    st.subheader(":material/sports_esports: Time Vermelho")
    red_gold = st.number_input(
        "Ouro total",
        5000,
        30000,
        16500,
        step=100,
        key="rg",
        help="Ouro total acumulado pelo time até ~min 10",
    )
    red_xp = st.number_input(
        "Experiência total",
        5000,
        25000,
        17900,
        step=100,
        key="rx",
        help="Experiência total acumulada pelo time até ~min 10",
    )
    red_kills = st.number_input(
        "Abates (kills)",
        0,
        25,
        6,
        step=1,
        key="rk",
        help="Total de campeões abatidos pelo time",
    )
    red_dragons = st.number_input(
        "Dragões abatidos",
        0,
        4,
        0,
        step=1,
        key="rd",
        help="Dragões capturados pelo time",
    )
    red_heralds = st.number_input(
        "Arautos abatidos",
        0,
        2,
        0,
        step=1,
        key="rh",
        help="Arautos (Heralds) capturados pelo time",
    )
    red_towers = st.number_input(
        "Torres destruídas",
        0,
        5,
        0,
        step=1,
        key="rt",
        help="Torres inimigas destruídas pelo time",
    )

# First Blood (não altera previsão — modelo L1 zerou o peso, mas é feature do desafio)
with st.container(horizontal=True):
    blue_first_blood = st.checkbox(
        "⚔️ First Blood para o Time Azul",
        value=False,
        help="Se o time azul obteve o primeiro abate da partida (feature do desafio; o modelo tunado não atribuiu peso a ela)",
    )

st.space("small")

# ---------------------------------------------------------------------------
# Feedback visual em tempo real: gold_dominance
# ---------------------------------------------------------------------------
gold_diff = blue_gold - red_gold
total_gold = blue_gold + red_gold
gold_dominance_live = gold_diff / total_gold if total_gold > 0 else 0.0

st.markdown(
    f"""
**📊 Gold Dominance (calculado em tempo real):** `{gold_dominance_live:+.3f}`  
*Vantagem de ouro normalizada pelo ouro total da partida — feature mais forte do modelo (peso +0.94)*
"""
)
st.space("small")

# ---------------------------------------------------------------------------
# Previsão
# ---------------------------------------------------------------------------
vector, row_used = build_feature_vector(
    feature_names,
    feature_means,
    blue_gold,
    red_gold,
    blue_xp,
    red_xp,
    blue_kills,
    red_kills,
    blue_dragons,
    red_dragons,
    blue_heralds,
    red_heralds,
    blue_towers,
    red_towers,
)
proba_blue = predict_proba_blue(model, scaler, vector)
proba_red = 1 - proba_blue
vencedor = "🔵 Time Azul" if proba_blue >= THRESHOLD else "🔴 Time Vermelho"

st.subheader(":material/bar_chart: Previsão")

bar_html = f"""
<div style="display:flex; width:100%; height:36px; border-radius:8px; overflow:hidden; font-weight:600; font-family:sans-serif;">
  <div style="width:{proba_blue * 100:.1f}%; background:#3B82C4; color:white; display:flex; align-items:center; justify-content:center;">
    {proba_blue * 100:.1f}%
  </div>
  <div style="width:{proba_red * 100:.1f}%; background:#C0392B; color:white; display:flex; align-items:center; justify-content:center;">
    {proba_red * 100:.1f}%
  </div>
</div>
"""
st.markdown(bar_html, unsafe_allow_html=True)
st.space("small")

c1, c2 = st.columns(2)
c1.metric("Prob. vitória — Time Azul", f"{proba_blue:.1%}")
c2.metric("Prob. vitória — Time Vermelho", f"{proba_red:.1%}")

st.success(f"**Vencedor previsto:** {vencedor}")
st.caption(
    f"Classificação usa o threshold operacional de **{THRESHOLD}** "
    "(otimizado para F1-Score no notebook, não o padrão 0.5) — "
    "prioriza detectar a maioria das vitórias reais, mesmo com mais falsos positivos."
)

# ---------------------------------------------------------------------------
# O que pesou na previsão
# ---------------------------------------------------------------------------
with st.expander("🔍 O que realmente pesou nessa previsão?"):
    st.markdown(
        """
O GridSearchCV escolheu regularização **L1 (Lasso)** com `C=0.01` — bem forte.
Isso zerou o peso de quase todas as 39 features, deixando **apenas 5** com
influência real na decisão do modelo:
        """
    )
    st.markdown(
        f"""
| Feature | O que é | Valor calculado nesta simulação | Peso no modelo |
|---|---|---|---|
| `gold_dominance` | vantagem de ouro, normalizada pelo ouro total da partida | {row_used["gold_dominance"]:+.3f} | **+0.94** (a mais forte) |
| `blueExperienceDiff` | diferença de XP entre os times | {row_used["blueExperienceDiff"]:+,.0f} | +0.37 |
| `blueDragons` | dragões abatidos pelo time azul | {row_used["blueDragons"]:.0f} | +0.11 |
| `redDragons` | dragões abatidos pelo time vermelho | {row_used["redDragons"]:.0f} | -0.09 |
| `elite_advantage` | vantagem em objetivos elite (dragão+arauto) | {row_used["elite_advantage"]:+.0f} | +0.03 |
        """
    )
    st.caption(
        "Todas as outras estatísticas (wards, assists, CS, nível médio, "
        "first blood etc.) foram fixadas na média do dataset — o modelo "
        "tunado não atribuiu peso a elas, então alterá-las não muda a "
        "previsão. Isso é esperado: `gold_dominance` já carrega boa parte "
        "da informação que ouro, XP e kills também carregam (features "
        "correlacionadas), então o L1 manteve só a mais forte."
    )

st.space("small")
st.caption(
    "Modelo: Regressão Logística tunada (GridSearchCV) · "
    "Dados capturados por volta do minuto 10 de partidas ranqueadas."
)

st.divider()
st.markdown(
    """
:small[**Projeto Final — Módulo 43 | Case 03 — Riot Games**  
Desenvolvido para o desafio da Bárbara Martinelli (Tech Lead, Riot Games)  
📓 Notebook completo: `lol_match_winner_prediction.ipynb`  
🐙 GitHub: [github.com/seu-usuario/projeto-final-mod43](https://github.com/seu-usuario/projeto-final-mod43)]
"""
)
