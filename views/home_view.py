"""
Aba 1: Início - Super-App IBPM CR.
Destaques do Culto Ao Vivo, Pílula Pastoral em Áudio, Frase Profética Interativa e Atalhos Rápidos.
"""
import flet as ft
from core.theme import (
    AppColors, FontScaleManager, Icons, AppPadding, AppMargin, AppBorder, AppAlignment
)
from core.config import YOUTUBE_LIVE_URL, CHAVE_PIX
from core.audio_service import AudioService, AudioTrack
from services.db_service import DatabaseService
from services.share_engine import ShareEngine

class HomeView(ft.Container):
    def __init__(self, page: ft.Page, navigate_to_tab=None):
        super().__init__(expand=True)
        self.app_page = page
        self.navigate_to_tab = navigate_to_tab
        self.db = DatabaseService()
        self.audio_service = AudioService()
        self.selected_sentimento = "todos"
        
        # Referências
        self.frase_text = ft.Text("", size=FontScaleManager.s(16), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE, text_align=ft.TextAlign.CENTER)
        self.frase_ref = ft.Text("", size=FontScaleManager.s(13), color=AppColors.SECONDARY_GOLD, weight=ft.FontWeight.W_600)
        self.current_frase_obj = None
        self.btn_audio_play = None
        self.audio_status_text = None
        self.btn_radio_play = None
        self.radio_status_text = None

        FontScaleManager.register_listener(self.on_font_scale_changed)
        self.build_ui()

    def on_font_scale_changed(self):
        self.update_font_sizes()
        try:
            self.app_page.update()
        except Exception:
            pass

    def update_font_sizes(self):
        self.frase_text.size = FontScaleManager.s(16)
        self.frase_ref.size = FontScaleManager.s(13)

    def build_ui(self):
        self.padding = AppPadding.all(12)

        # 1. BANNER DO CULTO AO VIVO / TRANSMISSÃO
        banner_ao_vivo = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Container(width=10, height=10, bgcolor=AppColors.PRIMARY_RUBI, border_radius=5),
                                        ft.Text("AO VIVO NO TEMPLO", size=FontScaleManager.s(12), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                                    ],
                                    spacing=6,
                                ),
                                bgcolor="#380D17",
                                padding=AppPadding.symmetric(horizontal=10, vertical=4),
                                border_radius=12,
                                border=AppBorder.all(1, AppColors.PRIMARY_RUBI),
                            ),
                            ft.Text("Domingo às 19h", size=FontScaleManager.s(12), color=AppColors.TEXT_MUTED),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Text(
                        "Culto da Família & Celebração Profética",
                        size=FontScaleManager.s(18),
                        weight=ft.FontWeight.BOLD,
                        color=AppColors.TEXT_WHITE,
                    ),
                    ft.Text(
                        "Venha adorar presencialmente na Carvalho Ramos ou acompanhe a transmissão ao vivo.",
                        size=FontScaleManager.s(13),
                        color=AppColors.TEXT_SECONDARY,
                    ),
                    ft.Container(height=6),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(Icons.PLAY_ARROW, color="#FFFFFF", size=20),
                                        ft.Text("Assistir Culto", weight=ft.FontWeight.BOLD, color="#FFFFFF", size=FontScaleManager.s(14)),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=6,
                                ),
                                style=ft.ButtonStyle(
                                    bgcolor=AppColors.PRIMARY_RUBI,
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    padding=AppPadding.symmetric(horizontal=16, vertical=12),
                                ),
                                on_click=lambda e: self.app_page.launch_url(YOUTUBE_LIVE_URL),
                            ),
                            ft.OutlinedButton(
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(Icons.SHARE, color=AppColors.SECONDARY_GOLD, size=18),
                                        ft.Text("Convidar", color=AppColors.SECONDARY_GOLD, weight=ft.FontWeight.BOLD, size=FontScaleManager.s(13)),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=6,
                                ),
                                style=ft.ButtonStyle(
                                    side=ft.BorderSide(1, AppColors.SECONDARY_GOLD),
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    padding=AppPadding.symmetric(horizontal=14, vertical=12),
                                ),
                                on_click=lambda e: ShareEngine.share_whatsapp_status(
                                    self.app_page,
                                    "🔥 Venha participar conosco do Culto da Família na IBPM CR! Transmissão ao vivo pelo canal oficial.",
                                    YOUTUBE_LIVE_URL
                                ),
                            ),
                        ],
                        spacing=10,
                    )
                ],
                spacing=8,
            ),
            bgcolor=AppColors.BG_SURFACE,
            padding=AppPadding.all(16),
            border_radius=16,
            border=AppBorder.all(1.5, AppColors.PRIMARY_RUBI),
            margin=AppMargin.only(bottom=12),
        )

        # 2. PÍLULA PASTORAL EM ÁUDIO (COM SUPORTE A TELA BLOQUEADA)
        self.btn_audio_play = ft.IconButton(
            icon=Icons.PLAY_ARROW,
            icon_color="#000000",
            bgcolor=AppColors.SECONDARY_GOLD,
            icon_size=26,
            tooltip="Ouvir pílula pastoral",
            on_click=self.tocar_pilula_pastoral,
        )
        self.audio_status_text = ft.Text("Toque para ouvir a ministração", size=FontScaleManager.s(12), color=AppColors.TEXT_MUTED)

        card_audio_pilula = ft.Container(
            content=ft.Row(
                controls=[
                    self.btn_audio_play,
                    ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text("Pílula Pastoral do Dia", size=FontScaleManager.s(15), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                                    ft.Container(
                                        content=ft.Text("ÁUDIO", size=FontScaleManager.s(10), weight=ft.FontWeight.BOLD, color=AppColors.SECONDARY_GOLD),
                                        bgcolor=AppColors.BG_DARK,
                                        padding=AppPadding.symmetric(horizontal=6, vertical=2),
                                        border_radius=6,
                                        border=AppBorder.all(1, AppColors.SECONDARY_GOLD),
                                    )
                                ],
                                spacing=8,
                            ),
                            ft.Text("Uma Palavra de Ânimo para a sua Semana", size=FontScaleManager.s(13), color=AppColors.SECONDARY_GOLD),
                            self.audio_status_text,
                        ],
                        expand=True,
                        spacing=2,
                    ),
                    ft.IconButton(
                        icon=Icons.HEADPHONES,
                        icon_color=AppColors.TEXT_MUTED,
                        tooltip="Suporte a tela bloqueada",
                    )
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
            ),
            bgcolor=AppColors.BG_SURFACE,
            padding=AppPadding.all(14),
            border_radius=14,
            border=AppBorder.all(1, AppColors.BORDER_DEFAULT),
            margin=AppMargin.only(bottom=12),
        )

        # 3. RÁDIO IBPM CR • 24 HORAS NO ALTAR (ESTILO RÁDIO MAANAIM)
        self.btn_radio_play = ft.IconButton(
            icon=Icons.RADIO,
            icon_color="#FFFFFF",
            bgcolor=AppColors.PRIMARY_RUBI,
            icon_size=26,
            tooltip="Ouvir Rádio IBPM CR Ao Vivo",
            on_click=self.tocar_radio_ibpmcr,
        )
        self.radio_status_text = ft.Text(
            "🔴 NO AR • Louvores & Palavra 24h",
            size=FontScaleManager.s(12),
            color=AppColors.SECONDARY_GOLD,
        )

        card_radio_ibpmcr = ft.Container(
            content=ft.Row(
                controls=[
                    self.btn_radio_play,
                    ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text("Rádio IBPM CR", size=FontScaleManager.s(15), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                                    ft.Container(
                                        content=ft.Text("AO VIVO 24H", size=FontScaleManager.s(9), weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                                        bgcolor=AppColors.PRIMARY_RUBI,
                                        padding=AppPadding.symmetric(horizontal=6, vertical=2),
                                        border_radius=6,
                                    )
                                ],
                                spacing=6,
                            ),
                            ft.Text("Sintonize a Presença de Deus no Altar", size=FontScaleManager.s(12), color=AppColors.TEXT_SECONDARY),
                            self.radio_status_text,
                        ],
                        expand=True,
                        spacing=2,
                    ),
                    ft.IconButton(
                        icon=Icons.FAVORITE,
                        icon_color=AppColors.SECONDARY_GOLD,
                        tooltip="Pedir Louvor / Oração na Rádio",
                        on_click=lambda e: ShareEngine.share_whatsapp_status(
                            self.app_page,
                            "📻 *Pedido de Louvor & Oração - Rádio IBPM CR*\nPaz do Senhor! Gostaria de pedir oração e um louvor abençoado na Rádio IBPM CR!"
                        )
                    )
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
            ),
            bgcolor=AppColors.BG_SURFACE,
            padding=AppPadding.all(14),
            border_radius=14,
            border=AppBorder.all(1.2, AppColors.SECONDARY_GOLD),
            margin=AppMargin.only(bottom=14),
        )

        # 4. WIDGET DA FRASE PROFÉTICA DO DIA (INTERATIVO POR SENTIMENTO)
        sentimentos_chips = [
            ("Todos", "todos"),
            ("Ansiedade", "ansiedade"),
            ("Medo", "medo"),
            ("Fé", "fe"),
            ("Gratidão", "gratidao"),
            ("Vitória", "vitoria"),
            ("Desânimo", "desanimo")
        ]

        chips_controls = []
        for rotulo, tag in sentimentos_chips:
            is_active = (self.selected_sentimento == tag)
            btn_chip = ft.Container(
                content=ft.Text(
                    rotulo,
                    size=FontScaleManager.s(13),
                    weight=ft.FontWeight.BOLD if is_active else ft.FontWeight.NORMAL,
                    color=AppColors.TEXT_WHITE if is_active else AppColors.TEXT_SECONDARY,
                ),
                bgcolor=AppColors.PRIMARY_RUBI if is_active else AppColors.BG_SURFACE_ALT,
                padding=AppPadding.symmetric(horizontal=12, vertical=8),
                border_radius=10,
                border=AppBorder.all(1, AppColors.PRIMARY_RUBI if is_active else AppColors.BORDER_DEFAULT),
                on_click=lambda e, t=tag: self.filtrar_frase(t),
            )
            chips_controls.append(btn_chip)

        self.atualizar_frase_exibida()

        card_frase_profetica = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(Icons.AUTO_AWESOME, color=AppColors.SECONDARY_GOLD, size=20),
                            ft.Text("Frase Profética para o Seu Dia", size=FontScaleManager.s(15), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                        ],
                        spacing=8,
                    ),
                    ft.Container(height=4),
                    # Carrossel horizontal de sentimentos
                    ft.Row(controls=chips_controls, scroll=ft.ScrollMode.AUTO, spacing=8),
                    ft.Container(height=8),
                    # Card central da frase
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                self.frase_text,
                                ft.Container(height=4),
                                self.frase_ref,
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=4,
                        ),
                        bgcolor=AppColors.BG_DARK,
                        padding=AppPadding.all(16),
                        border_radius=12,
                        border=AppBorder.all(1, AppColors.BORDER_GOLD),
                    ),
                    ft.Container(height=6),
                    # Botões de 1 Toque para Compartilhamento
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(Icons.SEND, color="#FFFFFF", size=16),
                                        ft.Text("Status WhatsApp", weight=ft.FontWeight.BOLD, color="#FFFFFF", size=FontScaleManager.s(12)),
                                    ],
                                    spacing=6,
                                ),
                                style=ft.ButtonStyle(
                                    bgcolor=AppColors.ACCENT_GREEN,
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    padding=AppPadding.symmetric(horizontal=12, vertical=10),
                                ),
                                on_click=self.compartilhar_frase_whatsapp,
                            ),
                            ft.OutlinedButton(
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(Icons.PHOTO_CAMERA, color=AppColors.PRIMARY_RUBI, size=16),
                                        ft.Text("Stories", color=AppColors.PRIMARY_RUBI, weight=ft.FontWeight.BOLD, size=FontScaleManager.s(12)),
                                    ],
                                    spacing=6,
                                ),
                                style=ft.ButtonStyle(
                                    side=ft.BorderSide(1, AppColors.PRIMARY_RUBI),
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    padding=AppPadding.symmetric(horizontal=12, vertical=10),
                                ),
                                on_click=self.compartilhar_frase_stories,
                            ),
                            ft.IconButton(
                                icon=Icons.COPY_ALL,
                                icon_color=AppColors.SECONDARY_GOLD,
                                tooltip="Copiar texto da frase",
                                on_click=self.copiar_frase,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
                spacing=8,
            ),
            bgcolor=AppColors.BG_SURFACE,
            padding=AppPadding.all(16),
            border_radius=16,
            border=AppBorder.all(1, AppColors.BORDER_DEFAULT),
            margin=AppMargin.only(bottom=14),
        )

        # 4. ATALHOS RÁPIDOS SÊNIOR-FRIENDLY (Área de Toque >= 48dp)
        atalhos_grid = ft.Row(
            controls=[
                self._criar_card_atalho("Dízimos", "Chave PIX", Icons.QR_CODE, AppColors.SECONDARY_GOLD, self.copiar_pix_oficial),
                self._criar_card_atalho("Oração", "Intercessão", Icons.VOLUNTEER_ACTIVISM, AppColors.PRIMARY_RUBI, lambda e: self.ir_para_aba(1)),
                self._criar_card_atalho("Estudos", "Palavra", Icons.MENU_BOOK, AppColors.ACCENT_BLUE, lambda e: self.ir_para_aba(2)),
                self._criar_card_atalho("Como Chegar", "Templo & Cultos", Icons.LOCATION_ON, AppColors.SECONDARY_GOLD, self.abrir_modal_como_chegar),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=6,
        )

        self.content = ft.ListView(
            controls=[
                banner_ao_vivo,
                card_audio_pilula,
                card_radio_ibpmcr,
                card_frase_profetica,
                ft.Text("Acesso Rápido da Congregação", size=FontScaleManager.s(15), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                ft.Container(height=4),
                atalhos_grid,
                ft.Container(height=30),
            ],
            expand=True,
            spacing=6,
        )

    def _criar_card_atalho(self, titulo: str, subtitulo: str, icone, cor_icone, on_click_action):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(icone, color=cor_icone, size=30),
                    ft.Text(titulo, size=FontScaleManager.s(13), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE, text_align=ft.TextAlign.CENTER),
                    ft.Text(subtitulo, size=FontScaleManager.s(11), color=AppColors.TEXT_MUTED, text_align=ft.TextAlign.CENTER),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=4,
            ),
            bgcolor=AppColors.BG_SURFACE,
            padding=AppPadding.all(12),
            border_radius=12,
            border=AppBorder.all(1, AppColors.BORDER_DEFAULT),
            expand=True,
            height=110,  # Área ampla para toque fácil de idosos (>> 48dp)
            on_click=on_click_action,
        )

    def filtrar_frase(self, sentimento: str):
        self.selected_sentimento = sentimento
        self.atualizar_frase_exibida()
        self.build_ui()
        try:
            self.app_page.update()
        except Exception:
            pass

    def atualizar_frase_exibida(self):
        frases = self.db.get_frases_por_sentimento(self.selected_sentimento)
        if frases:
            self.current_frase_obj = frases[0]
            self.frase_text.value = f"\"{self.current_frase_obj.frase}\""
            self.frase_ref.value = f"📖 {self.current_frase_obj.referencia_biblica or 'Palavra Pastoral'}"
        else:
            self.frase_text.value = "\"O Senhor é o meu pastor; nada me faltará.\""
            self.frase_ref.value = "📖 Salmos 23:1"

    def compartilhar_frase_whatsapp(self, e):
        texto = f"{self.frase_text.value}\n{self.frase_ref.value}"
        ShareEngine.share_whatsapp_status(self.app_page, texto)

    def compartilhar_frase_stories(self, e):
        ShareEngine.share_instagram_stories(self.app_page)

    def copiar_frase(self, e):
        ShareEngine.copy_to_clipboard(self.app_page, f"{self.frase_text.value} - {self.frase_ref.value}", "Frase copiada!")

    def tocar_pilula_pastoral(self, e):
        track = AudioTrack(
            title="Pílula Pastoral - Uma Palavra de Ânimo",
            subtitle="Pastor Presidente • IBPM CR",
            audio_url="https://midia.ibpmcr.com.br/audios/pilula_pastoral_hoje.mp3"
        )
        self.audio_service.play_track(track)
        self.audio_status_text.value = "▶️ Tocando em segundo plano..."
        self.audio_status_text.color = AppColors.SECONDARY_GOLD
        try:
            self.app_page.update()
        except Exception:
            pass
        ShareEngine.show_feedback(self.app_page, "🎧 Áudio em reprodução! Pode bloquear a tela que o som continuará.")

    def tocar_radio_ibpmcr(self, e):
        track = AudioTrack(
            title="Rádio IBPM CR • 24 Horas",
            subtitle="Louvores do Altar & Ministrações Contínuas",
            audio_url=os.getenv("RADIO_STREAM_URL", "https://stream.zeno.fm/f3wvbbqmdg8uv")
        )
        if self.audio_service.is_playing and self.audio_service.current_track and "Rádio IBPM" in self.audio_service.current_track.title:
            self.audio_service.toggle_play_pause()
            if self.radio_status_text:
                self.radio_status_text.value = "⏸️ Rádio Pausada • Toque para sintonizar"
                self.radio_status_text.color = AppColors.TEXT_MUTED
            if self.btn_radio_play:
                self.btn_radio_play.icon = Icons.PLAY_ARROW
        else:
            self.audio_service.play_track(track)
            if self.radio_status_text:
                self.radio_status_text.value = "▶️ Sintonizado • Tocando ao vivo em segundo plano"
                self.radio_status_text.color = AppColors.SECONDARY_GOLD
            if self.btn_radio_play:
                self.btn_radio_play.icon = Icons.PAUSE
            ShareEngine.show_feedback(self.app_page, "📻 Rádio IBPM CR sintonizada! Som contínuo em segundo plano.")
        try:
            self.app_page.update()
        except Exception:
            pass

    def copiar_pix_oficial(self, e):
        ShareEngine.copy_to_clipboard(self.app_page, CHAVE_PIX, f"✅ Chave PIX copiada: {CHAVE_PIX}")

    def ir_para_aba(self, indice_aba: int):
        if self.navigate_to_tab:
            self.navigate_to_tab(indice_aba)

    def abrir_modal_como_chegar(self, e):
        def fechar(ev):
            try:
                self.app_page.close(dlg)
            except Exception:
                dlg.open = False
                self.app_page.update()

        dlg = ft.AlertDialog(
            modal=False,
            title=ft.Row(
                controls=[
                    ft.Icon(Icons.CHURCH, color=AppColors.SECONDARY_GOLD, size=24),
                    ft.Text("Templo Sede • IBPM CR", weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE, size=FontScaleManager.s(16)),
                ],
                spacing=8,
            ),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("📍 ENDEREÇO OFICIAL", size=FontScaleManager.s(11), weight=ft.FontWeight.BOLD, color=AppColors.PRIMARY_RUBI),
                                    ft.Text("Rua Ajurana, 510 - Campo Grande / Carvalho Ramos", size=FontScaleManager.s(13), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                                    ft.Text("Rio de Janeiro - RJ • CEP 23050-000", size=FontScaleManager.s(12), color=AppColors.TEXT_MUTED),
                                ],
                                spacing=2,
                            ),
                            bgcolor=AppColors.BG_DARK,
                            padding=AppPadding.all(12),
                            border_radius=10,
                            border=AppBorder.all(1, AppColors.BORDER_DEFAULT),
                        ),
                        ft.Container(height=4),
                        ft.Text("🗺️ TRAÇAR ROTA NO GPS:", size=FontScaleManager.s(12), weight=ft.FontWeight.BOLD, color=AppColors.SECONDARY_GOLD),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    content=ft.Row([ft.Icon(Icons.MAP, size=16), ft.Text("Google Maps")]),
                                    style=ft.ButtonStyle(bgcolor=AppColors.PRIMARY_RUBI),
                                    on_click=lambda ev: self.app_page.launch_url("https://www.google.com/maps/search/?api=1&query=Rua+Ajurana+510+Campo+Grande+Rio+de+Janeiro"),
                                ),
                                ft.OutlinedButton(
                                    content=ft.Row([ft.Icon(Icons.DIRECTIONS_CAR, size=16), ft.Text("Waze")]),
                                    style=ft.ButtonStyle(side=ft.BorderSide(1, AppColors.SECONDARY_GOLD), color=AppColors.SECONDARY_GOLD),
                                    on_click=lambda ev: self.app_page.launch_url("https://waze.com/ul?q=Rua+Ajurana+510+Campo+Grande+Rio+de+Janeiro"),
                                ),
                            ],
                            spacing=8,
                        ),
                        ft.Divider(color=AppColors.DIVIDER),
                        ft.Text("🗓️ HORÁRIOS DOS CULTOS & CLAMORES:", size=FontScaleManager.s(12), weight=ft.FontWeight.BOLD, color=AppColors.SECONDARY_GOLD),
                        ft.Text("• Domingo às 19h00: Culto da Família & Celebração Profética", size=FontScaleManager.s(13), color=AppColors.TEXT_WHITE),
                        ft.Text("• Quarta às 19h30: Culto de Oração, Clamor & Doutrina", size=FontScaleManager.s(13), color=AppColors.TEXT_WHITE),
                        ft.Text("• Sexta às 19h30: Reunião da Mocidade & Clamor", size=FontScaleManager.s(13), color=AppColors.TEXT_WHITE),
                        ft.Text("• Diariamente às 06h00: Altar da Manhã & Intercessão", size=FontScaleManager.s(13), color=AppColors.TEXT_SECONDARY),
                        ft.Container(height=4),
                    ],
                    tight=True,
                    spacing=6,
                ),
                width=450,
            ),
            actions=[
                ft.ElevatedButton(
                    content=ft.Row([ft.Icon(Icons.CHAT, size=16), ft.Text("Falar com a Recepção")]),
                    style=ft.ButtonStyle(bgcolor=AppColors.ACCENT_GREEN),
                    on_click=lambda ev: ShareEngine.share_whatsapp_status(
                        self.app_page,
                        "🕊️ *Paz do Senhor!* Sou visitante no Super-App e gostaria de tirar dúvidas sobre o próximo culto presencial na IBPM CR!"
                    ),
                ),
                ft.TextButton("Fechar", on_click=fechar),
            ],
            bgcolor=AppColors.BG_SURFACE,
        )

        try:
            self.app_page.open(dlg)
        except Exception:
            self.app_page.dialog = dlg
            dlg.open = True
            self.app_page.update()
