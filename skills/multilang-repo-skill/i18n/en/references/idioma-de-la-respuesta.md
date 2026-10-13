<!-- i18n fuente-sha256=5741eaf9c542 estado=borrador-ia -->

# Response language of this skill

Detail of the “Response language” block of `SKILL.md`. Read it when the person asks for a language with
`idioma=xx` or `lang=xx`, or when you doubt how a marker is resolved, which fixed phrase goes with each
language or what is not translated. The selection rules and the fail-safe are in the block; what completes
them is here.

## Contents
- Available languages and status
- How a marker is resolved
- Fixed phrases of each language
- What is not translated

## Available languages and status

| Language | Folder | Status |
|---|---|---|
| `es` | the original files | reference |
| `en` | `i18n/en/` | `borrador-ia` (AI draft) |
| `fr` | `i18n/fr/` | `borrador-ia` |
| `zh-Hans` (Simplified Mandarin Chinese) | `i18n/zh-Hans/` | `borrador-ia` |
| `hi` (Hindi) | `i18n/hi/` | `experimental`: native review is essential (T6) |

No person has reviewed any translation (T5). The marker chooses the response language, not the languages a
repository is translated into.

## How a marker is resolved

Case-insensitively and dropping the character set (`en_US.UTF-8` is `en-US`):

| Marker | Result |
|---|---|
| `en`, `en-GB`, `en-US` | `en` |
| `fr`, `fr-CA`, `fr-FR` | `fr` |
| `hi`, `hi-IN` | `hi` |
| `zh`, `zh-CN`, `zh-SG`, `zh-Hans`, `zh-Hans-CN` | `zh-Hans` |
| `zh-Hant`, `zh-TW`, `zh-HK`, `zh-MO` | unavailable (D4): Simplified Chinese is not served to whoever asks for Traditional (D3) |
| any other (`de`, `pt-BR`…) | unavailable (D4): say so, name the available languages and continue as without a marker |

[scripts/resolver_idioma.py](../../../scripts/resolver_idioma.py) implements this rule; its source `defecto`
means “without a marker”, not “answer in Spanish”. For this list:

```
python3 <skill>/scripts/resolver_idioma.py --disponibles es,en,fr,hi,zh-Hans --defecto es --respaldo zh=zh-Hans --respaldo zh-CN=zh-Hans --respaldo zh-SG=zh-Hans --respaldo zh-TW=zh-Hant --respaldo zh-HK=zh-Hant --respaldo zh-MO=zh-Hant
```

## Fixed phrases of each language

They are shown only when the marker selects that language (D22): the notice opens every answer, and the
fail-safe line is added if you cannot read `i18n/<language>/` (D25).

| Language | Machine-translation notice | Fail-safe line |
|---|---|---|
| `en` | `Translation machine-generated, not human-reviewed.` | `English version unavailable; continuing with the Spanish files.` |
| `fr` | `Traduction automatique, non relue par une personne.` | `Version française indisponible ; poursuite avec les fichiers espagnols.` |
| `zh-Hans` | `机器翻译，未经人工审阅。` | `简体中文版本不可用；继续使用西班牙语文件。` |
| `hi` | `अनुवाद मशीन द्वारा तैयार किया गया है, मानव द्वारा समीक्षित नहीं। (Translation machine-generated, not human-reviewed.)` | `हिन्दी संस्करण उपलब्ध नहीं है; स्पैनिश फ़ाइलों के साथ आगे बढ़ा जा रहा है।` |

The Hindi notice is bilingual because that language is delivered as `experimental` (T6).

## What is not translated

Identifiers (R1…Doc9), module markers, file and script names, options, warning codes, commands and code
blocks. The scripts' messages stay in Spanish.
