"""
Módulo de Integração e Upload Oficial para Cloudflare R2 (S3 API).
Sincroniza os 576 cortes verticais (9:16) e capas HD para o bucket 'ibpmcr-midia'.
"""
import os
import sys
from pathlib import Path
import mimetypes
from dotenv import load_dotenv

# Carrega .env do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

R2_ENDPOINT = os.getenv("R2_ENDPOINT_URL", "")
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY_ID", "")
R2_SECRET_KEY = os.getenv("R2_SECRET_ACCESS_KEY", "")
R2_BUCKET = os.getenv("R2_BUCKET_NAME", "ibpmcr-midia")
R2_PUBLIC_URL = os.getenv("R2_PUBLIC_URL", "https://midia.ibpmcr.com.br")

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

def test_connection():
    """Testa a conexão e lista os objetos atuais do bucket."""
    print("Conectando ao Cloudflare R2...")
    s3 = get_s3_client()
    try:
        response = s3.list_objects_v2(Bucket=R2_BUCKET, MaxKeys=5)
        print(f"[OK] Conexão bem-sucedida ao bucket '{R2_BUCKET}'!")
        key_count = response.get("KeyCount", 0)
        print(f"Objetos no bucket atualmente: {key_count}")
        return True
    except Exception as e:
        print(f"[ERRO] Falha ao conectar ao R2: {e}")
        return False

def upload_file(local_path: Path, remote_key: str):
    """Envia um arquivo local para o Cloudflare R2 com content-type adequado."""
    s3 = get_s3_client()
    content_type, _ = mimetypes.guess_type(str(local_path))
    content_type = content_type or "application/octet-stream"

    extra_args = {"ContentType": content_type}

    s3.upload_file(
        Filename=str(local_path),
        Bucket=R2_BUCKET,
        Key=remote_key,
        ExtraArgs=extra_args
    )
    return f"{R2_PUBLIC_URL.rstrip('/')}/{remote_key}"

if __name__ == "__main__":
    test_connection()
