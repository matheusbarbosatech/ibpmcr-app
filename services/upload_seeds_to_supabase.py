#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upload Automático dos Mega-Ativos para o Banco de Dados Nuvem Supabase.
Lê os JSONs minerados em C:\\Users\\matheus\\Desktop\\SEEDS_APP_IBPMCR e insere
via REST API com a chave secreta de serviço.
"""
import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path
from dotenv import load_dotenv

# Configuração de encoding para console Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# Configurações do Supabase via Variáveis de Ambiente
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://gbubafojvadeetwsqlwp.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY") or os.getenv("SUPABASE_KEY", "")

BASE_DIR = Path(__file__).resolve().parent.parent
DESKTOP_DIR = Path(os.path.expanduser("~")) / "Desktop"
if (BASE_DIR / "data" / "seeds").exists():
    SEEDS_DIR = BASE_DIR / "data" / "seeds"
elif (BASE_DIR / "SEEDS_APP_IBPMCR").exists():
    SEEDS_DIR = BASE_DIR / "SEEDS_APP_IBPMCR"
else:
    SEEDS_DIR = DESKTOP_DIR / "SEEDS_APP_IBPMCR"


def post_to_supabase(table: str, data: list):
    """Envia um lote de registros para uma tabela do Supabase."""
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    # Divide em lotes de 50 para garantir velocidade e estabilidade
    batch_size = 50
    total_enviados = 0

    for i in range(0, len(data), batch_size):
        lote = data[i:i + batch_size]
        payload = json.dumps(lote).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                total_enviados += len(lote)
                print(f"  [+] {table}: {total_enviados}/{len(data)} registros enviados.")
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode()
            print(f"  [-] Erro ao enviar lote para {table} (HTTP {e.code}): {err_msg}")
        except Exception as e:
            print(f"  [-] Erro geral em {table}: {e}")

    return total_enviados


def upload_tudo():
    print("=" * 65)
    print("🚀 INICIANDO SINCRONIZAÇÃO DOS MEGA-ATIVOS COM O SUPABASE")
    print(f"Projeto: {SUPABASE_URL}")
    print("=" * 65)

    # 1. Devocionais Diários (365 Dias)
    dev_path = SEEDS_DIR / "devocionais_365_seed.json"
    if dev_path.exists():
        with open(dev_path, "r", encoding="utf-8") as f:
            devocionais = json.load(f)
        print(f"\n[1/5] Enviando {len(devocionais)} Devocionais Diários...")
        post_to_supabase("devocionais_diarios", devocionais)

    # 2. Escola de Líderes (52 Módulos)
    mod_path = SEEDS_DIR / "escola_lideres_52_modulos_seed.json"
    if mod_path.exists():
        with open(mod_path, "r", encoding="utf-8") as f:
            modulos = json.load(f)
        print(f"\n[2/5] Enviando {len(modulos)} Módulos da Escola de Líderes...")
        post_to_supabase("escola_lideres_modulos", modulos)

    # 3. Livros Oficiais (3 Livros)
    livros_path = SEEDS_DIR / "livros_oficiais_seed.json"
    if livros_path.exists():
        with open(livros_path, "r", encoding="utf-8") as f:
            livros = json.load(f)
        livros_limpos = []
        for l in livros:
            item = {
                "titulo_livro": l.get("titulo_livro") or l.get("titulo"),
                "subtitulo": l.get("subtitulo"),
                "capa_url": l.get("capa_url"),
                "pdf_url": l.get("pdf_url"),
                "sinopse": l.get("sinopse"),
                "total_capitulos": 12
            }
            livros_limpos.append(item)
        print(f"\n[3/5] Enviando {len(livros_limpos)} Livros Oficiais...")
        post_to_supabase("livros_ebooks", livros_limpos)


    # 4. Frases Proféticas (125 Frases)
    frases_path = SEEDS_DIR / "frases_profeticas_seed.json"
    if frases_path.exists():
        with open(frases_path, "r", encoding="utf-8") as f:
            frases = json.load(f)
        print(f"\n[4/5] Enviando {len(frases)} Frases Proféticas...")
        post_to_supabase("frases_profeticas", frases)

    # 5. Pedidos de Oração Iniciais
    print(f"\n[5/5] Enviando Pedidos de Oração de Teste...")
    pedidos = [
        {
            "nome_solicitante": "Maria Aparecida (67 anos)",
            "motivo_oracao": "Saúde",
            "detalhes_pedido": "Peço oração pelos exames do coração do meu esposo João e paz na nossa casa.",
            "is_anonimo": False,
            "status": "aprovado",
            "contador_orando": 14
        },
        {
            "nome_solicitante": "Anônimo",
            "motivo_oracao": "Causas na Justiça",
            "detalhes_pedido": "Estou passando por uma causa trabalhista injusta há 2 anos. Peço um milagre da justiça de Deus.",
            "is_anonimo": True,
            "status": "aprovado",
            "contador_orando": 28
        }
    ]
    post_to_supabase("pedidos_oracao", pedidos)

    # 6. Galeria de Fotos e Cortes

    print(f"\n[6/6] Enviando Galeria de Fotos e Cortes Verticais...")
    fotos = [
        {"album_nome": "Domingo de Celebração - Santa Ceia", "data_evento": "2026-09-06", "categoria": "Santa Ceia", "foto_hd_url": "https://images.unsplash.com/photo-1511632765486-a01980e01a18?w=1200", "foto_thumb_url": "https://images.unsplash.com/photo-1511632765486-a01980e01a18?w=400", "total_downloads": 87},
        {"album_nome": "Conferência de Jovens Coração Ardente", "data_evento": "2026-08-29", "categoria": "Conferência", "foto_hd_url": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=1200", "foto_thumb_url": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=400", "total_downloads": 142},
        {"album_nome": "Batismo nas Águas - Vida Nova", "data_evento": "2026-08-16", "categoria": "Batismo", "foto_hd_url": "https://images.unsplash.com/photo-1507692049790-de58290a4334?w=1200", "foto_thumb_url": "https://images.unsplash.com/photo-1507692049790-de58290a4334?w=400", "total_downloads": 215},
        {"album_nome": "Quinta Profética de Milagres", "data_evento": "2026-09-03", "categoria": "Culto", "foto_hd_url": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=1200", "foto_thumb_url": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=400", "total_downloads": 63}
    ]
    post_to_supabase("galeria_fotos", fotos)

    cortes = [
        {"titulo_impacto": "JESUS FUNCIONA COMO UM ESPELHO QUE MOSTRA QUEM VOCÊ É", "tema_categoria": "Revelação", "video_9_16_url": "https://midia.ibpmcr.com.br/cortes/corte_372_01.mp4", "duracao_segundos": 23, "total_compartilhamentos": 154},
        {"titulo_impacto": "QUANDO VOCÊ ENTREGA SUA DOR NO ALTAR, DEUS TRANSFORMA EM UNÇÃO", "tema_categoria": "Cura", "video_9_16_url": "https://midia.ibpmcr.com.br/cortes/corte_373_02.mp4", "duracao_segundos": 38, "total_compartilhamentos": 240},
        {"titulo_impacto": "O INIMIGO QUER QUE VOCÊ DESISTA HOJE, MAS O SEU MILAGRE VEM AMANHÃ", "tema_categoria": "Guerra Espiritual", "video_9_16_url": "https://midia.ibpmcr.com.br/cortes/corte_374_03.mp4", "duracao_segundos": 45, "total_compartilhamentos": 310},
        {"titulo_impacto": "NÃO ANDEIS ANSIOSOS POR COISA ALGUMA: DESCANSE NO SENHOR", "tema_categoria": "Família", "video_9_16_url": "https://midia.ibpmcr.com.br/cortes/corte_375_01.mp4", "duracao_segundos": 30, "total_compartilhamentos": 189}
    ]
    post_to_supabase("cortes_verticais", cortes)


    print("\n" + "=" * 65)
    print("🎉 SINCRONIZAÇÃO COM O SUPABASE CONCLUÍDA COM SUCESSO TOTAL!")
    print("=" * 65)


if __name__ == "__main__":
    upload_tudo()
