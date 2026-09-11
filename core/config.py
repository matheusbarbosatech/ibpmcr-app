"""
Configurações Globais do Super-App IBPM CR.
Carrega variáveis de ambiente e define URLs e credenciais padrão.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Garante a carga do arquivo .env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# Cloudflare R2
R2_PUBLIC_URL = os.getenv("R2_PUBLIC_URL", "https://midia.ibpmcr.com.br")

# DevWorld AI (Claude Sonnet 5)
DEVWORLD_API_KEY = os.getenv("DEVWORLD_API_KEY", "dw_live_UgEYtrkRzOvCU-BV-IR8TvAzKBdsHoEnIROAq0OthLU")
DEVWORLD_BASE_URL = os.getenv("DEVWORLD_BASE_URL", "https://chat.devwservices.shop/v1")
DEVWORLD_MODEL = os.getenv("DEVWORLD_MODEL", "claude-sonnet-5[1m]")

# Canais Oficiais
YOUTUBE_LIVE_URL = os.getenv("YOUTUBE_LIVE_URL", "https://www.youtube.com/@ibpmcr7976/live")
YOUTUBE_CHANNEL_URL = os.getenv("YOUTUBE_CHANNEL_URL", "https://www.youtube.com/@ibpmcr7976")
CHAVE_PIX = os.getenv("CHAVE_PIX", "pix@ibpmcr.com.br")

# Caminhos Locais
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "ibpmcr_local.db"
