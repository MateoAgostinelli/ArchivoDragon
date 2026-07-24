import { describe, it, expect } from "vitest";
import { RICH_VIEWS_THRESHOLD, decadeOf, exactDatedOnly, closestPieceToToday, type MinimalPiece } from "./views";

function piece(overrides: Partial<MinimalPiece["data"]> & { collection?: string; id?: string }): MinimalPiece {
  const { collection = "noticias", id = "test", ...data } = overrides;
  return {
    id,
    collection,
    data: {
      date: "2000-01-01",
      date_precision: "exact",
      ...data,
    },
  };
}

describe("decadeOf", () => {
  it("redondea el año a la década", () => {
    expect(decadeOf("1994-06-14")).toBe(1990);
    expect(decadeOf("1980-01-01")).toBe(1980);
    expect(decadeOf("2001-03-01")).toBe(2000);
  });
});

describe("exactDatedOnly", () => {
  it("filtra piezas aproximadas (evita el bug del 1 de enero)", () => {
    const pieces = [
      piece({ id: "a", date: "1994-06-14", date_precision: "exact" }),
      piece({ id: "b", date: "1980-01-01", date_precision: "decade" }),
      piece({ id: "c", date: "1935-01-01", date_precision: "year" }),
    ];
    const result = exactDatedOnly(pieces);
    expect(result.map((p) => p.id)).toEqual(["a"]);
  });
});

describe("closestPieceToToday", () => {
  it("devuelve la pieza del mismo día si existe", () => {
    const today = new Date("2026-07-24");
    const pieces = [
      piece({ id: "match", date: "1994-07-24", date_precision: "exact" }),
      piece({ id: "other", date: "2000-01-01", date_precision: "exact" }),
    ];
    expect(closestPieceToToday(pieces, today)?.id).toBe("match");
  });

  it("hace fallback a la pieza exacta más cercana si no hay ninguna de hoy", () => {
    const today = new Date("2026-07-24");
    const pieces = [
      piece({ id: "lejos", date: "1990-01-01", date_precision: "exact" }),
      piece({ id: "cerca", date: "2026-07-20", date_precision: "exact" }),
    ];
    expect(closestPieceToToday(pieces, today)?.id).toBe("cerca");
  });

  it("ignora piezas aproximadas para el fallback (nunca miente la fecha)", () => {
    const today = new Date("2026-01-01");
    const pieces = [piece({ id: "aprox", date: "2026-01-01", date_precision: "decade" })];
    expect(closestPieceToToday(pieces, today)).toBeNull();
  });

  it("devuelve null si no hay piezas exactas", () => {
    expect(closestPieceToToday([])).toBeNull();
  });
});

describe("RICH_VIEWS_THRESHOLD gating", () => {
  it("el umbral está fijado en 100 (decisión T1)", () => {
    expect(RICH_VIEWS_THRESHOLD).toBe(100);
  });
});
