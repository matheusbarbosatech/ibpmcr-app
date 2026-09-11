import flet as ft

try:
    from src.theme import AppColors, Icons, AppPadding, AppMargin, AppBorder, AppAlignment
except ModuleNotFoundError:
    from theme import AppColors, Icons, AppPadding, AppMargin, AppBorder, AppAlignment

class CortesView(ft.Container):
    """
    Tela de Cortes & Mensagens - Feed dos 217 cortes virais gerados pela automação.
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
                            ft.Icon(Icons.ONDEMAND_VIDEO, color=AppColors.PRIMARY, size=24),
                            ft.Text("Mensagens & Cortes", size=20, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Text(
                        "Alimento espiritual em doses rápidas para o seu dia.",
                        size=13,
                        color=AppColors.TEXT_SECONDARY,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(
                        content=ft.Text("🔥 217 cortes disponíveis na biblioteca", size=12, color=AppColors.TEXT_GOLD, weight=ft.FontWeight.BOLD),
                        bgcolor=AppColors.BG_SELECTED,
                        padding=AppPadding.symmetric(horizontal=12, vertical=6),
                        border_radius=20,
                        border=AppBorder.all(1, AppColors.BORDER_SELECTED),
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6,
            ),
            padding=AppPadding.symmetric(vertical=10),
        )

        # Mock dos Cortes em Destaque
        cortes_mock = [
            {
                "titulo": "Quando o Cansaço Parecer Maior que a Fé",
                "pregador": "Pastor Carlos",
                "data": "08 Set 2026",
                "resumo": "Deus não exige que você seja forte o tempo todo; Ele aperfeiçoa o poder d'Ele na sua fraqueza.",
                "duracao": "00:58",
            },
            {
                "titulo": "A Paz que Excede Todo o Entendimento",
                "pregador": "Pastor Carlos",
                "data": "01 Set 2026",
                "resumo": "Não tente controlar o amanhã. Entregue sua ansiedade no altar e descanse.",
                "duracao": "01:15",
            },
            {
                "titulo": "Você Não É Invisível aos Olhos do Pai",
                "pregador": "Ministério Pastoral",
                "data": "25 Ago 2026",
                "resumo": "Mesmo no último banco da igreja, os olhos do Senhor estão fixos em você.",
                "duracao": "00:47",
            }
        ]

        cards_list = []
        for corte in cortes_mock:
            card = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Container(
                                    content=ft.Icon(Icons.PLAY_ARROW, color="#000000", size=24),
                                    bgcolor=AppColors.PRIMARY,
                                    width=44,
                                    height=44,
                                    border_radius=22,
                                    alignment=AppAlignment.CENTER,
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text(corte["titulo"], size=15, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
                                        ft.Text(f"{corte['pregador']} • {corte['data']} • ⏱️ {corte['duracao']}", size=12, color=AppColors.TEXT_MUTED),
                                    ],
                                    expand=True,
                                    spacing=2,
                                ),
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Container(height=6),
                        ft.Text(f"💡 Resumo: \"{corte['resumo']}\"", size=13, color=AppColors.TEXT_SECONDARY, italic=True),
                        ft.Container(height=4),
                        ft.Row(
                            controls=[
                                ft.TextButton(
                                    "Assistir Corte Vertical",
                                    icon=Icons.PLAY_CIRCLE,
                                    style=ft.ButtonStyle(color=AppColors.PRIMARY),
                                ),
                                ft.TextButton(
                                    "Culto Completo (YouTube)",
                                    icon=Icons.OPEN_IN_NEW,
                                    style=ft.ButtonStyle(color=AppColors.TEXT_MUTED),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        )
                    ],
                ),
                bgcolor=AppColors.BG_SURFACE,
                padding=AppPadding.all(14),
                border_radius=14,
                border=AppBorder.all(1, AppColors.BORDER_DEFAULT),
                margin=AppMargin.only(bottom=10),
            )
            cards_list.append(card)

        self.content = ft.ListView(
            controls=[
                header,
                ft.Divider(color=AppColors.DIVIDER, height=15),
                *cards_list,
            ],
            expand=True,
            spacing=10,
        )
