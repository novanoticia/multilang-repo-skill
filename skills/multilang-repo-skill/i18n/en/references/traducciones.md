<!-- i18n fuente-sha256=b2f653950637 estado=borrador-ia -->

# Translations and high risk (T1–T7, D26)

Read it in Phase 5 and whenever [alto-riesgo] is active.

**T1 Glossary before translating.** Fix the terms and the form of address (`tú` or `usted`, `tu` or `vous`) and
always use them the same way. Guard it with a test proportional to the scale, and document the chosen form
of address.

**T2 Keep what is not prose.** Markers, emojis, format and machine contracts stay intact. Do not
translate product names, commands, modes, options, paths or codes (B1); values of closed vocabulary that
are only displayed (B2) are translated in prose, with the literal next to them if the person has to type
it. Respect the typography of each language (quotation marks «», spaces before certain signs in French)
and note the choice, because a native review may prefer another.

**T3 Close languages.** If your translation turns out identical to the original and the validator points
it out, look for the language's own wording; do not add exceptions to make it pass. Mark it invariant only
if the text justifies it (symbols, codes, proper names) and note the reason.

**T4 Official names (G).** Copy them from the official source in each language, reading the column by its
heading and not by its position, and check that it does not return the wrong language. If there is no
official version, use the code plus the official name available. If the source is inaccessible, apply R10
(`segunda-mano` or `no-comprobado`, and to pending items).

**T5 Honest status.** What an AI translates stays as `borrador-ia` (AI draft, D12): say so in the
repository and in the delivery (the report to the person; a notice in the runtime output is decided in
Phase 2, D22), and do not present it as reviewed. That another model reviews it does not make it reviewed.
Do not attribute reviewed linguistic quality to what has only gone through an AI.

**T6 Least certain language.** Say which language you judge with less certainty and why. A language you
cannot judge is delivered as `experimental` (which implies `borrador-ia`, D12), with a reinforced notice
(e.g. bilingual) and an indispensable native review, and only if the person authorizes it after knowing
the risk.

**T7 Free text of the model (H).** It does not fit in a catalog. Tell the model to write it in the chosen
language and declare in the documentation that it is unreviewed.

## [alto-riesgo]

**D26 Risk phrases.** Identify them one by one (`riesgo: alto`): confirmations of irreversible actions,
professional limits, safety warnings, doses, deadlines and obligations. Do not “improve” them when
translating them. Take care with constructions that invert the meaning (negative questions answered with
yes or no, double negatives). In languages you cannot judge, flag them as risk instead of rewording them if
that changes the contract with the original.

Requirements of the module:
- Two distinct human reviews before any professional use: that of the content, by a person who is a
  specialist in the domain (C8), and that of the translation of the risk phrases, by a native person (and
  a specialist where applicable). One does not replace the other. If it does not exist yet, the repository
  and the delivery say “pending human review” instead of treating the work as closed.
- Commits or PRs marked for human review of the diff, starting with the `riesgo: alto` keys.
- Scenarios (P13) that check the meaning of the risk phrases in each language, with level `simulada`
  (simulated) and without replacing human review.
