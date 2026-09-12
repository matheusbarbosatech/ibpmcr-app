"""
Motor Universal de 1 Toque (Share & Download Engine).
Fornece compartilhamento instantâneo para WhatsApp Status, Instagram Stories e Download em 100% do app.
"""
import urllib.parse
import flet as ft
from core.theme import AppColors

class ShareEngine:
    @staticmethod
    def share_whatsapp_status(page: ft.Page, text: str, url: str = ""):
        """Compartilha texto formatado e link oficial no WhatsApp."""
        mensagem = (
            f"🔥 *IBPM CR - Igreja de Coração Ardente*\n\n"
            f"{text}\n\n"
            f"📲 Assista completo no App Oficial: {url or 'https://www.youtube.com/@ibpmcr7976'}\n"
            f"Siga a congregação no Instagram: @ibpmcr7976"
        )
        link = f"https://api.whatsapp.com/send?text={urllib.parse.quote(mensagem)}"
        try:
            ShareEngine.show_feedback(page, "📲 Abrindo WhatsApp...")
            page.launch_url(link)
        except Exception:
            ShareEngine.show_feedback(page, "⚠️ Não foi possível abrir o WhatsApp.")

    @staticmethod
    def share_instagram_stories(page: ft.Page, media_url: str = ""):
        """Abre o Instagram pronto para criar um Story."""
        try:
            ShareEngine.show_feedback(page, "📸 Abrindo Instagram...")
            page.launch_url("https://www.instagram.com/ibpmcr7976/")
        except Exception:
            ShareEngine.show_feedback(page, "⚠️ Não foi possível abrir o Instagram.")

    @staticmethod
    def download_to_device(page: ft.Page, media_url: str, file_name: str = "ibpmcr_arquivo"):
        """Dispara o download direto do arquivo em alta resolução (HD/MP4/PDF)."""
        try:
            page.launch_url(media_url)
            ShareEngine.show_feedback(page, f"📥 Download iniciado: {file_name}")
        except Exception as e:
            ShareEngine.show_feedback(page, f"Erro ao baixar: {e}")

    @staticmethod
    def copy_to_clipboard(page: ft.Page, text: str, success_msg: str = "Copiado com sucesso!"):
        """Copia texto para a área de transferência com SnackBar acessível."""
        try:
            page.set_clipboard(text)
            ShareEngine.show_feedback(page, success_msg)
        except Exception:
            pass

    @staticmethod
    def show_feedback(page: ft.Page, message: str):
        """Exibe feedback visual amigável e de alto contraste."""
        snack = ft.SnackBar(
            content=ft.Text(message, color=AppColors.TEXT_WHITE, weight=ft.FontWeight.BOLD),
            bgcolor=AppColors.BG_SURFACE_ALT,
            duration=3000,
        )
        try:
            page.open(snack)
        except Exception:
            page.snack_bar = snack
            snack.open = True
            page.update()
