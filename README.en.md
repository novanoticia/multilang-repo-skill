<!-- i18n fuente-sha256=a9b043ab189b estado=borrador-ia -->

# MultiLang Repo Skill

A Claude Code skill that guides an agent to make a repository multilingual: programs, libraries,
servers, CLIs, skills, plugins, instructions for models, hybrid projects and repositories that already
use i18next, gettext or ICU.

The agent discovers the project, separates text for people from machine contracts, asks only what the
person decides, designs in proportion to the project, checks with evidence of a declared level and
publishes only what is authorized, action by action.

## Installation

As a plugin, from this repository:

```
/plugin marketplace add novanoticia/multilang-repo-skill
/plugin install multilang-repo-skill@multilang-repo-skill
```

Or by copying the skill's folder by hand: `skills/multilang-repo-skill/` goes in `~/.claude/skills/` (for
all your projects) or in `.claude/skills/` of a repository. Check that it shows up with `/skills`.

## Examples

1. “Make this repository multilingual: Spanish (reference) and English. Guided mode.”
2. “Before touching anything, audit this repo's language support and tell me which texts are hardcoded
   and which are machine contracts.” (analysis only: it modifies nothing)
3. “Add French and pt-BR to the app, which already uses i18next. Autonomous mode; you may push the `i18n`
   branch every time you finish a task, nothing more.”
4. “idioma=en Make this repository multilingual: Spanish (reference) and French. Guided mode.” (the skill
   answers in English).

## Languages

The skill is in Spanish (the reference language) and has an English translation. To ask for the answer in
English, write `idioma=en` (or `lang=en`) on the first line of your message. Without a marker it answers
in Spanish, as before: the language you write in is not detected. An unavailable language gives a notice
and continues in Spanish. The translation is a `borrador-ia` (AI draft) with no human review (status in
[skills/multilang-repo-skill/i18n/ESTADO.md](skills/multilang-repo-skill/i18n/ESTADO.md)). This README is
also available in [Spanish](README.md). <!-- i18n:exento -->

## What it includes

```
skills/multilang-repo-skill/
├── SKILL.md       core: activation, precedence, permissions, security, evidence, modes, scale, modules, workflow and closing
├── references/    12 modules that are read only if they are activated
├── assets/        5 templates (data and scope, session log, inventory, scenarios, evidence)
├── i18n/          English translation (mirror of the above), glossary and translation status
└── scripts/       verificar_adiciones.py, validar_catalogos.py, resolver_idioma.py, comprobar_paridad.py and their tests
```

The scripts use only the Python 3.8+ standard library and never modify files. To run their tests:

```
cd skills/multilang-repo-skill/scripts && python3 -B -m unittest discover -s tests
```

## Status

Version 9.1.0 (unpublished as of 2026-10-11). What has been checked, with its level (details of 9.0.0 and
the 9.1.0 addendum in [docs/VALIDACION.md](docs/VALIDACION.md)):

- **9.0.0:** skill validator, structural checks and identifier checks without errors (`local`); 78
  tests of the scripts with Python 3.14 and 3.9 and sabotage with 32 of 32 mutants detected (`local`);
  real activation in Claude Code and simulated behavior scenarios (17 runs, three versions of the
  skill), graded by agents other than those that ran them (`plataforma` (platform), `simulada`
  (simulated)).
- **9.1.0:** 138 tests with Python 3.9, 3.10, 3.13 and 3.14 (`local`); `comprobar_paridad.py` with 38
  of 38 mutants detected (`local`); structural parity of the 18 files of `i18n/en/` with their originals
  (`local`); `claude plugin validate --strict` without errors (`local`).

Limits: it has had no human review nor real use in projects; the scenarios are simulations with one run
each. The English translation is a `borrador-ia` that no person has reviewed. Activation and the
scenarios were measured with the `description` and the text of 9.0.0: 9.1.0 changes them (`description`
from 966 to 1023 characters and a new block in `SKILL.md`) and they have not been repeated (`pendiente`
(pending), `plataforma`). Uploading to claude.ai has not been tested (its help limits `description` to
200 characters and this one has 1023).

## Documentation

- [CHANGELOG.md](CHANGELOG.md): changes by version, with the approved exceptions and how to withdraw them.
- [docs/INFORME-ENTREGA.md](docs/INFORME-ENTREGA.md): summary, structure and use.
- [docs/AUDITORIA.md](docs/AUDITORIA.md): audit of the framework's previous versions (v1–v8).
- [docs/TRAZABILIDAD.md](docs/TRAZABILIDAD.md): changes with respect to v7 and the fate of each v8 proposal.
- [docs/VALIDACION.md](docs/VALIDACION.md): how it was validated and with what results.

Those documents cite `evaluacion/` and `entrega/`, folders of the working environment where the tests
were done; the tools and the raw evaluation data are not published here. The documents in `docs/` and the
`CHANGELOG.md` are in Spanish.

## License

[MIT](LICENSE).

---

AI-assisted; requires human review.
