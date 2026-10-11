<!-- i18n fuente-sha256=d085019ed69a estado=borrador-ia -->

# Plan, baseline, tests, review and triage (P1–P15)

Read it in Phases 4 and 8. Apply it according to the approved scale (R20 table in SKILL.md) and record each
check with its level (R7) in [assets/evidencias-y-cierre.md](../assets/evidencias-y-cierre.md).

## Contents
- P1–P3 Plan, baseline and extraction
- P4–P8 Tests and validation
- P9–P12 Package, CI and pace
- P13 Evaluating instructions by scenarios
- P14–P15 Independent review and triage

## Plan, baseline and extraction

**P1 Plan.** Small tasks, each with its test, its files and its criterion of “done”. If the real scope is
larger than expected, say so before continuing. In guided mode, the plan is approved before implementing
and each task closes with its summary; in autonomous mode, it is recorded and presented as a correctable
assumption (R18).

**P2 Baseline, before touching anything.** Generate it from the base commit (`git show <base>:<path>`),
not from the working copy, and make it deterministic: fixed date and paths, controlled environment and
binaries or zips compared by content.
- Programs: outputs per default language in the representative modes and error paths.
- Instructions: `verificar_adiciones.py` with the closed list of approved replacements (empty if
  everything is additions). The version lines that the version script automates are approved with a
  pattern.
- Manifests: equal except for the version.
- `git diff --numstat` is not enough. It counts lines, but does not say which ones changed: changing a
  non-approved line instead of an approved one gives the same figure.

**P3 Extraction with tools.** In this order: the ecosystem's extractor; a script that reads the real
literal (AST or codemod when the volume justifies it); and, at scale S, by hand, with a check that each
literal exists as is in the original. The extractor fails on zero and on several matches, and withstands
repeated phrases, phrases split across several lines, quotes and indented blocks. Coverage: all visible
text is a literal with a key or a declared instruction; what is excluded is listed with its reason.

## Tests and validation

**P4 Pseudo-locale.** Apply it when the text reaches an interface or console through code; if it adds no
value (few strings and all inventoried), omit it with its reason. Generate a synthetic language: each
phrase wrapped in visible markers, with accents and 30 % longer. What comes out without markers is a
literal outside the catalog; what comes out cut off, a space problem. It is a `local` run, not a
simulation. It is not distributed and does not apply to text that a model generates.

**P5 Tests first, where they provide evidence.**
- Code with new behavior (selection, fallback, formats, scripts, validators): write the test, watch it
  fail and then implement.
- Invariance tests (default output the same, contracts the same): they pass from the start by design.
  Their value is shown by deliberately breaking what they protect (P7), not by seeing them red.
- Content (catalogs): the validator acts as the test.
- Documentation: no TDD.

Do not invent red tests out of ceremony.

**P6 Catalog validation.** Use the ecosystem's validator first. For own JSON catalogs or i18next ones
without a validator (not ICU or ARB), use [scripts/validar_catalogos.py](../../../scripts/validar_catalogos.py):

```bash
python3 <skill>/scripts/validar_catalogos.py ruta/catalogos --referencia es \
  [--marcadores llave|doble-llave|printf] [--plurales sufijo] [--idiomas es,en,fr]
```

Basic checks: same keys; nothing empty or `TODO`; named markers identical across languages; what goes in
backticks identical; lists with the same number of entries; texts identical to the reference only if
declared invariant; status consistent with the reviewers (D12); shape (D13); and Unicode (D31). Add the
project's own rules: glossary, data formats and high-risk phrases with untranslated words of the original
(as a heuristic, not as truth; P8). If the validator fails on your content, fix the content, not the
validator.

**P7 Sabotage of the checks you write.** A new check only counts if it has been seen to fail against the
breakage it is meant to detect. Break a copy on purpose, one thing at a time:
- Guard: measure nothing if the unbroken suite does not pass in the same environment.
- Each breakage is applied exactly once. If it does not find its target or finds it several times, it is
  a tool failure, not a success.
- Record which check detects each breakage. If only a generic test (paths, environment) detects it, it
  counts as undetected.
- Survivors are closed with a new test or reasoned away as equivalent. “100 %” or “N of N” is never quoted
  before passing the guard.
- At scale L, also measure with breakages you did not design yourself (those of an independent reviewer),
  if there is one.
- Typical failures: assertions that accept a phrase repeated elsewhere, numbers that match by chance,
  tautological tests, YAML read at the wrong level, normalizations that hide changes. A test that pins
  literal strings is a snapshot, not a behavior test: say so.
- Do not sabotage the ecosystem's standard tools or this skill's scripts: they already have their own
  tests. A copy adapted to the project (D7) is your own code.

**P8 Heuristics between close languages.** A shared-words heuristic can be useless between close
languages (Spanish, Galician, Portuguese, Catalan). If it is, omit it visibly (a skipped test with its
reason) and replace it with orthographic markers or a word-by-word review. Ignore what goes in backticks.

## Package, CI and pace

**P9 [paquete] Package test.** In a temporary copy without `.git` or previous artifacts, run the real
packaging and compare the listing with what is expected: not one file too few (a new subfolder that the
script does not copy) nor one too many (tests, session log, copies of the templates, tools). Show the
listing (`unzip -l` or equivalent).

**P10 CI.** Use the one there is. Propose a minimal one only if the person wants it: read-only
permissions, full history only if the tests compare with git, and the validators and tests of your scale.
A workflow that has never run is not evidence. The name of the check is the job's `id`, or its `name`, and
it is confirmed in a real run. Read the results with the platform's tools, without polling loops. Without
permission to push there is no run: the level stays at `local` and CI at `pendiente`. A claim about the
state of CI cannot be watched from the repository: give it a date and a reference (R8). If the person asks
for “CI green” and there is no CI or remote, say so in the message, not only in the log: there is no CI
that can turn green nor a way to check it from here. Without CI, the status is `no aplica` with that
reason; if the person accepts a minimal workflow, it stays `pendiente` until it runs on the platform. The
suite in green is reported as `local`.

**P11 Maintainable version tests.** If a test pins the version number, the next version change will turn
CI red. Make it read the version from the manifests.

**P12 After each task.** The checks of your scale, green: suite, validator, baseline and, if you changed
checks, their sabotage.

## P13 Evaluating instructions by scenarios

For what only a model can show (response language, notices, fail-safe, resistance to instructions in
data). Template: [assets/escenarios-evaluacion.md](../assets/escenarios-evaluacion.md).
1. **Pre-register** before running anything: input, pass criterion, fail criterion and an example of each.
   The expected texts come from the catalogs. The criterion tolerates legitimate variations (filled-in
   gaps, numbers) without being so weak that any output passes.
2. **Run** each scenario in an isolated context (a new subagent, another session), with the package built
   by the real script and the scenario's message in the prompt. Whoever runs does not know the pass
   criterion. Whoever evaluates is another agent or a person. Fictitious cases, marked as such.
3. **Read** answers and notes, not just the verdict: findings appear that no criterion foresaw. Ask the
   runner which files it read and what seemed ambiguous to it.
4. If you change a criterion after seeing results, record it as a later change with its reason.
5. After fixing, a second round only with the affected scenarios, new runners and the same criteria.
6. Declare the limits: it is a simulation, not the real platform; the list of files read is declared by
   the runner itself; one run per scenario does not measure variability; models are not human review.
   Leave a table for the real runs (platform, model, date, result).
7. If there are no isolated contexts or the person does not authorize delegating (M1), the scenarios stay
   pre-registered and `pendiente`. Do not act them out in your own context to present them as executed.

## Independent review and triage

**P14 Review.** Independent means a clean-context reviewer, with read-only access, who does not receive
your conclusions: a subagent if available and authorized (M1) or a person. If not, do a self-review and
declare it as such. Minimum checklist: literal braces and data with braces; contamination from the
development environment; codes shaped like locales; machine format the same across languages; incomplete
catalogs; mixed languages in outputs and artifacts; advice that the program's own detector does not
recognize (D19); conflicts between rules (D21); bracketed lists treated as instructions; persistence of
the language; notices missing on paths that stop; paraphrases of official names; literals without a key;
inputs that degrade silently; installation routes without the new files; and figures in the documentation
that no longer add up. With high risk, human review of what is critical.

**P15 Triage.** What is critical and important is fixed with a test that fails first (or with the
breakage that shows the check). What is minor is noted with its reason for the report. What would alter
the default output or the contract with the original is noted and not touched without approval. After
fixing, repeat the sabotage of the new checks.
