<!-- i18n fuente-sha256=12f34a8dd4e7 estado=borrador-ia -->

# Catalogs, keys and execution (D8–D15, D17–D20)

Read it with [ecosistema], [programa] or when the project is going to have catalogs of its own.

## Contents
- First, the ecosystem
- D8–D13 Catalogs and keys
- D14–D15 Execution and interpolation
- D17–D20 Data, artifacts and language-dependent logic

## First, the ecosystem

If the project already has i18n or its ecosystem has a standard (gettext, i18next, ICU MessageFormat or
MessageFormat 2 if it already uses it, Fluent, Rails I18n, `strings.xml`, String Catalogs, ARB…), use its
format, its extractor, its plural rules, its fallback and its validator. Then D8–D9 are superfluous and
your work is coverage, glossary, tests and review. `validar_catalogos.py` only adds value if the format is
own JSON or i18next and the project has no validator (P6); it does not interpret ICU or ARB. Carry what
follows over to the format's native mechanisms: context with `msgctxt` and translator comments in gettext,
`@key` with `description` in ARB, notes in XLIFF, `translatable="false"` in Android. Do not impose fields
or encodings that the format does not admit.

Without i18n in place, the ecosystem is the language's or framework's standard mechanism. Check what it
covers without installing anything: Python's `gettext` module only reads already-compiled `.mo` files;
extracting and compiling requires `xgettext` and `msgfmt` (GNU gettext) or Babel. If they are missing,
installing is a decision (R2): present it with the own catalog (D8) as an alternative. `.mo` files are
versioned only if the project has no build step, with a test that compares them with their `.po` by
content (loading them, e.g. with `gettext.GNUTranslations`), not by bytes: different compilers give
different bytes. If the tool is missing, the test is skipped and it is declared.

## Catalogs and keys

**D8 Own catalog (only without an ecosystem).** One file per language, discovered when added: the code
does not enumerate the languages and auxiliary files (glossary, schema) do not count as a language. Access
with `t(key, **data)` or, in instructions, a `key → phrase` catalog that the model copies literally.
- If a key is missing, it falls back to the default language and is logged (in tests, it fails). If it is
  also missing in the default, it is a programming error.
- Per-key fallback mixes languages in the output. A language is only published as complete when the
  validator reports it complete. A partial one may be in the repository marked `experimental` (D12), with
  its limitation declared; the validator reports it as partial coverage, not as an error.

**D9 The default language is the reference.** Its phrases are the original's literals: they are extracted
with tools (P3), not rewritten by hand. It may carry new keys (notices that the original did not have),
marked as `origen: nuevo` (origin: new).

**D10 One literal, one key.** One key per complete phrase, also for headings, labels, stop questions and
each option list as a unit. Do not compose phrases from translated pieces.
- Plurals: use the language's CLDR categories (`zero`, `one`, `two`, `few`, `many`, `other`; each language
  uses a subset) with the ecosystem's mechanism: ICU plural, i18next suffixes, `ngettext` with
  `Plural-Forms`, `<plurals>`. Two keys (`uno`/`otros`, that is, one/others) are only valid if all the
  supported languages and the numbers shown use those two categories. If not, declare the limitation.
- [instrucciones] Distinguish “catalog literal: copy it as is” from “bracketed instruction: write it
  yourself”. A bracketed option list is not an instruction. Set a single policy for filling in the
  bracketed gaps.

**D11 Metadata per key, in proportion.** In own catalogs: `origen` (origin: `original` | `nuevo`),
`fuente` (source: file and line of the original, counted without added blocks), `contexto` (context: one
line for whoever translates or reviews: where it appears, what it means, length limit), `riesgo` (risk:
`alto` on phrases that confirm irreversible actions, limits or security), `invariable` (justified by the
text itself: symbols, codes or proper names) and `maquina` (machine: identical in all languages). At scale
S, `contexto` and `riesgo` where needed are enough. In ecosystem formats, use their native mechanism.
Shape in own JSON: the metadata goes in the reference as `"@key": {"contexto": …, "riesgo": …,
"invariable": true}` (ARB style), which the validator excludes from parity. What is invariant in all
languages is declared there; what is identical only in one language (frequent among close languages) is
declared in that catalog, in `_meta.invariables`, with its reason.

**D12 Status of each language.** `referencia` (reference), `borrador-ia` (AI draft), `experimental` or
`revisado` (reviewed), with who drafted and who reviewed. `experimental` is an incomplete `borrador-ia` or
one of a language that cannot be judged: besides not being reviewed, it carries a reinforced notice (T6).
`revisado` requires an identified reviewing person; another model's opinion does not change the status.
When there is human review, updating the field is enough. Where it is recorded: in own JSON catalogs, in
`_meta`; in ecosystem formats that do not admit that field (e.g. i18next JSON that the application loads
as is), in the project's documentation (languages section of the README) or in a separate status file,
never by adding fields that the loader would display or reject.
[scripts/validar_catalogos.py](../../../scripts/validar_catalogos.py) checks this consistency in JSON
catalogs (`_meta.estado`, `_meta.revisado_por`).

**D13 Shape of the file.** First, what the ecosystem's format requires: some formats declare their
encoding in the header and legacy formats are not UTF-8, so check it instead of assuming it. With no
imposed format: UTF-8 without BOM, final line break, deterministic key order and Unicode NFC in new
translations. Do not normalize the reference literals if that changes the bytes of the default output
(D1); declare it as a limitation or ask for the exception.

## Execution and interpolation

**D14 Language state at runtime.** In a single-request process, a global language fixed at startup is
enough. In servers, concurrent jobs or libraries, the language goes per request or per context, never in a
shared global variable.

**D15 Templates and interpolation.** Only named fields. Literal braces are escaped, and the interpolated
datum is never reinterpreted as a template, as markup or as an instruction. In instructions for a model,
delimit the interpolated datum as data (S1).

## Data, artifacts and language-dependent logic

**D17 Texts in configuration data.** The original language stays where it is and the others override it by
key: a single origin per text and language. If there was a language field that was ignored and is now
read, it is a change that goes to the CHANGELOG.

**D18 Artifacts (E).** Decide with the person whether the chosen language affects them. Ensure they do not
mix languages and declare the language in the formats that admit it (`lang` in HTML, metadata in PDF).
Adding that attribute to the default output changes its bytes, so it is an exception to approve (D23).

**D19 What is advised must be recognized.** If the program advises a phrase in a language, its detector
must recognize it in that language. The phrases that activate a mode (“execute”, “undo”) are also catalog
literals. The values shown in prose that come back as input are recognized by equivalence with the
catalog.

**D20 `--help` and parser errors.** They are usually built before the language is known: translate them by
resolving the language before building the parser, or declare the limitation. The messages of auxiliary
scripts may stay in the original language if it is declared. A new option (`--idioma`) by itself changes
the help and the usage line in the default language. If the person asked for that option, the change is
part of what was requested: it goes in the list of changes (D1), it is said in the summary and the rest
is compared byte for byte. If they did not ask for it (the selection is by marker or variable), do not
show it without approval: hide it from the help (e.g. `help=argparse.SUPPRESS`) and document it
separately. Hidden or not, a new option changes the abbreviations that argparse accepts (`--i` becomes
ambiguous if `--input` already existed): choose a name with no common prefix with the existing options or
include in the baseline (P2) the abbreviations that work today.
