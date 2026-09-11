import flet as ft

try:
    from src.theme import AppColors, Icons, AppPadding, AppMargin, AppBorder, AppAlignment
except ModuleNotFoundError:
    from theme import AppColors, Icons, AppPadding, AppMargin, AppBorder, AppAlignment

class AvisosView(ft.Container):
    """
    Tela de Comunidade & Avisos - Agenda da semana, cultos e chave PIX com cópia em 1 toque.
    """
    def __init__(self, page: ft.Page):
        super().__init__(expand=True)
        self.app_page = page
        self.padding = AppPadding.all(16)
        self.build_ui()

    def build_ui(self):
        header = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(Icons.NOTIFICATIONS_ACTIVE, color=AppColors.PRIMARY, size=24),
                            ft.Text("Comunidade & Avisos", size=20, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Text(
                        "Fique por dentro da programação da IBPM CR.",
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

        # Card de PIX / Contribuição Rápida
        def copiar_pix(e):
            target_page = self.app_page
            try:
                target_page.set_clipboard("pix@ibpmcr.com.br")
            except Exception:
                pass
            
            snack = ft.SnackBar(
                content=ft.Text("✨ Chave PIX copiada para a área de transferência!", color=AppColors.TEXT_PRIMARY),
                bgcolor=AppColors.BG_SURFACE,
            )
            try:
                target_page.open(snack)
            except Exception:
                target_page.snack_bar = snack
                snack.open = True
                target_page.update()

        pix_card = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(Icons.QR_CODE, color="#000000", size=26),
                        bgcolor=AppColors.PRIMARY,
                        width=46,
                        height=46,
                        border_radius=12,
                        alignment=AppAlignment.CENTER,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text("Dízimos e Ofertas (PIX)", size=15, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
                            ft.Text("pix@ibpmcr.com.br (Toque para copiar)", size=12, color=AppColors.TEXT_MUTED),
                        ],
                        expand=True,
                        spacing=2,
                    ),
                    ft.IconButton(
                        icon=Icons.COPY_ALL,
                        icon_color=AppColors.PRIMARY,
                        tooltip="Copiar chave PIX",
                        on_click=copiar_pix,
                    )
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=AppColors.BG_SELECTED,
            padding=AppPadding.all(14),
            border_radius=14,
            border=AppBorder.all(1, AppColors.BORDER_SELECTED),
            margin=AppMargin.only(bottom=10),
        )

        # Eventos da Semana
        eventos_mock = [
            {
                "titulo": "Culto da Família & Celebração",
                "dia": "Domingo às 19:00h",
                "local": "Templo Principal • IBPM CR",
                "badge": "Principal",
            },
            {
                "titulo": "Escola Bíblica Dominical (EBD)",
                "dia": "Domingo às 09:30h",
                "local": "Salas de Ensino",
                "badge": "Estudo",
            },
            {
                "titulo": "Culto de Oração & Edificação",
                "dia": "Quarta-feira às 20:00h",
                "local": "Templo Principal",
                "badge": "Oração",
            }
        ]

        eventos_controls = []
        for ev in eventos_mock:
            card = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(ev["titulo"], size=15, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY, expand=True),
                                ft.Container(
                                    content=ft.Text(ev["badge"], size=11, color=AppColors.PRIMARY, weight=ft.FontWeight.BOLD),
                                    bgcolor=AppColors.BG_MAIN,
                                    padding=AppPadding.symmetric(horizontal=8, vertical=4),
                                    border_radius=8,
                                    border=AppBorder.all(1, AppColors.BORDER_DEFAULT),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Container(height=4),
                        ft.Row(
                            controls=[
                                ft.Icon(Icons.ACCESS_TIME, size=14, color=AppColors.TEXT_GOLD),
                                ft.Text(ev["dia"], size=13, color=AppColors.TEXT_SECONDARY),
                            ],
                            spacing=6,
                        ),
                        ft.Row(
                            controls=[
                                ft.Icon(Icons.LOCATION_ON, size=14, color=AppColors.TEXT_MUTED),
                                ft.Text(ev["local"], size=12, color=AppColors.TEXT_MUTED),
                            ],
                            spacing=6,
                        ),
                    ],
                    spacing=4,
                ),
                bgcolor=AppColors.BG_SURFACE,
                padding=AppPadding.all(14),
                border_radius=12,
                border=AppBorder.all(1, AppColors.BORDER_DEFAULT),
                margin=AppMargin.only(bottom=8),
            )
            eventos_controls.append(card)

        self.content = ft.ListView(
            controls=[
                header,
                ft.Divider(color=AppColors.DIVIDER, height=15),
                pix_card,
                ft.Container(height=6),
                ft.Text("🗓️ Programação Semanal", size=16, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
                ft.Container(height=6),
                *eventos_controls,
            ],
            expand=True,
            spacing=10,
        )
