import urllib.request
import re

url = "https://www.youtube.com/@ibpmcr7976/videos"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
        video_ids = list(dict.fromkeys(re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', html)))
        titles = re.findall(r'"title":\{"runs":\[\{"text":"([^"]+)"', html)
        print(f"Total video_ids encontrados: {len(video_ids)}")
        for i, vid in enumerate(video_ids[:15]):
            title = titles[i] if i < len(titles) else "Culto Ao Vivo IBPM CR"
            print(f"{i+1}. {title}")
            print(f"   Thumb: https://img.youtube.com/vi/{vid}/maxresdefault.jpg")
except Exception as e:
    print("Erro:", e)
