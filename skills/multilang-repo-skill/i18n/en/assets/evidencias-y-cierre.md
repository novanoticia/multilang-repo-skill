<!-- i18n fuente-sha256=a3513292736f estado=borrador-ia -->

# Evidence and closing

One row per criterion. Status `superada` (passed) only if the check was really run and with that result.
What was designed and not run stays `pendiente` (pending), and what does not apply, `no aplica` (not
applicable) with its reason.

## Evidence table

| Criterion | Module / rule | Evidence (exact command or artifact) | Level (R7) | Status | Reference (commit, run, date) | Notes |
|---|---|---|---|---|---|---|
| Default output or original without unapproved changes | D1, P2 | | | | | |
| Machine contracts equal in all languages | B, P6 | | | | | |
| Requested languages in all modes and error paths | [programa] | | | | | |
| Instruction invariants per language | [instrucciones], P13 | | | | | |
| Language selection: case table and totality | D6, D7 | | | | | |
| Adding a language = dropping in a file; the validator says what is missing | D8, P6 | | | | | |
| No literals outside the catalog | P3, P4 | | | | | |
| Own checks sabotaged, with a guard | P7 | | | | | |
| Truthful translation status | D12, T5 | | | | | |
| Independent review or declared self-review | P14 | | | | | |
| Package with exactly the expected files | [paquete], P9 | | | | | |
| Platform CI | P10 | | | | | |
| External content with source level and validity | [contenido] | | | | | |
| Adversarial scenarios | [seguridad], S3 | | | | | |
| Human review of the risk phrases | [alto-riesgo] | | | | | |
| Each publication, authorized and recorded | R13, G | | | | | |

## Final report

1. **What there is now.**
2. **Own errors and corrections:** withdrawn figures, data from memory that turned out false, invalid
   tests, criteria changed after seeing results, and their effect.
3. **Decisions you took on the person's behalf** and their cost if they were wrong.
4. **Deviations from the skill**, citing identifiers and the reason.
5. **Evidence table** (above).
6. **Known limitations.**
7. **Pending items**, with their reason.
8. **What is up to the person:** merging, Release, branch protection, human review, tests on the real
   platform, domains or credentials.
9. **Delegation:** M7 log, or “there was no delegation”.

If the session was compacted along the way, rebuild the report from the session log, not from memory.
