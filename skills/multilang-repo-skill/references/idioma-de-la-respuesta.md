# Idioma de la respuesta de esta skill

Detalle del bloque «Idioma de la respuesta» de `SKILL.md`. Léelo cuando la persona pida un idioma con
`idioma=xx` o `lang=xx`, o cuando dudes de qué se traduce y qué no. Las reglas de selección, el aviso de
traducción automática y el fallo seguro están en el bloque; aquí solo va lo que lo completa.

## Contenido
- Qué idiomas hay y cómo se resuelve una marca
- Qué no se traduce

## Qué idiomas hay y cómo se resuelve una marca

- Disponibles: `es` (los ficheros originales) y `en` (carpeta `i18n/en/`).
- Una variante como `en-GB` o `en_US.UTF-8` cae en `en`, sin distinguir mayúsculas.
- [scripts/resolver_idioma.py](../scripts/resolver_idioma.py) implementa esta regla. Su origen `defecto`
  significa «sin marca», no «responde en español»: sin marca rige R16 (idioma de la persona).
- La marca elige el idioma de la respuesta, no los idiomas a los que se traduce un repositorio.

## Qué no se traduce

Identificadores (R1…Doc9), marcas de módulo, nombres de fichero y de script, opciones, códigos de aviso,
comandos y bloques de código. Los mensajes de los scripts siguen en español.
