# Skill Reader (en desarrollo)

Componente opcional y separado de `multilang-repo-skill`.

La versión `0.1.1` añade el comando `/skill-reader` y un panel vacío con el botón
«Cerrar». Todavía no hay selección de archivo ni traducción. La visualización
real en Claude Code está pendiente de comprobar.

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

## Privacidad y consumo en esta entrega

Al iniciar la sesión se registra el comando, sin abrir el panel. El panel se
abre cuando la persona ejecuta `/skill-reader`. El comando devuelve un resultado
vacío para no añadir contenido al historial del agente.

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

La documentación de instalación definitiva, pruebas, privacidad y limitaciones
se completará a medida que se implemente y compruebe cada parte.

## Referencias oficiales

- [Creación de mods](https://code.claude.com/docs/en/plugins/mods/create).
- [Interfaz de mods](https://code.claude.com/docs/en/plugins/mods/interface).
- [Distribución de plugins](https://code.claude.com/docs/en/plugins/publish).

Elaborado con asistencia de IA; requiere revisión humana.
