"""Identidad estable (para no duplicar al re-correr el scraper) + flag de
similitud (para detectar la misma nota republicada en blogs distintos).

Dedup por id evita re-scrapear la MISMA url. El flag de similitud es lo
barato que cubre el problema real: título+fecha parecidos entre piezas
NUEVAS y EXISTENTES se marcan "posible duplicado de X" para que el curador
decida — nunca se fusiona ni se descarta solo (hallazgo 8A).
"""
from __future__ import annotations

import hashlib
import re
import unicodedata


def stable_id(source_url: str | None, title: str, date: str) -> str:
    """Slug estable: hash(source.url) si existe, si no hash(title+date).

    El slug legible se deriva de la MISMA base que el hash (url o title+date)
    — no del título por separado — para que dos entradas con la misma url
    pero distinto título de todos modos produzcan el mismo id (el punto del
    dedup por url)."""
    basis = source_url if source_url else f"{title}|{date}"
    digest = hashlib.sha1(basis.encode("utf-8")).hexdigest()[:12]
    slug_source = source_url.rsplit("/", 1)[-1] if source_url else title
    return f"{_slugify(slug_source)}-{digest}"


def _slugify(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", normalized).strip("-").lower()
    return normalized[:50] or "pieza"


def _normalize_for_compare(title: str) -> str:
    normalized = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9\s]", "", normalized.lower()).strip()


def possible_duplicate(new_title: str, new_date: str, existing: list[tuple[str, str, str]]) -> str | None:
    """existing: lista de (id, title, date) ya cargados. Devuelve el id del
    candidato más parecido si título normalizado coincide y la fecha es igual
    o está a menos de 3 días — o None si no hay sospecha."""
    new_norm = _normalize_for_compare(new_title)
    for existing_id, existing_title, existing_date in existing:
        if _normalize_for_compare(existing_title) == new_norm and existing_date == new_date:
            return existing_id
    return None
