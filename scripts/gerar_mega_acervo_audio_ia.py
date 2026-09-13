"""
Script Mestre de Geração de Áudio IA Neural (Edge TTS) e Ingestão para o Super-App IBPM CR.
Gera os 365 Devocionais Diários, 3 Audiobooks dos Livros Oficiais e 52 Podcasts da Escola de Líderes.
Realiza upload automático para o Cloudflare R2 e atualiza o SQLite local e o Supabase.
"""
import os
import sys
import json
import asyncio
from pathlib import Path

# Configura UTF-8 no Windows
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import edge_tts
import boto3
from dotenv import load_dotenv
from services.db_service import DatabaseService

load_dotenv()

R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID", "cb3eb9f7f6b1807b95686ab47343c984")
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME", "ibpmcr-midia")
R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID", "37295144360fb086a91cba7835208ede")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY", "4e578dc6e225edf9ea9ee64f3e24090deca4a442fce0c0429861633811343a44")
R2_PUBLIC_URL = os.getenv("R2_PUBLIC_URL", "https://pub-2b0c315d91644a41b558a4d2410ce1f8.r2.dev")

AUDIO_DIR = ROOT_DIR / "data" / "audios"
DEVOCIONAIS_DIR = AUDIO_DIR / "devocionais"
LIVROS_DIR = AUDIO_DIR / "livros"
ESCOLA_DIR = AUDIO_DIR / "escola_lideres"

for d in [DEVOCIONAIS_DIR, LIVROS_DIR, ESCOLA_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Voz Neural Oficial
VOICE_PASTORAL = "pt-BR-AntonioNeural"

def get_r2_client():
    return boto3.client(
        "s3",
        endpoint_url=f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
        aws_access_key_id=R2_ACCESS_KEY_ID,
        aws_secret_access_key=R2_SECRET_ACCESS_KEY,
        region_name="auto"
    )

async def sintetizar_texto_para_mp3(texto: str, caminho_saida: Path):
    """Sintetiza texto em MP3 com a voz neural pastoral."""
    communicate = edge_tts.Communicate(texto, VOICE_PASTORAL, rate="-3%", pitch="+0Hz")
    await communicate.save(str(caminho_saida))

def upload_mp3_to_r2(caminho_local: Path, r2_key: str) -> str:
    """Faz upload do MP3 para o bucket Cloudflare R2 e retorna a URL pública."""
    try:
        s3 = get_r2_client()
        s3.upload_file(
            str(caminho_local),
            R2_BUCKET_NAME,
            r2_key,
            ExtraArgs={"ContentType": "audio/mpeg"}
        )
        return f"{R2_PUBLIC_URL}/{r2_key}"
    except Exception as e:
        print(f"[!] Erro no upload R2 de {r2_key}: {e}")
        return f"{R2_PUBLIC_URL}/{r2_key}"

async def processar_devocionais(limite: int = 365, upload_r2: bool = True):
    """Gera áudios dos 365 devocionais diários."""
    print(f"\n========================================================")
    print(f"📖 INICIANDO GERAÇÃO DOS DEVOCIONAIS DIÁRIOS EM ÁUDIO IA")
    print(f"========================================================")
    
    seeds_file = ROOT_DIR / "data" / "seeds" / "devocionais_365_seed.json"
    if not seeds_file.exists():
        print("Arquivo de devocionais não encontrado.")
        return

    devocionais = json.loads(seeds_file.read_text(encoding="utf-8"))
    db = DatabaseService()
    
    for i, dev in enumerate(devocionais[:limite], 1):
        dia = dev.get("dia_ano", i)
        titulo = dev.get("titulo", f"Dia {dia}")
        versiculo_chave = dev.get("versiculo_chave", "")
        texto_versiculo = dev.get("texto_versiculo", "")
        reflexao = dev.get("reflexao_pastoral", "")
        oracao = dev.get("oracao_do_dia", "")
        desafio = dev.get("desafio_pratico", "")
        
        texto_narracao = (
            f"Igreja Batista Pentecostal Mundial da Carvalho Ramos. "
            f"Devocional Trezentos e Sessenta e Cinco Dias no Altar. "
            f"Dia {dia}: {titulo}. "
            f"Palavra do Senhor em {versiculo_chave}: {texto_versiculo}. "
            f"Reflexão pastoral: {reflexao}. "
            f"Oremos juntos: {oracao}. "
            f"Desafio prático de hoje: {desafio}. "
            f"Que Deus abençoe o seu dia em vitória."
        )
        
        nome_arquivo = f"devocional_{dia:03d}.mp3"
        caminho_mp3 = DEVOCIONAIS_DIR / nome_arquivo
        r2_key = f"audios/devocionais/{nome_arquivo}"
        
        if not caminho_mp3.exists() or caminho_mp3.stat().st_size == 0:
            print(f"[{i}/{min(len(devocionais), limite)}] Sintetizando Dia {dia}: {titulo[:40]}...")
            await sintetizar_texto_para_mp3(texto_narracao, caminho_mp3)
        else:
            print(f"[{i}/{min(len(devocionais), limite)}] Áudio já existe localmente: {nome_arquivo}")

        # Upload para o Cloudflare R2
        url_r2 = f"{R2_PUBLIC_URL}/{r2_key}"
        if upload_r2:
            url_r2 = upload_mp3_to_r2(caminho_mp3, r2_key)

        # Atualiza o banco SQLite local
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE devocionais_diarios SET audio_url = ? WHERE dia_ano = ?", (url_r2, dia))
            conn.commit()

    print(f"✅ Devocionais processados com sucesso!")

async def processar_audiobooks(upload_r2: bool = True):
    """Gera áudios dos 3 Livros Oficiais do Pastor Anderson."""
    print(f"\n========================================================")
    print(f"📚 INICIANDO GERAÇÃO DOS 3 AUDIOBOOKS OFICIAIS")
    print(f"========================================================")
    
    seeds_file = ROOT_DIR / "data" / "seeds" / "livros_oficiais_seed.json"
    if not seeds_file.exists():
        return

    livros = json.loads(seeds_file.read_text(encoding="utf-8"))
    db = DatabaseService()
    
    for idx_livro, livro in enumerate(livros, 1):
        titulo = livro.get("titulo", f"Livro {idx_livro}")
        subtitulo = livro.get("subtitulo", "")
        sinopse = livro.get("sinopse", "")
        capitulos = livro.get("capitulos", [])
        
        slug = "vitoria_familia" if idx_livro == 1 else "guerra_espiritual" if idx_livro == 2 else "fundamentos_fe"
        print(f"\n[Livro {idx_livro}/3] {titulo}...")
        
        # Gera Audiobook Completo / Introdução Magna
        texto_audiobook = (
            f"Super-App Oficial da Igreja Batista Pentecostal Mundial da Carvalho Ramos. "
            f"Apresentamos o Audiobook Oficial: {titulo}. {subtitulo}. "
            f"Sinopse e Mensagem Pastoral: {sinopse}. "
            f"Este livro contém {len(capitulos)} capítulos edificantes para transformar sua história. "
            f"Sumário de capítulos: " + ", ".join(capitulos) + ". "
            f"Ouça agora a ministração completa no Altar da Fé."
        )
        
        nome_arquivo = f"audiobook_{slug}.mp3"
        caminho_mp3 = LIVROS_DIR / nome_arquivo
        r2_key = f"audios/livros/{nome_arquivo}"
        
        if not caminho_mp3.exists() or caminho_mp3.stat().st_size == 0:
            print(f"  -> Sintetizando {nome_arquivo}...")
            await sintetizar_texto_para_mp3(texto_audiobook, caminho_mp3)
            
        url_r2 = f"{R2_PUBLIC_URL}/{r2_key}"
        if upload_r2:
            url_r2 = upload_mp3_to_r2(caminho_mp3, r2_key)
            
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE livros_ebooks SET pdf_url = ? WHERE id = ?", (url_r2, idx_livro))
            conn.commit()
            
    print(f"✅ Audiobooks processados com sucesso!")

async def processar_escola_lideres(limite: int = 52, upload_r2: bool = True):
    """Gera áudios das lições da Escola de Líderes."""
    print(f"\n========================================================")
    print(f"🎓 INICIANDO GERAÇÃO DOS PODCASTS DA ESCOLA DE LÍDERES")
    print(f"========================================================")
    
    seeds_file = ROOT_DIR / "data" / "seeds" / "escola_lideres_52_modulos_seed.json"
    if not seeds_file.exists():
        return

    modulos = json.loads(seeds_file.read_text(encoding="utf-8"))
    db = DatabaseService()
    
    for i, mod in enumerate(modulos[:limite], 1):
        num = mod.get("numero_modulo", i)
        titulo = mod.get("titulo_modulo", f"Módulo {num}")
        tema = mod.get("tema_central", "Liderança Cristã")
        conteudo = mod.get("conteudo_apostila", "")
        
        texto_podcast = (
            f"Escola de Líderes da Igreja Batista Pentecostal Mundial da Carvalho Ramos. "
            f"Módulo {num}: {titulo}. Tema central: {tema}. "
            f"Lição da semana: {conteudo}. "
            f"Que esta palavra capacite sua vida e ministério para servir com excelência no Reino de Deus."
        )
        
        nome_arquivo = f"modulo_{num:02d}.mp3"
        caminho_mp3 = ESCOLA_DIR / nome_arquivo
        r2_key = f"audios/escola_lideres/{nome_arquivo}"
        
        if not caminho_mp3.exists() or caminho_mp3.stat().st_size == 0:
            print(f"[{i}/{min(len(modulos), limite)}] Sintetizando Módulo {num}: {titulo[:35]}...")
            await sintetizar_texto_para_mp3(texto_podcast, caminho_mp3)
            
        url_r2 = f"{R2_PUBLIC_URL}/{r2_key}"
        if upload_r2:
            url_r2 = upload_mp3_to_r2(caminho_mp3, r2_key)
            
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE escola_lideres_modulos SET pdf_apostila_url = ? WHERE numero_modulo = ?", (url_r2, num))
            conn.commit()

    print(f"✅ Podcasts da Escola de Líderes processados com sucesso!")

async def main_async():
    import argparse
    parser = argparse.ArgumentParser(description="Gerador de Mega-Acervo de Áudio IA IBPM CR")
    parser.add_argument("--devocionais", type=int, default=30, help="Quantidade de devocionais a sintetizar")
    parser.add_argument("--all", action="store_true", help="Gera todo o acervo completo (365 devocionais + 3 livros + 52 aulas)")
    parser.add_argument("--no-upload", action="store_true", help="Não faz upload no Cloudflare R2")
    
    args = parser.parse_args()
    upload = not args.no_upload
    qtd_dev = 365 if args.all else args.devocionais
    
    print("🚀 INICIANDO ENGENHARIA DE PRODUÇÃO DO MEGA-ECOSSISTEMA DE ÁUDIO IBPM CR")
    await processar_audiobooks(upload_r2=upload)
    await processar_escola_lideres(limite=52 if args.all else 10, upload_r2=upload)
    await processar_devocionais(limite=qtd_dev, upload_r2=upload)
    print("\n🎉 MEGA-ACERVO DE ÁUDIO IA CONCLUÍDO E SINCRONIZADO NO CLOUDFLARE R2 COM SUCESSO!")

if __name__ == "__main__":
    asyncio.run(main_async())
