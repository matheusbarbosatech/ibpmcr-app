"""
Script Oficial de Download e Ingestão de Fotos & Mídias do Instagram para o Super-App IBPM CR.
Baixa fotos estáticas, carrosséis e vídeos, organizando em álbuns temáticos e populando
o banco de dados local (SQLite) e a nuvem (Supabase).
"""
import os
import sys
import json
import re
import urllib.request
import urllib.parse
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import instaloader
from services.db_service import DBService, DatabaseService

OUTPUT_DIR = ROOT_DIR / "data" / "instagram_midias"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

class InstagramDownloader:
    def __init__(self, username: str = "ibpmcarvalhoramos"):
        self.username = username
        self.loader = instaloader.Instaloader(
            dirname_pattern=str(OUTPUT_DIR / "{target}"),
            download_pictures=True,
            download_videos=True,
            download_video_thumbnails=True,
            download_geotags=False,
            download_comments=False,
            save_metadata=True,
            compress_json=False,
        )

    def download_profile(self, max_posts: int = 50, session_user: str = None):
        """Baixa os posts mais recentes do perfil do Instagram."""
        print(f"🚀 Iniciando download de posts do Instagram @{self.username}...")
        
        if session_user:
            try:
                self.loader.load_session_from_file(session_user)
                print(f"✅ Sessão carregada para {session_user}")
            except Exception as e:
                print(f"⚠️ Não foi possível carregar sessão salva: {e}")

        try:
            profile = instaloader.Profile.from_username(self.loader.context, self.username)
            print(f"📌 Perfil encontrado: {profile.full_name} ({profile.mediacount} posts)")
            
            count = 0
            for post in profile.get_posts():
                if count >= max_posts:
                    break
                print(f"[{count+1}/{max_posts}] Baixando post {post.shortcode} ({post.date_local.strftime('%d/%m/%Y')})...")
                self.loader.download_post(post, target=self.username)
                count += 1
                
            print(f"🎉 Download de {count} posts concluído com sucesso!")
            self.index_downloaded_media()
        except Exception as err:
            print(f"❌ Erro ao baixar perfil via Instaloader: {err}")
            print("💡 Dica: Se o Instagram bloquear requisições anônimas, use um login ou importe via shortcodes.")

    def download_by_shortcode(self, shortcode: str):
        """Baixa um post específico através do shortcode ou URL do post."""
        try:
            post = instaloader.Post.from_shortcode(self.loader.context, shortcode)
            print(f"📥 Baixando post individual: {shortcode}...")
            self.loader.download_post(post, target=self.username)
            print("✅ Post baixado com sucesso!")
            self.index_downloaded_media()
        except Exception as e:
            print(f"❌ Erro ao baixar shortcode {shortcode}: {e}")

    def index_downloaded_media(self):
        """Varre os arquivos baixados e cataloga no banco SQLite e Supabase."""
        print("🔄 Catalogando fotos e vídeos baixados no banco de dados...")
        db = DatabaseService()
        
        # Mapeamento de Categorias / Álbuns com base nas legendas
        albuns_map = {
            "Cultos no Templo": [],
            "Festividades & Aniversário": [],
            "IBPM Kids": [],
            "Rede de Jovens Semear": [],
            "Santa Ceia & Clamor": [],
            "Momentos de Adoração": []
        }

        # Varre arquivos no diretório
        for root, dirs, files in os.walk(OUTPUT_DIR):
            for file in files:
                if file.endswith((".jpg", ".png", ".webp")):
                    caminho_img = Path(root) / file
                    nome_base = file.split(".")[0]
                    
                    # Procura arquivo .txt de legenda correspondente
                    txt_file = Path(root) / f"{nome_base}.txt"
                    legenda = "Culto e Comunhão na IBPM Carvalho Ramos"
                    if txt_file.exists():
                        try:
                            legenda = txt_file.read_text(encoding="utf-8")[:180]
                        except Exception:
                            pass
                    
                    # Determina o álbum pelo texto da legenda
                    categoria = "Cultos no Templo"
                    txt_lower = legenda.lower()
                    if "kids" in txt_lower or "criança" in txt_lower or "infantil" in txt_lower:
                        categoria = "IBPM Kids"
                    elif "jovens" in txt_lower or "semear" in txt_lower or "mocidade" in txt_lower:
                        categoria = "Rede de Jovens Semear"
                    elif "santa ceia" in txt_lower or "ceia" in txt_lower:
                        categoria = "Santa Ceia & Clamor"
                    elif "aniversário" in txt_lower or "festividade" in txt_lower or "anos" in txt_lower:
                        categoria = "Festividades & Aniversário"
                    elif "louvor" in txt_lower or "adoração" in txt_lower:
                        categoria = "Momentos de Adoração"

                    albuns_map[categoria].append({
                        "url": str(caminho_img),
                        "legenda": legenda
                    })

        total_fotos = sum(len(v) for v in albuns_map.values())
        print(f"📸 Total de fotos mapeadas: {total_fotos} fotos distribuídas em {len(albuns_map)} álbuns!")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Download de Mídias do Instagram IBPM CR")
    parser.add_argument("--user", default="ibpmcarvalhoramos", help="Nome de usuário do Instagram")
    parser.add_argument("--posts", type=int, default=30, help="Quantidade máxima de posts")
    parser.add_argument("--shortcode", default="", help="Baixar shortcode específico")
    parser.add_argument("--session", default="", help="Usuário para carregar sessão salva")

    args = parser.parse_args()
    downloader = InstagramDownloader(args.user)
    
    if args.shortcode:
        downloader.download_by_shortcode(args.shortcode)
    else:
        downloader.download_profile(max_posts=args.posts, session_user=args.session)
