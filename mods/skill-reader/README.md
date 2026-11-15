# NovaNoticia · Lector de skills (en desarrollo)

![Icono de NovaNoticia · Lector de skills](.claude-plugin/icon.png)

Componente opcional y separado de `multilang-repo-skill`. La versión `0.3.0`
implementa la lectura de un `SKILL.md` elegido expresamente y una traducción
de lectura al español, solicitada solo al pulsar «Traducir». La integración
con el modelo cuenta con una comprobación humana de un ejemplo sintético en
Claude Code `2.1.325`. La suite oficial ha superado sus 14 pruebas en el equipo
de la persona usuaria, según la salida que ha comunicado.

El identificador del plugin es `novanoticia-lector-skills`. Su carpeta es
`mods/skill-reader/` y el comando es `/skill-reader`.

## Función del prototipo

El panel permite cargar un archivo local, elegir «Español» en un selector
ampliable y solicitar su traducción. Antes del botón se explica qué se enviará
y que puede consumir uso o generar coste. Los estados son «Preparado»,
«Traduciendo…», «Completado» y «Error», además del estado de lectura del archivo.

Original y traducción se consultan mediante dos vistas dentro del mismo panel.
Se dibuja una sola vista cada vez para respetar el límite de texto de la interfaz.

La traducción es para la persona: no se incorpora como instrucciones del agente
ni modifica el archivo original. Se identifica como texto generado con IA que
requiere revisión humana.

## Preparación de la traducción

El módulo de funciones puras prepara la prosa y comprueba la respuesta
estructurada antes de reconstruir el documento. El panel lo utiliza para
preparar la petición y para aceptar o rechazar el resultado completo.

Los bloques técnicos identificados se conservan localmente. Los literales
reconocibles dentro de la prosa se sustituyen por marcadores. El mensaje preparado
contiene solo los segmentos de texto y el idioma de destino; no incluye el
contenido de los literales protegidos ni metadatos sobre la ruta seleccionada.

La comprobación rechaza respuestas incompletas, segmentos desconocidos o
repetidos y marcadores ausentes, duplicados o movidos a otro segmento. Una
respuesta inválida no produce una traducción parcial.

Esta protección es conservadora: un bloque ambiguo puede quedar sin traducir.
Si un bloque de código comienza dentro de una lista o cita, esta primera
preparación conserva desde esa apertura hasta el final del documento. También
puede conservar palabras completas que parezcan nombres técnicos.
Los nombres de herramientas y comandos escritos como prosa sin marcado no se
pueden reconocer universalmente. Su conservación y la fidelidad de la prosa
requieren revisión humana; no basta con superar una comprobación estructural.

La preparación admite originales de hasta 64 KiB UTF-8. El mensaje preparado
y la respuesta se limitan a 512 KiB; la reconstrucción, a 90.000 caracteres.
Si el documento genera demasiados fragmentos, falla la preparación antes de
llamar al modelo. Estos límites no garantizan que el proveedor acepte una
petición ni que la salida quepa en el límite de generación.

## Carga, uso y retirada

Desde la raíz de una copia del repositorio, carga el componente para una sesión:

```bash
claude --plugin-dir ./mods/skill-reader
```

Dentro de esa sesión:

1. Ejecuta `/skill-reader`.
2. Introduce una ruta local, por ejemplo
   `skills/multilang-repo-skill/SKILL.md`.
3. Pulsa «Cargar original» o Enter en el campo de ruta.
4. Lee el original. El estado pasa de «Leyendo…» a «Preparado»; si falla la
   carga, aparece «Error» con una explicación breve.
5. Comprueba el idioma y lee el aviso de privacidad y consumo. Solo si estás
   autorizado a enviar ese contenido, pulsa «Traducir».
6. Si el resultado supera las comprobaciones, aparece «Completado» y se muestra
   la traducción. Usa «Original» y «Traducción» para comparar las vistas.
7. Cierra con «Cerrar» o con Esc cuando el panel tenga el foco.

Las rutas relativas parten del directorio de la sesión. Se admiten espacios
en la ruta, sin comillas. No se expande `~`. El nombre del archivo debe ser
exactamente `SKILL.md`. El límite de esta versión es 64 KiB.
El archivo debe ser texto UTF-8.

Abrir el panel, escribir la ruta, cargar el original, elegir idioma o cambiar de
vista no llama al modelo. Escribir la ruta tampoco lee el archivo: la lectura
requiere «Cargar original» o Enter.

Cambiar la ruta descarta el contenido anterior. Cerrar el panel, terminar la
sesión o ejecutar `/clear` también descarta las referencias al contenido y la
selección. Si hay una traducción en curso, se solicita su interrupción y se
descarta cualquier respuesta tardía. Interrumpir no garantiza evitar el consumo.

La carga con `--plugin-dir` termina al salir de esa sesión. Para compartir el
componente, entrega solo la carpeta `skill-reader` o un ZIP que la contenga.
Para retirarlo del repositorio, elimina `mods/skill-reader/`.

Quien reciba solo esa carpeta puede cargarla desde el directorio que la contiene:

```bash
claude --plugin-dir ./skill-reader
```

Esta entrega de desarrollo no está publicada todavía en el directorio de Claude.
La carpeta incluye su [licencia MIT](LICENSE); consérvala al compartirla.

## Privacidad, lectura y consumo

Solo se consulta el tamaño y se lee la ruta elegida, tras una acción expresa.
No se recorren directorios ni se abren referencias del documento, imágenes,
URLs u otras skills. Los enlaces simbólicos se resuelven según el sistema de
archivos; la comprobación de tamaño no inmoviliza el archivo entre operaciones.

El contenido se trata como texto para mostrar. No se ejecutan sus instrucciones
ni comandos, y no se usa un renderizador Markdown que active enlaces o imágenes.
Los saltos CRLF se muestran como saltos de línea normales, conservando el texto
leído en memoria. Se rechazan archivos vacíos, NUL y otros controles no admitidos.

El mod no escribe archivos ni guarda contenido o traducciones de forma
persistente. El comando devuelve `{}` para no añadir el original ni la
traducción al historial del agente. Si una lectura o traducción termina después
de cerrar el panel o cambiar la selección, se descarta su resultado.

Al pulsar «Traducir», el mod solicita el alias `haiku` mediante
`$.model.complete`, independientemente del modelo usado por la conversación.
Utiliza el cliente y las credenciales de la sesión: plan de Claude, API o
proveedor configurado. No pide ni incorpora nuevas claves y no añade servicios
de traducción externos.

La petición independiente contiene las reglas de traducción, el idioma y los
segmentos preparados del archivo elegido, además del bloque identificativo que
añade Claude Code. No incluye el historial, `CLAUDE.md`, herramientas ni otros
archivos. El texto se trata como datos no confiables; sus instrucciones no son
órdenes para el traductor. La conservación de datos por parte del proveedor o
del entorno anfitrión depende de sus propias políticas: la ausencia de escritura
por parte del mod no equivale a ausencia de retención en esos servicios.

Cada intento con prosa traducible puede consumir cuota o generar cargos. El mod
no cambia automáticamente de modelo ante un error ni reintenta por su cuenta.
Si solo hay literales y no hay prosa que traducir, conserva el texto sin llamar
al modelo y lo indica.
La petición tiene un máximo de 32.000 tokens de salida y un tiempo de espera de
120 segundos. Un error, una interrupción o una respuesta rechazada puede haber
consumido uso. Si Claude Code devuelve recuentos, se muestran tokens, no un
importe monetario ni una estimación de coste.

Un fallo conserva el original y no muestra una traducción parcial. La persona
puede revisar el mensaje y decidir si desea volver a intentarlo.

## Eventos que utiliza el mod

- `session.start`: registra `/skill-reader` y continúa con `next(e)`, sin leer
  archivos ni abrir el panel durante el arranque.
- `command.run`: su filtro `{ command: 'skill-reader' }` limita el manejador a
  ese comando. Abre un panel nuevo sin selección y devuelve `{}`. Si otro código
  ejecuta ese mismo comando mediante `$.command.run`, también puede abrirlo.
- `ui.render`: dibuja solo el componente `Pane` cuyo `e.requestId` es
  `skill-reader`. Para otros paneles devuelve `next(e)`.
- `ui.close`: cuando se cierra el panel propio, limpia su estado y continúa
  el cierre con `next(e)`.
- `session.end`: limpia el estado propio y deja continuar el final de sesión,
  incluido el que acompaña a `/clear`, `/resume` o `/branch`.

El campo de ruta y las vistas cambian el estado local. La carga usa `$.fs.stat`
y `$.fs.read`; «Traducir» usa `$.model.complete` solo después de pulsarlo y
«Cerrar» usa `$.ui.close`. No se registran herramientas ni agentes y no se
interceptan ni aprueban permisos o llamadas a herramientas de Claude.

## Comprobaciones y compatibilidad

La [guía de pruebas](PRUEBAS.md) distingue comprobaciones locales simuladas,
pruebas escritas para el kit oficial y comprobaciones reales pendientes.

La integración tiene 15 escenarios locales simulados superados. Las funciones
de preparación y reconstrucción tienen 19 pruebas locales superadas. Estas
comprobaciones no utilizan un modelo real ni prueban el motor de Claude Code.

La persona usuaria ha confirmado una traducción real del ejemplo sintético de
la guía en Claude Code CLI `2.1.325` y ha aportado una captura (nivel humano).
En ese ejemplo se ve la prosa en español y se conservan los metadatos iniciales,
`Read`, `docs/guide.md`, el bloque de código, `R17` y la URL. Esta comprobación
no acredita todos los casos de error, interrupción y limpieza de estado.

La validación estática estricta se ha ejecutado con Claude Code `2.1.325` y ha
pasado. La persona usuaria ha ejecutado el kit oficial sobre el commit `ccd6721`
y ha comunicado su salida completa: **14 pruebas superadas y ninguna fallida**
(resultado de plataforma comunicado). Incluye la comprobación de cambiar la
ruta durante una traducción pendiente, tras corregir el filtro del hook de
prueba `ui.input`. No se cambió el código del lector ni el tiempo de espera.

En el entorno de desarrollo, el kit terminó antes de cargar los dos archivos;
una prueba mínima externa reprodujo ese problema y su causa sigue sin determinar.
Ese resultado se distingue de la ejecución satisfactoria comunicada por la
persona usuaria.

La versión mínima compatible sigue pendiente de determinar. Desktop y VS Code
no se han probado.

Comprobación local del icono: PNG válido de 1254 × 1254 píxeles y
1.133.861 bytes. El portal ha aceptado el icono en la validación de desarrollo.

## Publicación en el directorio de Claude

El objetivo es publicarlo por separado para Claude Code. En el portal, usa la
carpeta de plugin `mods/skill-reader`, no la raíz del repositorio. El manifiesto
y el marketplace de la raíz no se modifican para desarrollar este componente.

Abre el envío existente de esta carpeta en el [portal de
desarrollo](https://claude.ai/directory/manage) y comprueba los datos de origen:

| Campo del portal | Valor |
| --- | --- |
| Repository | `https://github.com/novanoticia/multilang-repo-skill` |
| Plugin path | `mods/skill-reader` |
| Branch or tag | `skill-reader-prototipo` |

Selecciona «Validate» o «Re-validate» después del último commit. La validación
corresponde a un commit concreto; una validación anterior no cubre cambios nuevos.
El mod no necesita una entrada en el marketplace raíz para este envío.

La validación de plataforma de la versión anterior, comunicada por la persona
usuaria, pasó con avisos: reconoció un mod, ningún servidor MCP, el nombre,
el editor y el icono. Esto no comprueba el funcionamiento del lector ni
sustituye el escaneo y la revisión posteriores a una solicitud. La versión
`0.3.0` necesita una validación nueva.

El portal ha mostrado `LOCAL_CODE_MOD` y `LOCAL_CODE_FILE_TYPE` como avisos que
todavía no rechazan este mod, anunciando una futura restricción para
organizaciones no Verified. Ese resultado no garantiza la admisión ni las
actualizaciones futuras. No se ha confirmado una fecha de entrada en vigor.

El portal advierte que el icono de la ficha se toma solo al guardar o enviar
el plugin por primera vez. Añadirlo a otra versión no garantiza cambiar la
imagen de una ficha ya guardada.

La suite oficial y la traducción real del ejemplo sintético ya cuentan con los
resultados descritos arriba. Falta validar el commit actual en el portal y
completar su revisión y publicación. La instalación desde una ficha publicada
todavía no se ha probado. Los resultados locales no garantizan la admisión en
el directorio.

## Referencias oficiales

- [Creación de mods](https://code.claude.com/docs/en/plugins/mods/create).
- [Interfaz de mods](https://code.claude.com/docs/en/plugins/mods/interface).
- [API de mods](https://code.claude.com/docs/en/plugins/mods/api).
- [Pruebas de mods](https://code.claude.com/docs/en/plugins/mods/test).
- [Distribución de plugins](https://code.claude.com/docs/en/plugins/publish).
- [Envío al directorio](https://claude.com/docs/plugins/submit).

Elaborado con asistencia de IA; requiere revisión humana.
