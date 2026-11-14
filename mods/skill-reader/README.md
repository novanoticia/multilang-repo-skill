# NovaNoticia · Lector de skills (en desarrollo)

![Icono de NovaNoticia · Lector de skills](.claude-plugin/icon.png)

Componente opcional y separado de `multilang-repo-skill`. La versión `0.2.1`
permite introducir la ruta de un archivo `SKILL.md`, cargarlo expresamente y
ver su contenido original. La traducción está pendiente de implementar.

El identificador del plugin es `novanoticia-lector-skills`. Su carpeta es
`mods/skill-reader/` y el comando es `/skill-reader`.

## Objetivo previsto

Mostrar el original y una traducción de lectura en un panel propio. El idioma
inicial será español. En una tarea posterior, solo el botón «Traducir» iniciará
una petición al modelo, después de mostrar el contenido que se enviará y un
aviso sobre el posible consumo o coste.

La traducción será para la persona: no se incorporará como instrucciones del
agente ni modificará el archivo original.

## Preparación de la traducción

Se incluye un módulo de funciones puras para preparar la prosa y comprobar una
respuesta estructurada antes de reconstruir el documento. En esta entrega
todavía no está conectado al panel ni a un modelo.

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
una futura llamada al modelo.

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
4. Lee el original en el panel. El estado pasa de «Leyendo…» a «Preparado»;
   si falla la carga, aparece «Error» con una explicación breve.
5. Cierra con «Cerrar» o con Esc cuando el panel tenga el foco.

Las rutas relativas parten del directorio de la sesión. Se admiten espacios
en la ruta, sin comillas. No se expande `~`. El nombre del archivo debe ser
exactamente `SKILL.md`. El límite de esta versión es 64 KiB.
El archivo debe ser texto UTF-8.

Escribir o cambiar la ruta no lee el archivo. Cambiarla descarta la carga
anterior. Cerrar el panel, terminar la sesión o ejecutar `/clear` también
descarta las referencias al contenido y la selección.

La carga con `--plugin-dir` termina al salir de esa sesión. Para compartir el
componente, entrega solo la carpeta `skill-reader` o un ZIP que la contenga.
Para retirarlo del repositorio, elimina `mods/skill-reader/`.

## Privacidad, lectura y consumo

Solo se consulta el tamaño y se lee la ruta elegida, tras una acción expresa.
No se recorren directorios ni se abren referencias del documento, imágenes,
URLs u otras skills. Los enlaces simbólicos se resuelven según el sistema de
archivos; la comprobación de tamaño no inmoviliza el archivo entre operaciones.

El contenido se trata como texto para mostrar. No se ejecutan sus instrucciones
ni comandos, y no se usa un renderizador Markdown que active enlaces o imágenes.
Los saltos CRLF se muestran como saltos de línea normales, conservando el texto
leído en memoria. Se rechazan archivos vacíos, NUL y otros controles no admitidos.

El mod no escribe archivos ni guarda contenido de forma persistente. El comando
devuelve `{}` para no añadir el original al historial del agente. Si una lectura
termina después de cerrar el panel o cambiar la selección, se descarta su resultado.

Esta versión no llama a modelos, no inicia procesos, no hace peticiones de red,
no requiere claves de API y no genera consumo de modelo propio. La traducción
futura necesitará su propia comprobación de privacidad y consumo.

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

El campo de ruta cambia el estado local. La carga usa `$.fs.stat` y `$.fs.read`;
el botón «Cerrar» usa `$.ui.close`. No se registran herramientas ni agentes y
no se interceptan ni aprueban permisos o llamadas a herramientas de Claude.

## Comprobaciones y compatibilidad

La [guía de pruebas](PRUEBAS.md) distingue comprobaciones locales simuladas,
pruebas escritas para el kit oficial y comprobaciones reales pendientes.

Una prueba manual comunicada por la persona usuaria confirma apertura del panel
y lectura visible del original, con estado «Preparado», en Claude Code CLI
`2.1.325` (nivel humano). Esta comprobación corresponde al lector; la preparación
de traducciones todavía no está conectada al panel.

No se ha confirmado el resultado del kit oficial de pruebas. La versión mínima
compatible sigue pendiente de determinar. Desktop y VS Code no se han probado.

Comprobación local del icono: PNG válido de 1254 × 1254 píxeles y
1.133.861 bytes. El portal ha aceptado el icono en la validación de desarrollo.

## Publicación en el directorio de Claude

El objetivo es publicarlo por separado para Claude Code. En el portal, usa la
carpeta de plugin `mods/skill-reader`, no la raíz del repositorio. El manifiesto
y el marketplace de la raíz no se modifican para desarrollar este componente.

La validación de plataforma de la versión anterior, comunicada por la persona
usuaria, pasó con avisos: reconoció un mod, ningún servidor MCP, el nombre,
el editor y el icono. Esto no comprueba el funcionamiento del lector ni
sustituye el escaneo y la revisión posteriores a una solicitud. La versión
`0.2.1` necesita una validación nueva.

El portal ha mostrado `LOCAL_CODE_MOD` y `LOCAL_CODE_FILE_TYPE` como avisos que
todavía no rechazan este mod, anunciando una futura restricción para
organizaciones no Verified. Ese resultado no garantiza la admisión ni las
actualizaciones futuras. No se ha confirmado una fecha de entrada en vigor.

El portal advierte que el icono de la ficha se toma solo al guardar o enviar
el plugin por primera vez. Añadirlo a otra versión no garantiza cambiar la
imagen de una ficha ya guardada.

Antes de enviarlo como producto terminado, hay que completar y probar la
traducción del archivo elegido y comprobar el lector en Claude Code.

## Referencias oficiales

- [Creación de mods](https://code.claude.com/docs/en/plugins/mods/create).
- [Interfaz de mods](https://code.claude.com/docs/en/plugins/mods/interface).
- [API de mods](https://code.claude.com/docs/en/plugins/mods/api).
- [Pruebas de mods](https://code.claude.com/docs/en/plugins/mods/test).
- [Distribución de plugins](https://code.claude.com/docs/en/plugins/publish).
- [Envío al directorio](https://claude.com/docs/plugins/submit).

Elaborado con asistencia de IA; requiere revisión humana.
