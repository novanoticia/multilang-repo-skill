# Estado de las traducciones

Registro del estado real de cada idioma (D12, T5). Las frases de estado envejecen (R8): las de este
fichero valen **a fecha 2026-10-13, rama `i18n/fr-zh-hi`**, y hay que revisarlas antes de cada publicación.

| Idioma | Estado | Redactó | Revisó | Cobertura |
|---|---|---|---|---|
| `es` | `referencia` | Autoría del proyecto | — | `SKILL.md`, 13 referencias y 5 plantillas (originales) |
| `en` | `borrador-ia` | IA (Claude Sonnet 5.5), 2026-10-11 | Nadie. Pendiente de revisión humana | `i18n/en/`: `SKILL.md`, 13 referencias y 5 plantillas |
| `fr` | `borrador-ia` | IA (Claude Sonnet 5.5, con subagentes), 2026-10-13 | Nadie. Pendiente de revisión humana | `i18n/fr/`: `SKILL.md`, 13 referencias y 5 plantillas |
| `zh-Hans` (chino mandarín simplificado) | `borrador-ia` | IA (Claude Sonnet 5.5, con subagentes), 2026-10-13 | Nadie. Pendiente de revisión humana nativa | `i18n/zh-Hans/`: `SKILL.md`, 13 referencias y 5 plantillas |
| `hi` (hindi) | `borrador-ia`, **`experimental`** (T6) | IA (Claude Sonnet 5.5, con subagentes), 2026-10-13 | Nadie. Revisión nativa imprescindible | `i18n/hi/`: `SKILL.md`, 13 referencias y 5 plantillas |

## Qué significa `borrador-ia` aquí

- Ninguna persona ha revisado el inglés. Que un modelo lo relea, o que pase el comprobador de paridad,
  no lo convierte en revisado (T5, M6).
- `scripts/comprobar_paridad.py --arbol skills/multilang-repo-skill skills/multilang-repo-skill/i18n/en --completo`
  comprueba la **estructura** (identificadores, marcas de módulo, encabezados, tablas, bloques de código,
  enlaces y huella del original). No comprueba que la traducción sea fiel ni natural.
- Cada fichero traducido lleva en su cabecera la huella del original del que parte. Si el original
  cambia, el comprobador marca la traducción como desfasada hasta que se revise y se actualice la huella.

## Idioma que se juzga con menos seguridad (T6)

**El hindi se entrega como `experimental`.** Quien lo redactó declara que su hindi técnico es menos seguro
que su francés o su inglés (registro, calcos frente a préstamos, género gramatical al evitar marcar
género); el aviso que abre cada respuesta en hindi es bilingüe y la revisión nativa es imprescindible. El
chino simplificado se juzga con seguridad media: la terminología técnica (p. ej. «fallo seguro», «contrato de
máquina», «catálogo») es la parte dudosa, y 用户 («usuario») aparece donde el original dice «la persona».
El francés tiene dudas de terminología menores (`balise` o `marqueur` para la marca, `repli` para el respaldo).
Los glosarios de cada idioma (`GLOSARIO.fr.md`, `GLOSARIO.zh-Hans.md`, `GLOSARIO.hi.md`) listan sus dudas.

El inglés es el idioma que mejor se maneja, así que no se entrega como `experimental`. El punto
menos seguro es la terminología de este marco (p. ej. «marca», «respaldo», «fallo seguro»), fijada en
`i18n/GLOSARIO.md` y revisable por una persona nativa o por quien conozca el dominio.

## Límites declarados

- Los mensajes de los scripts (`--help`, informes de `validar_catalogos.py` y `verificar_adiciones.py`,
  `comprobar_paridad.py`) siguen en español. `resolver_idioma.py` devuelve códigos de aviso que el agente
  localiza.
- `docs/` (auditoría, trazabilidad, validación e informe) no se traduce.
- Las comillas y la tipografía inglesas son una elección anotada (T2), no una decisión revisada. Lo mismo
  vale para las francesas, chinas e hindis de cada glosario.
- El chino tradicional (`zh-Hant`, `zh-TW`, `zh-HK`, `zh-MO`) **no está disponible** y no cae en el
  simplificado (D3); se avisa como idioma no disponible.
- Los espejos `fr`, `zh-Hans` y `hi` se tradujeron con subagentes en paralelo desde el original español y
  se comprobaron con `comprobar_paridad.py --completo` (0 errores, 0 avisos) y con una auditoría propia de
  las frases literales; **ningún evaluador nativo ha leído las respuestas** que producen.

## Pendiente de una persona

- Revisión humana de cada idioma, empezando por `SKILL.md` y las reglas R12, R13 y R18, y por el hindi (`experimental`).
- Prueba de activación y de comportamiento en la plataforma real, en los cinco idiomas (nivel
  `plataforma`).

---

Elaborado con asistencia de IA; requiere revisión humana.
