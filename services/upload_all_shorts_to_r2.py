#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upload em Lote dos 576 Cortes Verticais (9:16) para o Cloudflare R2.
Inclui:
- Barra de progresso detalhada e estimativa de tempo
- Manifesto de controle (data/r2_cortes_manifest.json) para retomada automática sem reenvios
- Upload de vídeos .mp4 e capas .jpg
- Catalogação dos links finais no Cloudflare R2
"""
import os
import sys
import time
import json
from pathlib import Path
import mimetypes
from dotenv import load_dotenv

# Configuração de encoding Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

R2_ENDPOINT = os.getenv("R2_ENDPOINT_URL")
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
R2_BUCKET = os.getenv("R2_BUCKET_NAME", "ibpmcr-midia")
R2_PUBLIC_URL = os.getenv("R2_PUBLIC_URL", "https://midia.ibpmcr.com.br")

SHORTS_DIR = Path(r"c:\Users\matheus\.gemini\antigravity-ide\scratch\ibpmcr-automation-system\data\fase3_renderizacao")
MANIFEST_PATH = BASE_DIR / "data" / "r2_cortes_manifest.json"


def get_s3_client():
    import boto3
    from botocore.config import Config
    return boto3.client(
        service_name="s3",
        endpoint_url=R2_ENDPOINT,
        aws_access_key_id=R2_ACCESS_KEY,
        aws_secret_access_key=R2_SECRET_KEY,
        region_name="auto",
        config=Config(signature_version="s3v4")
    )


def load_manifest() -> dict:
    if MANIFEST_PATH.exists():
        try:
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"enviados": {}, "total_enviados_mb": 0.0}


def save_manifest(manifest: dict):
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)


class ProgressCallback:
    def __init__(self, filename: str, total_bytes: int):
        self.filename = filename
        self.total_bytes = total_bytes
        self.uploaded_bytes = 0
        self.start_time = time.time()

    def __call__(self, bytes_amount: int):
        self.uploaded_bytes += bytes_amount


def main():
    print("=" * 70)
    print("🚀 INICIANDO UPLOAD EM SEGUNDO PLANO PARA O CLOUDFLARE R2")
    print(f"📦 Bucket Destino: {R2_BUCKET}")
    print(f"📂 Diretório de Origem: {SHORTS_DIR}")
    print("=" * 70)

    if not R2_ENDPOINT or not R2_ACCESS_KEY or not R2_SECRET_KEY:
        print("[ERRO] Credenciais do Cloudflare R2 não encontradas no .env!")
        return

    s3 = get_s3_client()
    manifest = load_manifest()
    enviados = manifest.get("enviados", {})

    # Mapeia todos os arquivos .mp4 e .jpg
    todos_arquivos = []
    for f in sorted(SHORTS_DIR.glob("*/*/*.*")):
        if f.suffix.lower() in [".mp4", ".jpg", ".jpeg"]:
            todos_arquivos.append(f)

    total_arquivos = len(todos_arquivos)
    total_bytes_geral = sum(f.stat().st_size for f in todos_arquivos)
    total_gb_geral = total_bytes_geral / (1024 ** 3)

    # Filtra os que ainda não foram enviados
    pendentes = [f for f in todos_arquivos if str(f) not in enviados]
    total_pendentes = len(pendentes)
    ja_enviados_count = total_arquivos - total_pendentes

    print(f"📊 Total de Arquivos Detectados: {total_arquivos} ({total_gb_geral:.2f} GB)")
    print(f"✅ Já enviados anteriormente: {ja_enviados_count}")
    print(f"⏳ Arquivos pendentes para upload: {total_pendentes}")
    print("=" * 70)

    if total_pendentes == 0:
        print("🎉 Todos os 576 cortes e capas já estão no Cloudflare R2!")
        return

    tempo_inicio_geral = time.time()
    bytes_enviados_sessao = 0

    for idx, arq in enumerate(pendentes, 1):
        rel_parts = arq.parts
        # Ex: culto_372/02_shorts_verticais_9x16/372_corte_01.mp4 -> cortes/culto_372/372_corte_01.mp4
        culto_pasta = arq.parent.parent.name
        remote_key = f"cortes/{culto_pasta}/{arq.name}"

        file_size = arq.stat().st_size
        size_mb = file_size / (1024 * 1024)

        content_type, _ = mimetypes.guess_type(str(arq))
        content_type = content_type or ("video/mp4" if arq.suffix.lower() == ".mp4" else "image/jpeg")

        t0 = time.time()
        try:
            callback = ProgressCallback(arq.name, file_size)
            s3.upload_file(
                Filename=str(arq),
                Bucket=R2_BUCKET,
                Key=remote_key,
                ExtraArgs={"ContentType": content_type},
                Callback=callback
            )
            dt = time.time() - t0
            speed_mb = size_mb / dt if dt > 0 else 0
            bytes_enviados_sessao += file_size

            # Atualiza manifesto
            url_publica = f"{R2_PUBLIC_URL.rstrip('/')}/{remote_key}"
            enviados[str(arq)] = {
                "key": remote_key,
                "url": url_publica,
                "size_mb": round(size_mb, 2),
                "timestamp": time.time()
            }
            manifest["enviados"] = enviados
            manifest["total_enviados_mb"] = sum(v["size_mb"] for v in enviados.values())
            save_manifest(manifest)

            # Cálculo de progresso e estimativa
            progresso_pct = ((ja_enviados_count + idx) / total_arquivos) * 100
            tempo_decorrido = time.time() - tempo_inicio_geral
            media_tempo_por_item = tempo_decorrido / idx
            itens_restantes = total_pendentes - idx
            eta_segundos = itens_restantes * media_tempo_por_item
            eta_min = eta_segundos / 60

            # Barra visual de progresso (20 blocos)
            blocos = int(progresso_pct // 5)
            barra = "█" * blocos + "░" * (20 - blocos)

            tipo_emoji = "🎬" if arq.suffix.lower() == ".mp4" else "🖼️"
            print(f"[{ja_enviados_count + idx}/{total_arquivos}] |{barra}| {progresso_pct:5.1f}% | {tipo_emoji} {arq.name[:35]:35} ({size_mb:5.1f} MB em {dt:4.1f}s @ {speed_mb:4.1f} MB/s) | ETA: {eta_min:4.1f} min")

        except Exception as e:
            print(f"[FALHA] Erro ao enviar {arq.name}: {e}")
            time.sleep(2)

    tempo_total = (time.time() - tempo_inicio_geral) / 60
    print("\n" + "=" * 70)
    print(f"🎉 UPLOAD COMPLETO! Todos os arquivos foram enviados em {tempo_total:.1f} minutos.")
    print(f"📁 Manifesto salvo em: {MANIFEST_PATH}")
    print("=" * 70)


if __name__ == "__main__":
    main()
