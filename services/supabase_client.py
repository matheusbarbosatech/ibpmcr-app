"""
Cliente Oficial do Supabase para Sincronização em Nuvem (PostgreSQL 15+).
Implementado com REST API nativa ultra-rápida (PostgREST), com timeout rigoroso
e fallback transparente para o SQLite local quando offline ou sem chaves ativas.
"""
import json
import urllib.request
import urllib.error
from typing import Optional, List, Dict, Any
from core.config import SUPABASE_URL, SUPABASE_KEY
from services.db_service import DatabaseService
from models.devocional import DevocionalDiario
from models.oracao import PedidoOracao


class SupabaseService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SupabaseService, cls).__new__(cls)
            cls._instance._init_client()
        return cls._instance

    def _init_client(self):
        self.is_connected = False
        self.local_db = DatabaseService()
        self.base_url = (SUPABASE_URL or "").rstrip("/")
        self.api_key = SUPABASE_KEY or ""

        if self.base_url and self.api_key and "seu-projeto" not in self.base_url:
            self.is_connected = True

    def _get_headers(self, prefer: str = "") -> dict:
        headers = {
            "apikey": self.api_key,
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        if prefer:
            headers["Prefer"] = prefer
        return headers

    def test_connection(self) -> bool:
        """Testa se a conexão com o Supabase está respondendo em até 3 segundos."""
        if not self.is_connected:
            return False
        try:
            url = f"{self.base_url}/rest/v1/devocionais_diarios?select=dia_ano&limit=1"
            req = urllib.request.Request(url, headers=self._get_headers())
            with urllib.request.urlopen(req, timeout=3) as resp:
                return resp.status == 200
        except Exception:
            return False

    def get_devocional_hoje(self, dia_ano: int = 1) -> Optional[DevocionalDiario]:
        """Busca o devocional do dia na nuvem Supabase; se offline, busca no SQLite local."""
        if self.is_connected:
            try:
                url = f"{self.base_url}/rest/v1/devocionais_diarios?dia_ano=eq.{dia_ano}&select=*"
                req = urllib.request.Request(url, headers=self._get_headers())
                with urllib.request.urlopen(req, timeout=3) as resp:
                    if resp.status == 200:
                        data = json.loads(resp.read().decode("utf-8"))
                        if data and len(data) > 0:
                            row = data[0]
                            return DevocionalDiario(
                                id=int(row.get("dia_ano", dia_ano)),
                                dia_ano=int(row.get("dia_ano", dia_ano)),
                                titulo=row.get("titulo", ""),
                                livro_biblia=row.get("referencia_biblica", "") or row.get("livro_biblia", ""),
                                versiculo_chave=row.get("referencia_biblica", "") or row.get("versiculo_chave", ""),
                                texto_versiculo=row.get("versiculo_chave", "") or row.get("texto_versiculo", ""),
                                reflexao_pastoral=row.get("devocional_texto", "") or row.get("reflexao_pastoral", ""),
                                oracao_do_dia=row.get("oracao_profetica", "") or row.get("oracao_do_dia", ""),
                                desafio_pratico=row.get("desafio_pratico", "Medite nesta palavra durante o seu dia."),
                                audio_url=row.get("audio_url"),
                            )
            except Exception:
                pass
        return self.local_db.get_devocional_hoje(dia_ano)

    def get_pedidos_oracao(self) -> List[PedidoOracao]:
        """Busca pedidos de oração aprovados na nuvem ou local."""
        if self.is_connected:
            try:
                url = f"{self.base_url}/rest/v1/pedidos_oracao?status=eq.aprovado&order=created_at.desc&select=*"
                req = urllib.request.Request(url, headers=self._get_headers())
                with urllib.request.urlopen(req, timeout=3) as resp:
                    if resp.status == 200:
                        data = json.loads(resp.read().decode("utf-8"))
                        if data:
                            return [
                                PedidoOracao(
                                    id=str(r.get("id")),
                                    nome_solicitante=r.get("nome_solicitante", ""),
                                    motivo_oracao=r.get("motivo_oracao", ""),
                                    detalhes_pedido=r.get("detalhes_pedido", ""),
                                    is_anonimo=bool(r.get("is_anonimo", False)),
                                    status=r.get("status", "aprovado"),
                                    contador_orando=int(r.get("contador_orando", 1)),
                                    created_at=r.get("created_at", ""),
                                )
                                for r in data
                            ]
            except Exception:
                pass
        return self.local_db.get_pedidos_oracao()

    def enviar_pedido_oracao(self, nome: str, motivo: str, detalhes: str, is_anonimo: bool):
        """Salva no SQLite local e envia para a nuvem Supabase."""
        local_pedido = self.local_db.add_pedido_oracao(nome, motivo, detalhes, is_anonimo)
        if self.is_connected:
            try:
                url = f"{self.base_url}/rest/v1/pedidos_oracao"
                payload = json.dumps({
                    "nome_solicitante": nome,
                    "motivo_oracao": motivo,
                    "detalhes_pedido": detalhes,
                    "is_anonimo": is_anonimo,
                    "status": "aprovado",
                    "contador_orando": 1,
                }).encode("utf-8")
                req = urllib.request.Request(
                    url,
                    data=payload,
                    headers=self._get_headers(prefer="return=minimal"),
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=3):
                    pass
            except Exception:
                pass
        return local_pedido

    def incrementar_orando(self, pedido_id: str) -> int:
        """Incrementa no SQLite local e sincroniza com o Supabase."""
        count = self.local_db.incrementar_orando(pedido_id)
        if self.is_connected:
            try:
                url = f"{self.base_url}/rest/v1/pedidos_oracao?id=eq.{pedido_id}"
                payload = json.dumps({"contador_orando": count}).encode("utf-8")
                req = urllib.request.Request(
                    url,
                    data=payload,
                    headers=self._get_headers(prefer="return=minimal"),
                    method="PATCH",
                )
                with urllib.request.urlopen(req, timeout=3):
                    pass
            except Exception:
                pass
        return count
