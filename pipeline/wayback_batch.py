"""Batch reanudable de archivado en Wayback Machine.

Paso SEPARADO del scraping (no inline): la Save API anónima limita a pocas
requests por minuto, archivar 100-200 URLs lleva horas y falla intermitente
(hallazgo del design doc). Cola persistida en disco, retry en 429, back-fill
de archived_url en las piezas ya aprobadas.

TODO antes de correr en volumen: registrar cuenta gratuita en archive.org y
setear WAYBACK_ACCESS_KEY / WAYBACK_SECRET_KEY (sube mucho el límite de
cuota vs. anónimo).
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import requests

QUEUE_FILE = Path(__file__).parent / "wayback_queue.jsonl"
SAVE_ENDPOINT = "https://web.archive.org/save/"
CHECK_ENDPOINT = "https://archive.org/wayback/available"


def enqueue(url: str) -> None:
    with QUEUE_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"url": url, "status": "pending", "attempts": 0}) + "\n")


def _load_queue() -> list[dict]:
    if not QUEUE_FILE.exists():
        return []
    return [json.loads(line) for line in QUEUE_FILE.read_text(encoding="utf-8").splitlines() if line.strip()]


def _save_queue(items: list[dict]) -> None:
    with QUEUE_FILE.open("w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item) + "\n")


def check_existing_snapshot(url: str) -> str | None:
    """Mide cobertura de Wayback para una fuente ya muerta (hallazgo T4:
    validar la asunción de que las fuentes muertas tienen copia)."""
    resp = requests.get(CHECK_ENDPOINT, params={"url": url}, timeout=15)
    resp.raise_for_status()
    snapshots = resp.json().get("archived_snapshots", {})
    closest = snapshots.get("closest")
    return closest["url"] if closest and closest.get("available") else None


def run_batch(max_per_run: int = 20) -> None:
    """Procesa hasta max_per_run items pendientes de la cola. Reanudable:
    se puede cortar y volver a correr sin perder progreso ni duplicar."""
    items = _load_queue()
    processed = 0
    for item in items:
        if processed >= max_per_run or item["status"] == "done":
            continue
        try:
            resp = requests.get(SAVE_ENDPOINT + item["url"], timeout=30)
            if resp.status_code == 429:
                item["attempts"] += 1
                item["status"] = "retry"
                time.sleep(5)
                continue
            resp.raise_for_status()
            item["status"] = "done"
            item["archived_url"] = resp.url
            processed += 1
        except requests.RequestException as exc:
            item["attempts"] += 1
            item["status"] = "error"
            item["last_error"] = str(exc)
    _save_queue(items)
    done = sum(1 for i in items if i["status"] == "done")
    print(f"Wayback batch: {done}/{len(items)} completados esta corrida: {processed}")
