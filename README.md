# MultiLang Repo Skill

Skill para Claude Code que guía a un agente para hacer multiidioma un repositorio: programas,
bibliotecas, servidores, CLI, skills, plugins, instrucciones para modelos, proyectos híbridos y
repositorios que ya usan i18next, gettext o ICU.

El agente descubre el proyecto, separa el texto para personas de los contratos de máquina, pregunta
solo lo que decide la persona, diseña en proporción al proyecto, comprueba con evidencias de nivel
declarado y publica solo lo autorizado, acción por acción.

## Instalación

Como plugin, desde este repositorio:

```
/plugin marketplace add novanoticia/multilang-repo-skill
/plugin install multilang-repo-skill@multilang-repo-skill
```

O copiando la carpeta de la skill a mano: `skills/multilang-repo-skill/` va en `~/.claude/skills/`
(para todos tus proyectos) o en `.claude/skills/` de un repositorio. Comprueba que aparece con
`/skills`.

## Ejemplos

1. «Haz multiidioma este repositorio: español (referencia) e inglés. Modo guiado.»
2. «Antes de tocar nada, audita el soporte de idiomas de este repo y dime qué textos están
   hardcodeados y cuáles son contratos de máquina.» (solo análisis: no modifica nada)
3. «Añade francés y pt-BR a la app, que ya usa i18next. Modo autónomo; puedes subir la rama `i18n`
   cada vez que termines una tarea, nada más.»
4. «idioma=en Make this repository multilingual: Spanish (reference) and French. Guided mode.» (la
   skill responde en inglés).

## Idiomas

La skill está en español (idioma de referencia) y tiene una traducción al inglés. Para pedir la
respuesta en inglés, escribe `idioma=en` (o `lang=en`) en la primera línea de tu mensaje; la marca vale
para toda la conversación y elige el idioma de la respuesta, no los idiomas a los que se traduce tu
repositorio (eso se acuerda en la conversación). Sin marca no cambia nada respecto a 9.0.0: la skill sigue respondiendo en el
idioma en que escribes (R16) y usa los ficheros en español. Un idioma no disponible da un aviso y
continúa como sin marca. La traducción es un `borrador-ia` sin revisión humana
(estado en [skills/multilang-repo-skill/i18n/ESTADO.md](skills/multilang-repo-skill/i18n/ESTADO.md)).
Este README también está en [inglés](README.en.md). <!-- i18n:exento -->

## Qué incluye

```
skills/multilang-repo-skill/
├── SKILL.md       núcleo: activación, precedencia, permisos, seguridad, evidencia, modos, escala, módulos, flujo y cierre
├── references/    12 módulos que se leen solo si se activan
├── assets/        5 plantillas (datos y alcance, registro de sesión, inventario, escenarios, evidencias)
├── i18n/          traducción al inglés (espejo de lo anterior), glosario y estado de las traducciones
└── scripts/       verificar_adiciones.py, validar_catalogos.py, resolver_idioma.py, comprobar_paridad.py y sus pruebas
```

Los scripts usan solo la biblioteca estándar de Python 3.8+ y nunca modifican ficheros. Para ejecutar
sus pruebas:

```
cd skills/multilang-repo-skill/scripts && python3 -B -m unittest discover -s tests
```

## Estado

Versión 9.1.4 (a fecha 2026-10-13). Lo comprobado, con su nivel (detalle de 9.0.0 y adenda de 9.1.x en
[docs/VALIDACION.md](docs/VALIDACION.md)):

- **9.0.0:** validador de skills, comprobaciones estructurales y de identificadores sin errores
  (`local`); 78 pruebas de los scripts con Python 3.14 y 3.9 y sabotaje con 32 de 32 mutantes
  detectados (`local`); activación real en Claude Code y escenarios de comportamiento simulados (17
  ejecuciones, tres versiones de la skill), calificados por agentes distintos de los que los
  ejecutaron (`plataforma`, `simulada`).
- **9.1.0:** 138 pruebas con Python 3.9, 3.10, 3.13 y 3.14 (`local`); `comprobar_paridad.py` con 38 de
  38 mutantes detectados (`local`); paridad estructural de los 18 ficheros de `i18n/en/` con sus
  originales (`local`); `claude plugin validate --strict` sin errores (`local`).
- **9.1.1:** una frase del bloque de idioma, tras un fallo de los escenarios (E-13). Segunda ronda de
  escenarios de selección de idioma: 7 PASS y 1 FAIL en 8 ejecuciones simuladas (`simulada`); el fallo, E-04,
  se corrige en la 9.1.2 (detalle en [docs/ESCENARIOS-9.1.0.md](docs/ESCENARIOS-9.1.0.md)).
- **9.1.2:** una viñeta del bloque de idioma, para que el aviso de traducción salga solo con `idioma=en`
  (E-04). Tercera ronda de escenarios: E-04 pasa 4 de 4 y las 11 ejecuciones, 11 de 11 (`simulada`); no prueba
  que el fallo intermitente esté resuelto.
- **9.1.3:** una frase que aclara que `idioma=` elige el idioma de la respuesta y no los idiomas a los que se
  traduce un repositorio. No se ha medido por escenarios (`pendiente`).
- **9.1.4:** el bloque «Idioma de la respuesta» se acorta (de 1 862 a 1 700 bytes) y su detalle pasa a una
  referencia nueva. Regresión (`simulada`, rondas 4 a 6): sin fallos reproducibles, pero E-10 cita el marcador `<!-- i18n:inicio -->` en 5 de 8 ejecuciones (8 de 8 con la 9.1.3), lo que desde el 2026-10-13 ya no cuenta como fallo y E-13 falló 1 de 6 (0 de 5 con la 9.1.3); sugiere un efecto de la 9.1.4, sin demostrarlo.

Límites: no ha tenido revisión humana ni uso real en proyectos; los escenarios son simulaciones con
entre una y diez ejecuciones cada uno. La traducción al inglés es un `borrador-ia` que ninguna persona ha
revisado. La activación y los 17 escenarios de 9.0.0 se midieron con la `description` y el texto de 9.0.0:
9.1.x los cambia (`description` de 966 a 1023 caracteres y un bloque nuevo en `SKILL.md`) y no se han
repetido (`pendiente`, `plataforma`). La subida a claude.ai no se ha probado (su ayuda limita `description` a 200
caracteres y esta tiene 1023).

## Documentación

- [CHANGELOG.md](CHANGELOG.md): cambios por versión, con las excepciones aprobadas y cómo retirarlas.
- [docs/INFORME-ENTREGA.md](docs/INFORME-ENTREGA.md): resumen, estructura y uso.
- [docs/AUDITORIA.md](docs/AUDITORIA.md): auditoría de las versiones anteriores del marco (v1–v8).
- [docs/TRAZABILIDAD.md](docs/TRAZABILIDAD.md): cambios respecto a v7 y destino de cada propuesta de v8.
- [docs/VALIDACION.md](docs/VALIDACION.md): cómo se validó y con qué resultados.

Esos documentos citan `evaluacion/` y `entrega/`, carpetas del entorno de trabajo donde se hicieron
las pruebas; las herramientas y los datos brutos de evaluación no se publican aquí.

## Licencia

[MIT](LICENSE).

---

Elaborado con asistencia de IA; requiere revisión humana.
