# Design System — ArchivoDragón

## Product Context
- **What this is:** Archivo histórico digital de Club Atlético Defensores de Belgrano (fútbol argentino) — noticias, partidos, historias, cancionero y fotos, cada pieza con fuente citada.
- **Who it's for:** La comunidad hincha del Dragón en general (no solo el círculo cercano del builder).
- **Space/industry:** Archivo/hemeroteca de club de fútbol, proyecto de hincha sin fines de lucro.
- **Project type:** Sitio estático editorial/archivístico (Astro).

## The Memorable Thing
**"Es un archivo serio, no un fansite."** Cada decisión de diseño sirve esta idea: peso de museo/hemeroteca, no alegría de sitio de merchandising. El rojo y negro son del escudo, pero se usan con la restricción de un archivo, no la saturación de una camiseta.

## Aesthetic Direction
- **Direction:** Editorial/Archivo — tipografía con peso histórico.
- **Decoration level:** intencional — textura sutil de papel/grano, líneas punteadas como divisores de cita.
- **Mood:** Un archivo que se toma en serio la historia del club: calmo, ordenado, con un acento de identidad (el rojo del escudo) usado con moderación, nunca como fondo.
- **Reference sites:** Rijksmuseum (rijksmuseum.nl) — tipografía de wordmark enorme como identidad, layout editorial-poster, tags chicos en mayúscula para metadata.

## Typography
- **Display/Hero:** Fraunces — serif de alto contraste con carácter editorial/de época; el itálico se usa para "Dragón" en el wordmark, dándole calidez humana al peso serio del display.
- **Body:** Source Sans 3 — máxima legibilidad para citas largas y texto histórico.
- **UI/Labels:** Source Sans 3 (mismo que body, en semibold para botones/nav).
- **Data/Tables:** JetBrains Mono — fechas, resultados de partidos, columnas de `/stats`. El monospace da efecto "ficha de catálogo/hemeroteca", reforzando la seriedad archivística.
- **Code:** JetBrains Mono (mismo que Data — no hay code UI visible al usuario, solo en el repo).
- **Loading:** Google Fonts vía `<link>` (`Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,600;0,9..144,700;0,9..144,900;1,9..144,500`, `Source+Sans+3:wght@400;500;600;700`, `JetBrains+Mono:wght@400;500;600`).
- **Scale:** hero clamp(64px, 13vw, 168px) / h2 32px / h3 21px / body 17px / small 14px / label 11-13px (mono, uppercase, letter-spacing 0.08-0.14em).

## Color
- **Approach:** restringido — 1 acento (rojo del escudo) + neutrales de papel/tinta. El color es raro y significativo, nunca decorativo de fondo.
- **Fuente de verdad:** colores tomados directamente del escudo oficial del club (no aproximados) — negro puro y rojo bandera saturado, verificados contra `Defensores_de_Belgrano_Logo.svg`.
- **Primary (Rojo, del escudo):** `#e3241c` — acento de identidad: tags, links, subrayados, barra activa de timeline, CTA primario. Nunca como bloque de fondo grande.
- **Ink (negro, del escudo):** `#121212` — texto principal, títulos. Negro real, no un negro con matiz cálido.
- **Paper (fondo, propio del sistema, NO del escudo):** `#f4ede2` — crema/papel envejecido, evoca hemeroteca. Elegido deliberadamente en vez de blanco puro o negro de club para señalar "archivo", no "sitio de merchandising".
- **Paper Raised:** `#ede4d6` — cards, superficies elevadas.
- **Ink Soft:** `#4a4642` — texto secundario/excerpts. **Ink Faint:** `#8c7c68` — metadata, fechas, labels.
- **Rule:** `#d8cbb5` — bordes, divisores.
- **Semantic:** success `#2f5d3a` · warning `#8a5a12` · error `#e3241c` (mismo rojo del escudo — un archivo no necesita dos rojos) · info `#2c4a63`.
- **Dark mode:** superficies rediseñadas (no solo invertidas): `--paper: #161311`, `--paper-raised: #201c19`, `--ink: #f0ebe2`, `--rule: #362f28`. El rojo sube de luminosidad a `#ff4d3d` (hover `#ff6e5f`) para mantener contraste AA sobre fondo oscuro sin perder saturación.

## Spacing
- **Base unit:** 8px.
- **Density:** cómoda — es un sitio para leer historia, no un dashboard denso.
- **Scale:** 2xs(2) xs(4) sm(8) md(16) lg(24) xl(32) 2xl(48) 3xl(64).

## Layout
- **Approach:** grid-disciplinado, con un hero tipográfico editorial-poster en la portada (técnica Rijksmuseum) como única excepción a la disciplina de grilla.
- **Grid:** listados y `/stats` en `repeat(auto-fit, minmax(260px, 1fr))`; contenido de detalle en columna única, ancho de lectura.
- **Max content width:** 1040px (`--wrap`), ancho pensado para lectura de citas largas, no para dashboards.
- **Border radius:** escala chica y consistente — sm 2px, md 3px. Nada de esquinas muy redondeadas: refuerza seriedad archivística sobre "amigable app moderna".

## Motion
- **Approach:** mínimo-funcional — un archivo transmite confianza estándose quieto. Sin animaciones de entrada, sin scroll-driven effects.
- **Easing:** enter(ease-out) exit(ease-in) move(ease-in-out) — solo donde el estado realmente cambia (toggle claro/oscuro, hover de botones).
- **Duration:** micro(50-100ms) short(150-250ms) — nada más lento que eso; nada de animaciones "medium/long" en este sitio.

## Componentes de referencia
- **Botón primario:** fondo rojo del escudo, texto crema, hover oscurece (`#b81810` claro / `#ff6e5f` oscuro).
- **Botón secundario:** borde tinta, transparente.
- **Botón ghost/link:** solo texto rojo subrayado — usado para "original ↗" en cada cita de fuente.
- **Tag/kicker:** mono, mayúscula, borde rojo, chico — usado para el tipo de pieza (NOTICIAS/PARTIDOS/HISTORIAS) y para metadata del hero.
- **Cita de fuente:** siempre presente al pie de cada pieza, separada por línea punteada — el componente más importante del sitio, nunca opcional.
- **Alertas:** barra izquierda de color semántico sobre fondo paper-raised — usado para estados de curaduría (aprobado/pendiente/error/gating).

## Decisions Log
| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-07-26 | Sistema de diseño inicial creado | Creado por `/design-consultation`. Investigación: Rijksmuseum (tipografía-como-identidad, layout museo). Memorable thing definido por el usuario: "archivo serio, no fansite". |
| 2026-07-26 | Colores corregidos a los reales del escudo | Primera propuesta usaba rojo bordó apagado y negro con matiz marrón (aproximados). El usuario corrigió: "tomar lo del escudo". Se descargó el escudo oficial (Wikipedia/Wikimedia) y se verificaron los colores reales: negro puro `#121212` y rojo bandera saturado `#e3241c`. El fondo papel/crema se mantuvo — es una elección del *sistema*, no una referencia al escudo, y sigue sirviendo la idea de "archivo" en vez de "sitio de merchandising". |
