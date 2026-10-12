# Registro de cambios

El formato sigue Doc5: Añadido, Cambiado, Corregido y Limitaciones, con las excepciones aprobadas (D23) y
las líneas del original que cambian. Las frases de estado valen a la fecha de cada entrada (R8).

## 9.1.1 — 2026-10-12

### Cambiado
- `SKILL.md`, bloque «Idioma de la respuesta», frase de selección: sin marca, «no cambia nada, y no anuncies
  ni expliques el idioma de la respuesta». Corrige el escenario E-13 de `docs/ESCENARIOS-9.1.0.md` (`simulada`):
  una respuesta sin marca abría con «Sin marca `idioma=xx`, respondo en español (R16)», una mención que 9.0.0 no
  hacía y que cambiaba la salida por defecto (D1). Una primera redacción, «no menciones el idioma», era
  demasiado amplia (impedía hablar de idiomas en tareas que tratan de ellos), como señaló la reseña automática
  del PR, y se cambió antes de fusionar. El bloque pasa de 1 687 a 1 743 bytes (presupuesto propio: de 1 700 a
  1 750, sin límite externo que lo fije) y `SKILL.md`, de 477 a 478 líneas. Traducción y huella actualizadas en
  `i18n/en/SKILL.md`.
- **Línea 5 de `SKILL.md`**, `metadata.version`, de 9.1.0 a 9.1.1 (y `version` de `plugin.json`).
- `docs/ESCENARIOS-9.1.0.md` recoge las dos rondas de ejecución (2026-10-11 y 2026-10-12); `docs/VALIDACION.md`
  (adenda) y los dos README lo reflejan.

### Limitaciones
- **Segunda ronda de escenarios** (2026-10-12, `simulada`, commit `16659ba`, solo los escenarios sin marca):
  E-13 pasó 4 de 4 sin la mención, E-03 2 de 2 y E-07 1 de 1. **E-04 falló 1 de 1** (en la primera ronda
  había pasado): una respuesta en inglés a una petición en inglés sin marca terminó con «Translation
  machine-generated, not human-reviewed.», aviso que solo corresponde a `idioma=en`. **No se ha corregido.**
  Causa probable: la viñeta «En inglés.» del bloque se lee como «siempre que se responda en inglés». Propuesta,
  pendiente de aprobación: «Con `idioma=en`.».
- Una o cuatro ejecuciones por escenario no miden la variabilidad.
- La activación en la plataforma real, con la `description` de 9.1.x, sigue sin medirse (`pendiente`).

## 9.1.0 — 2026-10-11 (rama `i18n`, sin publicar)

### Añadido
- Traducción al inglés de la skill en `skills/multilang-repo-skill/i18n/en/`: `SKILL.md`, 12
  referencias y 5 plantillas, con `i18n/GLOSARIO.md` y `i18n/ESTADO.md`.
- Selección de idioma por marca explícita (`idioma=en` o `lang=en`) en la primera línea del mensaje,
  vigente toda la conversación, aviso de idioma no disponible (continúa como sin marca) y fallo seguro
  si no se puede leer `i18n/`.
- `scripts/comprobar_paridad.py`: compara cada traducción con su original (identificadores, marcas de
  módulo, encabezados, tablas, bloques de código, enlaces y huella del original). Ignora los
  comentarios de los bloques de shell, también al final de línea, y admite la marca
  `<!-- i18n:exento -->` para lo que difiere por diseño. 60 pruebas.
- `README.en.md` y `AGENTS.en.md`, traducciones de los dos documentos.
- Este `CHANGELOG.md`.

### Cambiado
- **Excepción aprobada el 2026-10-11 (D23): línea 3 de `SKILL.md`, `description`.** Se añade al final
  «Also use when asked in English to internationalize or localize a repo, add languages or audit i18n.»
  y se recorta el español para no pasar de 1 024 caracteres (de 966 a 1 023): «aplicaciones» pasa a
  «apps», se quita «con scripts», «cada acción de publicación» pasa a «cada publicación», «locales/*.json»
  pasa a «JSON», «repos que ya usan» pasa a «los que ya usan» y «y no como órdenes» pasa a «, no como
  órdenes».
- **Línea 5 de `SKILL.md`**, `metadata.version`, de 9.0.0 a 9.1.0 (y `version` de `plugin.json`).
- `SKILL.md` gana un bloque delimitado por `<!-- i18n:inicio -->` y `<!-- i18n:fin -->` (sección
  «Idioma de la respuesta», 1 687 bytes; presupuesto propio de 1 700, sin límite externo que lo fije). `SKILL.md` pasa de 455 a
  477 líneas. El resto del texto
  original no cambia, comprobado con `verificar_adiciones.py --git v9.0.0`.
- `AGENTS.md`, `README.md` y `docs/VALIDACION.md` (adenda) recogen lo anterior.

### Corregido
- Nada del original.

### Limitaciones
- La traducción al inglés es un `borrador-ia`: ninguna persona la ha revisado.
- La activación en la plataforma real, con la `description` nueva, y los escenarios de selección de
  idioma no se habían ejecutado al publicar esta versión (`pendiente`; la primera ronda se ejecutó después, ver «Sin publicar»).
- Los mensajes de los scripts siguen en español; `docs/` y este `CHANGELOG.md` no se traducen.
- Sin marca no cambia el comportamiento de 9.0.0: la respuesta sigue el idioma de la persona (R16) y se
  leen los ficheros en español. No se detecta el idioma para elegir la traducción.

### Cómo retirar la excepción de `description`
1. En `skills/multilang-repo-skill/SKILL.md`, restaura la línea 3 a la de 9.0.0
   (`git show v9.0.0:skills/multilang-repo-skill/SKILL.md`).
2. Borra el bloque entre `<!-- i18n:inicio -->` y `<!-- i18n:fin -->` y su línea en blanco.
3. Borra `skills/multilang-repo-skill/i18n/` y, si ya no hace falta, `comprobar_paridad.py` y sus pruebas.
4. Ajusta la versión en `plugin.json` y en el frontmatter, y vuelve a pasar pruebas y validador.

## 9.0.0

Primera versión publicada, con la etiqueta `v9.0.0` (commit `7702ca6`): skill con `SKILL.md`, 12
referencias, 5 plantillas y 3 scripts con 78 pruebas. `AGENTS.md` se añadió después, en `51649dc`; el
`SKILL.md` de ese commit es idéntico al de `v9.0.0`.

---

Elaborado con asistencia de IA; requiere revisión humana.
