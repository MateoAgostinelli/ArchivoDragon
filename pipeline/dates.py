"""Parser de fechas en prosa castellana, como aparecen en blogs viejos.

Devuelve (date, date_precision, date_display):
  - date: SIEMPRE YYYY-MM-DD, sortable (fechas aproximadas se normalizan a
    YYYY-01-01 o YYYY-MM-01 — nunca se inventa un día real).
  - date_precision: "exact" | "year" | "decade"
  - date_display: string legible cuando la precisión no es exacta (None si exact)

IMPORTANTE (hallazgo 6A del eng review): solo las piezas "exact" entran a
tal-día-como-hoy y a la máquina del tiempo. No relajar ese filtro.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

MESES = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
    "julio": 7, "agosto": 8, "septiembre": 9, "setiembre": 9, "octubre": 10,
    "noviembre": 11, "diciembre": 12,
}

_EXACT_ISO = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")
_EXACT_PROSE = re.compile(
    r"(\d{1,2})\s+de\s+(" + "|".join(MESES) + r")\s+de\s+(\d{4})", re.IGNORECASE
)
_DECADE_PROSE = re.compile(r"(?:c\.?\s*)?a[ñn]os?\s+(\d{2,4})", re.IGNORECASE)
_YEAR_ONLY = re.compile(r"\b(1[89]\d{2}|20\d{2})\b")


@dataclass
class ParsedDate:
    date: str
    date_precision: str  # exact | year | decade
    date_display: str | None


def parse_spanish_date(text: str) -> ParsedDate | None:
    """Intenta parsear una fecha en texto castellano. None si no encuentra nada."""
    text = text.strip()

    m = _EXACT_ISO.match(text)
    if m:
        return ParsedDate(text, "exact", None)

    m = _EXACT_PROSE.search(text)
    if m:
        day, month_name, year = m.groups()
        month = MESES[month_name.lower()]
        return ParsedDate(f"{int(year):04d}-{month:02d}-{int(day):02d}", "exact", None)

    m = _DECADE_PROSE.search(text)
    if m:
        raw = m.group(1)
        decade_year = int(raw) if len(raw) == 4 else 1900 + int(raw)
        decade = (decade_year // 10) * 10
        return ParsedDate(f"{decade}-01-01", "decade", f"c. años {decade % 100}")

    m = _YEAR_ONLY.search(text)
    if m:
        year = int(m.group(1))
        return ParsedDate(f"{year:04d}-01-01", "year", str(year))

    return None
