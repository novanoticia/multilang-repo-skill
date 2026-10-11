# Registro de cambios

El formato sigue Doc5: Añadido, Cambiado, Corregido y Limitaciones, con las excepciones aprobadas (D23) y
las líneas del original que cambian. Las frases de estado valen a la fecha de cada entrada (R8).

## 9.1.0 — 2026-10-11 (rama `i18n`, sin publicar)

### Añadido
- Traducción al inglés de la skill en `skills/multilang-repo-skill/i18n/en/`: `SKILL.md`, 12
  referencias y 5 plantillas, con `i18n/GLOSARIO.md` y `i18n/ESTADO.md`.
- Selección de idioma por marca explícita (`idioma=en` o `lang=en`) en la primera línea del mensaje,
  con respaldo al español, aviso de idioma no disponible y fallo seguro si no se puede leer `i18n/`.
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
  «Idioma de la respuesta», 1 345 bytes). `SKILL.md` pasa de 455 a 473 líneas. El resto del texto
  original no cambia, comprobado con `verificar_adiciones.py --git 51649dc`.
- `AGENTS.md`, `README.md` y `docs/VALIDACION.md` (adenda) recogen lo anterior.

### Corregido
- Nada del original.

### Limitaciones
- La traducción al inglés es un `borrador-ia`: ninguna persona la ha revisado.
- La activación en la plataforma real, con la `description` nueva, y los escenarios de selección de
  idioma no se han ejecutado (`pendiente`).
- Los mensajes de los scripts siguen en español; `docs/` y este `CHANGELOG.md` no se traducen.
- No se detecta el idioma en que escribe la persona: sin marca se responde en español.

### Cómo retirar la excepción de `description`
1. En `skills/multilang-repo-skill/SKILL.md`, restaura la línea 3 a la de 9.0.0
   (`git show 51649dc:skills/multilang-repo-skill/SKILL.md`).
2. Borra el bloque entre `<!-- i18n:inicio -->` y `<!-- i18n:fin -->` y su línea en blanco.
3. Borra `skills/multilang-repo-skill/i18n/` y, si ya no hace falta, `comprobar_paridad.py` y sus pruebas.
4. Ajusta la versión en `plugin.json` y en el frontmatter, y vuelve a pasar pruebas y validador.

## 9.0.0

Versión del repositorio en su commit inicial (`51649dc`): skill con `SKILL.md`, 12 referencias, 5
plantillas y 3 scripts con 78 pruebas.

---

Elaborado con asistencia de IA; requiere revisión humana.
