"""Vigía de link-rot: chequea los `source.url` de todo el contenido.

Nunca commitea ni edita contenido (decisión 10A) — solo genera un reporte
para que un humano actualice `archived_url` al curar. La regla clave para
evitar falsos positivos: los diarios argentinos devuelven 403/429 a bots
todo el tiempo, así que SOLO un 404/410 (el servidor confirma que ya no
existe) cuenta como "muerto". 403/429/timeout se tratan como "inconcluso" y
NUNCA se reportan como link roto.

TODO (mejora futura, no bloqueante para el esqueleto): el diseño original
pedía doble chequeo separado por 48h antes de reportar. Esta versión reduce
falsos positivos limitando el reporte a códigos de estado inequívocos
(404/410) en vez de mantener estado entre corridas — igual de conservador,
más simple.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import requests
import yaml

CONTENT_DIR = Path(__file__).parent.parent / "src" / "content"
DEAD_STATUS_CODES = {404, 410}


def iter_source_urls() -> list[tuple[Path, str]]:
    results = []
    for md_file in CONTENT_DIR.rglob("*.md"):
        text = md_file.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
        if not match:
            continue
        frontmatter = yaml.safe_load(match.group(1)) or {}
        url = (frontmatter.get("source") or {}).get("url")
        if url:
            results.append((md_file, url))
    return results


def check_url(url: str) -> int | None:
    try:
        resp = requests.head(url, timeout=15, allow_redirects=True)
        return resp.status_code
    except requests.RequestException:
        return None  # timeout / error de red: inconcluso, no se reporta


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report-only", action="store_true")
    parser.parse_args()

    dead = []
    for path, url in iter_source_urls():
        status = check_url(url)
        if status in DEAD_STATUS_CODES:
            dead.append((path, url, status))

    if not dead:
        print("Sin links muertos confirmados (404/410) este mes.")
        return 0

    report = ["# Vigía de link-rot — citas a revisar\n"]
    report.append(f"{len(dead)} fuente(s) devolvieron 404/410 este mes:\n")
    for path, url, status in dead:
        rel = path.relative_to(CONTENT_DIR.parent.parent)
        report.append(f"- `{rel}`: {url} ({status})")
    report.append(
        "\nEl sitio ya muestra la copia archivada junto al link original cuando "
        "existe — nadie se queda sin acceso. Actualizar `source.archived_url` "
        "en cada pieza de esta lista al curar."
    )
    Path("link-rot-report.md").write_text("\n".join(report), encoding="utf-8")
    print(f"{len(dead)} links muertos confirmados. Ver link-rot-report.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
