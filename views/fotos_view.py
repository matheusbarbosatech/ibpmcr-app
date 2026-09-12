"""
Aba 4: Fotos & Mídia - Super-App IBPM CR.
Super Galeria de fotos dos cultos em alta resolução e feed de Cortes Verticais (Shorts 9:16).
Todos os itens com botões de 1 clique para WhatsApp Status, Stories e Download HD.
"""
import flet as ft
from core.theme import (
    AppColors, FontScaleManager, Icons, AppPadding, AppMargin, AppBorder, AppAlignment
)
from services.db_service import DatabaseService
from services.share_engine import ShareEngine

class FotosView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True)
        self.app_page = page
        self.db = DatabaseService()
        self.active_subtab = 0  # 0: Fotos, 1: Cortes Verticais
        self.content_area = ft.Container(expand=True)

        FontScaleManager.register_listener(self.on_font_scale_changed)
        self.build_ui()

    def on_font_scale_changed(self):
        self.render_content()
        try:
            self.app_page.update()
        except Exception:
            pass

    def build_ui(self):
        self.padding = AppPadding.all(12)

        # Seletor Superior: Fotos dos Cultos vs Cortes Verticais (Shorts)
        btn_fotos = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(Icons.PHOTO_LIBRARY, color=AppColors.TEXT_WHITE if self.active_subtab == 0 else AppColors.SECONDARY_GOLD, size=18),
                    ft.Text("Galeria de Fotos", size=FontScaleManager.s(13), weight=ft.FontWeight.BOLD if self.active_subtab == 0 else ft.FontWeight.NORMAL, color=AppColors.TEXT_WHITE if self.active_subtab == 0 else AppColors.TEXT_SECONDARY),
                ],
                spacing=6,
            ),
            bgcolor=AppColors.PRIMARY_RUBI if self.active_subtab == 0 else AppColors.BG_SURFACE_ALT,
            padding=AppPadding.symmetric(horizontal=14, vertical=10),
            border_radius=10,
            border=AppBorder.all(1, AppColors.PRIMARY_RUBI if self.active_subtab == 0 else AppColors.BORDER_DEFAULT),
            ink=True,
            on_click=lambda e: self.alternar_subtab(0),
        )

        btn_cortes = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(Icons.ONDEMAND_VIDEO, color=AppColors.TEXT_WHITE if self.active_subtab == 1 else AppColors.SECONDARY_GOLD, size=18),
                    ft.Text("Cortes Verticais (Shorts)", size=FontScaleManager.s(13), weight=ft.FontWeight.BOLD if self.active_subtab == 1 else ft.FontWeight.NORMAL, color=AppColors.TEXT_WHITE if self.active_subtab == 1 else AppColors.TEXT_SECONDARY),
                ],
                spacing=6,
            ),
            bgcolor=AppColors.PRIMARY_RUBI if self.active_subtab == 1 else AppColors.BG_SURFACE_ALT,
            padding=AppPadding.symmetric(horizontal=14, vertical=10),
            border_radius=10,
            border=AppBorder.all(1, AppColors.PRIMARY_RUBI if self.active_subtab == 1 else AppColors.BORDER_DEFAULT),
            ink=True,
            on_click=lambda e: self.alternar_subtab(1),
        )

        barra_selecao = ft.Row(
            controls=[btn_fotos, btn_cortes],
            spacing=8,
        )

        self.render_content()

        self.content = ft.Column(
            controls=[
                barra_selecao,
                ft.Divider(color=AppColors.DIVIDER, height=15),
                self.content_area,
            ],
            expand=True,
            spacing=8,
        )

    def alternar_subtab(self, subtab_idx: int):
        self.active_subtab = subtab_idx
        self.build_ui()
        try:
            self.app_page.update()
        except Exception:
            pass

    def render_content(self):
        if self.active_subtab == 0:
            self.content_area.content = self._render_galeria_fotos()
        else:
            self.content_area.content = self._render_cortes_verticais()

    # 1. SUPER GALERIA DE FOTOS DOS CULTOS
    def _render_galeria_fotos(self):
        fotos = self.db.get_galeria_fotos()
        cards_fotos = []

        for f in fotos:
            card = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(f.album_nome, size=FontScaleManager.s(15), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE, expand=True),
                                ft.Container(
                                    content=ft.Text(f.categoria, size=FontScaleManager.s(11), weight=ft.FontWeight.BOLD, color=AppColors.SECONDARY_GOLD),
                                    bgcolor=AppColors.BG_DARK,
                                    padding=AppPadding.symmetric(horizontal=8, vertical=4),
                                    border_radius=8,
                                    border=AppBorder.all(1, AppColors.SECONDARY_GOLD),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Text(f"📅 Data: {f.data_evento}", size=FontScaleManager.s(12), color=AppColors.TEXT_MUTED),
                        ft.Container(height=4),
                        # Foto com pré-visualização
                        ft.Container(
                            content=ft.Image(
                                src=f.foto_thumb_url,
                                width=400,
                                height=200,
                                fit="cover",
                                border_radius=10,
                            ),
                            alignment=AppAlignment.CENTER,
                            on_click=lambda e, foto=f: self.abrir_foto_modal(foto),
                        ),
                        ft.Container(height=6),
                        # Botões de 1 Toque Universal
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(Icons.SEND, color="#FFFFFF", size=16),
                                            ft.Text("Status", color="#FFFFFF", weight=ft.FontWeight.BOLD, size=FontScaleManager.s(12)),
                                        ],
                                        spacing=4,
                                    ),
                                    style=ft.ButtonStyle(
                                        bgcolor=AppColors.ACCENT_GREEN,
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                        padding=AppPadding.symmetric(horizontal=10, vertical=10),
                                    ),
                                    on_click=lambda e, foto=f: ShareEngine.share_whatsapp_status(
                                        self.app_page,
                                        f"📸 *{foto.album_nome} - IBPM CR*\nConfira as fotos e venha celebrar conosco!",
                                        foto.foto_hd_url
                                    ),
                                ),
                                ft.OutlinedButton(
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(Icons.PHOTO_CAMERA, color=AppColors.PRIMARY_RUBI, size=16),
                                            ft.Text("Stories", color=AppColors.PRIMARY_RUBI, weight=ft.FontWeight.BOLD, size=FontScaleManager.s(12)),
                                        ],
                                        spacing=4,
                                    ),
                                    style=ft.ButtonStyle(
                                        side=ft.BorderSide(1, AppColors.PRIMARY_RUBI),
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                        padding=AppPadding.symmetric(horizontal=10, vertical=10),
                                    ),
                                    on_click=lambda e: ShareEngine.share_instagram_stories(self.app_page),
                                ),
                                ft.ElevatedButton(
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(Icons.DOWNLOAD, color="#FFFFFF", size=16),
                                            ft.Text("Baixar HD", color="#FFFFFF", weight=ft.FontWeight.BOLD, size=FontScaleManager.s(12)),
                                        ],
                                        spacing=4,
                                    ),
                                    style=ft.ButtonStyle(
                                        bgcolor=AppColors.PRIMARY_RUBI,
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                        padding=AppPadding.symmetric(horizontal=10, vertical=10),
                                    ),
                                    on_click=lambda e, foto=f: ShareEngine.download_to_device(
                                        self.app_page, foto.foto_hd_url, f"{foto.album_nome}.jpg"
                                    ),
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        )
                    ],
                    spacing=4,
                ),
                bgcolor=AppColors.BG_SURFACE,
                padding=AppPadding.all(14),
                border_radius=14,
                border=AppBorder.all(1, AppColors.BORDER_DEFAULT),
                margin=AppMargin.only(bottom=10),
            )
            cards_fotos.append(card)

        return ft.ListView(
            controls=[
                ft.Text("📸 Super Galeria de Fotos dos Cultos", size=FontScaleManager.s(18), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                ft.Text("Baixe fotos de alta definição dos cultos, batismos e eventos da igreja.", size=FontScaleManager.s(13), color=AppColors.TEXT_MUTED),
                ft.Container(height=6),
                *cards_fotos,
                ft.Container(height=30),
            ],
            expand=True,
            spacing=8,
        )

    def abrir_foto_modal(self, foto):
        def fechar(e=None):
            try:
                self.app_page.close(dlg)
            except Exception:
                dlg.open = False
                self.app_page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(foto.album_nome, size=FontScaleManager.s(16), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
            content=ft.Column(
                controls=[
                    ft.Image(src=foto.foto_hd_url, width=400, height=280, fit="contain", border_radius=8),
                    ft.Container(height=6),
                    ft.Text("Foto em resolução original HD.", size=FontScaleManager.s(12), color=AppColors.TEXT_MUTED),
                ],
                tight=True,
                spacing=6,
            ),
            actions=[
                ft.TextButton("Fechar", on_click=fechar),
                ft.ElevatedButton(
                    "Baixar Foto HD",
                    bgcolor=AppColors.PRIMARY_RUBI,
                    color="#FFFFFF",
                    on_click=lambda e: ShareEngine.download_to_device(self.app_page, foto.foto_hd_url, f"{foto.album_nome}.jpg"),
                )
            ],
            bgcolor=AppColors.BG_SURFACE,
        )

        try:
            self.app_page.open(dlg)
        except Exception:
            self.app_page.dialog = dlg
            dlg.open = True
            self.app_page.update()

    # 2. CORTES VERTICAIS (SHORTS 9:16)
    def _render_cortes_verticais(self):
        cortes = self.db.get_cortes_verticais()
        cards_cortes = []

        for c in cortes:
            card = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Container(
                                    content=ft.Text(f"🔥 Nota {c.nota_viral}", size=FontScaleManager.s(11), weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                                    bgcolor=AppColors.PRIMARY_RUBI,
                                    padding=AppPadding.symmetric(horizontal=8, vertical=4),
                                    border_radius=8,
                                ),
                                ft.Text(f"⏱️ {c.duracao_segundos}s • {c.tema_categoria}", size=FontScaleManager.s(12), color=AppColors.SECONDARY_GOLD),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Container(height=4),
                        ft.Text(c.titulo_impacto, size=FontScaleManager.s(15), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                        ft.Container(height=6),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(Icons.PLAY_ARROW, color="#FFFFFF", size=18),
                                            ft.Text("Assistir Corte", color="#FFFFFF", weight=ft.FontWeight.BOLD, size=FontScaleManager.s(12)),
                                        ],
                                        spacing=4,
                                    ),
                                    style=ft.ButtonStyle(
                                        bgcolor=AppColors.PRIMARY_RUBI,
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                        padding=AppPadding.symmetric(horizontal=12, vertical=10),
                                    ),
                                    on_click=lambda e, vid=c: self.app_page.launch_url(vid.video_9_16_url),
                                ),
                                ft.ElevatedButton(
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(Icons.SEND, color="#FFFFFF", size=16),
                                            ft.Text("Status WhatsApp", color="#FFFFFF", weight=ft.FontWeight.BOLD, size=FontScaleManager.s(12)),
                                        ],
                                        spacing=4,
                                    ),
                                    style=ft.ButtonStyle(
                                        bgcolor=AppColors.ACCENT_GREEN,
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                        padding=AppPadding.symmetric(horizontal=10, vertical=10),
                                    ),
                                    on_click=lambda e, vid=c: ShareEngine.share_whatsapp_status(
                                        self.app_page,
                                        f"🎬 *{vid.titulo_impacto} - IBPM CR*\nAssista a este corte abençoado!",
                                        vid.video_9_16_url
                                    ),
                                ),
                                ft.IconButton(
                                    icon=Icons.DOWNLOAD,
                                    icon_color=AppColors.SECONDARY_GOLD,
                                    tooltip="Baixar vídeo MP4",
                                    on_click=lambda e, vid=c: ShareEngine.download_to_device(
                                        self.app_page, vid.video_9_16_url, f"{vid.titulo_impacto}.mp4"
                                    ),
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        )
                    ],
                    spacing=4,
                ),
                bgcolor=AppColors.BG_SURFACE,
                padding=AppPadding.all(14),
                border_radius=14,
                border=AppBorder.all(1, AppColors.BORDER_DEFAULT),
                margin=AppMargin.only(bottom=10),
            )
            cards_cortes.append(card)

        return ft.ListView(
            controls=[
                ft.Text("🎬 Cortes Verticais & Mensagens de Impacto", size=FontScaleManager.s(18), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                ft.Text("Vídeos curtos (9:16) prontos para postar no WhatsApp Status e Instagram Stories.", size=FontScaleManager.s(13), color=AppColors.TEXT_MUTED),
                ft.Container(height=6),
                *cards_cortes,
                ft.Container(height=30),
            ],
            expand=True,
            spacing=8,
        )
