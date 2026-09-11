"""
Modelo de Dados para Devocionais Diários (365 Dias no Altar).
"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class DevocionalDiario:
    id: int
    dia_ano: int
    titulo: str
    livro_biblia: str
    versiculo_chave: str
    texto_versiculo: str
    reflexao_pastoral: str
    oracao_do_dia: str
    desafio_pratico: Optional[str] = None
    audio_url: Optional[str] = None
