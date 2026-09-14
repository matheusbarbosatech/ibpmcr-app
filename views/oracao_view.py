"""
Aba 2: Oração - Mural Social de Oração & Intercessão.
Membros interagem clicando em 'Estou Orando por Você' e enviam novos pedidos para o altar pastoral.
"""
import flet as ft
from core.theme import (
    AppColors, FontScaleManager, Icons, AppPadding, AppMargin, AppBorder, AppAlignment, AppDialog
)
from services.db_service import DatabaseService
from services.supabase_client import SupabaseService
from services.share_engine import ShareEngine

class OracaoView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True)
        self.app_page = page
        self.db = DatabaseService()
        self.supabase = SupabaseService()
        self.pedidos_column = ft.Column(spacing=12)

        # Campos do Modal de Novo Pedido
        self.input_nome = ft.TextField(
            label="Seu Nome ou Apelido",
            hint_text="Ex: Maria Aparecida",
            border_color=AppColors.BORDER_DEFAULT,
            focused_border_color=AppColors.PRIMARY_RUBI,
            text_style=ft.TextStyle(color=AppColors.TEXT_WHITE),
        )
        self.input_motivo = ft.Dropdown(
            label="Motivo do Pedido",
            options=[
                ft.dropdown.Option("Saúde & Cura"),
                ft.dropdown.Option("Família & Casamento"),
                ft.dropdown.Option("Causas na Justiça"),
                ft.dropdown.Option("Libertação Espiritual"),
                ft.dropdown.Option("Vida Financeira & Trabalho"),
                ft.dropdown.Option("Paz na Mente / Ansiedade"),
            ],
            value="Saúde & Cura",
            border_color=AppColors.BORDER_DEFAULT,
            focused_border_color=AppColors.PRIMARY_RUBI,
            text_style=ft.TextStyle(color=AppColors.TEXT_WHITE),
        )
        self.input_detalhes = ft.TextField(
            label="Descreva brevemente o motivo",
            hint_text="Ex: Peço oração pela minha família e livramento...",
            multiline=True,
            min_lines=2,
            max_lines=3,
            border_color=AppColors.BORDER_DEFAULT,
            focused_border_color=AppColors.PRIMARY_RUBI,
            text_style=ft.TextStyle(color=AppColors.TEXT_WHITE),
        )
        self.switch_anonimo = ft.Switch(
            value=False,
            active_color=AppColors.PRIMARY_RUBI,
        )

        FontScaleManager.register_listener(self.on_font_scale_changed)
        self.build_ui()

    def on_font_scale_changed(self):
        self.render_pedidos()
        try:
            self.app_page.update()
        except Exception:
            pass

    def build_ui(self):
        self.padding = AppPadding.all(12)

        # Cabeçalho da Aba de Oração
        header = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(Icons.VOLUNTEER_ACTIVISM, color=AppColors.PRIMARY_RUBI, size=24),
                            ft.Text("Mural de Intercessão", size=FontScaleManager.s(20), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Text(
                        "\"Orai uns pelos outros para que sejais curados.\" (Tiago 5:16)",
                        size=FontScaleManager.s(13),
                        color=AppColors.SECONDARY_GOLD,
                        italic=True,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "Toque em 'Estou Orando' para fortalecer um irmão ou envie o seu clamor para o altar.",
                        size=FontScaleManager.s(12),
                        color=AppColors.TEXT_MUTED,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=6),
                    # Botão Grande para Enviar Pedido
                    ft.ElevatedButton(
                        content=ft.Row(
                            controls=[
                                ft.Icon(Icons.ADD_CIRCLE, color="#FFFFFF", size=22),
                                ft.Text("COLOCAR MEU PEDIDO NO ALTAR", weight=ft.FontWeight.BOLD, size=FontScaleManager.s(14), color="#FFFFFF"),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=8,
                        ),
                        style=ft.ButtonStyle(
                            bgcolor=AppColors.PRIMARY_RUBI,
                            shape=ft.RoundedRectangleBorder(radius=12),
                            padding=AppPadding.symmetric(horizontal=16, vertical=14),
                        ),
                        height=52,  # Área ampla de toque
                        on_click=self.abrir_modal_novo_pedido,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6,
            ),
            bgcolor=AppColors.BG_SURFACE,
            padding=AppPadding.all(16),
            border_radius=16,
            border=AppBorder.all(1, AppColors.BORDER_DEFAULT),
            margin=AppMargin.only(bottom=14),
        )

        self.render_pedidos()

        self.content = ft.ListView(
            controls=[
                header,
                ft.Row(
                    controls=[
                        ft.Text("Pedidos Recentes da Congregação", size=FontScaleManager.s(15), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                        ft.IconButton(icon=Icons.REFRESH, icon_color=AppColors.SECONDARY_GOLD, tooltip="Atualizar pedidos", on_click=lambda e: self.recarregar_pedidos()),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                self.pedidos_column,
                ft.Container(height=30),
            ],
            expand=True,
            spacing=8,
        )

    def recarregar_pedidos(self, e=None):
        self.render_pedidos()
        try:
            self.app_page.update()
        except Exception:
            pass

    def render_pedidos(self):
        self.pedidos_column.controls.clear()
        pedidos = self.db.get_pedidos_oracao()

        for p in pedidos:
            nome_exibicao = "Irmão(ã) em Oração (Anônimo)" if p.is_anonimo else p.nome_solicitante
            icone_perfil = Icons.SHIELD if p.is_anonimo else Icons.PERSON

            card = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(icone_perfil, size=18, color=AppColors.SECONDARY_GOLD if p.is_anonimo else AppColors.TEXT_WHITE),
                                        ft.Text(nome_exibicao, size=FontScaleManager.s(14), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                                    ],
                                    spacing=6,
                                ),
                                ft.Container(
                                    content=ft.Text(p.motivo_oracao, size=FontScaleManager.s(11), weight=ft.FontWeight.BOLD, color=AppColors.PRIMARY_RUBI),
                                    bgcolor="#2D111A",
                                    padding=AppPadding.symmetric(horizontal=8, vertical=4),
                                    border_radius=8,
                                    border=AppBorder.all(1, AppColors.PRIMARY_RUBI),
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Container(height=4),
                        ft.Text(f"\"{p.detalhes_pedido}\"", size=FontScaleManager.s(14), color=AppColors.TEXT_SECONDARY, italic=True),
                        ft.Container(height=8),
                        ft.Row(
                            controls=[
                                # Botão Grande "Estou Orando por Você"
                                ft.ElevatedButton(
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(Icons.FAVORITE, color="#FFFFFF", size=18),
                                            ft.Text(f"Estou Orando ({p.contador_orando})", color="#FFFFFF", weight=ft.FontWeight.BOLD, size=FontScaleManager.s(13)),
                                        ],
                                        spacing=6,
                                    ),
                                    style=ft.ButtonStyle(
                                        bgcolor=AppColors.PRIMARY_RUBI,
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                        padding=AppPadding.symmetric(horizontal=14, vertical=12),
                                    ),
                                    height=48,  # Acessibilidade sênior
                                    on_click=lambda e, pid=p.id: self.orar_pelo_pedido(pid),
                                ),
                                ft.IconButton(
                                    icon=Icons.SHARE,
                                    icon_color=AppColors.TEXT_MUTED,
                                    tooltip="Compartilhar no grupo de oração",
                                    on_click=lambda e, ped=p: ShareEngine.share_whatsapp_status(
                                        self.app_page,
                                        f"🙏 *Clamor de Oração - IBPM CR*\nMotivo: {ped.motivo_oracao}\n\"{ped.detalhes_pedido}\"\nVamos nos unir em oração por essa vida!"
                                    )
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        )
                    ],
                    spacing=4,
                ),
                bgcolor=AppColors.BG_SURFACE,
                padding=AppPadding.all(18),
                border_radius=18,
                border=AppBorder.all(1, AppColors.BORDER_DEFAULT),
            )
            self.pedidos_column.controls.append(card)

    def orar_pelo_pedido(self, pedido_id: str):
        novo_total = self.supabase.incrementar_orando(pedido_id)
        self.render_pedidos()
        try:
            self.app_page.update()
        except Exception:
            pass
        ShareEngine.show_feedback(self.app_page, f"🙏 Glória a Deus! Você se uniu em intercessão (Total: {novo_total} orando).")

    def abrir_modal_novo_pedido(self, e):
        def fechar_modal(ev=None):
            AppDialog.close(self.app_page, dialogo)

        def salvar_pedido(ev):
            nome = self.input_nome.value.strip() or "Irmão(ã) da Fé"
            motivo = self.input_motivo.value or "Oração Geral"
            detalhes = self.input_detalhes.value.strip()

            if not detalhes:
                ShareEngine.show_feedback(self.app_page, "⚠️ Por favor, escreva o motivo do seu pedido.")
                return

            self.supabase.enviar_pedido_oracao(nome, motivo, detalhes, self.switch_anonimo.value)
            self.input_detalhes.value = ""
            fechar_modal()
            self.render_pedidos()
            try:
                self.app_page.update()
            except Exception:
                pass
            ShareEngine.show_feedback(self.app_page, "✨ Seu clamor foi colocado no altar! A igreja estará em oração por você.")

        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Icon(Icons.VOLUNTEER_ACTIVISM, color=AppColors.PRIMARY_RUBI, size=24),
                    ft.Text("Colocar Pedido no Altar", weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE, size=FontScaleManager.s(16)),
                ],
                spacing=8,
            ),
            content=ft.Column(
                controls=[
                    ft.Text("Deixe seu pedido de oração para a liderança e congregação.", size=FontScaleManager.s(12), color=AppColors.TEXT_MUTED),
                    self.input_nome,
                    self.input_motivo,
                    self.input_detalhes,
                    ft.Row(
                        controls=[
                            ft.Text("Oração 100% Anônima", size=FontScaleManager.s(13), color=AppColors.TEXT_WHITE),
                            self.switch_anonimo,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
                tight=True,
                spacing=10,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=fechar_modal),
                ft.ElevatedButton(
                    "Enviar Pedido",
                    bgcolor=AppColors.PRIMARY_RUBI,
                    color="#FFFFFF",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                    on_click=salvar_pedido,
                ),
            ],
            bgcolor=AppColors.BG_SURFACE,
        )

        AppDialog.open(self.app_page, dialogo)
