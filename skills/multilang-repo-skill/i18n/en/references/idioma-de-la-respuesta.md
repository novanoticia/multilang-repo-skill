<!-- i18n fuente-sha256=9d873c92e736 estado=borrador-ia -->

# Response language of this skill

Detail of the “Response language” block of `SKILL.md`. Read it when the person asks for a language with
`idioma=xx` or `lang=xx`, or when you doubt what is translated and what is not. The selection rules, the
machine-translation notice and the fail-safe are in the block; only what completes it is here.

## Contents
- Which languages exist and how a marker is resolved
- What is not translated

## Which languages exist and how a marker is resolved

- Available: `es` (the original files) and `en` (folder `i18n/en/`).
- A variant such as `en-GB` or `en_US.UTF-8` falls back to `en`, case-insensitively.
- [scripts/resolver_idioma.py](../../../scripts/resolver_idioma.py) implements this rule. Its source `defecto`
  means “without a marker”, not “answer in Spanish”: without a marker R16 governs (the person's language).
- The marker chooses the response language, not the languages a repository is translated into.

## What is not translated

Identifiers (R1…Doc9), module markers, file and script names, options, warning codes, commands and code
blocks. The scripts' messages stay in Spanish.
