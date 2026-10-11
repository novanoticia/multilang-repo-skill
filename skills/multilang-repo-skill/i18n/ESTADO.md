# Estado de las traducciones

Registro del estado real de cada idioma (D12, T5). Las frases de estado envejecen (R8): las de este
fichero valen **a fecha 2026-10-11, rama `i18n`**, y hay que revisarlas antes de cada publicación.

| Idioma | Estado | Redactó | Revisó | Cobertura |
|---|---|---|---|---|
| `es` | `referencia` | Autoría del proyecto | — | `SKILL.md`, 12 referencias y 5 plantillas (originales) |
| `en` | `borrador-ia` | IA (Claude Sonnet 5.5), 2026-10-11 | Nadie. Pendiente de revisión humana | `i18n/en/`: `SKILL.md`, 12 referencias y 5 plantillas |

## Qué significa `borrador-ia` aquí

- Ninguna persona ha revisado el inglés. Que un modelo lo relea, o que pase el comprobador de paridad,
  no lo convierte en revisado (T5, M6).
- `scripts/comprobar_paridad.py --arbol skills/multilang-repo-skill skills/multilang-repo-skill/i18n/en --completo`
  comprueba la **estructura** (identificadores, marcas de módulo, encabezados, tablas, bloques de código,
  enlaces y huella del original). No comprueba que la traducción sea fiel ni natural.
- Cada fichero traducido lleva en su cabecera la huella del original del que parte. Si el original
  cambia, el comprobador marca la traducción como desfasada hasta que se revise y se actualice la huella.

## Idioma que se juzga con menos seguridad (T6)

El inglés es el idioma que mejor se maneja, así que no se entrega como `experimental`. El punto
menos seguro es la terminología de este marco (p. ej. «marca», «respaldo», «fallo seguro»), fijada en
`i18n/GLOSARIO.md` y revisable por una persona nativa o por quien conozca el dominio.

## Límites declarados

- Los mensajes de los scripts (`--help`, informes de `validar_catalogos.py` y `verificar_adiciones.py`,
  `comprobar_paridad.py`) siguen en español. `resolver_idioma.py` devuelve códigos de aviso que el agente
  localiza.
- `docs/` (auditoría, trazabilidad, validación e informe) no se traduce.
- Las comillas y la tipografía inglesas son una elección anotada (T2), no una decisión revisada.

## Pendiente de una persona

- Revisión humana del inglés, empezando por `i18n/en/SKILL.md` y las reglas R12, R13 y R18.
- Prueba de activación y de comportamiento en la plataforma real, en español y en inglés (nivel
  `plataforma`).

---

Elaborado con asistencia de IA; requiere revisión humana.
