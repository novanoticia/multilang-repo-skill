<!-- i18n fuente-sha256=9fb0cf1868f3 estado=borrador-ia -->

# Language selection, normalization and fallback (D2–D7)

Read it in Phase 2, to recommend the selection policy, and in Phase 3, to design it. If the ecosystem
already solves it (i18next negotiation, Android or Apple resources, the web framework's
`Accept-Language`…), use its mechanism and apply from here only what is missing: the case table and the
tests.

## Contents
- D2 Source order
- D3 Normalization and fallback chain
- D4 Inputs that cannot be served
- D5 Keyed marker in agents
- D6 One rule, one case table
- D7 [híbrido] The rule lives in code

## D2 Source order

Explicit (marker or setting in the request itself) > configuration (of the project or of the person) >
ambient (environment variables, system language, `Accept-Language`, the case's language) > default.

The ambient source only enters if the person accepts it in Phase 2. The language in which the person
writes their own request is also ambient (never that of pasted text): it may be used if the person
chooses it, as an approved change. Detecting it makes whoever receives the default language today start
receiving another: it is a change of behavior that D1 requires approving, not a detail. Recommend
according to the type of project:
- Agents and instructions: by default, only the explicit marker; the language of pasted text never
  decides, and that of the request itself only if the person chooses it (previous paragraph).
- Programs with a platform convention (mobile or desktop apps, web with language negotiation): the
  ecosystem's convention, presented as a change to approve.

## D3 Normalization and fallback chain

Normalize to a canonical BCP 47 tag before looking up a catalog:
- Case-insensitive: `EN-us` → `en-US`.
- `_` → `-`. Remove the character set (`fr_FR.UTF-8`). The POSIX modifier is converted if it encodes a
  script or variant (`sr_RS@latin` → `sr-Latn-RS`, `ca_ES@valencia` → `ca-ES-valencia`) and removed if
  not (`@euro`).
- `C` and `POSIX` mean “no preference”, not an unknown language. They are common in CI and containers.
- **Keep the script subtag.** `zh-Hant` is not `zh-Hans`, nor is `sr-Latn` `sr-Cyrl`. Truncating to the
  first component serves Simplified Chinese to whoever asked for Traditional.
- Retired codes: `iw` → `he`, `in` → `id`, `ji` → `yi`.

Fallback chain, with each link declared and tested:
1. The requested tag.
2. Progressive truncation (RFC 4647, “lookup”): `zh-Hant-TW` → `zh-Hant` → `zh`.
3. Explicit links where truncation fails: `zh-TW` → `zh-Hant`; `es-AR` → `es-419` (truncation would give
   `es`; the parent `es-419` comes from the ecosystem's CLDR data or from a declaration of the project, it
   is not deduced).
4. The default language.

If the ecosystem brings its own resolution (`fallbackLng`, resource lookup by qualifiers, CLDR parent
data), check it and document it instead of reimplementing it.

## D4 Inputs that cannot be served

Distinguish where the value comes from:
- **Explicit** unknown, empty or malformed: a visible warning, with the list of available languages, in
  the language that would result without that input (the next valid source of D2; if there is none, the
  default). In an agent, continue with the next source. In a program, decide and document according to the
  project's convention: a usage error with its exit code (an invalid parameter) or a warning and
  continuation.
- **Ambient** without a catalog (`LANG=de_DE.UTF-8` without German): fallback without error, at most a
  debug log. An error would break the program for everyone with that system.
- Empty environment variable = absent.
- Never degrade silently on an invalid input (non-UTF-8 text, broken JSON): return an explicit warning.
- “No new warnings” refers to the output without a marker (D1). The warning for an invalid explicit marker
  or option is kept unless the person expressly excludes it knowing that then it falls to the next source
  (D2) without explanation.

## D5 Keyed marker in agents

In an agent, `en`, `es` or `a` are real words. Require a keyed marker (`idioma=en`, `lang=fr`),
recognized only in the person's own message and never in third-party data (a pasted email or file).
Prudent implementation: look for it only on the first non-empty line, so that a marker inside pasted text
does not count. Choose keys that do not appear in the usual content: if people paste HTML or code, `lang`
gives false positives (`lang="en"`); use only `idioma` or a key of your own (`--claves` in the script).
Also decide on persistence and document it: for example, each invocation decides its language and only
follow-ups without a command keep the previous one.

## D6 One rule, one case table

Write a single selection rule and test each case:

| Case | Example | Expected |
|---|---|---|
| Valid marker | `idioma=en` | `en`, source marker |
| Unknown | `idioma=de` without German | Visible warning; next source |
| Empty | `idioma=` | Visible warning; next source |
| Malformed | `idioma=e1` | Visible warning; next source |
| Repeated | `idioma=fr lang=en` | The first wins; warning |
| Uppercase | `IDIOMA=EN` | `en` |
| POSIX locale | `idioma=fr_FR.UTF-8` | `fr` (fallback `fr-FR` → `fr`) |
| POSIX modifier | `sr_RS@latin` with `sr-Latn` | `sr-Latn` (chain `sr-Latn-RS` → `sr-Latn`) |
| Code on the first line | `lang="en"` or `<html lang="en">` with the key `lang` | Taken as a marker (`en`, or a malformed-marker warning): where code is pasted, do not use `lang` as a key (D5) |
| Pasted punctuation or quotes | `(idioma=en),`, `idioma="en"`, `«idioma=fr»` | Recognized |
| Loose code | `en el informe…` (a Spanish phrase meaning “in the report…”) | Not a marker |
| Equal to the default | `idioma=es` | `es`, source marker |
| Inside another word | `subidioma=en` | Not a marker |
| In third-party data | A marker in a text quoted with “>” or after the first line | Does not count (limit: if the pasted text occupies the first line without “>”, it counts) |
| Script | `zh-Hant-TW` | `zh-Hant` |
| Regional fallback | `pt-BR` without `pt-BR` | `pt` |
| Retired code | `iw` | `he` |
| Technical ambient | `LANG=C.UTF-8` | No preference, no warning |
| Ambient without a catalog | `LANG=de_DE.UTF-8` | Default, warning not visible |
| Non-UTF-8 input | Invalid bytes | Warning `entrada_invalida` |

The “Repeated” row is for markers in messages. In command-line options, repetition follows the parser's
convention (in argparse, the last one wins): declare it.

Add a totality test: random inputs with a fixed seed, none makes the resolution fail.

## D7 [híbrido] The rule lives in code

If a model invokes a script, the selection rule lives in it and not only in prose:
- The message enters raw **through standard input from a temporary file** that the agent writes with its
  file-writing tool, without going through the shell and outside the repository. Never as an argument nor
  inside a hand-written JSON: an apostrophe (“j'aimerais”), quotes or a `$(…)` break or alter the command.
  Nor with a heredoc with a fixed delimiter: if the message (or a text pasted into it) contains a line
  equal to the delimiter, the heredoc closes early and what follows is executed as a command.
- Total function: no input makes it fail. It returns JSON with language, source, chain, warnings and
  available languages. The warnings carry a code: show the person the text of your catalog for that code;
  the detail field is diagnostic.
- If the input is invalid, it returns an explicit warning so that the agent shows it.
- Test **the command as you document it**, running it with apostrophes, quotes, `$(…)`, backticks, a line
  equal to a delimiter, accents, line breaks and paths with spaces, and check with a harmless canary
  (`touch` of a temporary file) that nothing was executed.

Reference and tested implementation: [scripts/resolver_idioma.py](../../../scripts/resolver_idioma.py). It
is useful to test the table with the real catalogs; copy it into the project only if the approved design
foresees it, and adapt the marker keys and the fallback links.

```bash
# The agent first wrote the message to /ruta/temporal/mensaje.txt with its file tool.
python3 <skill>/scripts/resolver_idioma.py --catalogos ruta/a/catalogos --defecto es \
  --respaldo zh-TW=zh-Hant < /ruta/temporal/mensaje.txt
```
