# Pruebas del lector de skills

Esta guía corresponde a la versión `0.3.0`. Las pruebas automatizadas sustituyen
las llamadas al modelo y no consumen la cuenta. La prueba manual de traducción
real sí envía contenido al proveedor configurado y puede consumir cuota o
generar coste; solo se inicia al pulsar «Traducir» después de leer el aviso.

## Niveles de comprobación

- **Estática:** revisión del código, JSON, rutas y APIs documentadas.
- **Local:** pruebas de funciones puras ejecutadas con Node.js.
- **Simulada local:** ejecución del módulo con una API sustituida, sin Claude Code.
- **Plataforma:** validación y pruebas con Claude Code o con el portal del directorio.
- **Humana:** inspección del panel en una sesión real.

La validación estática estricta ha pasado con Claude Code `2.1.325`. La persona
usuaria ha aportado una captura de la ejecución del kit oficial con 14 pruebas:
13 superadas y 1 fallida (resultado de plataforma comunicado). El nombre y el
mensaje de la prueba fallida están pendientes.

La persona usuaria también ha confirmado la traducción real del ejemplo sintético
de esta guía y ha aportado una captura en Claude Code CLI `2.1.325` (nivel humano).
Se ve la prosa en español y la conservación de los metadatos iniciales, `Read`,
`docs/guide.md`, el bloque de código, `R17` y la URL. Esta evidencia no acredita
todos los casos de las tablas ni todos los controles del mod.

Una simulación local no comprueba el motor de mods, los permisos efectivos ni
cómo se dibuja la interfaz real.

Resultado de integración de `0.3.0` (simulada local): 15 escenarios superados,
incluidas ausencia de llamadas automáticas, petición explícita, protección de
los datos enviados, estados, errores, interrupción y descarte de resultados
tardíos. El modelo y las llamadas de la API se sustituyeron por respuestas de
prueba; no hubo una petición real ni consumo de cuenta.

Resultado previo del lector (simulada local): 13 escenarios superados, incluidos
cambios de selección con lecturas pendientes, cierre durante `stat` o `read`, tamaño antes y después
de leer, controles no admitidos y lectura del `SKILL.md` del repositorio sin
modificarlo. Se mantuvieron fuera del paquete las herramientas y los datos brutos
de esa simulación.

## Funciones de preparación y reconstrucción

Desde la raíz del repositorio, con Node.js (comprobado localmente con `24.19.0`):

```bash
node mods/skill-reader/tests/translation.node.test.mjs
```

Estas pruebas ejecutan funciones puras del módulo de traducción. No cargan el
motor de Claude Code, no llaman a modelos y no necesitan credenciales. Se ejecutan
por separado porque el kit de mods no ofrece los módulos de Node.js que utiliza
este archivo de pruebas.

Resultado local: 19 pruebas superadas con Node.js `24.19.0`. Incluyen CRLF y
espacios originales, fences y comentarios HTML, identificadores y URLs, colisiones
de marcadores, intercambio entre segmentos, respuestas malformadas y límites.

La conservación literal y el rechazo de respuestas malformadas no demuestran
fidelidad semántica de una traducción. El ejemplo sintético de esta guía cuenta
con una comprobación humana de traducción real. La fidelidad de otros documentos
requiere su propia revisión.

## Kit oficial de Claude Code

Desde la raíz del repositorio:

```bash
claude --version
claude plugin validate --strict ./mods/skill-reader
claude plugin test ./mods/skill-reader
```

Resultado con una instalación temporal de Claude Code `2.1.325`: la validación
estricta pasó. El ejecutor de pruebas terminó antes de cargar ambos archivos,
con el mensaje `the file did not load` y `its run ended without a report
(exit code 0)`. El mismo resultado apareció con un mod vacío y una sola prueba
mínima externa al repositorio. No se ha confirmado aquí la causa de ese problema
del ejecutor. No se cuentan como superadas ni como 14 aserciones fallidas las
pruebas que no llegaron a cargarse.

En una ejecución posterior comunicada por la persona usuaria, Claude Code
`2.1.325` cargó las 14 pruebas y comunicó 13 superadas y 1 fallida. La captura
disponible no contiene el nombre ni el mensaje del fallo; su diagnóstico y
resolución siguen pendientes.

Los archivos `tests/panel.test.ts` y `tests/translation-panel.test.ts` contienen
14 pruebas escritas: seis del lector y ocho de la integración de traducción.
Sustituyen las lecturas, las respuestas del modelo y el resto de llamadas necesarias
mediante el kit `claude-code/testing`. No leen las skills instaladas ni contactan
con un proveedor real.

Las pruebas del lector comprueban apertura y edición sin lectura automática,
carga expresa del archivo, conservación del texto, rutas y tamaños inválidos, y
descarte de lecturas tardías. Las pruebas de traducción comprueban la ausencia
de peticiones automáticas, la llamada expresa y su contenido preparado, los
estados de éxito y error, la conservación del original, los resultados inválidos,
la interrupción y el caso sin prosa traducible.

Un fallo al validar o al ejecutar debe corregirse antes de afirmar compatibilidad
con la versión concreta mostrada por `claude --version`.

## Prueba manual de lectura

```bash
claude --plugin-dir ./mods/skill-reader
```

Ejecuta `/skill-reader` dentro de esa sesión. Comprueba estos casos:

| Caso | Resultado esperado |
| --- | --- |
| Abrir el panel | Sin selección ni lectura automática. |
| Escribir una ruta sin cargar | No se lee el archivo. |
| Cargar `skills/multilang-repo-skill/SKILL.md` | Estado «Preparado» y contenido original visible. |
| Introducir un `README.md` o una URL | Error sin leer esa ruta. |
| Elegir una ruta inexistente o sin permiso | Error breve, sin volcar el error interno ni contenido al historial. |
| Cambiar la ruta después de cargar | Desaparece el original anterior hasta una nueva carga expresa. |
| Cerrar y volver a abrir | No reaparecen selección ni contenido anteriores. |
| Ejecutar `/clear` y volver a abrir | El panel vuelve a estar vacío. |

Revisa que un documento con código, comandos, rutas, URLs e instrucciones para
un agente se muestre como texto de lectura, sin ejecución ni apertura de enlaces.
Desplázate por el contenido y comprueba también un terminal estrecho.

Después, desde la raíz del repositorio, comprueba que el original no cambió:

```bash
git diff --exit-code -- skills/multilang-repo-skill/SKILL.md
```

## Primera traducción real

Esta comprobación necesita tu cuenta de Claude Code y puede consumir uso o
generar coste. Usa un archivo sintético corto en inglés, sin secretos ni datos
personales: el `SKILL.md` principal ya está en español y no sirve bien para
comprobar si se ha traducido la prosa.

Con tu editor, crea una carpeta de prueba fuera del paquete `mods/skill-reader/`
y guarda un archivo llamado exactamente `SKILL.md` con este contenido. No hace
falta subirlo a GitHub:

````markdown
---
name: reading-check
description: Synthetic reading check.
---

# Reading check

Follow these instructions carefully.

Use `Read` to inspect `docs/guide.md`. Do not run the example command.

```sh
echo "read-only example"
```

Keep the identifier R17 unchanged and the URL https://example.invalid/guide.
````

1. Usa una copia actualizada de `skill-reader-prototipo` y carga el mod con el
   comando anterior. Ejecuta `/skill-reader`.
2. Introduce la ruta de ese archivo y pulsa «Cargar original». Antes de traducir,
   comprueba que el original se ve y que el selector indica «Español».
3. Lee el aviso de envío y consumo. Solo si quieres realizar la petición real,
   pulsa «Traducir» una vez.
4. Comprueba «Traduciendo…» y después «Completado», o anota el mensaje breve de
   «Error». El mod solicita Haiku aunque la conversación use otro modelo.
5. En «Traducción», comprueba que la prosa está en español. Los metadatos iniciales,
   el código, `Read`, `docs/guide.md`, `R17` y la URL deben mantenerse literalmente.
6. Usa «Original» para comparar. Confirma que el archivo del editor no ha cambiado
   y que la traducción no se añadió a la conversación del agente.
7. Cierra y vuelve a abrir: la selección y los textos deben haber desaparecido.

Un error no debe reemplazar el original ni mostrar una traducción parcial. Cada
nuevo intento puede consumir otra vez. Cerrar el panel, cambiar de archivo o
terminar la sesión solicita la interrupción; no garantiza coste cero. Las
pruebas automatizadas cubren las respuestas tardías sin realizar peticiones reales.

Los recuentos mostrados son tokens comunicados por Claude Code, no dinero.
Revisa la fidelidad de la prosa por separado de la conservación de los literales.
Los bloques ambiguos, en particular código dentro de listas o citas, pueden
quedar sin traducir por la protección conservadora del prototipo.

## Directorio de Claude

Repite la validación del borrador con la carpeta `mods/skill-reader` y la rama
`skill-reader-prototipo`. Los avisos de capacidad pueden seguir apareciendo.
Un resultado del portal no sustituye la ejecución de las pruebas anteriores.
La prueba real del ejemplo sintético cuenta con comprobación humana. Antes de
enviar esta versión como producto terminado, resuelve la prueba fallida y vuelve
a ejecutar el kit oficial y la validación del borrador.

Elaborado con asistencia de IA; requiere revisión humana.
