# ArchivoDragón

Archivo histórico digital de Club Atlético Defensores de Belgrano — noticias,
cancionero, historias, fotos y partidos, con fuente citada siempre.

Plan completo, decisiones y por qué de cada cosa: [`docs/designs/archivodragon.md`](docs/designs/archivodragon.md).
Trabajo pendiente: [`TODOS.md`](TODOS.md).

## Estructura

```
src/
  content.config.ts   # schema de cada tipo de pieza (noticias/canciones/partidos/historias/fotos)
  content/             # las piezas en sí (Markdown + frontmatter)
  lib/views.ts         # lógica pura de vistas derivadas (gating, fallback tal-día) — testeada con vitest
  lib/archive.ts        # helpers que sí tocan astro:content
  pages/                # inicio, listados, detalle, tal-día, máquina del tiempo
pipeline/
  dates.py              # parser de fechas en prosa castellana
  normalize.py          # HTML scrapeado -> Markdown sanitizado (defensa XSS)
  dedupe.py             # id estable + flag de posible duplicado
  quarantine.py          # escritura a cuarentena + skipped.jsonl
  curate.py              # CLI de curaduría (aprobar/editar/descartar) — el paso que más importa
  wayback_batch.py       # cola reanudable de archivado en Wayback Machine
  check_link_rot.py      # vigía mensual de citas muertas (solo reporta, nunca commitea)
  scrapers/_template.py  # copiar por cada fuente nueva a scrapear
  tests/                 # pytest
.github/workflows/
  ci.yml                # tests + build en cada push/PR
  deploy.yml             # build + deploy a GitHub Pages
  daily-rebuild.yml      # cron diario para "tal día como hoy" + keep-alive mensual
  link-rot.yml            # dispara check_link_rot.py una vez por mes
```

## Cómo arrancar (el primer paso real)

Antes de tocar el scraper: archivar 20 piezas A MANO del blog más rico que
encuentres, para validar el schema con contenido real. Ver "The Assignment"
en el design doc.

## Comandos

```sh
npm install                          # dependencias del sitio
npm run dev                          # servidor local
npm run build                        # build de producción (valida el schema de todo el contenido)
npm run test                         # tests de las vistas derivadas (vitest)

pip install -r pipeline/requirements.txt
python -m pytest pipeline/tests -q   # tests del pipeline (fechas, dedup, sanitización)
python pipeline/curate.py            # revisar la cuarentena pieza por pieza
```

## Decisiones clave (por qué está armado así)

- **`date` vs `published_date`**: `date` es la fecha del EVENTO histórico
  (ordena timeline/tal-día/máquina del tiempo), no la de publicación del blog.
- **`date_precision`**: solo piezas `"exact"` entran a tal-día y máquina del
  tiempo — evita que "c. 1935" aparezca cada 1 de enero como si fuera de ese día.
- **Vistas ricas gateadas**: timeline, tal-día y máquina del tiempo se ocultan
  hasta 100 piezas curadas (`RICH_VIEWS_THRESHOLD` en `src/lib/views.ts`).
- **zod es el único dueño del schema**: Python solo da forma; `npm run build`
  es el gate real.
- **El bot de link-rot nunca commitea**: solo abre issues; la curaduría manual
  aplica los cambios.

Más contexto en el design doc.
