"""CLI de curaduría: revisa la cuarentena pieza por pieza.

Aprobar (a) mueve el archivo a src/content/{tipo}/. Editar (e) abre el
archivo en el editor por defecto para ajustar fecha/texto antes de aprobar.
Descartar (d) borra el borrador y lo registra como descarte manual.

Este es el TODO-2 (P1): el cuello de botella real del proyecto es la
curaduría humana, no los scrapers — esta herramienta ataca eso directo
(hallazgo 12A del eng review).

Uso: python pipeline/curate.py
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

QUARANTINE_DIR = Path(__file__).parent / "quarantine"
CONTENT_DIR = Path(__file__).parent.parent / "src" / "content"


def iter_drafts() -> list[Path]:
    if not QUARANTINE_DIR.exists():
        return []
    return sorted(QUARANTINE_DIR.rglob("*.md"))


def show(path: Path) -> None:
    print("\n" + "=" * 70)
    print(f"{path.relative_to(QUARANTINE_DIR)}")
    print("=" * 70)
    print(path.read_text(encoding="utf-8"))


def approve(path: Path) -> None:
    collection = path.parent.name
    dest = CONTENT_DIR / collection / path.name
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(path), str(dest))
    print(f"✓ Aprobada -> {dest}")


def edit(path: Path) -> None:
    editor = os.environ.get("EDITOR", "notepad" if os.name == "nt" else "vi")
    subprocess.run([editor, str(path)])


def discard(path: Path) -> None:
    path.unlink()
    print(f"✗ Descartada: {path.name}")


def main() -> None:
    drafts = iter_drafts()
    if not drafts:
        print("Cuarentena vacía. Corré el scraper primero.")
        return

    print(f"{len(drafts)} piezas en cuarentena.\n")
    i = 0
    while i < len(drafts):
        path = drafts[i]
        if not path.exists():
            i += 1
            continue
        show(path)
        choice = input("\n[a]probar / [e]ditar / [d]escartar / [s]altear / [q]salir: ").strip().lower()
        if choice == "a":
            approve(path)
            i += 1
        elif choice == "e":
            edit(path)
            # No avanza: vuelve a mostrar la pieza editada para decidir.
        elif choice == "d":
            discard(path)
            i += 1
        elif choice == "s":
            i += 1
        elif choice == "q":
            break
        else:
            print("Opción inválida.")

    print(f"\nQuedan {len(iter_drafts())} piezas en cuarentena.")


if __name__ == "__main__":
    sys.exit(main())
