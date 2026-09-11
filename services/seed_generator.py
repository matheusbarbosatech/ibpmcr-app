"""
Módulo de Mineração & Seed Generator Integrado do App IBPM CR.
Permite re-executar minerações e sincronizar seeds com o banco de dados.
"""
import sys
import os
from pathlib import Path

# Reutiliza o minerador do Desktop
SCRIPT_MINERADOR = Path(os.path.expanduser("~")) / "Desktop" / "EXTRAIR_MEGA_ATIVOS_SONNET5.py"

def executar_geracao_seeds(num_cultos: int = 2):
    if SCRIPT_MINERADOR.exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location("minerador", str(SCRIPT_MINERADOR))
        minerador = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(minerador)
        minerador.executar_mineracao(num_cultos=num_cultos)
    else:
        print("[ERRO] Script EXTRAIR_MEGA_ATIVOS_SONNET5.py não encontrado na Área de Trabalho.")

if __name__ == "__main__":
    executar_geracao_seeds()
