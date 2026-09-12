"""
Super-App Oficial da Igreja Batista Pentecostal Mundial da Carvalho Ramos (IBPM CR).
Tecnologia: Python Flet, SQLite Local (Offline-First), Supabase Sync, Cloudflare R2.
Acessibilidade: WCAG AAA, Redimensionamento Sênior Global (80% a 150%), Áudio em Segundo Plano.
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
from core.audio_service import AudioService
from services.db_service import DBService
from views.home_view import HomeView
from views.oracao_view import OracaoView
from views.palavra_view import PalavraView
from views.fotos_view import FotosView


def main(page: ft.Page):
    # 1. Configurações Globais da Janela e Tema
    page.title = "IBPM CR - Super-App Oficial"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 420
    page.window.height = 890
    page.window.min_width = 360
    page.window.min_height = 700
    page.window.resizable = True
    page.padding = 0
    page.bgcolor = AppColors.BG_DARK

    # 2. Inicialização do Banco de Dados Local (Offline-First)
    try:
        DBService.init_db()
        DBService.seed_initial_data()
    except Exception as err:
        print(f"[DB INIT ERROR]: {err}")

    # 3. Inicialização do Serviço de Áudio com a Página
    audio_service = AudioService()
    audio_service.set_page(page)

    # 4. Controle de Acessibilidade Sênior (AppBar)
    scale_text = ft.Text(
        f"{int(FontScaleManager.get_scale() * 100)}%",
        color=AppColors.GOLD_LIGHT,
        size=13,
        weight=ft.FontWeight.BOLD,
    )

    def update_scale_ui():
        scale_text.value = f"{int(FontScaleManager.get_scale() * 100)}%"
        page.update()

    FontScaleManager.register_listener(update_scale_ui)

    def on_zoom_in(e):
        FontScaleManager.increase()

    def on_zoom_out(e):
        FontScaleManager.decrease()

    # 5. Top AppBar com Marca Oficial e Redimensionador Sênior
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

    # 6. Criação das 4 Telas Principais com Navegação Conectada
    def switch_tab(index: int):
        if 0 <= index < len(views):
            nav_bar.selected_index = index
            content_area.content = views[index]
            page.update()

    home_view = HomeView(page, navigate_to_tab=switch_tab)
    oracao_view = OracaoView(page)
    palavra_view = PalavraView(page)
    fotos_view = FotosView(page)

    views = [home_view, oracao_view, palavra_view, fotos_view]

    # Container Dinâmico Central (Permite rolagem suave por tela)
    content_area = ft.Container(
        content=views[0],
        expand=True,
        bgcolor=AppColors.BG_DARK,
    )

    # 7. Mini-Player Flutuante de Áudio (Persistente em Segundo Plano)
    player_title = ft.Text(
        "Nenhum áudio em reprodução",
        size=13,
        weight=ft.FontWeight.BOLD,
        color=AppColors.TEXT_WHITE,
        max_lines=1,
        overflow=ft.TextOverflow.ELLIPSIS,
    )
    player_subtitle = ft.Text(
        "Toque em uma ministração pastoral para ouvir",
        size=11,
        color=AppColors.TEXT_MUTED,
        max_lines=1,
        overflow=ft.TextOverflow.ELLIPSIS,
    )
    play_pause_btn = ft.IconButton(
        icon=Icons.PLAY_ARROW_ROUNDED,
        icon_color=AppColors.PRIMARY_RUBI,
        icon_size=28,
        tooltip="Tocar / Pausar",
        on_click=lambda e: audio_service.toggle_play_pause(),
    )

    def on_audio_state_change():
        if audio_service.current_track:
            player_title.value = audio_service.current_track.title
            player_subtitle.value = audio_service.current_track.subtitle
            play_pause_btn.icon = (
                Icons.PAUSE_ROUNDED if audio_service.is_playing else Icons.PLAY_ARROW_ROUNDED
            )
            mini_player.visible = True
        else:
            mini_player.visible = False
        page.update()

    audio_service.register_listener(on_audio_state_change)

    mini_player = ft.Container(
        visible=False,
        bgcolor=AppColors.BG_SURFACE_ALT,
        border=AppBorder.all(1, AppColors.BORDER_RUBI),
        border_radius=12,
        margin=AppMargin.only(left=12, right=12, bottom=6),
        padding=AppPadding.symmetric(horizontal=12, vertical=6),
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Icon(Icons.HEADPHONES_ROUNDED, color=AppColors.SECONDARY_GOLD, size=22),
                    padding=AppPadding.all(6),
                    bgcolor=AppColors.BG_SURFACE,
                    border_radius=8,
                ),
                ft.Column(
                    controls=[player_title, player_subtitle],
                    spacing=2,
                    alignment=ft.MainAxisAlignment.CENTER,
                    expand=True,
                ),
                play_pause_btn,
                ft.IconButton(
                    icon=Icons.CLOSE_ROUNDED,
                    icon_color=AppColors.TEXT_MUTED,
                    icon_size=18,
                    tooltip="Fechar Player",
                    on_click=lambda e: audio_service.stop(),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    # 8. Navegação por Abas (Material 3 Bottom Navigation)
    def on_nav_change(e):
        selected_index = e.control.selected_index
        if 0 <= selected_index < len(views):
            content_area.content = views[selected_index]
            page.update()

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
            icon=Icons.AUTO_STORIES_OUTLINED,
            selected_icon=Icons.AUTO_STORIES_ROUNDED,
            label="Palavra",
        ),
        NavigationDestination(
            icon=Icons.PHOTO_LIBRARY_OUTLINED,
            selected_icon=Icons.PHOTO_LIBRARY_ROUNDED,
            label="Mídia",
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

    # 9. Montagem da Página Principal
    page.add(
        ft.Column(
            controls=[
                content_area,
                mini_player,
            ],
            expand=True,
            spacing=0,
        )
    )
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
