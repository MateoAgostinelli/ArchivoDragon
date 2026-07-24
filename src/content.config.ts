import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

// Fuente citada: name es lo único siempre obligatorio. url es obligatorio si la
// fuente es online. archived_url acepta "pending" mientras corre el batch de
// Wayback (ver pipeline/wayback_batch.py); una fuente impresa sin url documenta
// el motivo en el cuerpo de la pieza.
const sourceSchema = z
  .object({
    name: z.string().min(1),
    url: z.string().url().optional(),
    archived_url: z.union([z.string().url(), z.literal("pending")]).optional(),
  })
  .refine((s) => !s.archived_url || s.archived_url === "pending" || s.url, {
    message: "archived_url requiere url",
  });

// date = fecha del EVENTO histórico (ordena timeline, tal-día, máquina del
// tiempo). published_date = cuándo se publicó la fuente, si es relevante y
// distinta. date_precision limita qué vistas pueden usar la fecha: solo
// "exact" entra a tal-día y máquina del tiempo (ver docs/designs/archivodragon.md,
// hallazgos 5A/6A del eng review — evita fechar piezas aproximadas como si
// fueran del día exacto, ej. "c. 1935" -> 1935-01-01 inundando cada 1 de enero).
const baseSchema = z.object({
  id: z.string().min(1), // slug estable: hash(source.url) o hash(title+date). El pipeline lo usa para dedup.
  title: z.string().min(1),
  date: z.string().date(), // YYYY-MM-DD, siempre presente y ordenable
  date_precision: z.enum(["exact", "year", "decade"]).default("exact"),
  date_display: z.string().optional(), // ej. "c. años 80" — lo que ve el usuario cuando la precisión no es exacta
  published_date: z.string().date().optional(),
  source: sourceSchema,
  tags: z.array(z.string()).default([]),
  possible_duplicate_of: z.string().optional(), // id de otra pieza — flag de curaduría (similitud título+fecha), nunca automático
});

const noticias = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/noticias" }),
  schema: baseSchema,
});

const canciones = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/canciones" }),
  schema: baseSchema.extend({
    youtube_url: z.string().url().optional(), // embed del cancionero; Wayback no preserva audio reproducible
  }),
});

const historias = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/historias" }),
  schema: baseSchema,
});

const fotos = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/fotos" }),
  schema: baseSchema.extend({
    image_url: z.string().url().optional(), // etapa 1: solo link + archived_url, sin copia local (ver TODOS.md)
  }),
});

// Schema v2 de partido diseñado ahora, implementado después (T5): la vista
// máquina del tiempo lo necesita completo, pero cargar partidos con estos
// campos desde el día 1 evita re-tocar piezas ya curadas.
const partidos = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/partidos" }),
  schema: baseSchema.extend({
    rival: z.string().optional(),
    resultado: z.string().optional(), // ej. "2-1"
    torneo: z.string().optional(),
    formacion: z.array(z.string()).optional(),
  }),
});

export const collections = { noticias, canciones, historias, fotos, partidos };
