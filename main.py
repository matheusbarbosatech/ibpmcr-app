"""
Super-App Oficial da Igreja Batista Pentecostal Mundial da Carvalho Ramos (IBPM CR).
Tecnologia: Python Flet, SQLite Local (Offline-First), Supabase Sync, Cloudflare R2.
Acessibilidade: WCAG AAA, Redimensionamento Sênior Global (80% a 150%).
Versão 1.0 Enxuta: 4 Abas Fluidas e Respiradas (Início, Oração, Retiro 2026, Igreja).
"""
import sys
from pathlib import Path

# Garante resolução dos módulos tanto da raiz quanto de subpastas
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import flet as ft
from core.theme import (
    AppColors,
    FontScaleManager,
    Icons,
    Colors,
    NavigationDestination,
    AppPadding,
    AppMargin,
    AppBorder,
    AppAlignment,
)
from services.db_service import DBService
from views.home_view import HomeView
from views.oracao_view import OracaoView
from views.retiro_view import RetiroView
from views.igreja_view import IgrejaView


def main(page: ft.Page):
    # 1. Configurações Globais da Janela e Tema
    page.title = "IBPM CR - Super-App Oficial"
    page.theme_mode = ft.ThemeMode.DARK
    try:
        page.window.width = 420
        page.window.height = 890
        page.window.min_width = 360
        page.window.min_height = 700
        page.window.resizable = True
    except Exception:
        pass
    page.padding = 0
    page.bgcolor = AppColors.BG_DARK

    # 2. Inicialização do Banco de Dados Local (Offline-First)
    try:
        DBService.init_db()
        DBService.seed_initial_data()
    except Exception as err:
        print(f"[DB INIT ERROR]: {err}")

    # 3. Controle de Acessibilidade Sênior (AppBar)
    scale_text = ft.Text(
        f"{int(FontScaleManager.get_scale() * 100)}%",
        color=AppColors.GOLD_LIGHT,
        size=13,
        weight=ft.FontWeight.BOLD,
    )

    def update_scale_ui():
        scale_text.value = f"{int(FontScaleManager.get_scale() * 100)}%"
        try:
            page.update()
        except Exception:
            pass

    FontScaleManager.register_listener(update_scale_ui)

    def on_zoom_in(e):
        FontScaleManager.increase()

    def on_zoom_out(e):
        FontScaleManager.decrease()

    # 4. Top AppBar com Marca Oficial e Redimensionador Sênior
    app_bar = ft.AppBar(
        leading=ft.Container(
            content=ft.Icon(Icons.LOCAL_FIRE_DEPARTMENT_ROUNDED, color=AppColors.PRIMARY_RUBI, size=26),
            padding=AppPadding.only(left=12),
            alignment=AppAlignment.CENTER,
        ),
        leading_width=44,
        title=ft.Column(
            controls=[
                ft.Text(
                    "IBPM CARVALHO RAMOS",
                    size=15,
                    weight=ft.FontWeight.BOLD,
                    color=AppColors.TEXT_WHITE,
                ),
                ft.Text(
                    "Super-App da Família em Cristo",
                    size=11,
                    color=AppColors.TEXT_MUTED,
                ),
            ],
            spacing=1,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        center_title=False,
        bgcolor=AppColors.BG_SURFACE,
        actions=[
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=Icons.TEXT_DECREASE_ROUNDED,
                            icon_color=AppColors.TEXT_SECONDARY,
                            icon_size=18,
                            tooltip="Diminuir Texto (A-)",
                            on_click=on_zoom_out,
                        ),
                        scale_text,
                        ft.IconButton(
                            icon=Icons.TEXT_INCREASE_ROUNDED,
                            icon_color=AppColors.SECONDARY_GOLD,
                            icon_size=20,
                            tooltip="Aumentar Texto Sênior (A+)",
                            on_click=on_zoom_in,
                        ),
                    ],
                    spacing=2,
                    alignment=ft.MainAxisAlignment.END,
                ),
                padding=AppPadding.only(right=8),
            )
        ],
    )
    page.appbar = app_bar

    # 5. Criação das 4 Telas Principais da v1.0
    def switch_tab(index: int):
        if 0 <= index < len(views):
            nav_bar.selected_index = index
            content_area.content = views[index]
            try:
                page.update()
            except Exception:
                pass

    home_view = HomeView(page, navigate_to_tab=switch_tab)
    oracao_view = OracaoView(page)
    retiro_view = RetiroView(page)
    igreja_view = IgrejaView(page)

    views = [home_view, oracao_view, retiro_view, igreja_view]

    # Container Dinâmico Central (Permite rolagem suave por tela com respiro)
    content_area = ft.Container(
        content=views[0],
        expand=True,
        bgcolor=AppColors.BG_DARK,
    )

    # 6. Navegação por Abas (Material 3 Bottom Navigation Enxuta)
    def on_nav_change(e):
        selected_index = e.control.selected_index
        if 0 <= selected_index < len(views):
            content_area.content = views[selected_index]
            try:
                page.update()
            except Exception:
                pass

    nav_destinations = [
        NavigationDestination(
            icon=Icons.HOME_OUTLINED,
            selected_icon=Icons.HOME_ROUNDED,
            label="Início",
        ),
        NavigationDestination(
            icon=Icons.VOLUNTEER_ACTIVISM_OUTLINED,
            selected_icon=Icons.VOLUNTEER_ACTIVISM_ROUNDED,
            label="Oração",
        ),
        NavigationDestination(
            icon=Icons.LOCAL_FIRE_DEPARTMENT_OUTLINED,
            selected_icon=Icons.LOCAL_FIRE_DEPARTMENT_ROUNDED,
            label="Retiro 2026",
        ),
        NavigationDestination(
            icon=Icons.CHURCH_OUTLINED,
            selected_icon=Icons.CHURCH_ROUNDED,
            label="Igreja",
        ),
    ]

    nav_bar = ft.NavigationBar(
        selected_index=0,
        bgcolor=AppColors.BG_SURFACE,
        indicator_color=AppColors.PRIMARY_RUBI,
        on_change=on_nav_change,
        destinations=nav_destinations,
        height=68,
    )
    page.navigation_bar = nav_bar

    # 7. Montagem Direta e Limpa da Página Principal
    page.add(content_area)
    try:
        page.update()
    except Exception:
        pass


if __name__ == "__main__":
    ft.run(main=main, assets_dir="assets")
