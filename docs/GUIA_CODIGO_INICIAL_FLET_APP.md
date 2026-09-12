# 📱 GUIA DE ESTRUTURA INICIAL DO SUPER-APP IBPM CR (FLET + SUPABASE + R2)

Este guia contém o esqueleto inicial em Python para o Agente desenvolvedor criar o aplicativo oficial da **Igreja Batista Pentecostal Mundial da Carvalho Ramos (IBPM CR)**.

---

## 📂 1. Estrutura de Pastas Recomendada

```text
ibpmcr_app/
├── assets/
│   ├── icon.png                 # Ícone do App (Coração Ardente)
│   ├── logo_ibpm.png            # Logotipo oficial
│   └── splash.png               # Imagem da tela de abertura
├── core/
│   ├── config.py                # Credenciais Supabase e Cloudflare R2
│   ├── theme.py                 # Cores Oficiais (#07090E, #E11D48, #F59E0B)
│   └── audio_service.py         # Player de áudio com suporte a Background Service
├── models/
│   ├── devocional.py
│   ├── foto.py
│   ├── video.py
│   └── oracao.py
├── services/
│   ├── supabase_client.py       # Conexão com banco Supabase
│   ├── r2_storage.py            # Links do CDN Cloudflare R2
│   └── share_engine.py          # Motor de 1-Clique para WhatsApp / Stories / Download
├── views/
│   ├── home_view.py             # Aba 1: Início, Destaques, Culto Ao Vivo & Frase do Dia
│   ├── oracao_view.py           # Aba 2: Mural Social de Oração & Intercessão
│   ├── palavra_view.py          # Aba 3: Bíblia Offline, Devocional 365, Livros & Escola de Líderes
│   └── fotos_view.py            # Aba 4: Super Galeria de Fotos dos Cultos (Álbuns e Download HD)
├── requirements.txt
└── main.py                      # Ponto de entrada do aplicativo
```

---

## 🎨 2. Paleta de Cores & Tema (`core/theme.py`)

```python
import flet as ft

# Cores Oficiais - Igreja de Coração Ardente
BG_DARK = "#07090E"         # Dark Obsidian Profundo
SURFACE_CARD = "#131722"    # Card Glassmorphism
PRIMARY_RUBI = "#E11D48"    # Rubi / Brasa Pentecostal
SECONDARY_GOLD = "#F59E0B"  # Ouro Imperial do Altar
TEXT_WHITE = "#FFFFFF"      # Branco Puro para Contraste Máximo
TEXT_MUTED = "#94A3B8"      # Cinza Claro para Subtítulos
ACCENT_GREEN = "#10B981"    # Verde WhatsApp para Ações Rápidas

APP_THEME = ft.Theme(
    color_scheme_seed=PRIMARY_RUBI,
    font_family="Inter",
)
```

---

## ⚡ 3. Motor de 1 Toque Universal (`services/share_engine.py`)

```python
import urllib.parse
import flet as ft

class ShareEngine:
    @staticmethod
    def share_whatsapp_status(page: ft.Page, text: str, url: str = ""):
        mensagem = f"{text}\n\n📲 Assista no App da @ibpmcr: {url}"
        link = f"https://api.whatsapp.com/send?text={urllib.parse.quote(mensagem)}"
        page.launch_url(link)

    @staticmethod
    def share_instagram_stories(page: ft.Page, media_url: str):
        # Abre o Instagram para postagem
        page.launch_url("instagram://story-camera")

    @staticmethod
    def download_to_device(page: ft.Page, media_url: str, file_name: str):
        page.launch_url(media_url) # Dispara o download nativo do arquivo HD
```

---

## 🚀 4. Ponto de Entrada com as 4 Abas (`main.py`)

```python
import flet as ft
from core.theme import BG_DARK, PRIMARY_RUBI, SECONDARY_GOLD, TEXT_WHITE, APP_THEME
from views.home_view import HomeView
from views.oracao_view import OracaoView
from views.palavra_view import PalavraView
from views.fotos_view import FotosView

def main(page: ft.Page):
    page.title = "IBPM CR - Igreja de Coração Ardente"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = BG_DARK
    page.theme = APP_THEME
    page.padding = 0

    # Inicializa as views
    home_view = HomeView(page)
    oracao_view = OracaoView(page)
    palavra_view = PalavraView(page)
    fotos_view = FotosView(page)

    container_principal = ft.Container(
        content=home_view,
        expand=True,
        padding=12
    )

    def on_nav_change(e):
        idx = e.control.selected_index
        if idx == 0:
            container_principal.content = home_view
        elif idx == 1:
            container_principal.content = oracao_view
        elif idx == 2:
            container_principal.content = palavra_view
        elif idx == 3:
            container_principal.content = fotos_view
        page.update()

    # Barra Inferior com 4 Abas Acessíveis (Botões Grandes)
    page.navigation_bar = ft.NavigationBar(
        selected_index=0,
        bgcolor="#0B0E17",
        indicator_color=PRIMARY_RUBI,
        on_change=on_nav_change,
        destinations=[
            ft.NavigationDestination(icon=ft.icons.HOME_ROUNDED, label="Início"),
            ft.NavigationDestination(icon=ft.icons.VOLUNTEER_ACTIVISM_ROUNDED, label="Oração"),
            ft.NavigationDestination(icon=ft.icons.MENU_BOOK_ROUNDED, label="Palavra & Estudos"),
            ft.NavigationDestination(icon=ft.icons.PHOTO_LIBRARY_ROUNDED, label="Fotos & Mídia"),
        ]
    )

    page.add(container_principal)

if __name__ == "__main__":
    ft.app(target=main)
```
