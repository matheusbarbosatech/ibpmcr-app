"""
Auto-Deploy Completo do Super-App IBPM CR:
1. Conecta ao celular via ADB (192.168.1.8:5555 ou USB).
2. Transfere o APK oficial de produção.
3. Instala e abre o aplicativo no celular.
4. Inicia o Scrcpy para controle total pelo PC.
"""
import os
import sys
import subprocess
import time
from pathlib import Path

ADB_PATH = r"C:\Users\matheus\AppData\Local\Android\Sdk\platform-tools\adb.exe"
SCRCPY_PATH = r"C:\Users\matheus\AppData\Local\Microsoft\WinGet\Packages\Genymobile.scrcpy_Microsoft.Winget.Source_8wekyb3d8bbwe\scrcpy-win64-v4.1\scrcpy.exe"
APK_DESKTOP = r"C:\Users\matheus\Desktop\IBPMCR-App-Oficial.apk"
PACKAGE_NAME = "org.ibpmcr"
DEVICE_IP = "192.168.1.8:5555"

def run_cmd(cmd_list, timeout=60):
    try:
        res = subprocess.run(cmd_list, capture_output=True, text=True, timeout=timeout)
        return res.stdout.strip() + "\n" + res.stderr.strip()
    except Exception as e:
        return str(e)

def main():
    print("=" * 65)
    print("🚀 AUTO-DEPLOY ANDROID: IBPM CR SUPER-APP")
    print("=" * 65)
    
    # 1. Conectar ADB
    print("1️⃣ Conectando ao celular Xiaomi via ADB...")
    out_conn = run_cmd([ADB_PATH, "connect", DEVICE_IP])
    print(f"   -> {out_conn.strip()}")
    
    # 2. Transferir APK para o celular
    if os.path.exists(APK_DESKTOP):
        print("2️⃣ Enviando APK atualizado para a pasta Downloads do celular...")
        out_push = run_cmd([ADB_PATH, "-s", DEVICE_IP, "push", APK_DESKTOP, "/sdcard/Download/IBPMCR-App-Oficial.apk"], timeout=120)
        print(f"   -> {out_push.strip()}")
    else:
        print(f"⚠️ APK não encontrado em {APK_DESKTOP}")

    # 3. Tentar instalar via ADB
    print("3️⃣ Tentando instalação nativa...")
    out_inst = run_cmd([ADB_PATH, "-s", DEVICE_IP, "install", "-r", "-d", APK_DESKTOP], timeout=60)
    print(f"   -> {out_inst.strip()}")
    
    # 4. Abrir Gerenciador de Arquivos se necessário
    print("4️⃣ Abrindo Gerenciador de Arquivos Xiaomi / Downloads...")
    run_cmd([ADB_PATH, "-s", DEVICE_IP, "shell", "am", "start", "-n", "com.mi.android.globalFileexplorer/com.android.fileexplorer.FileExplorerTabActivity"])

    # 5. Iniciar Scrcpy
    print("5️⃣ Iniciando espelhamento com Scrcpy...")
    subprocess.Popen([
        SCRCPY_PATH, "-s", DEVICE_IP,
        "--window-title", "IBPM CR - Celular Xiaomi",
        "--stay-awake"
    ])
    print("🎉 Scrcpy aberto com sucesso no seu monitor!")

if __name__ == "__main__":
    main()
