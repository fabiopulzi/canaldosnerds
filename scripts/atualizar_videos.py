#!/usr/bin/env python3
"""Atualiza videos.json com os vídeos mais recentes do canal no YouTube.

Lê o feed RSS público do canal (não precisa de chave de API) e guarda só os
vídeos normais (os Shorts ficam de fora, porque a miniatura vertical não
combina com o carrossel). Roda sozinho pelo GitHub Actions
(.github/workflows/videos.yml), mas também pode ser rodado à mão:

    python3 scripts/atualizar_videos.py
"""
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

CANAL_ID = "UCDJ9oeYZRi0BFsfohrv_a1w"  # @eduardotirapani
MAX_VIDEOS = 12
SAIDA = Path(__file__).resolve().parent.parent / "videos.json"

NS = {
    "a": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
}


def main() -> int:
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={CANAL_ID}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (atualizar-videos)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        raiz = ET.fromstring(r.read())

    videos = []
    for e in raiz.findall("a:entry", NS):
        link = e.find("a:link", NS).get("href", "")
        if "/shorts/" in link:
            continue
        videos.append({
            "id": e.find("yt:videoId", NS).text,
            "titulo": e.find("a:title", NS).text,
            "data": e.find("a:published", NS).text[:10],
        })
        if len(videos) >= MAX_VIDEOS:
            break

    if not videos:
        print("Nenhum vídeo encontrado no feed; videos.json não foi alterado.", file=sys.stderr)
        return 1

    SAIDA.write_text(json.dumps(videos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(videos)} vídeos gravados em {SAIDA.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
