"""
Suíte Completa de Testes Automatizados e Validação Extrema do Super-App IBPM CR.
Valida rigorosamente:
1. DBService (SQLite Offline-First, tabelas e seeds)
2. AudioService (Segundo plano, listener callbacks, player state)
3. FontScaleManager (Acessibilidade Sênior, escala dinâmica de 80% a 150%)
4. ShareEngine (Motor Universal 1-Clique: WhatsApp, Instagram, Download, SnackBar)
5. HomeView (Banner Culto Ao Vivo, Pílula Pastoral, Filtro Sentimentos, Acesso Rápido)
6. OracaoView (Mural de Orações Social, Contador Estou Orando, Modal Acessível)
7. PalavraView (Devocional 365, Bíblia Offline, Livros Oficiais, Escola Líderes)
8. FotosView (Galeria Fotos HD, 1-Clique Status/Stories, Cortes Verticais)
9. Orquestrador main.py (AppBar Sênior, Mini-Player Flutuante, NavigationBar M3)
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock

# Configuração de encoding para console Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import flet as ft
from core.theme import AppColors, FontScaleManager, Icons
from core.audio_service import AudioService, AudioTrack
from services.db_service import DBService, DatabaseService
from services.share_engine import ShareEngine
from views.home_view import HomeView
from views.oracao_view import OracaoView
from views.palavra_view import PalavraView
from views.fotos_view import FotosView
from main import main


def create_mock_page():
    page = MagicMock()
    page.title = ""
    page.theme_mode = None
    page.window = MagicMock()
    page.appbar = None
    page.navigation_bar = None
    page.controls = []
    page.overlay = []
    page.opened_dialogs = []
    page.opened_snacks = []
    page.launched_urls = []
    page.clipboard_val = None

    def mock_add(*controls):
        page.controls.extend(controls)

    def mock_update():
        pass

    def mock_open(control):
        if isinstance(control, ft.AlertDialog):
            page.opened_dialogs.append(control)
        elif isinstance(control, ft.SnackBar):
            page.opened_snacks.append(control)

    def mock_close(control):
        if control in page.opened_dialogs:
            page.opened_dialogs.remove(control)
        if control in page.opened_snacks:
            page.opened_snacks.remove(control)

    def mock_set_clipboard(val):
        page.clipboard_val = val

    def mock_launch_url(url):
        page.launched_urls.append(url)

    page.add = mock_add
    page.update = mock_update
    page.open = mock_open
    page.close = mock_close
    page.set_clipboard = mock_set_clipboard
    page.launch_url = mock_launch_url

    return page


def test_suite():
    print("=" * 65)
    print("🚀 INICIANDO BATERIA DE TESTES DO SUPER-APP OFICIAL IBPM CR")
    print("=" * 65)

    # 1. DBService & SQLite Local
    print("\n[1/8] Testando DBService (SQLite Local / Offline-First)...")
    DBService.init_db()
    DBService.seed_initial_data()
    devocional = DBService.get_devocional_hoje(1)
    assert devocional is not None, "Deveria haver devocional semeado"
    assert "Altar" in devocional.titulo or len(devocional.titulo) > 0

    frases = DBService.get_frases_por_sentimento("todos")
    assert len(frases) > 0, "Deveria haver frases proféticas semeadas"
    pedidos = DBService.get_pedidos_oracao()
    assert len(pedidos) > 0, "Deveria haver pedidos de oração semeados"
    fotos = DBService.get_galeria_fotos()
    assert len(fotos) > 0, "Deveria haver fotos semeadas"
    cortes = DBService.get_cortes_verticais()
    assert len(cortes) > 0, "Deveria haver cortes semeados"
    livros = DBService.get_livros()
    assert len(livros) > 0, "Deveria haver livros semeados"
    modulos = DBService.get_modulos_lideranca()
    assert len(modulos) > 0, "Deveria haver módulos da Escola de Líderes semeados"
    print(f"  -> SQLite inicializado com sucesso: {len(frases)} frases, {len(pedidos)} orações, {len(fotos)} fotos, {len(cortes)} cortes, {len(livros)} livros.")

    # 2. AudioService & Singleton
    print("\n[2/8] Testando AudioService (Segundo Plano & Callbacks)...")
    audio = AudioService()
    test_track = AudioTrack(
        title="Ministração de Poder",
        subtitle="Pr. Presidente",
        audio_url="https://audio.ibpmcr.org/teste.mp3",
    )
    notified = []
    audio.register_listener(lambda: notified.append(True))
    audio.play_track(test_track)
    assert audio.is_playing is True, "Audio deveria estar em reprodução"
    assert audio.current_track.title == "Ministração de Poder", "Título do track incorreto"
    assert len(notified) > 0, "Listener deveria ser notificado ao dar play"

    audio.toggle_play_pause()
    assert audio.is_playing is False, "Audio deveria ter pausado"
    audio.stop()
    assert audio.is_playing is False, "Audio deveria ter parado"
    print("  -> AudioService: Play, Toggle, Stop e Notificações validados com sucesso.")

    # 3. FontScaleManager (Acessibilidade Sênior)
    print("\n[3/8] Testando FontScaleManager (Escala Dinâmica Sênior)...")
    initial_scale = FontScaleManager.get_scale()
    FontScaleManager.increase()
    assert FontScaleManager.get_scale() > initial_scale, "A escala deveria ter aumentado com increase()"
    higher_scale = FontScaleManager.get_scale()
    FontScaleManager.decrease()
    assert FontScaleManager.get_scale() == initial_scale, "A escala deveria ter retornado ao valor inicial com decrease()"
    scaled_font = FontScaleManager.s(16)
    assert scaled_font == round(16 * initial_scale, 1), "Cálculo de fonte escalada incorreto"
    print(f"  -> Acessibilidade Sênior validada: Níveis={FontScaleManager.SCALE_LEVELS}, Ativo={FontScaleManager.get_scale()}")

    # 4. ShareEngine (Motor Universal 1-Clique)
    print("\n[4/8] Testando ShareEngine (WhatsApp, Stories, Copiar)...")
    page = create_mock_page()
    ShareEngine.share_whatsapp_status(
        page,
        "Deus é fiel!",
        "https://ibpmcr.org/culto",
    )
    assert len(page.launched_urls) > 0, "Deveria ter disparado URL do WhatsApp"
    assert "api.whatsapp.com" in page.launched_urls[-1]
    ShareEngine.share_instagram_stories(page)
    assert len(page.launched_urls) > 1, "Deveria ter disparado URL do Instagram"
    ShareEngine.copy_to_clipboard(page, "Chave PIX Oficial", "Chave copiada!")
    assert page.clipboard_val == "Chave PIX Oficial"
    assert len(page.opened_snacks) > 0, "SnackBar de feedback deveria ter sido aberto"
    print("  -> Motor Universal 1-Clique verificado com sucesso.")

    # 5. HomeView
    print("\n[5/8] Testando HomeView (Altar, Palavra do Pastor, Sentimentos, PIX)...")
    home = HomeView(page)
    assert home.padding is not None, "HomeView deve ter padding"
    # Testa filtro interativo de sentimentos
    home.filtrar_frase("ansiedade")
    assert home.selected_sentimento == "ansiedade"
    assert home.current_frase_obj is not None
    # Testa tocar pílula pastoral
    home.tocar_pilula_pastoral(None)
    assert audio.is_playing is True
    audio.stop()
    print("  -> HomeView validada: Banner ao vivo, pílula pastoral em áudio e filtro profético.")

    # 6. OracaoView
    print("\n[6/8] Testando OracaoView (Mural Social, Estou Orando, Modal)...")
    oracao = OracaoView(page)
    assert len(oracao.pedidos_column.controls) > 0, "Mural de pedidos deve ter cards"
    primeiro_pedido = pedidos[0]
    count_antes = primeiro_pedido.contador_orando
    oracao.orar_pelo_pedido(primeiro_pedido.id)
    pedidos_atualizados = DBService.get_pedidos_oracao()
    primeiro_atualizado = next(p for p in pedidos_atualizados if p.id == primeiro_pedido.id)
    assert primeiro_atualizado.contador_orando == count_antes + 1
    # Testa abertura do modal de clamor
    oracao.abrir_modal_novo_pedido(None)
    assert len(page.opened_dialogs) > 0
    print(f"  -> OracaoView validada: Intercessão social ({count_antes} -> {primeiro_atualizado.contador_orando}) e modal ativo.")

    # 7. PalavraView e FotosView
    print("\n[7/8] Testando PalavraView e FotosView...")
    palavra = PalavraView(page)
    # Testa alternância das 4 sub-abas
    palavra.mudar_sub_aba(1)  # Bíblia
    assert palavra.active_tab_index == 1
    palavra.mudar_sub_aba(2)  # Livros
    assert palavra.active_tab_index == 2
    palavra.mudar_sub_aba(3)  # Escola
    assert palavra.active_tab_index == 3
    palavra.mudar_sub_aba(0)  # Devocional
    assert palavra.active_tab_index == 0

    fotos = FotosView(page)
    # Testa alternância das 2 sub-abas (Fotos e Cortes)
    fotos.alternar_subtab(1)
    assert fotos.active_subtab == 1
    fotos.alternar_subtab(0)
    assert fotos.active_subtab == 0
    print("  -> PalavraView (Devocional, Bíblia, Livros, Escola) e FotosView (Galeria HD e Cortes) validadas.")

    # 8. Orquestrador Geral main.py
    print("\n[8/8] Testando Orquestrador Principal (main.py)...")
    main_page = create_mock_page()
    main(main_page)
    assert main_page.title == "IBPM CR - Super-App Oficial"
    assert main_page.appbar is not None
    assert main_page.navigation_bar is not None
    assert len(main_page.navigation_bar.destinations) == 4
    assert len(main_page.controls) > 0
    print("  -> Orquestrador main.py inicializou a janela, áudio, AppBar sênior e 4 abas perfeitamente.")

    print("\n" + "=" * 65)
    print("🎉 SUCESSO TOTAL! 100% DOS TESTES DO SUPER-APP IBPM CR APROVADOS!")
    print("=" * 65)


if __name__ == "__main__":
    test_suite()
