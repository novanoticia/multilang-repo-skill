# AGENTS.md

Lo que hay que saber antes de tocar nada en este repositorio. Vale para agentes de IA y para personas.

## Qué es esto

Un plugin de Claude Code con una sola skill, `multilang-repo-skill`, que guía a un agente para hacer
multiidioma un repositorio. El producto es sobre todo prosa normativa: reglas con identificador que
otro agente lee y sigue. El único código ejecutable son tres scripts de apoyo y sus pruebas.

```
.claude-plugin/plugin.json            manifiesto del plugin (nombre, versión, autor, licencia)
.claude-plugin/marketplace.json       marketplace de un solo plugin (source: "./")
skills/multilang-repo-skill/SKILL.md  núcleo: se carga entero en cada invocación
skills/multilang-repo-skill/references/  módulos que el agente lee solo si se activan
skills/multilang-repo-skill/assets/      plantillas que el agente copia junto a su registro
skills/multilang-repo-skill/scripts/     verificar_adiciones.py, validar_catalogos.py, resolver_idioma.py
skills/multilang-repo-skill/scripts/tests/  pruebas unittest de los tres scripts
docs/                                 auditoría, trazabilidad, validación e informe (no forman parte de la skill)
```

## Comandos

Ejecuta las pruebas sin tuberías detrás, para que el código de salida sea el de `unittest`:

```bash
cd skills/multilang-repo-skill/scripts && python3 -B -m unittest discover -s tests
```

Hoy son **78 pruebas** y salen todas en verde. Si ves menos, alguna no se está descubriendo.

```bash
claude plugin validate --strict .                 # manifiesto, marketplace y skill
wc -l skills/multilang-repo-skill/SKILL.md        # debe quedar por debajo de 500
```

`-B` evita que se cree `__pycache__` dentro de la skill: no debe acabar en el paquete.

## Restricciones innegociables

1. **Identificadores estables.** Las reglas se citan por identificador (R1–R20, D1–D31, P1–P15,
   T1–T7, C1–C9, S1–S6, G1–G9, M1–M7, Doc1–Doc9). No renumeres ni reutilices uno. Una regla nueva
   recibe el siguiente libre y se añade a `references/identificadores.md`; una retirada deja una
   línea que lo dice (como S5). Cada identificador se define una sola vez y todo lo citado existe.
2. **Carga progresiva.** `SKILL.md` por debajo de 500 líneas, con el núcleo (precedencia, permisos,
   seguridad, evidencia, modos) siempre en él. Las referencias cuelgan directamente de `SKILL.md`, a
   un solo nivel, y cada una aparece en su tabla de Recursos con el momento en que se lee. Una
   referencia de más de 100 líneas lleva índice al principio.
3. **Frontmatter válido.** `name` igual al nombre de la carpeta, en kebab-case. `description` en
   YAML válido y como mucho de 1024 caracteres. Cuidado con «: » dentro del texto, que ya rompió el
   YAML una vez. Si cambias la descripción, vuelve a probar la activación.
4. **Scripts.** Solo biblioteca estándar de Python 3.8+. **Nunca escriben ficheros.**
   `resolver_idioma.py` es total: ninguna entrada lo hace fallar. El mensaje de la persona le llega
   desde un fichero temporal redirigido a la entrada estándar, nunca como argumento ni en un heredoc
   (un heredoc de delimitador fijo admite inyección; hay una prueba que lo demuestra).
5. **Prueba primero.** Un cambio de comportamiento en un script empieza por una prueba que falla.
   Comprueba que la prueba nueva detecta el fallo rompiendo el código a propósito antes de darla
   por buena.
6. **Coherencia antes que añadidos.** Casi todos los fallos encontrados fueron dos reglas correctas
   por separado que se contradecían (por ejemplo, cuándo parar en modo guiado y en autónomo). Antes
   de añadir una regla, busca las que tratan lo mismo y deja una sola fuente; si una referencia
   repite algo del núcleo, remite a él en vez de copiarlo con matices.
7. **Afirmaciones con nivel.** En la skill y en `docs/`, «comprobado» o «verificado» llevan su nivel
   (`estática`, `local`, `ci`, `simulada`, `plataforma`, `humana`). Nada diseñado se presenta como
   ejecutado. Si cambias algo que `docs/VALIDACION.md` mide, actualiza las cifras o marca la
   comprobación como pendiente.
8. **Nada personal ni local.** Sin rutas absolutas, nombres de usuario ni datos de quien ejecutó las
   pruebas. Las herramientas y los datos brutos de evaluación no se publican en este repositorio.
9. **Nota de IA solo donde toca.** Los documentos públicos para personas (README, notas de Release)
   terminan una vez con «Elaborado con asistencia de IA; requiere revisión humana.». Nunca en
   ficheros que consume una máquina (código, JSON, YAML).
10. **Prosa en español.** Los textos de la skill, los mensajes de los scripts y la documentación van
    en español con acentuación correcta; los nombres en el código, en ASCII.

## Publicar una versión

1. Sube a la vez `version` en `.claude-plugin/plugin.json` y `metadata.version` en el frontmatter de
   `SKILL.md`. Si no cambias `version`, quien ya tiene el plugin no recibe la actualización.
2. Pasa las pruebas y `claude plugin validate --strict .`.
3. Crea la Release con la etiqueta `vX.Y.Z` y adjunta `multilang-repo-skill.zip`, que contiene la
   carpeta `skills/multilang-repo-skill/` en la raíz del ZIP, sin `__pycache__` ni `.DS_Store`.
   Comprueba el ZIP descomprimiéndolo en una carpeta vacía y pasando allí las pruebas.

---

Elaborado con asistencia de IA; requiere revisión humana.
