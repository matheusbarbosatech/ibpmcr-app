"""
Script de Automação para Baixar o APK Oficial da IBPM CR Diretamente para a Área de Trabalho (Desktop).
Permite ao desenvolvedor/pastor ter sempre o arquivo .apk atualizado pronto na Área de Trabalho para enviar via WhatsApp/USB para o celular.
"""
import os
import sys
import urllib.request
from pathlib import Path

# Configura UTF-8 no Windows
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

DESKTOP_DIR = Path.home() / "Desktop"
DESTINO_APK = DESKTOP_DIR / "IBPMCR-App-Oficial.apk"
URL_APK_R2 = "https://pub-2b0c315d91644a41b558a4d2410ce1f8.r2.dev/app/IBPMCR-App-Oficial.apk"

def baixar_apk_desktop():
    print("=" * 65)
    print("📲 BAIXADOR AUTOMÁTICO DO APK OFICIAL IBPM CR PARA O DESKTOP")
    print("=" * 65)
    print(f"🔗 URL Pública Cloudflare R2: {URL_APK_R2}")
    print(f"📁 Destino na Área de Trabalho: {DESTINO_APK}\n")
    
    try:
        req = urllib.request.Request(URL_APK_R2, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp, open(DESTINO_APK, "wb") as out_file:
            total_size_hdr = resp.headers.get("content-length")
            total_size = int(total_size_hdr) if total_size_hdr else 0
            bloco_size = 1024 * 1024  # 1MB
            baixado = 0
            
            while True:
                buffer = resp.read(bloco_size)
                if not buffer:
                    break
                baixado += len(buffer)
                out_file.write(buffer)
                if total_size > 0:
                    porc = (baixado / total_size) * 100
                    print(f"  -> Progresso: {baixado / (1024*1024):.1f} MB / {total_size / (1024*1024):.1f} MB ({porc:.1f}%)", end="\r")
                else:
                    print(f"  -> Baixado: {baixado / (1024*1024):.1f} MB", end="\r")
                    
        tam_mb = os.path.getsize(DESTINO_APK) / (1024 * 1024)
        print(f"\n\n🎉 SUCESSO ABSOLUTO! APK gravado diretamente na sua Área de Trabalho:")
        print(f"👉 {DESTINO_APK} ({tam_mb:.1f} MB)")
        print(f"💡 Agora basta arrastar para o seu WhatsApp Web ou copiar para o celular!")
        return True
    except Exception as e:
        print(f"\n[!] Erro ao baixar APK: {e}")
        return False

if __name__ == "__main__":
    baixar_apk_desktop()
