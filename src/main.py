"""
Redirecionamento para o ponto de entrada principal do Super-App IBPM CR.
Permite execução transparente a partir de 'python src/main.py' ou 'python main.py'.
"""
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from main import main
import flet as ft

if __name__ == "__main__":
    ft.app(target=main)
