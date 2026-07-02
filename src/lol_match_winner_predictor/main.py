"""
Ponto de entrada do projeto — inicia o Simulador de Partida (Streamlit).

Uso (a partir da raiz do projeto):
    uv run python -m lol_match_winner_predictor.main

Ou, se registrado como script no pyproject.toml (veja instruções abaixo):
    uv run lol-predictor

Qualquer argumento extra é repassado direto pro Streamlit, por exemplo:
    uv run python -m lol_match_winner_predictor.main --server.port 8502
"""

import sys
from pathlib import Path

from streamlit.web import cli as stcli


def main() -> None:
    app_path = Path(__file__).resolve().parent / "app" / "streamlit_app.py"
    sys.argv = ["streamlit", "run", str(app_path), *sys.argv[1:]]
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
