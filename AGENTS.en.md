<!-- i18n fuente-sha256=7cf117033a1f estado=borrador-ia -->

# AGENTS.md

What you need to know before touching anything in this repository. It applies to AI agents and to people.

## What this is

A Claude Code plugin with a single skill, `multilang-repo-skill`, that guides an agent to make a
repository multilingual. The product is mostly normative prose: rules with an identifier that another
agent reads and follows. The only executable code is four helper scripts and their tests.

```
.claude-plugin/plugin.json            plugin manifest (name, version, author, license)
.claude-plugin/marketplace.json       single-plugin marketplace (source: "./")
skills/multilang-repo-skill/SKILL.md  core: loaded whole on every invocation
skills/multilang-repo-skill/references/  modules that the agent reads only if they are activated
skills/multilang-repo-skill/assets/      templates that the agent copies next to its log
skills/multilang-repo-skill/i18n/        mirror translation into English (en/), GLOSARIO.md and ESTADO.md
skills/multilang-repo-skill/scripts/     verificar_adiciones.py, validar_catalogos.py, resolver_idioma.py,
                                      comprobar_paridad.py
skills/multilang-repo-skill/scripts/tests/  unittest tests of the four scripts
README.en.md, AGENTS.en.md            English translations of these two documents
CHANGELOG.md                          changes by version, with the approved exceptions
docs/                                 audit, traceability, validation and report (not part of the skill)
```

## Commands

Run the tests with nothing piped after them, so that the exit code is `unittest`'s:

```bash
cd skills/multilang-repo-skill/scripts && python3 -B -m unittest discover -s tests
```

Today there are **138 tests** and all of them pass. If you see fewer, one is not being discovered.

```bash
claude plugin validate --strict .                 # manifest, marketplace and skill
wc -l skills/multilang-repo-skill/SKILL.md        # must stay below 500
```

Parity of the translations: no errors or warnings, with the AI note in both documents.

```bash
S=skills/multilang-repo-skill
python3 -B $S/scripts/comprobar_paridad.py --arbol $S $S/i18n/en --completo
python3 -B $S/scripts/comprobar_paridad.py --par README.md README.en.md --nota-ia "AI-assisted; requires human review."
python3 -B $S/scripts/comprobar_paridad.py --par AGENTS.md AGENTS.en.md --nota-ia "AI-assisted; requires human review."
```

`-B` prevents `__pycache__` from being created inside the skill: it must not end up in the package.

## Non-negotiable constraints

1. **Stable identifiers.** Rules are cited by identifier (R1–R20, D1–D31, P1–P15, T1–T7, C1–C9, S1–S6,
   G1–G9, M1–M7, Doc1–Doc9). Do not renumber or reuse one. A new rule gets the next free one and is added
   to `references/identificadores.md`; a withdrawn one leaves a line saying so (like S5). Each identifier
   is defined once and everything cited exists.
2. **Progressive loading.** `SKILL.md` below 500 lines, with the core (precedence, permissions, security,
   evidence, modes) always in it. The references hang directly from `SKILL.md`, at a single level, and each
   one appears in its Resources table with the moment when it is read. Only exception: `references/idioma-de-la-respuesta.md`, which is read from the delimited “Response language” block, because the original text of `SKILL.md` cannot change outside that block. A reference of more than 100 lines
   carries an index at the beginning.
3. **Valid frontmatter.** `name` equal to the folder's name, in kebab-case. `description` in valid YAML
   and at most 1024 characters. Beware of “: ” inside the text, which once broke the YAML. If you change
   the description, test activation again.
4. **Scripts.** Only the Python 3.8+ standard library. **They never write files.** `resolver_idioma.py` is
   total: no input makes it fail. The person's message reaches it from a temporary file redirected to
   standard input, never as an argument nor in a heredoc (a heredoc with a fixed delimiter admits
   injection; there is a test that demonstrates it).
5. **Test first.** A change of behavior in a script starts with a test that fails. Check that the new test
   detects the failure by deliberately breaking the code before accepting it.
6. **Coherence before additions.** Almost all the failures found were two rules, each correct on its own,
   that contradicted each other (for example, when to stop in guided and in autonomous mode). Before
   adding a rule, look for those that deal with the same thing and leave a single source; if a reference
   repeats something from the core, refer to it instead of copying it with nuances.
7. **Claims with a level.** In the skill and in `docs/`, “checked” or “verified” carry their level
   (`estática`, `local`, `ci`, `simulada`, `plataforma`, `humana`). Nothing designed is presented as
   executed. If you change something that `docs/VALIDACION.md` measures, update the figures or mark the
   check as pending.
8. **Nothing personal or local.** No absolute paths, usernames or data of whoever ran the tests. The tools
   and the raw evaluation data are not published in this repository.
9. **AI note only where it belongs.** Public documents for people (README, CHANGELOG, Release notes and the
   `.en.md` versions of README and AGENTS) end once, in their language, with “AI-assisted; requires human
   review.” (in Spanish: `Elaborado con asistencia de IA; requiere revisión humana.`). Never in files that
   a machine consumes (code, JSON, YAML).
10. **Prose in Spanish.** The skill's texts, the scripts' messages and the documentation are in Spanish
    with correct accents; names in code, in ASCII. Exception: `i18n/en/`, `README.en.md` and `AGENTS.en.md`
    are in English by design (constraint 11). The scripts' messages and `docs/` remain in Spanish.
11. **Spanish is the source; English is a mirror.** Every file in `i18n/en/` and every `.en.md` starts with
    `<!-- i18n fuente-sha256=… estado=… -->` carrying the fingerprint of its original
    (`comprobar_paridad.py --hash FILE`). If you change an original, the checker marks its translation as
    outdated: retranslate it, or check that it is still faithful and update the fingerprint. Identifiers,
    module markers, file names, options, warning codes and code blocks are not translated. Everything an AI
    translates is `borrador-ia` until an identified person reviews it (`i18n/ESTADO.md`,
    `i18n/GLOSARIO.md`). Changes to `description` and to the version in `SKILL.md` are approved as
    replacements of `verificar_adiciones.py` against the version's base commit.

## Publishing a version

1. Raise `version` in `.claude-plugin/plugin.json` and `metadata.version` in the frontmatter of `SKILL.md`
   together. If you do not change `version`, whoever already has the plugin does not receive the update.
   When `SKILL.md` changes, its fingerprint changes: update the header of `i18n/en/SKILL.md` and add the
   entry to `CHANGELOG.md`.
2. Run the tests, `claude plugin validate --strict .` and the parity of the translations.
3. Create the Release with the tag `vX.Y.Z` and attach `multilang-repo-skill.zip`, which contains the
   folder `skills/multilang-repo-skill/` (with `i18n/`) at the root of the ZIP, without `__pycache__` or
   `.DS_Store`. Check the ZIP by unzipping it into an empty folder and running the tests there.

---

AI-assisted; requires human review.
