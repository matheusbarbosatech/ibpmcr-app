import flet as ft

try:
    from src.theme import AppColors, Icons, AppPadding, AppMargin, AppBorder, AppAlignment
except ModuleNotFoundError:
    from theme import AppColors, Icons, AppPadding, AppMargin, AppBorder, AppAlignment

class GabineteView(ft.Container):
    """
    Tela do Gabinete Pastoral - Painel reservado para o Pastor e equipe de intercessão.
    Permite visualizar os pedidos recebidos no Refúgio Silencioso e orar por cada um.
    """
    def __init__(self, page: ft.Page):
        super().__init__(expand=True)
        self.app_page = page
        self.padding = AppPadding.all(16)
        self.filtro = "pendente"  # 'pendente' ou 'orado'
        self.pedidos_list_column = ft.Column(spacing=10)
        
        # Mock de pedidos para visualização do Módulo 2
        self.pedidos_data = [
            {
                "id": "1",
                "sentimento": "O peito está pesado hoje, só peço uma oração em silêncio.",
                "tempo": "Há 15 min",
                "is_anonimo": True,
                "nome": "Anônimo",
                "status": "pendente"
            },
            {
                "id": "2",
                "sentimento": "Estou cansado e não sei explicar o que sinto.",
                "tempo": "Há 42 min",
                "is_anonimo": False,
                "nome": "Lucas B. (11) 98888-7777",
                "status": "pendente"
            },
            {
                "id": "3",
                "sentimento": "Preciso apenas de paz para conseguir descansar hoje.",
                "tempo": "Hoje às 11:20",
                "is_anonimo": True,
                "nome": "Anônimo",
                "status": "orado"
            }
        ]
        
        self.build_ui()

    def build_ui(self):
        header = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(Icons.ADMIN_PANEL_SETTINGS, color=AppColors.PRIMARY, size=24),
                            ft.Text("Gabinete Pastoral", size=20, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Text(
                        "Gestão confidencial de pedidos do Refúgio Silencioso.",
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

        # Filtros de Status
        self.btn_filtro_pendentes = ft.ElevatedButton(
            "Não Orados (2)",
            style=ft.ButtonStyle(
                bgcolor=AppColors.PRIMARY,
                color="#000000",
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            on_click=lambda e: self.set_filtro("pendente"),
        )
        self.btn_filtro_orados = ft.OutlinedButton(
            "Já Orados (1)",
            style=ft.ButtonStyle(
                color=AppColors.TEXT_SECONDARY,
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            on_click=lambda e: self.set_filtro("orado"),
        )

        filtros_row = ft.Row(
            controls=[self.btn_filtro_pendentes, self.btn_filtro_orados],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )

        self.render_pedidos()

        self.content = ft.ListView(
            controls=[
                header,
                ft.Divider(color=AppColors.DIVIDER, height=15),
                filtros_row,
                ft.Container(height=10),
                self.pedidos_list_column,
            ],
            expand=True,
            spacing=10,
        )

    def set_filtro(self, status: str):
        self.filtro = status
        if status == "pendente":
            self.btn_filtro_pendentes.style.bgcolor = AppColors.PRIMARY
            self.btn_filtro_pendentes.style.color = "#000000"
            self.btn_filtro_orados.style.color = AppColors.TEXT_SECONDARY
        else:
            self.btn_filtro_pendentes.style.bgcolor = AppColors.TRANSPARENT
            self.btn_filtro_pendentes.style.color = AppColors.TEXT_SECONDARY
            self.btn_filtro_orados.style.color = AppColors.PRIMARY
        
        self.render_pedidos()
        target_page = self.app_page
        if target_page:
            try:
                target_page.update()
            except Exception:
                pass

    def render_pedidos(self):
        self.pedidos_list_column.controls.clear()
        filtrados = [p for p in self.pedidos_data if p["status"] == self.filtro]

        if not filtrados:
            self.pedidos_list_column.controls.append(
                ft.Container(
                    content=ft.Text("Nenhum pedido nesta lista.", color=AppColors.TEXT_MUTED, italic=True),
                    alignment=AppAlignment.CENTER,
                    padding=AppPadding.all(20),
                )
            )
            return

        for pedido in filtrados:
            is_pendente = (pedido["status"] == "pendente")
            
            card = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(
                                            Icons.LOCK if pedido["is_anonimo"] else Icons.CONTACT_PHONE,
                                            size=16,
                                            color=AppColors.PRIMARY if pedido["is_anonimo"] else AppColors.INFO,
                                        ),
                                        ft.Text(pedido["nome"], size=13, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
                                    ],
                                    spacing=6,
                                ),
                                ft.Text(pedido["tempo"], size=12, color=AppColors.TEXT_MUTED),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Container(height=4),
                        ft.Text(f"\"{pedido['sentimento']}\"", size=14, color=AppColors.TEXT_GOLD, weight=ft.FontWeight.W_500),
                        ft.Container(height=6),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "Marcar como Orado 🙏" if is_pendente else "Já Orado ✨",
                                    icon=Icons.CHECK_CIRCLE if not is_pendente else Icons.PAN_TOOL_ALT,
                                    disabled=not is_pendente,
                                    style=ft.ButtonStyle(
                                        bgcolor=AppColors.SUCCESS if is_pendente else AppColors.BG_SURFACE_ALT,
                                        color="#FFFFFF" if is_pendente else AppColors.TEXT_MUTED,
                                    ),
                                    on_click=lambda e, pid=pedido["id"]: self.marcar_como_orado(pid),
                                )
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        )
                    ],
                ),
                bgcolor=AppColors.BG_SURFACE,
                padding=AppPadding.all(14),
                border_radius=12,
                border=AppBorder.all(1, AppColors.BORDER_DEFAULT),
            )
            self.pedidos_list_column.controls.append(card)

    def marcar_como_orado(self, pedido_id: str):
        for p in self.pedidos_data:
            if p["id"] == pedido_id:
                p["status"] = "orado"
                break
        self.render_pedidos()
        target_page = self.app_page
        if target_page:
            snack = ft.SnackBar(
                content=ft.Text("✨ Oração concluída e intercessão registrada!", color=AppColors.TEXT_PRIMARY),
                bgcolor=AppColors.SUCCESS,
            )
            try:
                target_page.open(snack)
            except Exception:
                target_page.snack_bar = snack
                snack.open = True
                target_page.update()
