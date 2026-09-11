"""
Cliente Oficial do Supabase para Sincronização em Nuvem (PostgreSQL 15+).
Possui fallback transparente para o SQLite local quando offline ou sem chaves ativas.
"""
from typing import Optional
from core.config import SUPABASE_URL, SUPABASE_KEY
from services.db_service import DatabaseService

class SupabaseService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SupabaseService, cls).__new__(cls)
            cls._instance._init_client()
        return cls._instance

    def _init_client(self):
        self.is_connected = False
        self.client = None
        self.local_db = DatabaseService()

        if SUPABASE_URL and SUPABASE_KEY and "seu-projeto" not in SUPABASE_URL:
            try:
                from supabase import create_client, Client
                self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
                self.is_connected = True
            except Exception:
                self.is_connected = False

    def get_devocional_hoje(self, dia_ano: int = 1):
        if self.is_connected and self.client:
            try:
                res = self.client.table("devocionais_diarios").select("*").eq("dia_ano", dia_ano).execute()
                if res.data:
                    return res.data[0]
            except Exception:
                pass
        return self.local_db.get_devocional_hoje(dia_ano)

    def get_pedidos_oracao(self):
        if self.is_connected and self.client:
            try:
                res = self.client.table("pedidos_oracao").select("*").eq("status", "aprovado").order("created_at", desc=True).execute()
                if res.data:
                    return res.data
            except Exception:
                pass
        return self.local_db.get_pedidos_oracao()

    def enviar_pedido_oracao(self, nome: str, motivo: str, detalhes: str, is_anonimo: bool):
        # Sempre salva no banco local SQLite para garantia de funcionamento
        local_pedido = self.local_db.add_pedido_oracao(nome, motivo, detalhes, is_anonimo)
        if self.is_connected and self.client:
            try:
                self.client.table("pedidos_oracao").insert({
                    "id": local_pedido.id,
                    "nome_solicitante": nome,
                    "motivo_oracao": motivo,
                    "detalhes_pedido": detalhes,
                    "is_anonimo": is_anonimo,
                    "status": "aprovado",
                    "contador_orando": 1
                }).execute()
            except Exception:
                pass
        return local_pedido

    def incrementar_orando(self, pedido_id: str):
        count = self.local_db.incrementar_orando(pedido_id)
        if self.is_connected and self.client:
            try:
                self.client.rpc("incrementar_orando", {"row_id": pedido_id}).execute()
            except Exception:
                pass
        return count
