// Prefija rutas internas con el "base" configurado en astro.config.mjs
// (necesario porque el sitio se sirve en /ArchivoDragon/ en GitHub Pages,
// no en la raíz del dominio). Usar SIEMPRE esto en vez de hardcodear
// href="/..." o src="/..." en componentes/páginas.
export function url(path: string): string {
  // BASE_URL a veces viene sin "/" final (depende de config/entorno) — se
  // normaliza acá para no depender de ese detalle.
  const base = import.meta.env.BASE_URL.replace(/\/?$/, "/");
  return base + path.replace(/^\//, "");
}
