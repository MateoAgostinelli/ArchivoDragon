# TODOS — ArchivoDragon

Diferidos con contexto. Origen: /office-hours + /plan-ceo-review del 2026-07-23.

## P3 — Paginación de listados
- **Qué:** `paginate()` de Astro en los listados por tipo.
- **Por qué:** con miles de piezas una página única se vuelve pesada.
- **Contexto:** umbral práctico ~1.000 piezas por tipo; hoy innecesario. CC ~5 min.
- **Depende de:** crecimiento del contenido.

## P3 — Galería de fotos (etapa 2)
- **Qué:** galería con copias locales en `/public/img/`, optimizadas al ingestar.
- **Bloqueado por:** definir política de derechos de imagen (la de TEXTO ya está decidida: extracto+link para medios, completo con permiso para blogs de hinchas).
- **Contexto:** en etapa 1 las piezas `foto` llevan solo link + archived_url. Límite blando GitHub Pages ~1 GB.

## P3 — Feed RSS / newsletter de piezas nuevas
- **Qué:** feed autogenerado del dataset. CC ~10 min cuando se quiera.

## P3 — Dominio propio (archivodragon.com.ar)
- **Qué:** comprar y apuntar dominio; hoy alcanza el subdominio gratuito de Pages.

## ✅ CLI de curaduría de cuarentena — construido
`pipeline/curate.py` ya existe (aprobar/editar/descartar por tecla). No se usó
todavía para las primeras 22 piezas (se cargaron a mano directo, sin pasar
por cuarentena) — queda listo para cuando el scraper empiece a producir
borradores.

## P2 — Contactar a La Máquina del Bajo (fuente elegida)
- **Qué:** escribir al autor del blog `lamaquinadelbajo.blogspot.com` (historia,
  ídolos, campeonatos, hemeroteca) contando el proyecto, pidiendo permiso para
  citar texto completo (política T3), e invitándolo a colaborar.
- **Contexto:** primera fuente real usada — 22 piezas (2026-07-25) archivadas a
  mano desde 3 páginas del blog (`historia_15.html`, `links.html`,
  `hemeroteca.html`). Hoy están cargadas como EXTRACTO/paráfrasis propia (no
  copia textual) porque todavía no hay permiso — cumple la política T3 por
  defecto. Si el autor autoriza, se puede enriquecer con más detalle textual.
- **Cobertura Wayback (T4):** no medida todavía — pendiente cuando se corra
  `pipeline/wayback_batch.py` sobre las 22 fuentes.

## P3 — Audio propio de tribuna
- **Qué:** grabaciones reales de la popular, georreferenciadas a partidos. "Nadie archiva el sonido."
