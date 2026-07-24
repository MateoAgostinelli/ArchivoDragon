"""Escritura de piezas a cuarentena + reporte de descartes.

Cero fallas silenciosas (hallazgo 2A): todo lo que el scraper no pudo
procesar se registra en skipped.jsonl con motivo — nunca se pierde en
silencio ni se publica basura. Las piezas válidas van a cuarentena (no
directo a src/content/) para pasar por curate.py antes de commitear
(hallazgo 12A / TODO-2).
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

QUARANTINE_DIR = Path(__file__).parent / "quarantine"
SKIPPED_LOG = Path(__file__).parent / "skipped.jsonl"


def write_draft(collection: str, piece_id: str, frontmatter: dict, body: str) -> Path:
    QUARANTINE_DIR.mkdir(exist_ok=True)
    lines = ["---"]
    for key, value in frontmatter.items():
        if value is None:
            continue
        if isinstance(value, list):
            items = ", ".join(f'"{v}"' for v in value)
            lines.append(f"{key}: [{items}]")
        else:
            lines.append(f'{key}: "{value}"' if isinstance(value, str) else f"{key}: {value}")
    lines.append("---")
    lines.append("")
    lines.append(body)

    path = QUARANTINE_DIR / collection / f"{piece_id}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def log_skipped(source_url: str, reason: str) -> None:
    entry = {
        "url": source_url,
        "reason": reason,
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    with SKIPPED_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def print_run_summary(processed: int, skipped: int) -> None:
    print(f"Procesó {processed}, descartó {skipped}" + (f" — ver {SKIPPED_LOG}" if skipped else ""))
