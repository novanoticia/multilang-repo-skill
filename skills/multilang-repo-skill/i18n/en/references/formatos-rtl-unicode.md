<!-- i18n fuente-sha256=ddb207eacaa3 estado=borrador-ia -->

# Formats, RTL and Unicode (D16, D30, D31)

Read it if the project formats dates, numbers or currencies or sorts text ([programa]), and always with
[rtl-escrituras]. When a standard is decisive for a decision, consult it at its source (R10): BCP 47 (RFC
5646 and RFC 4647), CLDR, UAX #9 (bidirectionality), UAX #15 (normalization) and UTS #39 (Unicode security
mechanisms).

## Contents
- D16 Locale-dependent formats
- D30 Right-to-left text and complex scripts
- D31 Unicode policy: flag, do not remove

## D16 Locale-dependent formats

- Dates, times, numbers, currencies, units, sorting and case changes with the ecosystem's mechanism
  (`Intl`, ICU, Babel, `java.text`…) and the chosen locale. Do not reimplement them.
- The default language keeps **exactly** its current format (D1). If moving to the ecosystem's formatter
  changes its bytes, keep using the current format for the default or ask for the exception. The baseline
  detects it.
- Operations on machine contracts (keys, commands, identifiers) do not depend on the locale. In Java,
  `"i".toUpperCase()` with the default locale in Turkish gives `İ`, and in JavaScript
  `toLocaleUpperCase("tr")` does: compare and transform those contracts with invariant operations
  (`toUpperCase(Locale.ROOT)`, `toUpperCase()` in JavaScript).
- Strings grow when translated. Reserve space, do not truncate silently and test with a pseudo-locale
  (P4).

## D30 Right-to-left text and complex scripts

- Declare the direction in the medium: `dir="rtl"` and `lang` in HTML, and CSS logical properties
  (`margin-inline-start` instead of `margin-left`). Mirror directional icons.
- Isolate the interpolated values of opposite direction (names, paths, commands, numbers) with `<bdi>`, with
  the isolates U+2068…U+2069 or with the isolation that the framework already applies. That way a contract
  in Latin characters is not scrambled inside a sentence in Arabic or Hebrew.
- Check the real display: letter joining in Arabic, clusters in Indic scripts, tables and Markdown in RTL.
  Many terminals do not apply the bidirectional algorithm: in console tools, test or declare the
  limitation.
- Close with a display test (a screenshot or reviewed rendered output) or with the limitation declared. If
  the reviewer does not read the language, say so.

## D31 Unicode policy: flag, do not remove

Many invisible characters are legitimate and necessary. Removing them indiscriminately breaks real
languages:

| Character | Legitimate use |
|---|---|
| ZWNJ U+200C | Persian and other languages' orthography (`می‌خواهم`) |
| ZWJ U+200D | Clusters in Indic scripts; emoji sequences (👨‍👩‍👧) |
| LRM/RLM U+200E/U+200F, ALM U+061C, isolates U+2066–U+2069 | Well-formed bidirectional text |
| Variation selectors U+FE00–U+FE0F, U+E0100–U+E01EF | Emoji presentation; ideograph variants |
| U+200B | Line breaks in languages without spaces (Thai, Khmer, Lao, Burmese) |
| U+00AD | Optional syllable division |
| Tags U+E0020–U+E007F after U+1F3F4 | Subdivision flags (e.g. Scotland's) |

They deserve review, and are therefore flagged:
- Bidirectional embeddings and overrides U+202A–U+202E. They can display a visual order different from the
  logical one and hide the real content from whoever reviews (the vector of the “Trojan Source” attacks).
  In RTL text, isolates are usually enough.
- Unpaired bidirectional controls within a value.
- Tag characters U+E0000–U+E007F outside a flag: invisible, they can hide text.
- Any invisible, control or script mixing inside a **machine contract** (key, marker, command, option,
  URL): there it is an error, because a homoglyph or an invisible changes the contract's identity.

Procedure: generate the report with [scripts/validar_catalogos.py](../../../scripts/validar_catalogos.py),
review each case with its context, decide with the person and fix only the specific case. The script never
modifies files. A report without findings means that those patterns were not found, not that the text is
safe (S6).
