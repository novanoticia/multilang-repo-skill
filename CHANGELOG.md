# Registro de cambios

El formato sigue Doc5: Añadido, Cambiado, Corregido y Limitaciones, con las excepciones aprobadas (D23) y
las líneas del original que cambian. Las frases de estado valen a la fecha de cada entrada (R8).

## Sin publicar — 2026-10-13 (solo documentación)

No cambia `SKILL.md`, los scripts ni la versión (sigue la 9.1.4). Registra dos rondas de regresión sobre el texto final de la 9.1.4.

### Añadido
- `docs/ESCENARIOS-9.1.0.md` y `docs/VALIDACION.md` (adenda) recogen la **quinta ronda** (2026-10-12, `simulada`, sobre `c2e1a5e`): 21 ejecuciones calificadas por tres evaluadores independientes, 18 PASS, 2 INDETERMINADO y 1 FAIL; y la **sexta** (2026-10-13): E-10 y E-13 cinco veces sobre la 9.1.3 y cinco sobre la 9.1.4, con E-13 calificado a ciegas y E-10 por recuento literal.

### Cambiado
- **Criterio de E-10** (`docs/ESCENARIOS-9.1.0.md`): el «Pasa si» deja de exigir citar el marcador `<!-- i18n:inicio -->`; basta citar `verificar_adiciones.py`. Decisión de la persona del 2026-10-13, **tomada con los resultados de las rondas 4 a 6 a la vista**, para resolver una ambigüedad del propio criterio. Los veredictos ya registrados no se modifican; con el criterio nuevo, las 3 ejecuciones INDETERMINADO de E-10 pasarían a PASS.

### Limitaciones (lo que dicen esas rondas)
- **E-13** falló una vez (anunció «No hay marca `idioma=xx`, así que respondo en español»): 1 de 6 con la 9.1.4 y 0 de 5 con la 9.1.3. Con diez repeticiones no se reprodujo, pero la muestra es pequeña.
- **E-10** cita el script siempre y el marcador `<!-- i18n:inicio -->` en 5 de 8 ejecuciones con la 9.1.4 y en 8 de 8 con la 9.1.3. Con tres casos sin marcador todos en la 9.1.4, la probabilidad de que sea azar es de un 10 % (prueba exacta de Fisher, una cola): **sugiere un efecto de la 9.1.4, sin demostrarlo**. Además, el criterio de E-10 es ambiguo (el «Pasa si» exige el marcador y el «Ejemplo que pasa» no), y el 2026-10-13 se decidió que omitirlo **no** es un fallo (ver «Cambiado»); el hecho medido, 5 de 8 frente a 8 de 8, queda como observación.
- La calificación de E-10-a en la cuarta ronda (FAIL, por el agente que orquesta) habría sido INDETERMINADO con un evaluador independiente.
- **Las notas de la Release `v9.1.4` no mencionan estas dos rondas** (se publicaron antes). No se han modificado.
- El aislamiento de los ejecutores sigue siendo declarado, no verificado.

## 9.1.4 — 2026-10-12

### Cambiado
- `SKILL.md`, bloque «Idioma de la respuesta», **acortado**: el detalle de los idiomas disponibles y de lo que
  no se traduce pasa a la referencia nueva `references/idioma-de-la-respuesta.md` (con su espejo en
  `i18n/en/references/`), enlazada desde el bloque. Siguen en el bloque la selección, el aviso de la
  traducción automática (D22), el caso de no disponible o mal formada (D4) y el fallo seguro (D25). El bloque
  pasa de 1 862 a 1 700 bytes (presupuesto propio: de 1 900 a 1 700, sin límite externo que lo fije) y
  `SKILL.md`, de 479 a 477 líneas. Es lo que el `CHANGELOG` de la 9.1.3 dejó anunciado.
- **Línea 5 de `SKILL.md`**, `metadata.version`, de 9.1.3 a 9.1.4 (y `version` de `plugin.json`).
- **Excepción a la regla 2 de `AGENTS.md`** (aprobada por la persona el 2026-10-12): la referencia nueva no está en la
  tabla de Recursos, porque añadir su fila cambiaría texto original de `SKILL.md` fuera del bloque delimitado. Se
  carga desde el bloque, que escribe su condición («si dudas de cómo se resuelve una marca o de qué no se
  traduce»). El bloque queda en 1 700 bytes, justo en el presupuesto (1 700): no hay margen. Para volver a la regla, se añade la fila
  a la tabla con un cambio aprobado de texto original. La reseña automática del PR #7 lo señaló.
- `i18n/en/SKILL.md` sigue el cambio y su huella se actualiza; `i18n/ESTADO.md` cuenta 13 referencias.

### Añadido
- `references/idioma-de-la-respuesta.md` y `i18n/en/references/idioma-de-la-respuesta.md` (`borrador-ia`).

### Limitaciones
- **Regresión de la 9.1.4** (`simulada`, `docs/ESCENARIOS-9.1.0.md`, cuarta ronda): E-05 a E-09 y E-12 pasan 7 de 7.
  E-10 falló en una ejecución (no citó el marcador `<!-- i18n:inicio -->`) y pasó en tres repeticiones; sobre la
  9.1.3 pasó 3 de 3. Es compatible con variabilidad, pero 1 fallo en 4 frente a 0 en 3 no permite descartar un
  efecto del cambio. Las calificó el agente que orquesta, sin evaluador independiente.
  La ronda se ejecutó sobre un bloque de 1 617 bytes; la condición de lectura añadida después (1 700 bytes)
  **no se ha ejecutado por escenarios**.
- Sin cambios respecto a la 9.1.3 en lo demás: la activación real, el fallo intermitente de E-04 y la revisión
  humana del inglés siguen pendientes.

## 9.1.3 — 2026-10-12

### Cambiado
- `SKILL.md`, bloque «Idioma de la respuesta», viñeta de selección: añade que la marca «elige el idioma de la
  respuesta, no los idiomas a los que se traduce un repositorio». Aclara una confusión vista en varias
  ejecuciones simuladas (E-05 y las rondas siguientes): quien ejecutaba la skill se preguntaba si `idioma=en`
  significaba «añade inglés al repositorio». Los dos README lo dicen también y la traducción de `SKILL.md`
  lleva la misma frase. El bloque pasa de 1 773 a 1 862 bytes (presupuesto propio: de 1 800 a 1 900, sin límite
  externo que lo fije; es la cuarta vez que se sube, y si vuelve a crecer conviene mover detalle a una
  referencia) y `SKILL.md`, de 478 a 479 líneas.
- **Línea 5 de `SKILL.md`**, `metadata.version`, de 9.1.2 a 9.1.3 (y `version` de `plugin.json`).
- `docs/ESCENARIOS-9.1.0.md` y `docs/VALIDACION.md` (adenda) recogen la **tercera ronda de escenarios**
  (2026-10-12, `simulada`, sobre 9.1.2): 11 ejecuciones y 11 PASS, con E-04 pasando 4 de 4 tras la corrección de
  la 9.1.2 y el escenario nuevo E-14 (`lang=en`). Las 4 ejecuciones de E-04 las calificó un evaluador
  independiente; las otras 7, el agente que orquesta.

### Limitaciones
- **La aclaración no se ha medido por escenarios** (`pendiente`): es una frase informativa y no hay un
  escenario preregistrado que la compruebe.
- Cuatro ejecuciones de E-04 sin fallo no prueban que el fallo intermitente esté resuelto: si fallaba la mitad
  de las veces, cuatro pases seguidos ocurrirían por azar en un 6 % de los casos.
- Siguen vigentes las limitaciones anteriores: el inglés es un `borrador-ia` y la activación real no se ha
  medido.

## 9.1.2 — 2026-10-12

### Cambiado
- `SKILL.md`, bloque «Idioma de la respuesta», viñeta del inglés: «En inglés.» pasa a «Si la marca elige
  `en`.» y la frase del aviso termina con «solo en ese caso». Redactado así y no con el literal `idioma=en`
  para cubrir también `lang=en`, `IDIOMA=EN` o `idioma=en-GB`, como señaló la reseña automática del PR. Corrige
  el escenario E-04 de `docs/ESCENARIOS-9.1.0.md` (`simulada`): una respuesta en inglés a una petición en
  inglés sin marca terminó con «Translation machine-generated, not human-reviewed.», aviso que solo
  corresponde a la marca que elige `en`. El bloque pasa de 1 743 a 1 773 bytes (presupuesto propio: de 1 750 a
  1 800, sin límite externo que lo fije); `SKILL.md` sigue en 478 líneas. Traducción y huella actualizadas en
  `i18n/en/SKILL.md`.
- **Línea 5 de `SKILL.md`**, `metadata.version`, de 9.1.1 a 9.1.2 (y `version` de `plugin.json`).
- `docs/ESCENARIOS-9.1.0.md`, `docs/VALIDACION.md` (adenda) y los dos README reflejan la corrección.

### Limitaciones
- **La corrección de E-04 no se había vuelto a medir al publicar esta versión** (la tercera ronda la midió
  después: 4 PASS de 4, ver 9.1.3); la activación en la plataforma real sigue `pendiente`. El fallo era intermitente (1 de 2 ejecuciones), así que una ejecución sin
  fallo no lo demostraría.
- Siguen vigentes las limitaciones de 9.1.0 y 9.1.1: el inglés es un `borrador-ia` y la activación real no se
  ha medido.

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
  machine-generated, not human-reviewed.», aviso que solo corresponde a `idioma=en`. **No se corrigió en esta versión** (se corrige
  en la 9.1.2). Causa probable: la viñeta «En inglés.» del bloque se lee como «siempre que se responda en inglés».
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
