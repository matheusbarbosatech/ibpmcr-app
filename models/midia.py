"""
Modelos de Dados para Cultos, Cortes Verticais, Galeria de Fotos, Frases e Livros.
"""
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

@dataclass
class CultoAcervo:
    id: int
    numero_culto: int
    data_culto: str
    tipo_culto: str
    titulo_pregacao: str
    pastor_ministrante: str
    video_16_9_url: Optional[str] = None
    audio_mp3_url: Optional[str] = None
    duracao_minutos: int = 90
    resumo_pregacao: Optional[str] = None

@dataclass
class CorteVertical:
    id: int
    culto_id: Optional[int]
    titulo_impacto: str
    tema_categoria: str
    video_9_16_url: str
    duracao_segundos: int = 45
    total_compartilhamentos: int = 0
    nota_viral: int = 90

@dataclass
class FotoGaleria:
    id: int
    album_nome: str
    data_evento: str
    categoria: str
    foto_hd_url: str
    foto_thumb_url: str
    total_downloads: int = 0

@dataclass
class FraseProfetica:
    id: int
    frase: str
    sentimento_tag: str  # ansiedade, medo, desanimo, gratidao, fe, vitoria
    referencia_biblica: Optional[str] = None

@dataclass
class LivroEbook:
    id: int
    titulo_livro: str
    subtitulo: str
    capa_url: str
    pdf_url: str
    sinopse: str
    total_capitulos: int = 12

@dataclass
class ModuloLideranca:
    id: int
    numero_modulo: int
    titulo_modulo: str
    tema_central: str
    conteudo_apostila: str
    pdf_apostila_url: Optional[str] = None
    questoes_quiz: Optional[List[Dict[str, Any]]] = None
