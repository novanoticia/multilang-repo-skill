# Pruebas del lector de skills

Esta guía corresponde a la versión `0.2.0`. Ninguna prueba de esta versión
necesita un modelo ni una clave de API: todavía no se ha implementado la traducción.

## Niveles de comprobación

- **Estática:** revisión del código, JSON, rutas y APIs documentadas.
- **Simulada local:** ejecución del módulo con una API sustituida, sin Claude Code.
- **Plataforma:** validación y pruebas con Claude Code o con el portal del directorio.
- **Humana:** inspección del panel en una sesión real.

Las pruebas del kit oficial se entregan escritas; su ejecución y la revisión
visual en Claude Code están pendientes. Una simulación local no comprueba el
motor de mods, los permisos efectivos ni cómo se dibuja la interfaz real.

Resultado local simulado: 13 escenarios superados, incluidos cambios de selección
con lecturas pendientes, cierre durante `stat` o `read`, tamaño antes y después
de leer, controles no admitidos y lectura del `SKILL.md` del repositorio sin
modificarlo. Se mantuvieron fuera del paquete las herramientas y los datos brutos
de esa simulación.

## Kit oficial de Claude Code

Desde la raíz del repositorio:

```bash
claude --version
claude plugin validate --strict ./mods/skill-reader
claude plugin test ./mods/skill-reader
```

El archivo `tests/panel.test.ts` sustituye las lecturas y el resto de llamadas
necesarias mediante el kit `claude-code/testing`. No lee las skills instaladas.
Comprueba apertura y edición sin lectura automática, carga expresa del archivo,
conservación del texto, rechazo de rutas y tamaños inválidos, y descarte de
resultados tardíos después de cerrar el panel.

Un fallo al validar o al ejecutar debe corregirse antes de afirmar compatibilidad
con la versión concreta mostrada por `claude --version`.

## Prueba manual en Claude Code

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

## Directorio de Claude

Repite la validación del borrador con la carpeta `mods/skill-reader` y la rama
`skill-reader-prototipo`. Los avisos de capacidad pueden seguir apareciendo.
Un resultado del portal no sustituye la ejecución de las pruebas anteriores.
No envíes esta versión como un traductor terminado: aún solo muestra el original.

Elaborado con asistencia de IA; requiere revisión humana.
