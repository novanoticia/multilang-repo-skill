# Formatos, RTL y Unicode (D16, D30, D31)

Léelo si el proyecto formatea fechas, números, monedas u ordena texto ([programa]), y siempre con
[rtl-escrituras]. Cuando un estándar sea determinante para una decisión, consúltalo en su fuente
(R10): BCP 47 (RFC 5646 y RFC 4647), CLDR, UAX #9 (bidireccionalidad), UAX #15 (normalización) y
UTS #39 (mecanismos de seguridad Unicode).

## Contenido
- D16 Formatos dependientes del locale
- D30 Texto de derecha a izquierda y escrituras complejas
- D31 Política Unicode: señalar, no eliminar

## D16 Formatos dependientes del locale

- Fechas, horas, números, monedas, unidades, ordenación y cambio de mayúsculas con el mecanismo del
  ecosistema (`Intl`, ICU, Babel, `java.text`…) y el locale elegido. No los reimplementes.
- El idioma por defecto conserva **exactamente** su formato actual (D1). Si pasar al formateador del
  ecosistema cambia sus bytes, sigue usando el formato actual para el defecto o pide la excepción. La
  línea base lo detecta.
- Las operaciones sobre contratos de máquina (claves, comandos, identificadores) no dependen del
  locale. En Java, `"i".toUpperCase()` con el locale por defecto en turco da `İ`, y en JavaScript lo
  hace `toLocaleUpperCase("tr")`: compara y transforma esos contratos con operaciones invariantes
  (`toUpperCase(Locale.ROOT)`, `toUpperCase()` en JavaScript).
- Las cadenas crecen al traducirse. Reserva espacio, no trunques en silencio y prueba con
  pseudo-locale (P4).

## D30 Texto de derecha a izquierda y escrituras complejas

- Declara la dirección en el soporte: `dir="rtl"` y `lang` en HTML, y propiedades lógicas de CSS
  (`margin-inline-start` en lugar de `margin-left`). Refleja los iconos direccionales.
- Aísla los valores de dirección contraria que se interpolan (nombres, rutas, comandos, números) con
  `<bdi>`, con los aislamientos U+2068…U+2069 o con el aislamiento que ya aplique el framework. Así un
  contrato en caracteres latinos no se desordena dentro de una frase en árabe o hebreo.
- Comprueba la visualización real: unión de letras en árabe, conjuntos en escrituras índicas, tablas y
  Markdown en RTL. Muchos terminales no aplican el algoritmo bidireccional: en herramientas de
  consola, prueba o declara la limitación.
- Cierra con una prueba de visualización (captura o salida renderizada revisada) o con la limitación
  declarada. Si el revisor no lee el idioma, dilo.

## D31 Política Unicode: señalar, no eliminar

Muchos caracteres invisibles son legítimos y necesarios. Eliminarlos de forma indiscriminada rompe
idiomas reales:

| Carácter | Uso legítimo |
|---|---|
| ZWNJ U+200C | Ortografía persa y de otras lenguas (`می‌خواهم`) |
| ZWJ U+200D | Conjuntos en escrituras índicas; secuencias de emoji (👨‍👩‍👧) |
| LRM/RLM U+200E/U+200F, ALM U+061C, aislamientos U+2066–U+2069 | Texto bidireccional bien formado |
| Selectores de variación U+FE00–U+FE0F, U+E0100–U+E01EF | Presentación de emoji; variantes de ideogramas |
| U+200B | Cortes de línea en lenguas sin espacios (tailandés, jemer, lao, birmano) |
| U+00AD | División silábica opcional |
| Etiquetas U+E0020–U+E007F tras U+1F3F4 | Banderas de subdivisión (p. ej. la de Escocia) |

Merecen revisión, y por eso se señalan:
- Incrustaciones y anulaciones bidireccionales U+202A–U+202E. Pueden mostrar un orden visual
  distinto del lógico y ocultar el contenido real a quien revisa (el vector de los ataques «Trojan
  Source»). En texto RTL suelen bastar los aislamientos.
- Controles bidireccionales sin pareja dentro de un valor.
- Caracteres de etiqueta U+E0000–U+E007F fuera de una bandera: invisibles, pueden ocultar texto.
- Cualquier invisible, control o mezcla de escrituras dentro de un **contrato de máquina** (clave,
  marcador, comando, opción, URL): allí es un error, porque un homógrafo o un invisible cambia la
  identidad del contrato.

Procedimiento: genera el informe con
[scripts/validar_catalogos.py](../scripts/validar_catalogos.py), revisa cada caso con su contexto,
decide con la persona y corrige solo el caso concreto. El script nunca modifica ficheros. Un informe
sin hallazgos significa que no se encontraron esos patrones, no que el texto sea seguro (S6).
