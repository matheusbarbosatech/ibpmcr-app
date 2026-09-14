"""
Aba 3: Retiro Face a Face 2026 — IBPM CR.
Página oficial, dedicada e respirada para o grande encontro da igreja.
Permite inscrição direta, escolha do tamanho da camisa oficial e cópia da chave PIX.
"""
import time
from datetime import date
import flet as ft
from core.theme import (
    AppColors, FontScaleManager, Icons, AppPadding, AppMargin, AppBorder, AppAlignment, AppDialog, AppUrl
)
from services.db_service import DatabaseService
from services.share_engine import ShareEngine


class RetiroView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True)
        self.app_page = page
        self.db = DatabaseService()
        self.tamanho_selecionado = "M"
        self.nome_input = ft.TextField(
            label="Seu Nome Completo",
            hint_text="Ex: Matheus Barbosa",
            bgcolor=AppColors.BG_SURFACE_ALT,
            border_color=AppColors.BORDER_DEFAULT,
            color=AppColors.TEXT_WHITE,
            border_radius=12,
        )
        self.whatsapp_input = ft.TextField(
            label="Seu WhatsApp com DDD",
            hint_text="Ex: 21999998888",
            bgcolor=AppColors.BG_SURFACE_ALT,
            border_color=AppColors.BORDER_DEFAULT,
            color=AppColors.TEXT_WHITE,
            border_radius=12,
            keyboard_type=ft.KeyboardType.PHONE,
        )
        self.build_ui()

    def build_ui(self):
        # 1. Contagem regressiva para 24/10/2026
        hoje = date.today()
        alvo = date(2026, 10, 24)
        dias_restantes = max((alvo - hoje).days, 0)

        header = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(Icons.LOCAL_FIRE_DEPARTMENT_ROUNDED, color=AppColors.PRIMARY_RUBI, size=24),
                            ft.Text("RETIRO OFICIAL IBPM CR", size=FontScaleManager.s(12), weight=ft.FontWeight.BOLD, color=AppColors.SECONDARY_GOLD),
                        ],
                        spacing=6,
                    ),
                    ft.Text(
                        "Face a Face com Deus 2026",
                        size=FontScaleManager.s(22),
                        weight=ft.FontWeight.BOLD,
                        color=AppColors.TEXT_WHITE,
                    ),
                    ft.Text(
                        "3 dias de imersão espiritual, comunhão e milagres no Sítio Vale das Bênçãos.",
                        size=FontScaleManager.s(13),
                        color=AppColors.TEXT_SECONDARY,
                    ),
                    ft.Container(height=6),
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(Icons.TIMER_ROUNDED, color=AppColors.SECONDARY_GOLD, size=18),
                                ft.Text(f"Faltam {dias_restantes} dias para o grande encontro!", size=FontScaleManager.s(13), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                            ],
                            spacing=8,
                        ),
                        bgcolor=AppColors.BG_SURFACE_ALT,
                        padding=AppPadding.symmetric(horizontal=14, vertical=10),
                        border_radius=14,
                        border=AppBorder.all(1, AppColors.BORDER_DEFAULT),
                    ),
                ],
                spacing=4,
            ),
            padding=AppPadding.only(bottom=16),
        )

        # 2. Card O que está incluso
        def criar_beneficio(icone, titulo, descricao):
            return ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(icone, color=AppColors.SECONDARY_GOLD, size=20),
                        bgcolor=AppColors.BG_SURFACE_ALT,
                        padding=AppPadding.all(8),
                        border_radius=12,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(titulo, size=FontScaleManager.s(13), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                            ft.Text(descricao, size=FontScaleManager.s(11), color=AppColors.TEXT_MUTED),
                        ],
                        spacing=1,
                        expand=True,
                    ),
                ],
                spacing=12,
            )

        card_incluso = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("O que está incluso na sua inscrição:", size=FontScaleManager.s(14), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                    ft.Container(height=6),
                    criar_beneficio(Icons.HOTEL_ROUNDED, "Hospedagem Completa", "Quartos confortáveis com ar-condicionado e suíte"),
                    criar_beneficio(Icons.RESTAURANT_ROUNDED, "Alimentação 5 Estrelas", "Café da manhã, almoço, lanche da tarde e jantar"),
                    criar_beneficio(Icons.DIRECTIONS_BUS_ROUNDED, "Transporte Executivo", "Ida e volta saindo direto do templo em Marechal"),
                    criar_beneficio(Icons.CHECKROOM_ROUNDED, "Camisa Oficial 2026", "Tecido dry-fit exclusivo do evento Face a Face"),
                ],
                spacing=10,
            ),
            bgcolor=AppColors.BG_SURFACE,
            padding=AppPadding.all(18),
            border_radius=18,
            border=AppBorder.all(1, AppColors.BORDER_DEFAULT),
        )

        # 3. Seletor de Tamanho da Camisa
        tamanhos = ["P", "M", "G", "GG", "XG"]
        botoes_tamanho = []
        for tam in tamanhos:
            ativo = (self.tamanho_selecionado == tam)
            botoes_tamanho.append(
                ft.Container(
                    content=ft.Text(tam, size=FontScaleManager.s(13), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE if ativo else AppColors.TEXT_SECONDARY),
                    bgcolor=AppColors.PRIMARY_RUBI if ativo else AppColors.BG_SURFACE_ALT,
                    padding=AppPadding.symmetric(horizontal=18, vertical=10),
                    border_radius=12,
                    border=AppBorder.all(1, AppColors.PRIMARY_RUBI if ativo else AppColors.BORDER_DEFAULT),
                    ink=True,
                    on_click=lambda e, t=tam: self._selecionar_tamanho(t),
                )
            )

        self.row_tamanhos = ft.Row(controls=botoes_tamanho, spacing=8)

        card_camisa = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(Icons.CHECKROOM_ROUNDED, color=AppColors.SECONDARY_GOLD, size=20),
                            ft.Text("Escolha o Tamanho da sua Camisa Oficial", size=FontScaleManager.s(13), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                        ],
                        spacing=8,
                    ),
                    ft.Container(height=6),
                    self.row_tamanhos,
                ],
                spacing=6,
            ),
            bgcolor=AppColors.BG_SURFACE,
            padding=AppPadding.all(18),
            border_radius=18,
            border=AppBorder.all(1, AppColors.BORDER_DEFAULT),
        )

        # 4. Formulário e PIX do Retiro
        card_inscricao = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Garanta sua vaga agora mesmo", size=FontScaleManager.s(14), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                    ft.Text("Investimento: R$ 250,00 (ou até 3x no cartão com a liderança)", size=FontScaleManager.s(12), color=AppColors.SECONDARY_GOLD),
                    ft.Container(height=8),
                    self.nome_input,
                    ft.Container(height=4),
                    self.whatsapp_input,
                    ft.Container(height=10),
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(Icons.QR_CODE_ROUNDED, color=AppColors.SECONDARY_GOLD, size=22),
                                ft.Column(
                                    controls=[
                                        ft.Text("Chave PIX Oficial do Retiro:", size=FontScaleManager.s(11), color=AppColors.TEXT_MUTED),
                                        ft.Text("ibpmcr7976@gmail.com", size=FontScaleManager.s(13), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                                    ],
                                    spacing=2,
                                    expand=True,
                                ),
                                ft.IconButton(
                                    icon=Icons.COPY_ROUNDED,
                                    icon_color=AppColors.SECONDARY_GOLD,
                                    icon_size=20,
                                    tooltip="Copiar Chave PIX",
                                    on_click=self.copiar_pix,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        bgcolor=AppColors.BG_SURFACE_ALT,
                        padding=AppPadding.symmetric(horizontal=14, vertical=10),
                        border_radius=14,
                    ),
                    ft.Container(height=12),
                    ft.ElevatedButton(
                        content=ft.Row(
                            controls=[
                                ft.Icon(Icons.SEND_ROUNDED, color=AppColors.TEXT_WHITE, size=18),
                                ft.Text("Enviar Inscrição via WhatsApp", size=FontScaleManager.s(14), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=8,
                        ),
                        bgcolor=AppColors.PRIMARY_RUBI,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=14),
                            padding=AppPadding.symmetric(horizontal=20, vertical=14),
                        ),
                        on_click=self.enviar_inscricao,
                    ),
                ],
                spacing=6,
            ),
            bgcolor=AppColors.BG_SURFACE,
            padding=AppPadding.all(18),
            border_radius=18,
            border=AppBorder.all(1, AppColors.BORDER_DEFAULT),
        )

        self.content = ft.ListView(
            controls=[
                header,
                card_incluso,
                ft.Container(height=14),
                card_camisa,
                ft.Container(height=14),
                card_inscricao,
                ft.Container(height=24),
            ],
            padding=AppPadding.symmetric(horizontal=16, vertical=12),
            spacing=0,
        )

    def _selecionar_tamanho(self, tam: str):
        self.tamanho_selecionado = tam
        self.build_ui()
        try:
            self.app_page.update()
        except Exception:
            pass

    def copiar_pix(self, e=None):
        ShareEngine.copy_to_clipboard(self.app_page, "ibpmcr7976@gmail.com", "Chave PIX do Retiro copiada com sucesso!")

    def enviar_inscricao(self, e=None):
        nome = (self.nome_input.value or "").strip()
        tel = (self.whatsapp_input.value or "").strip()

        if not nome:
            ShareEngine.show_feedback(self.app_page, "Por favor, digite seu nome completo.")
            return

        mensagem = (
            f"🔥 *INSCRIÇÃO OFICIAL — RETIRO FACE A FACE 2026*\n\n"
            f"👤 *Nome:* {nome}\n"
            f"📲 *WhatsApp:* {tel or 'Não informado'}\n"
            f"👕 *Tamanho da Camisa:* {self.tamanho_selecionado}\n"
            f"💰 *Valor:* R$ 250,00\n\n"
            f"Segue meu comprovante de inscrição!"
        )
        ShareEngine.share_whatsapp_status(self.app_page, mensagem)
