# Revisión de PR con Mistral

El workflow `Mistral PR Review` (`.github/workflows/mistral-review.yml`) tiene
dos jobs:

- `pruebas`: los tests de los scripts de la skill, sin la clave de Mistral.
- `mistral-review`: **llama** al revisor compartido
  [novanoticia/mistral-review](https://github.com/novanoticia/mistral-review),
  que lee el diff y las reglas de `REVIEW.md`, `AGENTS.md` o `CLAUDE.md`, por
  ese orden. Mistral solo analiza y comenta: las reparaciones corresponden a
  Claude y al mantenedor.

Desde el 2026-11-15 el código, las pruebas y la documentación detallada del
revisor (citas, segunda solicitud, cortes por `length`, límites de tamaño,
secretos tachados) viven en ese repo; antes había aquí una copia propia en
`.github/scripts/`, con sus tests en `tests/`. Una mejora se hace allí una vez y
llega a todos los repos.

## Activación

En Settings → Secrets and variables → Actions:

1. Secreto `MISTRAL_API_KEY` con la clave de Mistral. Su valor nunca se incluye
   en los informes.
2. Opcional: variable `MISTRAL_MODEL`; sin ella se usa el modelo por defecto
   del revisor compartido (`zai-glm-5-3-flash`).

Si falta la clave, el resumen indica «revisión omitida», que no equivale a una
evaluación sin hallazgos. GitHub no entrega secretos a PR de forks. El check se
llama `mistral-review / mistral-review`.

## Lo propio de este repo

No se excluye ningún archivo: las traducciones también se revisan. El revisor
vive fuera de la skill distribuida y no ejecuta el contenido del PR.

## Contraste de revisiones de otras IAs

El workflow `Mistral Reply to AI Reviews` (`.github/workflows/mistral-reply.yml`)
llama a `reply.yml` del mismo revisor compartido. Cuando otra IA (Codex, Claude,
Copilot, CodeRabbit o Gemini) deja hallazgos en un PR, Mistral contrasta cada uno
leyendo el código y responde con un dictamen: de acuerdo, no se sostiene, ya
corregido o pendiente, con citas literales. Solo comenta: no aplica parches.
Además del código, envía a Mistral el texto de esos hallazgos.

Usa el mismo secreto y las mismas variables que la revisión. La variable
opcional `MISTRAL_REPLY_MODEL` elige otro modelo de Mistral solo para el
contraste. Tampoco excluye ningún archivo. También se puede lanzar a mano: **Actions → Mistral Reply to
AI Reviews → Run workflow**, con el número del PR y el id del comentario.

Los dos workflows están fijados en la misma versión del revisor: `@` de `uses:`
y `ref:` deben coincidir en ambos archivos. El dictamen es otra opinión
automatizada; compruébalo antes de actuar.

## Límites

Es una segunda opinión barata, no un detector fiable. Una cita válida no
demuestra un defecto y un resultado sin hallazgos no demuestra que el PR esté
libre de defectos. Los informes no autorizan reparaciones automáticas.
