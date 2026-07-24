// Lógica pura de las vistas derivadas — sin dependencia de astro:content, así
// se testea con vitest normal (sin el runtime de Astro). archive.ts la usa
// con datos reales de las colecciones.

export const PIECE_TYPES = ["noticias", "canciones", "historias", "fotos", "partidos"] as const;
export type PieceType = (typeof PIECE_TYPES)[number];

// Lanzamiento híbrido (decisión T1): el sitio publica desde el día 1 con
// listado+detalle+búsqueda; las vistas dependientes de contenido (tal-día,
// máquina del tiempo) quedan ocultas hasta este umbral de piezas curadas.
// NOTA: hoy es un gate a nivel de página (oculta el link de navegación), no
// una exclusión de build — Pagefind seguirá indexando esas rutas si existen.
// Riesgo aceptado sin corregir en /plan-eng-review 2026-07-24 (hallazgo 13A).
export const RICH_VIEWS_THRESHOLD = 100;

export interface MinimalPiece {
  id: string;
  collection: string;
  data: {
    date: string;
    date_precision: "exact" | "year" | "decade";
  };
}

export function sortByDate<T extends MinimalPiece>(pieces: T[]): T[] {
  return [...pieces].sort((a, b) => a.data.date.localeCompare(b.data.date));
}

export function decadeOf(dateStr: string): number {
  const year = Number(dateStr.slice(0, 4));
  return Math.floor(year / 10) * 10;
}

// Solo piezas con fecha exacta entran a tal-día / máquina del tiempo — evita
// que una pieza "c. 1935" (forzada a 1935-01-01) aparezca cada 1 de enero
// como si fuera un evento real de ese día (hallazgo 6A del eng review).
export function exactDatedOnly<T extends MinimalPiece>(pieces: T[]): T[] {
  return pieces.filter((p) => p.data.date_precision === "exact");
}

// Fallback de "tal día como hoy": si no hay piezas exactas para la fecha de
// hoy, devuelve la pieza exacta más cercana en vez de una página vacía.
//
// Usa SIEMPRE componentes UTC: las fechas de las piezas son "YYYY-MM-DD" sin
// hora, que `new Date(...)` parsea como medianoche UTC. Compararlas con
// getMonth()/getDate() (hora LOCAL) corre el día en cualquier timezone
// negativo — en Argentina (UTC-3), medianoche UTC del 24 todavía es 23 a la
// noche hora local. Mismo tipo de bug que el timezone del cron (hallazgo 13A).
export function closestPieceToToday<T extends MinimalPiece>(pieces: T[], today = new Date()): T | null {
  const exact = exactDatedOnly(pieces);
  if (exact.length === 0) return null;
  const todayMD = `${String(today.getUTCMonth() + 1).padStart(2, "0")}-${String(today.getUTCDate()).padStart(2, "0")}`;
  const sameDay = exact.find((p) => p.data.date.slice(5) === todayMD);
  if (sameDay) return sameDay;
  const target = Date.UTC(today.getUTCFullYear(), today.getUTCMonth(), today.getUTCDate());
  return exact.reduce((closest, p) => {
    const pTime = new Date(p.data.date + "T00:00:00Z").getTime();
    const closestTime = new Date(closest.data.date + "T00:00:00Z").getTime();
    return Math.abs(pTime - target) < Math.abs(closestTime - target) ? p : closest;
  }, exact[0]);
}
