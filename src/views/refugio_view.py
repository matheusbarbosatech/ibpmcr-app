import flet as ft

try:
    from src.theme import AppColors, SENTIMENTOS_PADRAO, Icons, AppPadding, AppMargin, AppBorder
except ModuleNotFoundError:
    from theme import AppColors, SENTIMENTOS_PADRAO, Icons, AppPadding, AppMargin, AppBorder

class RefugioView(ft.Container):
    """
    Tela do Refúgio Silencioso - O coração acolhedor do IBPM CR App.
    Permite pedir oração em 1 toque sem atrito de digitação e com total respeito à privacidade.
    """
    def __init__(self, page: ft.Page):
        super().__init__(expand=True)
        self.app_page = page
        self.selected_sentimento_id = "peito_pesado"  # Padrão carinhoso pré-selecionado
        self.is_anonimo = True
        
        # Referências de controles
        self.sentiment_cards_column = ft.Column(spacing=10)
        self.custom_text_field = ft.TextField(
            label="Desabafe em poucas palavras (opcional)",
            hint_text="Escreva aqui se desejar...",
            multiline=True,
            min_lines=2,
            max_lines=3,
            border_color=AppColors.BORDER_DEFAULT,
            focused_border_color=AppColors.PRIMARY,
            text_style=ft.TextStyle(color=AppColors.TEXT_PRIMARY, size=14),
            visible=False,
        )
        
        # Campos de contato discreto
        self.nome_input = ft.TextField(
            label="Seu Nome ou Apelido",
            hint_text="Ex: Lucas",
            border_color=AppColors.BORDER_DEFAULT,
            focused_border_color=AppColors.PRIMARY,
            text_style=ft.TextStyle(color=AppColors.TEXT_PRIMARY, size=14),
            prefix_icon=Icons.PERSON,
        )
        self.whatsapp_input = ft.TextField(
            label="Seu WhatsApp (apenas para contato pastoral)",
            hint_text="(11) 99999-9999",
            keyboard_type=ft.KeyboardType.PHONE,
            border_color=AppColors.BORDER_DEFAULT,
            focused_border_color=AppColors.PRIMARY,
            text_style=ft.TextStyle(color=AppColors.TEXT_PRIMARY, size=14),
            prefix_icon=Icons.PHONE,
        )
        self.contato_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Informações para cuidado discreto:",
                        size=13,
                        color=AppColors.TEXT_GOLD,
                        weight=ft.FontWeight.W_500,
                    ),
                    self.nome_input,
                    self.whatsapp_input,
                ],
                spacing=8,
            ),
            visible=False,
            padding=AppPadding.only(top=8, bottom=8),
        )
        
        self.build_ui()

    def build_ui(self):
        self.padding = AppPadding.all(16)
        
        # Header Acolhedor
        header = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(Icons.FAVORITE, color=AppColors.PRIMARY, size=24),
                            ft.Text(
                                "Refúgio Silencioso",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=AppColors.TEXT_PRIMARY,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Text(
                        "Como está o seu coração hoje?",
                        size=22,
                        weight=ft.FontWeight.W_700,
                        color=AppColors.TEXT_PRIMARY,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "Um espaço seguro onde você não precisa explicar nada. Apenas toque no que sente.",
                        size=13,
                        color=AppColors.TEXT_SECONDARY,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6,
            ),
            padding=AppPadding.symmetric(vertical=10),
        )
        
        # Renderiza a lista de cards de sentimento
        self.render_sentiment_cards()
        
        # Seção de Privacidade
        privacidade_switch = ft.Switch(
            value=self.is_anonimo,
            active_color=AppColors.PRIMARY,
            on_change=self.toggle_anonimato,
        )
        
        privacidade_card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(Icons.SHIELD, color=AppColors.PRIMARY, size=20),
                            ft.Column(
                                controls=[
                                    ft.Text("Oração 100% Anônima", size=14, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
                                    ft.Text("Ninguém saberá quem você é, apenas que há uma dor.", size=12, color=AppColors.TEXT_MUTED),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            privacidade_switch,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    self.contato_container,
                ],
            ),
            bgcolor=AppColors.BG_SURFACE,
            padding=AppPadding.all(14),
            border_radius=12,
            border=AppBorder.all(1, AppColors.BORDER_DEFAULT),
        )
        
        # Botão Principal de Pedido de Oração
        btn_pedir_oracao = ft.Container(
            content=ft.ElevatedButton(
                content=ft.Row(
                    controls=[
                        ft.Icon(Icons.VOLUNTEER_ACTIVISM, color="#000000", size=20),
                        ft.Text(
                            "PEDIR ORAÇÃO AGORA (1 TOQUE)",
                            weight=ft.FontWeight.BOLD,
                            size=15,
                            color="#000000",
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=8,
                ),
                style=ft.ButtonStyle(
                    bgcolor=AppColors.PRIMARY,
                    shape=ft.RoundedRectangleBorder(radius=12),
                    padding=AppPadding.symmetric(vertical=16),
                ),
                on_click=self.enviar_pedido_oracao,
            ),
            margin=AppMargin.only(top=10, bottom=20),
        )
        
        self.content = ft.ListView(
            controls=[
                header,
                ft.Divider(color=AppColors.DIVIDER, height=20),
                self.sentiment_cards_column,
                self.custom_text_field,
                ft.Container(height=10),
                privacidade_card,
                btn_pedir_oracao,
            ],
            expand=True,
            spacing=10,
        )

    def render_sentiment_cards(self):
        self.sentiment_cards_column.controls.clear()
        for item in SENTIMENTOS_PADRAO:
            is_selected = (item["id"] == self.selected_sentimento_id)
            
            card = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(item["emoji"], size=20),
                        ft.Text(
                            item["texto"],
                            size=14,
                            color=AppColors.TEXT_PRIMARY if is_selected else AppColors.TEXT_SECONDARY,
                            weight=ft.FontWeight.W_600 if is_selected else ft.FontWeight.NORMAL,
                            expand=True,
                        ),
                        ft.Icon(
                            Icons.CHECK_CIRCLE if is_selected else Icons.RADIO_BUTTON_UNCHECKED,
                            color=AppColors.PRIMARY if is_selected else AppColors.TEXT_MUTED,
                            size=20,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=12,
                ),
                bgcolor=AppColors.BG_SELECTED if is_selected else AppColors.BG_SURFACE,
                border=AppBorder.all(1.5 if is_selected else 1, AppColors.BORDER_SELECTED if is_selected else AppColors.BORDER_DEFAULT),
                border_radius=12,
                padding=AppPadding.symmetric(horizontal=14, vertical=12),
                animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                on_click=lambda e, sent_id=item["id"]: self.selecionar_sentimento(sent_id),
            )
            self.sentiment_cards_column.controls.append(card)

    def selecionar_sentimento(self, sent_id: str):
        self.selected_sentimento_id = sent_id
        self.custom_text_field.visible = (sent_id == "outro")
        self.render_sentiment_cards()
        self.safe_update()

    def toggle_anonimato(self, e):
        self.is_anonimo = e.control.value
        self.contato_container.visible = not self.is_anonimo
        self.safe_update()

    def safe_update(self):
        try:
            if self.app_page:
                self.app_page.update()
        except Exception:
            pass

    def enviar_pedido_oracao(self, e):
        # Encontra o texto do sentimento selecionado
        sentimento_selecionado = next(
            (s["texto"] for s in SENTIMENTOS_PADRAO if s["id"] == self.selected_sentimento_id),
            "Pedido em silêncio"
        )
        
        target_page = self.app_page

        def fechar_dialogo(dlg):
            try:
                target_page.close(dlg)
            except Exception:
                dlg.open = False
                target_page.update()

        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Icon(Icons.FAVORITE, color=AppColors.PRIMARY, size=28),
                    ft.Text("Você foi ouvido.", weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
                ],
                spacing=8,
            ),
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Seu pedido chegou ao coração da nossa liderança pastoral.",
                        size=14,
                        color=AppColors.TEXT_PRIMARY,
                        weight=ft.FontWeight.W_500,
                    ),
                    ft.Container(height=6),
                    ft.Text(
                        "🕊️ Você não está sozinho. Uma oração está sendo levantada por você neste exato momento.",
                        size=13,
                        color=AppColors.TEXT_GOLD,
                    ),
                    ft.Container(height=8),
                    ft.Text(
                        f"Motivo: {sentimento_selecionado}",
                        size=12,
                        color=AppColors.TEXT_MUTED,
                        italic=True,
                    ),
                    ft.Text(
                        f"Privacidade: {'Totalmente Anônimo' if self.is_anonimo else 'Contato pastoral autorizado'}",
                        size=12,
                        color=AppColors.SUCCESS if self.is_anonimo else AppColors.INFO,
                    ),
                ],
                tight=True,
                spacing=4,
            ),
            actions=[
                ft.TextButton(
                    "Amém, obrigado.",
                    style=ft.ButtonStyle(color=AppColors.PRIMARY),
                    on_click=lambda ev: fechar_dialogo(dialogo),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=AppColors.BG_SURFACE,
        )

        try:
            target_page.open(dialogo)
        except Exception:
            target_page.dialog = dialogo
            dialogo.open = True
            target_page.update()
