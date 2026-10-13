# Idioma de la respuesta de esta skill

Detalle del bloque «Idioma de la respuesta» de `SKILL.md`. Léelo cuando la persona pida un idioma con
`idioma=xx` o `lang=xx`, o cuando dudes de cómo se resuelve una marca, de qué frase fija va en cada
idioma o de qué no se traduce. Las reglas de selección y el fallo seguro están en el bloque; aquí va lo
que lo completa.

## Contenido
- Idiomas disponibles y estado
- Cómo se resuelve una marca
- Frases fijas de cada idioma
- Qué no se traduce

## Idiomas disponibles y estado

| Idioma | Carpeta | Estado |
|---|---|---|
| `es` | los ficheros originales | referencia |
| `en` | `i18n/en/` | `borrador-ia` |
| `fr` | `i18n/fr/` | `borrador-ia` |
| `zh-Hans` (chino mandarín simplificado) | `i18n/zh-Hans/` | `borrador-ia` |
| `hi` (hindi) | `i18n/hi/` | `experimental`: revisión nativa imprescindible (T6) |

Ninguna traducción la ha revisado una persona (T5). La marca elige el idioma de la respuesta, no los
idiomas a los que se traduce un repositorio.

## Cómo se resuelve una marca

Sin distinguir mayúsculas y quitando el juego de caracteres (`en_US.UTF-8` es `en-US`):

| Marca | Resultado |
|---|---|
| `en`, `en-GB`, `en-US` | `en` |
| `fr`, `fr-CA`, `fr-FR` | `fr` |
| `hi`, `hi-IN` | `hi` |
| `zh`, `zh-CN`, `zh-SG`, `zh-Hans`, `zh-Hans-CN` | `zh-Hans` |
| `zh-Hant`, `zh-TW`, `zh-HK`, `zh-MO` | no disponible (D4): no se sirve chino simplificado a quien pide tradicional (D3) |
| cualquier otro (`de`, `pt-BR`…) | no disponible (D4): dilo, nombra los idiomas disponibles y continúa como sin marca |

[scripts/resolver_idioma.py](../scripts/resolver_idioma.py) implementa esta regla; su origen `defecto`
significa «sin marca», no «responde en español». Para esta lista:

```
python3 <skill>/scripts/resolver_idioma.py --disponibles es,en,fr,hi,zh-Hans --defecto es --respaldo zh=zh-Hans --respaldo zh-CN=zh-Hans --respaldo zh-SG=zh-Hans --respaldo zh-TW=zh-Hant --respaldo zh-HK=zh-Hant --respaldo zh-MO=zh-Hant
```

## Frases fijas de cada idioma

Se muestran solo cuando la marca elige ese idioma (D22): el aviso abre cada respuesta, y la línea de
fallo seguro se añade si no puedes leer `i18n/<idioma>/` (D25).

| Idioma | Aviso de traducción automática | Línea de fallo seguro |
|---|---|---|
| `en` | `Translation machine-generated, not human-reviewed.` | `English version unavailable; continuing with the Spanish files.` |
| `fr` | `Traduction automatique, non relue par une personne.` | `Version française indisponible ; poursuite avec les fichiers espagnols.` |
| `zh-Hans` | `机器翻译，未经人工审阅。` | `简体中文版本不可用；继续使用西班牙语文件。` |
| `hi` | `अनुवाद मशीन द्वारा तैयार किया गया है, मानव द्वारा समीक्षित नहीं। (Translation machine-generated, not human-reviewed.)` | `हिन्दी संस्करण उपलब्ध नहीं है; स्पैनिश फ़ाइलों के साथ आगे बढ़ा जा रहा है।` |

El aviso del hindi es bilingüe porque ese idioma se entrega como `experimental` (T6).

## Qué no se traduce

Identificadores (R1…Doc9), marcas de módulo, nombres de fichero y de script, opciones, códigos de aviso,
comandos y bloques de código. Los mensajes de los scripts siguen en español.
