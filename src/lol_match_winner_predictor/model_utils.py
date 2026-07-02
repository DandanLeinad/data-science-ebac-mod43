"""
Utilitários do simulador — carrega os artefatos reais gerados pelo notebook
(`models/logistic_regression_tuned.pkl`, `models/scaler.pkl`) e reproduz
localmente as mesmas etapas de limpeza / feature engineering do notebook
para saber a ordem das 39 colunas e os valores "neutros" (média) das
features que o simulador não expõe ao usuário.

Modelo final: Regressão Logística tunada (GridSearchCV, C=0.01, penalty='l1')
Threshold operacional: 0.32 (otimizado para F1-Score)
"""

from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Paths — resolvidos a partir deste arquivo, funcionam com qualquer cwd
# lol_match_winner_predictor/ -> src/ -> raiz do projeto
# ---------------------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parents[2]
MODELS_DIR = ROOT_DIR / "models"
DATA_PATH = ROOT_DIR / "data" / "raw" / "Base_M43_Pratique_LOL_RANKED_WIN.csv"

THRESHOLD = (
    0.32  # otimizado para F1-Score no notebook (seção "Otimização de Threshold")
)

# Mesmas colunas removidas no notebook (data leakage / espelhos exatos)
COLS_DROP = [
    "gameId",
    "blueDeaths",
    "redFirstBlood",
    "redDeaths",
    "redGoldDiff",
    "redExperienceDiff",
]


# ---------------------------------------------------------------------------
# Carregar modelo e scaler reais (gerados pelo notebook, não recriados aqui)
# ---------------------------------------------------------------------------
@st.cache_resource
def load_model_and_scaler():
    model = joblib.load(MODELS_DIR / "logistic_regression_tuned.pkl")
    scaler = joblib.load(MODELS_DIR / "scaler.pkl")
    return model, scaler


# ---------------------------------------------------------------------------
# Reproduzir a feature engineering do notebook para obter:
#  - a ordem exata das 39 colunas usadas no treino
#  - a média de cada uma (valor "neutro" para as features que o app não edita)
# ---------------------------------------------------------------------------
@st.cache_data
def load_feature_reference():
    df = pd.read_csv(DATA_PATH)
    df_clean = df.drop(columns=COLS_DROP).copy()

    df_fe = df_clean.copy()
    df_fe["kill_advantage"] = df_fe["blueKills"] - df_fe["redKills"]
    df_fe["ward_advantage"] = df_fe["blueWardsPlaced"] - df_fe["redWardsPlaced"]
    df_fe["elite_advantage"] = df_fe["blueEliteMonsters"] - df_fe["redEliteMonsters"]

    total_gold = df_fe["blueTotalGold"] + df_fe["redTotalGold"]
    df_fe["gold_dominance"] = df_fe["blueGoldDiff"] / total_gold

    total_xp = df_fe["blueTotalExperience"] + df_fe["redTotalExperience"]
    df_fe["xp_dominance"] = df_fe["blueExperienceDiff"] / total_xp

    df_fe["ward_denial"] = df_fe["blueWardsDestroyed"] / (df_fe["redWardsPlaced"] + 1)

    X = df_fe.drop(columns=["blueWins"])
    feature_names = list(X.columns)
    feature_means = X.mean().to_dict()

    # Percentis para definir ranges realistas dos inputs no app
    raw_stats = df.describe(percentiles=[0.05, 0.5, 0.95])

    return feature_names, feature_means, raw_stats


# ---------------------------------------------------------------------------
# Construção do vetor de features a partir dos 12 inputs simplificados
# ---------------------------------------------------------------------------
def build_feature_vector(
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
):
    row = dict(feature_means)  # começa com a média em tudo (neutro)

    blue_elite = blue_dragons + blue_heralds
    red_elite = red_dragons + red_heralds

    row.update(
        {
            "blueTotalGold": blue_gold,
            "redTotalGold": red_gold,
            "blueGoldDiff": blue_gold - red_gold,
            "blueGoldPerMin": blue_gold / 10,
            "redGoldPerMin": red_gold / 10,
            "blueTotalExperience": blue_xp,
            "redTotalExperience": red_xp,
            "blueExperienceDiff": blue_xp - red_xp,
            "blueKills": blue_kills,
            "redKills": red_kills,
            "blueDragons": blue_dragons,
            "redDragons": red_dragons,
            "blueHeralds": blue_heralds,
            "redHeralds": red_heralds,
            "blueEliteMonsters": blue_elite,
            "redEliteMonsters": red_elite,
            "blueTowersDestroyed": blue_towers,
            "redTowersDestroyed": red_towers,
            "kill_advantage": blue_kills - red_kills,
            "elite_advantage": blue_elite - red_elite,
            "gold_dominance": (blue_gold - red_gold) / (blue_gold + red_gold),
            "xp_dominance": (blue_xp - red_xp) / (blue_xp + red_xp),
        }
    )

    vector = pd.DataFrame([[row[c] for c in feature_names]], columns=feature_names)
    return vector, row


def predict_proba_blue(model, scaler, vector):
    vector_scaled = scaler.transform(vector)
    return model.predict_proba(vector_scaled)[0, 1]
