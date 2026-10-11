<!-- i18n fuente-sha256=07e40f3e506e estado=borrador-ia -->

# Documentation, version and package (Doc1–Doc9)

Read it in Phase 7, with [documentación] or with [paquete]. Follow the repository's conventions (R17): if
it does not use a CHANGELOG, `AGENTS.md` or a pending-items log, propose creating them before doing so.

**Doc1 README.** How to choose a language, what is translated and what is not (machine contracts, the
model's free text), how to add a language, edge cases, limitations (what a detector does not cover,
experimental languages) and the real status of the translations (`borrador-ia`, `revisado`…), once per
language. The AI authorship note follows R16. If the scope is short, one multilingual section is enough;
do not translate the whole README unless asked. When translating documentation, keep code blocks,
commands, anchors and links intact.

**Doc2 Manual installation routes.** If one consists of copying files by hand, add the new ones
(catalogs, scripts) to its list. Without them, the feature does not exist for whoever installs that way.

**Doc3 `AGENTS.md` or `CLAUDE.md`.** If they exist: no new literals outside the catalog; delimited
blocks; frontmatter intact; untouchable files; human review of high-risk diffs; validation commands; do
not merge with CI red; what to do at the next version change; and known unrelated pending items. If only
one exists, check whether it links to the other.

**Doc4 Version.** According to the project's policy (e.g. semver: a compatible feature is a minor), with
its script if it exists, in all manifests at once and with a test that compares them (P11).

**Doc5 CHANGELOG.** Added, Changed, Fixed and Limitations, including the approved exceptions (D23) and the
lines of the original that change. Before closing, look up each figure quoted (keys, breakages, scenarios,
sizes) and compare it with the current state (R9).

**Doc6 Pending-items log** (`PENDIENTES.md` or the repository's equivalent). Only what is checked: what
requires a person (review, credentials), what requires another session or access to domains, which sources
are missing, which scenarios have not been run and which changes are not yet on the main branch.

**Doc7 [paquete] Package contents.** The packaging script includes all the new files and nothing else,
shown with P9. If there are old packages already downloaded, the version note says that the complete
package must be reinstalled.

**Doc8 [paquete] Names of the attachments.** If the README links an attachment by name (e.g.
`releases/latest/download/<name>.zip`), the attachment is named exactly that: a version suffix breaks the
link.

**Doc9 Manual of use, if it exists.** Read it whole before changing it. Keep its structure and its
numbering, because other parts refer to them; add the new material at the end, with a what's-new box at
the beginning. If a PDF is generated (e.g. from HTML with a headless browser), check by eye the cover and
a page with a table. It carries the AI note (R16) and keeps the previous version as history.
