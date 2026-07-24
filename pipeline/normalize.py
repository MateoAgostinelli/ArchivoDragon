"""HTML scrapeado -> Markdown sanitizado.

Este es el único paso de normalización que necesita el pipeline de todos
modos (el sitio guarda Markdown, no HTML) — y como efecto colateral gratis
elimina scripts y HTML activo (defensa XSS, hallazgo 3A del eng review:
"no es complejidad extra, es el mismo paso con nombre de seguridad").
El sitio JAMÁS debe recibir HTML crudo scrapeado.
"""
from __future__ import annotations

import chardet
from bs4 import BeautifulSoup
from markdownify import markdownify as html_to_markdown

# Tags que nunca deben sobrevivir a la conversión, ni siquiera como texto.
_DANGEROUS_TAGS = ["script", "style", "iframe", "object", "embed", "form"]


def decode_bytes(raw: bytes) -> str:
    """Decodifica bytes de un blog viejo con fallback de encoding (hallazgo 2A)."""
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        detected = chardet.detect(raw)
        encoding = detected.get("encoding") or "latin-1"
        return raw.decode(encoding, errors="replace")


def sanitize_html(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, "html.parser")
    for tag_name in _DANGEROUS_TAGS:
        for tag in soup.find_all(tag_name):
            tag.decompose()
    # Elimina atributos de evento (onclick, onerror, etc.) que sobrevivirían
    # como texto plano si no se limpian antes de la conversión a Markdown.
    for tag in soup.find_all(True):
        for attr in list(tag.attrs):
            if attr.startswith("on"):
                del tag.attrs[attr]
    return str(soup)


def html_to_clean_markdown(raw_html: str) -> str:
    """Punto de entrada del pipeline: HTML sucio -> Markdown seguro."""
    clean_html = sanitize_html(raw_html)
    return html_to_markdown(clean_html, heading_style="ATX").strip()
