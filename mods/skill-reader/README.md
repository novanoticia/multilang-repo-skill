# Skill Reader (en desarrollo)

Componente opcional y separado de `multilang-repo-skill`.

Esta entrega contiene únicamente la base del plugin. Todavía no hay comando,
panel, selección de archivo ni traducción.

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
- `hooks/register.js`: punto de entrada vacío, sin eventos registrados.

El manifiesto y el marketplace de la raíz del repositorio no se modifican.

## Privacidad y consumo en esta entrega

El módulo actual no lee archivos, no llama a modelos, no inicia procesos,
no hace peticiones de red y no guarda contenido. No requiere claves de API.
La futura traducción necesitará su propia comprobación de privacidad y consumo.

## Comprobación pendiente en Claude Code

Desde la raíz del repositorio, los comandos previstos para comprobar esta base son:

```bash
claude plugin validate --strict ./mods/skill-reader
claude --plugin-dir ./mods/skill-reader
```

La carga con `--plugin-dir` es temporal, para esa sesión. Esta base no mostrará
un panel ni añadirá `/skill-reader`. Al salir termina esa carga temporal.

Para compartir la base, se puede entregar solo la carpeta `skill-reader`
o un ZIP que la contenga. Para retirarla del repositorio, se elimina
`mods/skill-reader/`.

No se ha ejecutado la validación ni la carga en Claude Code. La compatibilidad
con una versión concreta está pendiente; esta base no es un prototipo funcional.

La documentación de instalación definitiva, pruebas, privacidad y limitaciones
se completará a medida que se implemente y compruebe cada parte.

## Referencias oficiales

- [Creación de mods](https://code.claude.com/docs/en/plugins/mods/create).
- [Distribución de plugins](https://code.claude.com/docs/en/plugins/publish).

Elaborado con asistencia de IA; requiere revisión humana.
