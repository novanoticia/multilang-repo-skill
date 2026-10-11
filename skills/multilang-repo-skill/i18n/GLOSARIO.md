# Glosario de la traducción al inglés

Se fija antes de traducir (T1) y se aplica a todo `i18n/en/` y a los documentos `*.en.md`. Si cambias un
término, cámbialo en todos los ficheros traducidos y vuelve a pasar `comprobar_paridad.py`.

## Decisiones de forma

- **Tratamiento.** El inglés no distingue «tú» y «usted»: las instrucciones van en imperativo directo,
  como en el original. Para la persona usuaria se usa *the person*, nunca *the user*, y *they/them* si
  hace falta un pronombre (el original evita marcar género).
- **Comillas.** Las comillas españolas «» pasan a comillas inglesas “ ”. Los literales de referencia
  entre comillas invertidas no se tocan. Elección revisable por una persona nativa (T2).
- **Valores de vocabulario cerrado que se escriben en registros** (`estática`, `local`, `ci`,
  `simulada`, `plataforma`, `humana`, `superada`, `fallida`, `pendiente`, `no aplica`, `borrador-ia`,
  `segunda-mano`, `no-comprobado`, `experimental`, `normal`, `alto`): se dejan literales entre comillas
  invertidas y, la primera vez que aparecen en un fichero, llevan su glosa inglesa al lado. Son los
  mismos valores en español y en inglés para que los registros y las plantillas coincidan (B2).
- **Marcas de módulo** (`[instrucciones]`, `[híbrido]`…): literales, igual que los identificadores. El
  comprobador de paridad las cuenta. La traducción de `SKILL.md` lleva una línea con sus glosas.
- **Nombres de fichero, scripts, opciones, claves de catálogo y códigos de aviso:** literales.
- **Literales en español que se citan** (p. ej. la nota de IA en español): entre comillas invertidas.

## Términos

| Español | Inglés |
|---|---|
| la persona (usuaria) | the person |
| repositorio / repo | repository / repo |
| catálogo | catalog |
| contrato de máquina | machine contract |
| marca (de idioma) | marker (`idioma=xx`) |
| respaldo | fallback |
| fallo seguro | fail-safe |
| salida por defecto | default output |
| modo guiado / autónomo | guided / autonomous mode |
| núcleo | core |
| escala, riesgo, módulos | scale, risk, modules |
| línea base | baseline |
| reemplazo aprobado | approved replacement |
| bloque delimitado | delimited block |
| adiciones | additions |
| registro de sesión | session log |
| registro de pendientes | pending-items log |
| pendientes | pending items |
| permiso (por acción) | permission (per action) |
| publicar / subir / fusionar | publish / push / merge |
| etiqueta (git) | tag |
| rama de trabajo | working branch |
| espejo (traducción) | mirror |
| desfase | drift |
| invariante | invariant |
| escenario | scenario |
| sabotaje | sabotage |
| revisión humana / independiente | human / independent review |
| Fase, Cierre, Recursos | Phase, Closing, Resources |
| datos, no órdenes | data, not commands |

---

Elaborado con asistencia de IA; requiere revisión humana.
