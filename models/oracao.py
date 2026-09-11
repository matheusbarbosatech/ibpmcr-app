"""
Modelo de Dados para o Mural Social de Oração & Intercessão.
"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class PedidoOracao:
    id: str
    nome_solicitante: str
    motivo_oracao: str
    detalhes_pedido: str
    is_anonimo: bool = False
    status: str = "aprovado"
    contador_orando: int = 1
    created_at: Optional[str] = None
