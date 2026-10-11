<!-- i18n fuente-sha256=22bfd9e76ce2 estado=borrador-ia -->

# Index of identifiers

It serves to locate a rule by its identifier, cite it or exempt from it. The identifiers are stable: a
withdrawn rule is not reused with another meaning.

## Contents
- Where each rule is
- Changes with respect to the previous framework (v7)

## Where each rule is

| Prefix | Scope | Identifiers | File |
|---|---|---|---|
| R | Core: work, permissions, evidence | R1–R20 | SKILL.md |
| D | Design | D1 | SKILL.md (Phase 3) |
| | | D2–D7 | references/seleccion-idioma.md |
| | | D8–D15, D17–D20 | references/diseno-catalogos.md |
| | | D16, D30, D31 | references/formatos-rtl-unicode.md |
| | | D21–D23, D25, D27–D29 | references/instrucciones-y-agentes.md |
| | | D24 | references/seguridad.md |
| | | D26 | references/traducciones.md |
| P | Tests, review and triage | P1–P15 | references/pruebas-y-evidencia.md |
| T | Translations | T1–T7 | references/traducciones.md |
| C | External content | C1–C9 | references/contenido-externo.md |
| S | Security | S1–S4, S6 (S5 withdrawn) | references/seguridad.md |
| Doc | Documentation and package | Doc1–Doc9 | references/documentacion-y-paquete.md |
| G | Publishing | G1–G9 | references/publicacion.md |
| M | Delegation | M1–M7 | references/delegacion.md |

The phases keep the numbering 0–9. The inventory categories are single letters (A–H) and must not be
confused with rule identifiers.

## Changes with respect to the previous framework (v7)

The number and meaning of R1–R16, D1–D29, P1–P12, T1–T6, C1–C8, G1–G9 and M1–M7 are kept. Some rules
widen or narrow their scope without changing their purpose:

| Identifier | Change |
|---|---|
| R4, R5 | The pace of summaries and questions depends on the supervision mode (R18). |
| R6 | Adds the location of the log and resuming with a single confirmation. |
| R7 | Six levels: adds `estática` and `humana` and distinguishes `ci` from `local`. |
| R13 | Distinguishes capability, need and authorization; standing permissions are not asked for again. |
| R16 | The AI note only goes in public documents for people, never in machine files. |
| D1 | Distinguishes deterministic outputs (exact comparison) from instructions for models (exact text and invariants). |
| D3 | Keeps the script subtag, treats `C`/`POSIX` as absence and admits explicit links. |
| D4 | Distinguishes explicit input from ambient input. |
| D13 | First, the ecosystem's format; NFC is not imposed on reference literals. |
| D16 | No longer includes RTL, which moves to D30. |
| D18 | Adding `lang` to the default output requires an exception (D23). |
| D22 | Notices never go inside machine formats. |
| P4 | Does not apply to model-generated text; it is level `local`. |
| P5 | Invariance tests are validated with sabotage, not by seeing them red. |
| P7 | Applies to the checks you write, in proportion to the scale. |
| M1–M7 | The [multi-modelo] module becomes [delegación] and no longer depends on an external protocol. |

New identifiers: R17 (precedence, formerly a paragraph without an identifier), R18 (modes), R19 (scope of
the request), R20 (proportionality, formerly a paragraph and the table of Phase 1.8), D30, D31, P13–P15
(formerly Phases 8.2, 8.1 and 8.3, without an identifier), T7, C9, S1–S4, S6, and Doc1–Doc9 (formerly
Phase 7, without identifiers).

Module labels: `[alto riesgo]` becomes `[alto-riesgo]` and no longer forces scale L; `[multi-modelo]`
becomes `[delegación]`; `[release]` is split between `[paquete]` and `[publicación]`. `[ecosistema]`,
`[rtl-escrituras]`, `[seguridad]` and `[documentación]` are new. The scales S, M and L keep their
letters, but now measure only structure; risk is a separate axis.
