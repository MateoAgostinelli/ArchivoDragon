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

## P1 — CLI de curaduría de cuarentena
- **Qué:** comando que muestra pieza por pieza (texto + fecha propuesta + flag de duplicado) con aprobar/editar/descartar por tecla.
- **Por qué:** el cuello de botella real del proyecto es la curaduría manual, no los scrapers (blogs fuente están muertos/congelados, se scrapean una vez).
- **Contexto:** /plan-eng-review 2026-07-24. Reemplaza la ceremonia de tests exhaustivos por-scraper.
- **Esfuerzo:** CC ~30 min.

## P2 — Contactar dueños de blogs fuente
- **Qué:** escribir a La Máquina del Bajo y similares: contar el proyecto, pedir permiso para textos completos (política T3), invitar a colaborar.
- **Contexto:** puede convertir la fuente más rica en el primer colaborador.

## P3 — Audio propio de tribuna
- **Qué:** grabaciones reales de la popular, georreferenciadas a partidos. "Nadie archiva el sonido."
