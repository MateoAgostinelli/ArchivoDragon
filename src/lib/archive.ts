import { getCollection, type CollectionEntry, type CollectionKey } from "astro:content";
import { PIECE_TYPES, type PieceType } from "./views";

export { PIECE_TYPES, RICH_VIEWS_THRESHOLD, sortByDate, decadeOf, exactDatedOnly, closestPieceToToday } from "./views";
export type { PieceType } from "./views";

export type AnyPiece = CollectionEntry<PieceType>;

export async function getAllPieces(): Promise<AnyPiece[]> {
  const collections = await Promise.all(
    PIECE_TYPES.map((type) => getCollection(type as CollectionKey))
  );
  return collections.flat() as AnyPiece[];
}

export async function richViewsUnlocked(): Promise<boolean> {
  const { RICH_VIEWS_THRESHOLD } = await import("./views");
  const pieces = await getAllPieces();
  return pieces.length >= RICH_VIEWS_THRESHOLD;
}
