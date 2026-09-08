import flet as ft

def main(page: ft.Page):
    page.title = "IBPM CR - Igreja Batista do Povo"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 390
    page.window.height = 844
    page.padding = 0

    page.add(
        ft.SafeArea(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.AppBar(
                            title=ft.Text("IBPM CR", weight=ft.FontWeight.BOLD),
                            bgcolor=ft.colors.SURFACE_VARIANT,
                            center_title=True,
                        ),
                        ft.Container(
                            padding=20,
                            content=ft.Column(
                                controls=[
                                    ft.Text("Bem-vindo à IBPM CR", size=22, weight=ft.FontWeight.BOLD),
                                    ft.Text("O app da congregação 100% em Python.", color=ft.colors.GREY_400),
                                    ft.Divider(),
                                    ft.ElevatedButton("Assistir Cortes & Mensagens", icon=ft.icons.PLAY_CIRCLE_FILL),
                                ],
                            ),
                        ),
                    ],
                ),
            )
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
