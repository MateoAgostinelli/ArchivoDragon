"""Plantilla para un scraper de una fuente específica (ej. un blogspot viejo).

No hay UN scraper genérico que sirva para todos los blogs — cada uno tiene su
propio layout, HTML roto y formato de fecha (design doc + hallazgo del eng
review). Copiar este archivo como `scrapers/nombre_del_blog.py` y ajustar
`extract_posts` a la estructura real del sitio.

Uso: python -m pipeline.scrapers.nombre_del_blog
"""
from __future__ import annotations

import requests
from bs4 import BeautifulSoup

from pipeline.dates import parse_spanish_date
from pipeline.dedupe import stable_id
from pipeline.normalize import decode_bytes, html_to_clean_markdown
from pipeline.quarantine import log_skipped, print_run_summary, write_draft

# TODO: reemplazar por la URL del índice/archivo del blog real.
SOURCE_NAME = "Nombre del blog (a completar)"
INDEX_URL = "https://ejemplo.blogspot.com/"
COLLECTION = "historias"  # noticias | canciones | historias | fotos | partidos


def extract_posts(index_html: str) -> list[dict]:
    """Devuelve una lista de {url, title, date_text, body_html} por post.
    AJUSTAR a la estructura real del blog objetivo."""
    soup = BeautifulSoup(index_html, "html.parser")
    posts = []
    for entry in soup.select(".post"):  # selector de ejemplo
        title_el = entry.select_one(".post-title")
        date_el = entry.select_one(".date-header")
        body_el = entry.select_one(".post-body")
        if not (title_el and body_el):
            continue
        posts.append({
            "url": title_el.find("a")["href"] if title_el.find("a") else INDEX_URL,
            "title": title_el.get_text(strip=True),
            "date_text": date_el.get_text(strip=True) if date_el else "",
            "body_html": str(body_el),
        })
    return posts


def run() -> None:
    resp = requests.get(INDEX_URL, timeout=30)
    html = decode_bytes(resp.content)
    posts = extract_posts(html)

    processed, skipped = 0, 0
    for post in posts:
        parsed_date = parse_spanish_date(post["date_text"])
        if parsed_date is None:
            log_skipped(post["url"], "no se pudo parsear la fecha")
            skipped += 1
            continue

        body_md = html_to_clean_markdown(post["body_html"])
        piece_id = stable_id(post["url"], post["title"], parsed_date.date)

        write_draft(
            COLLECTION,
            piece_id,
            {
                "id": piece_id,
                "title": post["title"],
                "date": parsed_date.date,
                "date_precision": parsed_date.date_precision,
                "date_display": parsed_date.date_display,
                "source": {"name": SOURCE_NAME, "url": post["url"], "archived_url": "pending"},
                "tags": [],
            },
            body_md,
        )
        processed += 1

    print_run_summary(processed, skipped)


if __name__ == "__main__":
    run()
