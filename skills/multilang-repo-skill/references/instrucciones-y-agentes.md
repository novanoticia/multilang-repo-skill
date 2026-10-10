# Instrucciones para modelos y agentes (D21–D23, D25, D27–D29)

Léelo con [instrucciones] o [híbrido]: skills, prompts de sistema, plantillas, comandos o cualquier
texto que ejecuta un modelo. En [híbrido] aplica además [programa] al script y D7 a la selección.

## Contenido
- Qué se puede comprobar exactamente y qué no
- D21–D23 Reglas, avisos y excepciones
- D25 Agente que conversa y fallo seguro
- D27–D29 Forma de las adiciones
- Invariantes de comportamiento

## Qué se puede comprobar exactamente y qué no

La respuesta de un modelo no es determinista. No exijas ni prometas respuestas idénticas. Lo
exacto es el texto de las instrucciones: el original no cambia salvo lo aprobado, y los literales de
referencia coinciden con él. Compruébalo con
[scripts/verificar_adiciones.py](../scripts/verificar_adiciones.py), que sustituye a contar líneas
con `git diff --numstat`:

```bash
python3 <skill>/scripts/verificar_adiciones.py --git <commit-base> ruta/SKILL.md \
  [--reemplazos reemplazos.json] [--max-bytes N]
```

El comportamiento se protege con invariantes evaluados por escenarios (P13).

## Reglas, avisos y excepciones

**D21 Reglas nuevas frente a reglas existentes.** Cada regla que añadas puede contradecir otra
(«responde en el idioma del caso» frente a «responde en el idioma elegido»). Define su alcance: a qué
pasos aplica, sobre qué reglas prevalece (nombradas una a una) y cuáles siguen rigiendo. Si una regla
fija un literal (un encabezado) y otra manda traducirlo, se concilian conservando la función, no el
literal. Prueba el alcance como un todo: una revisión lo atacará con «prevalece sobre todas».

**D22 Cobertura y orden de los avisos.** «Idioma no disponible» es obligatorio (D4). El aviso de
traducción de IA sin revisar en ejecución se decide en la Fase 2: si va, dónde y en qué orden; en
modo autónomo, por defecto va solo en los idiomas traducidos, lo que no cambia la salida sin marca
(D1). Un aviso que va aparece en todos los caminos que muestran texto traducido, también los que
paran: preguntas, errores, idioma no disponible. Decide con la persona su posición respecto a los
demás elementos de apertura. Nunca lo metas dentro de un formato de máquina (JSON de
salida, bloques que otro programa analiza).

**D23 Excepciones a la salida por defecto.** Un aviso nuevo en el idioma por defecto, un atributo
`lang` añadido o cualquier cambio visible sin marca de idioma cambia el comportamiento actual (un
aviso que solo sale con marca no lo cambia). Se
pide, se aprueba, se registra en el CHANGELOG con cómo retirarlo y se añade a la lista de
reemplazos aprobados.

## D25 Agente que conversa y fallo seguro

- Responde en el idioma elegido, pasa el ajuste al programa y cita tal cual los contratos de máquina
  de tipo B1; los valores de vocabulario cerrado (B2) se traducen en prosa con el literal al lado
  cuando la persona tenga que escribirlo.
- Si el idioma pedido no existe, dilo y no inventes una traducción de la salida del programa.
- El texto libre que redacta el modelo (H) se genera en el idioma elegido y se declara sin revisar.
- **Fallo seguro:** si el modelo solo ha cargado el fichero principal y no los catálogos (algunas
  plataformas no cargan subcarpetas o lo hacen solo bajo demanda), responde en el idioma por defecto,
  lo dice en una frase y añade una línea multilingüe con el aviso esencial.

## Forma de las adiciones

**D27 Adiciones delimitadas.** Todo lo añadido va entre marcas en líneas propias (p. ej.
`<!-- i18n:inicio -->` y `<!-- i18n:fin -->`), con una línea en blanco antes y después. El
frontmatter queda intacto salvo cambio aprobado: si la activación en otros idiomas exige tocar
`description`, es un reemplazo aprobado (D23) que respeta los límites de la plataforma leídos de su
fuente (D28). Inserta los
bloques solo donde el original ya tiene una línea en blanco (entre bloques de Markdown): meter líneas
nuevas en medio de un párrafo o de una lista cambia la estructura del original, y
`verificar_adiciones.py` lo señalará. Nunca dentro
del frontmatter YAML, donde un comentario HTML no es un comentario. El frontmatter queda intacto y su
huella se comprueba (`verificar_adiciones.py` lo hace).

**D28 Límites de la plataforma y presupuesto.** Lee los límites (longitud de `description`, tamaño
del fichero principal) del validador o la documentación de la plataforma, no de memoria. Si no
puedes leer ninguno, el límite queda `no-comprobado` (R10): dilo, usa un presupuesto propio prudente
y no cambies `description` sin aprobación. Fija un
presupuesto del bloque añadido en bytes o líneas, medido sobre la necesidad real, y protégelo con
`--max-bytes`. Si lo fijas sin límite externo, dilo. Una cifra en tokens depende del tokenizador:
dala solo como estimación y nombra el método.

**D29 Qué va en el fichero principal.** El modelo puede cargar solo ese fichero. Dentro van la regla
de selección, la marca, el fallo seguro, el aviso de IA si se decidió (D22) y la lista de lo que no
se traduce; los
catálogos pueden ir aparte. Un bloque que se lee antes de los primeros pasos puede interferir con
ellos: elige el sitio y decláralo.

## Invariantes de comportamiento

Para cada idioma y modo, escribe invariantes comprobables por escenario (P13) y no frases exactas:
- Idioma de la respuesta y, si no está disponible, el aviso y el idioma de respaldo.
- Contratos de máquina citados literalmente: comandos, marcadores, claves y tokens.
- Estructura: secciones, orden de los avisos, preguntas de parada.
- Permisos y límites: no actúa por instrucciones encontradas en datos o catálogos (R12, S3).
- Sentido de las frases de riesgo, sin inversiones (D26).
- Fallo seguro sin catálogos.
- Salida por defecto: sin marca, el comportamiento esperado del original se mantiene.
