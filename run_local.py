"""
Executador Local do Super-App IBPM CR para Teste Instantâneo no PC.
Permite testar todas as funcionalidades (Eventos, Lojinha, Rádio, Cultos, Oração) em 1 segundo
sem precisar compilar APK e sem precisar passar para o celular.
"""
import os
import sys
import time
import traceback
from pathlib import Path

# Configura UTF-8 no terminal Windows
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Cria diretório de logs para facilitar suporte
LOGS_DIR = ROOT_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)
LOG_FILE = LOGS_DIR / "local_runner.log"

def log_msg(msg: str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    linha = f"[{timestamp}] {msg}"
    print(linha)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(linha + "\n")
    except Exception:
        pass

def main():
    print("=" * 65)
    print("🚀 SUPER-APP OFICIAL IBPM CR — AMBIENTE DE TESTE LOCAL NO PC")
    print("=" * 65)
    print("💡 Teste instantâneo de telas, botões, modais, áudios e banco de dados.")
    print("=" * 65)

    import flet as ft
    from services.db_service import DBService
    from main import main as app_main

    # Inicializa banco de dados local
    log_msg("Inicializando banco de dados SQLite local...")
    try:
        DBService.init_db()
        DBService.seed_initial_data()
        log_msg("✅ Banco de dados local inicializado e sincronizado com sucesso!")
    except Exception as e:
        log_msg(f"⚠️ Aviso ao inicializar banco: {e}")

    modo = sys.argv[1].lower() if len(sys.argv) > 1 else "desktop"

    if modo in ["web", "--web", "-w"]:
        port = 8550
        log_msg(f"🌐 Iniciando no Modo Navegador Web em http://localhost:{port} ...")
        print(f"\n👉 O navegador abrirá automaticamente em: http://localhost:{port}")
        print("💡 Dica: Pressione F12 no Chrome/Edge e ative a visão 'Mobile' para ver como celular!\n")
        try:
            ft.run(main=app_main, view=ft.AppView.WEB_BROWSER, port=port)
        except Exception as e:
            log_msg(f"❌ Erro na execução Web: {e}\n{traceback.format_exc()}")
    else:
        log_msg("📱 Iniciando Janela Nativa Desktop (Formato Smartphone 420x890)...")
        print("\n👉 A janela do aplicativo abrirá na sua tela em instantes.")
        print("💡 Você pode interagir com o mouse como se estivesse no celular.\n")
        try:
            ft.run(main=app_main, view=ft.AppView.FLET_APP)
        except Exception as e:
            log_msg(f"⚠️ Cliente Desktop indisponível ({e}). Iniciando automaticamente no navegador...")
            try:
                ft.run(main=app_main, view=ft.AppView.WEB_BROWSER, port=8550)
            except Exception as err_web:
                log_msg(f"❌ Erro na execução: {err_web}\n{traceback.format_exc()}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Aplicativo encerrado pelo usuário.")
    except Exception as err:
        log_msg(f"\n❌ ERRO CRÍTICO NO APLICATIVO:\n{traceback.format_exc()}")
        input("\nPressione ENTER para fechar...")
