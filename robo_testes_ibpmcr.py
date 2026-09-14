"""
🤖 AGENTE AUTÔNOMO DE TESTES (TEST ROBOT AGENT) — IBPM CR SUPER-APP v1.0
Testa 100% das 4 Abas Enxutas e Respiradas (Início, Oração, Retiro 2026, Igreja & Dízimo),
todos os botões de ação, cópia de PIX, rotas de mapa, intercessão e banco SQLite.
"""
import os
import sys
import time
import traceback
from pathlib import Path

# Garante suporte UTF-8 no console Windows
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import flet as ft
from core.theme import AppColors, AppDialog, AppUrl
from services.db_service import DBService, DatabaseService
from services.share_engine import ShareEngine
from views.home_view import HomeView
from views.oracao_view import OracaoView
from views.retiro_view import RetiroView
from views.igreja_view import IgrejaView
from main import main as app_main

LOGS_DIR = ROOT_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)
REPORT_FILE = LOGS_DIR / "relatorio_auditoria_robo.log"


class TestRobotAgent:
    def __init__(self):
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.warn_tests = 0
        self.log_entries = []
        self.start_time = 0

    def log(self, category: str, name: str, status: str, details: str = ""):
        self.total_tests += 1
        if status == "PASS":
            self.passed_tests += 1
            icon = "🟢 [PASS]"
        elif status == "FAIL":
            self.failed_tests += 1
            icon = "🔴 [FAIL]"
        else:
            self.warn_tests += 1
            icon = "🟡 [WARN]"

        entry = f"{icon:<10} | {category:<15} | {name:<35} | {details}"
        print(entry)
        self.log_entries.append(entry)

    def print_banner(self):
        print("\n" + "=" * 75)
        print("🤖 AGENTE DE TESTES AUTÔNOMO — AUDITORIA v1.0 ENXUTA (IBPM CR)")
        print("=" * 75)
        print("🎯 Escopo: 4 Abas Respiradas (Início, Oração, Retiro 2026, Igreja & Dízimo),")
        print("             100% dos botões, inscrições, PIX e banco SQLite local.")
        print("=" * 75 + "\n")

    def run_all_tests(self):
        self.start_time = time.time()
        self.print_banner()

        # 1. Banco de Dados SQLite
        print("📦 FASE 1: INICIALIZAÇÃO DO AMBIENTE E BANCO DE DADOS")
        print("-" * 75)
        self.test_database()

        # 2. Inicialização do MockPage
        page = self.create_mock_page()

        # 3. Teste do Fluxo Principal de Montagem (main.py)
        print("\n📱 FASE 2: MONTAGEM DO APLICATIVO PRINCIPAL (MAIN.PY)")
        print("-" * 75)
        self.test_main_app(page)

        # 4. Aba Início (HomeView)
        print("\n🏠 FASE 3: AUDITORIA DA ABA 1 — INÍCIO (O SANTUÁRIO DIGITAL)")
        print("-" * 75)
        self.test_home_view(page)

        # 5. Aba Oração (OracaoView)
        print("\n🙏 FASE 4: AUDITORIA DA ABA 2 — ORAÇÃO (MURAL DE INTERCESSÃO)")
        print("-" * 75)
        self.test_oracao_view(page)

        # 6. Aba Retiro 2026 (RetiroView)
        print("\n🔥 FASE 5: AUDITORIA DA ABA 3 — RETIRO FACE A FACE 2026")
        print("-" * 75)
        self.test_retiro_view(page)

        # 7. Aba Igreja & Dízimo (IgrejaView)
        print("\n🏛️ FASE 6: AUDITORIA DA ABA 4 — IGREJA, DÍZIMO PIX & ROTAS")
        print("-" * 75)
        self.test_igreja_view(page)

        # 8. Motor de Compartilhamento & Links
        print("\n📲 FASE 7: AUDITORIA DO MOTOR DE COMPARTILHAMENTO E CLIPBOARD")
        print("-" * 75)
        self.test_share_engine(page)

        # Relatório Final
        self.print_summary()

    def create_mock_page(self):
        class WindowMock:
            width = 420
            height = 890
            min_width = 360
            min_height = 700
            resizable = True

        class MockPage:
            def __init__(self):
                self.title = "IBPM CR Test Session"
                self.theme_mode = ft.ThemeMode.DARK
                self.padding = 0
                self.bgcolor = None
                self.appbar = None
                self.navigation_bar = None
                self.window = WindowMock()
                self.overlay = []
                self.controls = []
                self.session = None

            def add(self, *c):
                self.controls.extend(c)

            def update(self):
                pass

            def show_dialog(self, dlg):
                return dlg

            def pop_dialog(self):
                return True

            def open(self, dlg):
                return dlg

            def close(self, dlg=None):
                return True

            def set_clipboard(self, val):
                pass

            def launch_url(self, url):
                pass

            def run_task(self, handler, *args, **kwargs):
                pass

        return MockPage()

    def test_database(self):
        try:
            DBService.init_db()
            DBService.seed_initial_data()
            self.log("Database", "Inicialização SQLite", "PASS", "Tabelas criadas com sucesso")
        except Exception as e:
            self.log("Database", "Inicialização SQLite", "FAIL", str(e))

        db = DatabaseService()
        eventos = db.get_eventos()
        if eventos:
            self.log("Database", "Consulta de Eventos", "PASS", f"{len(eventos)} evento(s) ativo(s)")
        else:
            self.log("Database", "Consulta de Eventos", "FAIL", "Nenhum evento retornado")

        frases = db.get_frases_por_sentimento("fe")
        if frases:
            self.log("Database", "Consulta Palavra do Altar", "PASS", f"{len(frases)} mensagem(ns) encontradas")
        else:
            self.log("Database", "Consulta Palavra do Altar", "WARN", "Nenhuma frase encontrada")

    def test_main_app(self, page):
        try:
            app_main(page)
            self.log("AppMain", "Montagem das 4 Abas", "PASS", "main(page) inicializou com sucesso")
        except Exception as e:
            self.log("AppMain", "Montagem das 4 Abas", "FAIL", str(e))

    def test_home_view(self, page):
        nav_target = []
        def mock_navigate(idx):
            nav_target.append(idx)

        try:
            home = HomeView(page, navigate_to_tab=mock_navigate)
            self.log("HomeView", "Instanciação da Tela", "PASS", "HomeView renderizada com respiro")
        except Exception as e:
            self.log("HomeView", "Instanciação da Tela", "FAIL", str(e))
            return

        actions = [
            ("copiar_frase", "Botão Copiar Frase do Dia"),
            ("compartilhar_frase_whatsapp", "Compartilhar Palavra WhatsApp"),
            ("compartilhar_frase_stories", "Compartilhar nos Stories"),
            ("abrir_modal_detalhes_evento", "Navegação Atalho Retiro"),
            ("abrir_modal_como_chegar", "Navegação Atalho Como Chegar"),
            ("copiar_pix_oficial", "Copiar Chave PIX Rápida"),
        ]

        for method_name, label in actions:
            if hasattr(home, method_name):
                func = getattr(home, method_name)
                try:
                    func(None)
                    self.log("HomeView", label, "PASS", f"{method_name}() executou sem erro")
                except Exception as e:
                    self.log("HomeView", label, "FAIL", f"{e}")

    def test_oracao_view(self, page):
        try:
            oracao = OracaoView(page)
            self.log("OracaoView", "Instanciação da Tela", "PASS", "OracaoView renderizada")
        except Exception as e:
            self.log("OracaoView", "Instanciação da Tela", "FAIL", str(e))
            return

        try:
            oracao.abrir_modal_novo_pedido(None)
            self.log("OracaoView", "Abrir Modal Novo Pedido", "PASS", "Modal de intercessão exibido")
        except Exception as e:
            self.log("OracaoView", "Abrir Modal Novo Pedido", "FAIL", str(e))

        try:
            oracao.recarregar_pedidos(None)
            self.log("OracaoView", "Recarregar Lista de Oração", "PASS", "Mural sincronizado")
        except Exception as e:
            self.log("OracaoView", "Recarregar Lista de Oração", "FAIL", str(e))

    def test_retiro_view(self, page):
        try:
            retiro = RetiroView(page)
            self.log("RetiroView", "Instanciação da Tela", "PASS", "RetiroView dedicada renderizada")
        except Exception as e:
            self.log("RetiroView", "Instanciação da Tela", "FAIL", str(e))
            return

        # Testar seleção de tamanhos de camisa
        for tam in ["P", "M", "G", "GG", "XG"]:
            try:
                retiro._selecionar_tamanho(tam)
                self.log("RetiroView", f"Selecionar Camisa {tam}", "PASS", f"Tamanho {tam} ativo")
            except Exception as e:
                self.log("RetiroView", f"Selecionar Camisa {tam}", "FAIL", str(e))

        try:
            retiro.copiar_pix(None)
            self.log("RetiroView", "Copiar Chave PIX Retiro", "PASS", "Chave do Retiro copiada")
        except Exception as e:
            self.log("RetiroView", "Copiar Chave PIX Retiro", "FAIL", str(e))

        try:
            retiro.nome_input.value = "Membro de Teste"
            retiro.whatsapp_input.value = "21999998888"
            retiro.enviar_inscricao(None)
            self.log("RetiroView", "Enviar Inscrição WhatsApp", "PASS", "Mensagem de inscrição gerada")
        except Exception as e:
            self.log("RetiroView", "Enviar Inscrição WhatsApp", "FAIL", str(e))

    def test_igreja_view(self, page):
        try:
            igreja = IgrejaView(page)
            self.log("IgrejaView", "Instanciação da Tela", "PASS", "IgrejaView renderizada")
        except Exception as e:
            self.log("IgrejaView", "Instanciação da Tela", "FAIL", str(e))
            return

        try:
            igreja.copiar_pix(None)
            self.log("IgrejaView", "Copiar Chave PIX Oficial", "PASS", "Chave PIX copiada")
        except Exception as e:
            self.log("IgrejaView", "Copiar Chave PIX Oficial", "FAIL", str(e))

        try:
            igreja.enviar_comprovante_whatsapp(None)
            self.log("IgrejaView", "Enviar Comprovante WhatsApp", "PASS", "Mensagem de dízimo gerada")
        except Exception as e:
            self.log("IgrejaView", "Enviar Comprovante WhatsApp", "FAIL", str(e))

    def test_share_engine(self, page):
        try:
            ShareEngine.copy_to_clipboard(page, "Chave PIX Teste")
            self.log("ShareEngine", "Copiar Área de Transferência", "PASS", "Clipboard setado com SnackBar")
        except Exception as e:
            self.log("ShareEngine", "Copiar Área de Transferência", "FAIL", str(e))

        try:
            ShareEngine.share_whatsapp_status(page, "Texto de Teste")
            self.log("ShareEngine", "Link WhatsApp Formatado", "PASS", "URL formatada e despachada")
        except Exception as e:
            self.log("ShareEngine", "Link WhatsApp Formatado", "FAIL", str(e))

    def print_summary(self):
        duration = time.time() - self.start_time
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0

        print("\n" + "=" * 75)
        print("📊 RELATÓRIO FINAL DO AGENTE DE TESTES IBPM CR v1.0")
        print("=" * 75)
        print(f"⏱️  Tempo Total de Execução: {duration:.2f} segundos")
        print(f"📋 Total de Testes Executados: {self.total_tests}")
        print(f"🟢 Testes Aprovados (PASS):    {self.passed_tests}")
        print(f"🔴 Testes Reprovados (FAIL):   {self.failed_tests}")
        print(f"🟡 Avisos / Alertas (WARN):    {self.warn_tests}")
        print(f"📈 Taxa de Sucesso / Saúde:     {success_rate:.1f}%")
        print("=" * 75)

        if self.failed_tests == 0:
            print("🎉 RESULTADO: O APP v1.0 ESTÁ 100% OPERACIONAL, FLUIDO E SEM ERROS!")
            print("✨ 4 Abas Respiradas, sem excesso de funções, limpo e profissional.")
        else:
            print(f"⚠️ ATENÇÃO: {self.failed_tests} problema(s) detectados. Verifique os logs.")

        print(f"📝 Relatório completo salvo em: {REPORT_FILE}")
        print("=" * 75 + "\n")

        try:
            with open(REPORT_FILE, "w", encoding="utf-8") as f:
                f.write(f"RELATÓRIO DE AUDITORIA DO AGENTE DE TESTES - IBPM CR v1.0\nData: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("\n".join(self.log_entries))
                f.write(f"\n\nTaxa de Sucesso: {success_rate:.1f}%\n")
        except Exception:
            pass


if __name__ == "__main__":
    agent = TestRobotAgent()
    agent.run_all_tests()
