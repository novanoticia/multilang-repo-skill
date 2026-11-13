# NovaNoticia · Lector de skills (en desarrollo)

Componente opcional y separado de `multilang-repo-skill`.

La versión `0.1.2` contiene el comando `/skill-reader` y un panel vacío con el
botón «Cerrar». Todavía no hay selección de archivo ni traducción. La
visualización real en Claude Code está pendiente de comprobar.

El identificador del plugin es `novanoticia-lector-skills`. Su carpeta sigue
siendo `mods/skill-reader/` y el comando sigue siendo `/skill-reader`.

## Objetivo previsto

Leer un archivo `SKILL.md` elegido expresamente y mostrar su original y una
traducción de lectura en un panel propio. El idioma inicial será español.
Solo el botón «Traducir» iniciará una petición al modelo, después de mostrar
un aviso sobre el contenido enviado y el posible consumo o coste.

La traducción será para la persona: no se incorporará como instrucciones
del agente ni modificará el archivo original.

## Archivos actuales

- `.claude-plugin/plugin.json`: identidad y versión propias del componente.
- `hooks/hooks.json`: ubicación del módulo del mod.
- `hooks/register.js`: registro del comando y dibujo del panel propio.

El manifiesto y el marketplace de la raíz del repositorio no se modifican.

## Eventos que utiliza el mod

- `session.start`: registra el comando `/skill-reader` y continúa el inicio de
  sesión con `next(e)`. No abre el panel durante el arranque.
- `command.run`: su filtro `{ command: 'skill-reader' }` limita el manejador a
  ese comando. Abre el panel propio y devuelve `{}`, sin añadir texto al
  historial del agente. Si otro código ejecuta ese mismo comando mediante
  `$.command.run`, el manejador también puede recibir esa operación y abrir
  el panel. Los demás comandos no coinciden con este filtro.
- `ui.render`: se limita al componente `Pane`. Dibuja contenido solo cuando
  `e.requestId` coincide con `skill-reader`; para otros paneles devuelve
  `next(e)`, conservando su comportamiento. El botón «Cerrar» llama a
  `$.ui.close` con el identificador del panel propio.

Estos manejadores no registran herramientas ni agentes y no interceptan
ni aprueban permisos o llamadas a herramientas de Claude.

## Privacidad y consumo en esta entrega

La apertura del panel se limita al comando `/skill-reader`, tal como se explica
en la sección de eventos. Abrir el panel no inicia una traducción.

El módulo actual no lee archivos, no llama a modelos, no inicia procesos,
no hace peticiones de red y no guarda contenido. No requiere claves de API
ni genera consumo de modelo propio. La futura traducción necesitará su propia
comprobación de privacidad y consumo.

## Carga y retirada para desarrollo

Desde la raíz del repositorio, carga este componente para una sesión:

```bash
claude --plugin-dir ./mods/skill-reader
```

Dentro de esa sesión, ejecuta `/skill-reader`. El comportamiento esperado es
un panel «Lector de skills» con espacios vacíos para original y traducción.
El botón «Cerrar» permite cerrarlo; también se solicita cierre con Esc cuando
el panel tiene el foco. No se inicia una traducción.

La carga con `--plugin-dir` es temporal, para esa sesión. Al salir termina.

Para compartir esta entrega, se puede entregar solo la carpeta `skill-reader`
o un ZIP que la contenga. Para retirarla del repositorio, se elimina
`mods/skill-reader/`.

## Comprobaciones

Comandos para una instalación de Claude Code:

```bash
claude --version
claude plugin validate --strict ./mods/skill-reader
```

Prueba manual pendiente:

1. Cargar el componente y comprobar que el panel no se abre automáticamente.
2. Ejecutar `/skill-reader` y comprobar el título y los espacios vacíos.
3. Pulsar «Cerrar», volver a abrir, enfocar el panel y comprobar el cierre con Esc.
4. Comprobar que otros paneles siguen funcionando.
5. Confirmar que este componente no lee archivos ni llama al modelo.

La revisión estática se ha realizado. Las llamadas del módulo se han comprobado
mediante una simulación local con API sustituida, sin ejecutar Claude Code.
Esa simulación no comprueba el dibujo real, los permisos ni el motor de mods.

No se ha ejecutado la validación ni la carga en Claude Code. La documentación
oficial sitúa el inicio de soporte de mods del CLI en `2.1.287`; la versión mínima
efectiva de este componente está pendiente de verificar. Desktop y VS Code
tampoco se han probado. Esta entrega aún no permite leer ni traducir una skill.

## Publicación en el directorio de Claude

El objetivo es publicar este componente por separado para Claude Code. En el
portal, su carpeta de plugin es `mods/skill-reader`, no la raíz del repositorio.

La validación de plataforma del borrador, comunicada por la persona usuaria,
pasó con avisos. Reconoció un mod y ningún servidor MCP. Esa validación no
comprueba el funcionamiento del panel ni sustituye el escaneo y la revisión
posteriores a una solicitud. La versión `0.1.2` requiere una nueva validación
para comprobar su nombre y documentación.

El aviso de parecido del nombre con otra marca motivó el uso del identificador
distintivo `novanoticia-lector-skills`. Su aceptación sigue pendiente del portal.
El icono del directorio también está pendiente y debe prepararse antes de
solicitar la publicación.

El portal ha mostrado `LOCAL_CODE_MOD` y `LOCAL_CODE_FILE_TYPE` como avisos que
todavía no rechazan este mod, anunciando una futura restricción para
organizaciones no Verified. Ese resultado no garantiza la admisión ni las
actualizaciones futuras. No se ha confirmado una fecha de entrada en vigor.

Antes de enviar el componente como producto terminado, hay que completar y
probar la selección, lectura y traducción del archivo elegido.

La documentación de instalación definitiva, pruebas, privacidad y limitaciones
se completará a medida que se implemente y compruebe cada parte.

## Referencias oficiales

- [Creación de mods](https://code.claude.com/docs/en/plugins/mods/create).
- [Interfaz de mods](https://code.claude.com/docs/en/plugins/mods/interface).
- [Distribución de plugins](https://code.claude.com/docs/en/plugins/publish).
- [Envío al directorio](https://claude.com/docs/plugins/submit).

Elaborado con asistencia de IA; requiere revisión humana.
