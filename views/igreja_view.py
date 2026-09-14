"""
Aba 4: Igreja & Dízimo — IBPM CR.
Página dedicada, digna e transparente para Dízimos e Ofertas no PIX,
Localização com rotas (Waze, Maps, Uber) e Contatos Pastorais.
"""
import urllib.parse
import flet as ft
from core.theme import (
    AppColors, FontScaleManager, Icons, AppPadding, AppMargin, AppBorder, AppAlignment, AppDialog, AppUrl
)
from services.share_engine import ShareEngine


class IgrejaView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True)
        self.app_page = page
        self.pix_chave = "ibpmcr7976@gmail.com"
        self.endereco_igreja = "Rua General Carvalho Ramos, Marechal Hermes, Rio de Janeiro - RJ"
        self.build_ui()

    def build_ui(self):
        # 1. Header Oficial
        header = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(Icons.CHURCH_ROUNDED, color=AppColors.SECONDARY_GOLD, size=24),
                            ft.Text("COMUNHÃO & GENEROSIDADE", size=FontScaleManager.s(12), weight=ft.FontWeight.BOLD, color=AppColors.SECONDARY_GOLD),
                        ],
                        spacing=6,
                    ),
                    ft.Text(
                        "IBPM Carvalho Ramos",
                        size=FontScaleManager.s(22),
                        weight=ft.FontWeight.BOLD,
                        color=AppColors.TEXT_WHITE,
                    ),
                    ft.Text(
                        "Uma igreja de coração ardente, missionária e acolhedora em Marechal Hermes.",
                        size=FontScaleManager.s(13),
                        color=AppColors.TEXT_SECONDARY,
                    ),
                ],
                spacing=4,
            ),
            padding=AppPadding.only(bottom=16),
        )

        # 2. Card Dízimos e Ofertas PIX (Digno, limpo e seguro)
        card_dizimo = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Icon(Icons.VOLUNTEER_ACTIVISM_ROUNDED, color=AppColors.PRIMARY_RUBI, size=22),
                                bgcolor=AppColors.BG_SURFACE_ALT,
                                padding=AppPadding.all(8),
                                border_radius=12,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text("Dízimos e Ofertas do Altar", size=FontScaleManager.s(15), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                                    ft.Text("“Cada um contribua segundo propôs no seu coração” (2 Co 9:7)", size=FontScaleManager.s(11), color=AppColors.TEXT_MUTED),
                                ],
                                spacing=1,
                                expand=True,
                            ),
                        ],
                        spacing=12,
                    ),
                    ft.Container(height=12),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Chave PIX Oficial (E-mail):", size=FontScaleManager.s(11), color=AppColors.TEXT_MUTED),
                                ft.Row(
                                    controls=[
                                        ft.Text(self.pix_chave, size=FontScaleManager.s(14), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE, expand=True),
                                        ft.ElevatedButton(
                                            content=ft.Row(
                                                controls=[
                                                    ft.Icon(Icons.COPY_ROUNDED, size=16, color=AppColors.TEXT_WHITE),
                                                    ft.Text("Copiar PIX", size=FontScaleManager.s(12), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                                                ],
                                                spacing=4,
                                            ),
                                            bgcolor=AppColors.PRIMARY_RUBI,
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=10),
                                                padding=AppPadding.symmetric(horizontal=12, vertical=8),
                                            ),
                                            on_click=self.copiar_pix,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                ft.Container(height=2),
                                ft.Text("Favorecido: Igreja Batista do Povo Missionária", size=FontScaleManager.s(11), color=AppColors.SECONDARY_GOLD),
                            ],
                            spacing=4,
                        ),
                        bgcolor=AppColors.BG_SURFACE_ALT,
                        padding=AppPadding.all(14),
                        border_radius=14,
                        border=AppBorder.all(1, AppColors.BORDER_DEFAULT),
                    ),
                    ft.Container(height=6),
                    ft.TextButton(
                        content=ft.Row(
                            controls=[
                                ft.Icon(Icons.SEND_ROUNDED, color=AppColors.ACCENT_GREEN, size=16),
                                ft.Text("Enviar Comprovante no WhatsApp da Secretaria", size=FontScaleManager.s(12), color=AppColors.ACCENT_GREEN, weight=ft.FontWeight.BOLD),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=6,
                        ),
                        on_click=self.enviar_comprovante_whatsapp,
                    ),
                ],
                spacing=6,
            ),
            bgcolor=AppColors.BG_SURFACE,
            padding=AppPadding.all(18),
            border_radius=18,
            border=AppBorder.all(1, AppColors.BORDER_DEFAULT),
        )

        # 3. Card Localização & Rotas (Waze, Maps, Uber)
        def criar_btn_rota(rotulo, icone, url_destino):
            return ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(icone, color=AppColors.SECONDARY_GOLD, size=16),
                        ft.Text(rotulo, size=FontScaleManager.s(12), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=6,
                ),
                bgcolor=AppColors.BG_SURFACE_ALT,
                padding=AppPadding.symmetric(horizontal=12, vertical=10),
                border_radius=12,
                border=AppBorder.all(1, AppColors.BORDER_DEFAULT),
                expand=True,
                ink=True,
                on_click=lambda e: AppUrl.launch(self.app_page, url_destino),
            )

        card_localizacao = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(Icons.MAP_ROUNDED, color=AppColors.SECONDARY_GOLD, size=20),
                            ft.Text("Onde Estamos", size=FontScaleManager.s(14), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                        ],
                        spacing=8,
                    ),
                    ft.Text(
                        self.endereco_igreja,
                        size=FontScaleManager.s(13),
                        color=AppColors.TEXT_SECONDARY,
                    ),
                    ft.Container(height=8),
                    ft.Row(
                        controls=[
                            criar_btn_rota("Waze", Icons.NAVIGATION_ROUNDED, f"https://waze.com/ul?q={urllib.parse.quote(self.endereco_igreja)}"),
                            criar_btn_rota("Google Maps", Icons.PIN_DROP_ROUNDED, f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(self.endereco_igreja)}"),
                            criar_btn_rota("Uber", Icons.LOCAL_TAXI_ROUNDED, f"https://m.uber.com/ul/?action=setPickup&dropoff[formatted_address]={urllib.parse.quote(self.endereco_igreja)}"),
                        ],
                        spacing=8,
                    ),
                ],
                spacing=6,
            ),
            bgcolor=AppColors.BG_SURFACE,
            padding=AppPadding.all(18),
            border_radius=18,
            border=AppBorder.all(1, AppColors.BORDER_DEFAULT),
        )

        # 4. Card Redes e Contato Oficial
        def criar_canal(nome, subtitulo, icone, link):
            return ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(icone, color=AppColors.SECONDARY_GOLD, size=20),
                        ft.Column(
                            controls=[
                                ft.Text(nome, size=FontScaleManager.s(13), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                                ft.Text(subtitulo, size=FontScaleManager.s(11), color=AppColors.TEXT_MUTED),
                            ],
                            spacing=1,
                            expand=True,
                        ),
                        ft.Icon(Icons.CHEVRON_RIGHT_ROUNDED, color=AppColors.TEXT_MUTED, size=18),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=AppPadding.symmetric(vertical=6),
                ink=True,
                on_click=lambda e: AppUrl.launch(self.app_page, link),
            )

        card_redes = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Canais Oficiais da Congregação", size=FontScaleManager.s(14), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                    ft.Container(height=4),
                    criar_canal("Instagram Oficial", "@ibpmcr7976 • Fotos e Avisos", Icons.CAMERA_ALT_ROUNDED, "https://www.instagram.com/ibpmcr7976/"),
                    criar_canal("Canal do YouTube", "Cultos ao vivo e pregações", Icons.PLAY_ARROW_ROUNDED, "https://www.youtube.com/@ibpmcr7976"),
                    criar_canal("WhatsApp Secretaria", "Atendimento e Gabinete Pastoral", Icons.CHAT_ROUNDED, "https://api.whatsapp.com/send?phone=5521999999999&text=Ol%C3%A1%2C%20gostaria%20de%20informa%C3%A7%C3%B5es%20sobre%20a%20IBPM%20CR"),
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
                card_dizimo,
                ft.Container(height=14),
                card_localizacao,
                ft.Container(height=14),
                card_redes,
                ft.Container(height=24),
            ],
            padding=AppPadding.symmetric(horizontal=16, vertical=12),
            spacing=0,
        )

    def copiar_pix(self, e=None):
        ShareEngine.copy_to_clipboard(self.app_page, self.pix_chave, "Chave PIX oficial copiada com sucesso!")

    def enviar_comprovante_whatsapp(self, e=None):
        mensagem = (
            f"🕊️ *COMPROVANTE DE DÍZIMO / OFERTA — IBPM CR*\n\n"
            f"Olá secretaria, segue o meu comprovante de contribuição ao Reino de Deus.\n"
            f"“Deus ama ao que dá com alegria!” (2 Co 9:7)"
        )
        ShareEngine.share_whatsapp_status(self.app_page, mensagem)
