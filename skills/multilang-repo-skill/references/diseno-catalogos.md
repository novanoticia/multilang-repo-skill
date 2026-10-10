# Catálogos, claves y ejecución (D8–D15, D17–D20)

Léelo con [ecosistema], [programa] o cuando el proyecto vaya a tener catálogos propios.

## Contenido
- Primero, el ecosistema
- D8–D13 Catálogos y claves
- D14–D15 Ejecución e interpolación
- D17–D20 Datos, artefactos y lógica dependiente del idioma

## Primero, el ecosistema

Si el proyecto ya tiene i18n o su ecosistema tiene un estándar (gettext, i18next, ICU MessageFormat o
MessageFormat 2 si ya lo usa, Fluent, Rails I18n, `strings.xml`, String Catalogs, ARB…), usa su
formato, su extractor, sus reglas de plural, su respaldo y su validador. Entonces D8–D9 sobran y tu
trabajo es cobertura, glosario, pruebas y revisión. `validar_catalogos.py` solo aporta si el formato es
JSON propio o de i18next y el proyecto no tiene validador (P6); no interpreta ICU ni ARB. Traslada lo que sigue a
los mecanismos nativos del formato: contexto con `msgctxt` y comentarios para traductores en gettext,
`@clave` con `description` en ARB, notas en XLIFF, `translatable="false"` en Android. No impongas
campos ni codificaciones que el formato no admite.

Sin i18n implantado, el ecosistema es el mecanismo estándar del lenguaje o del framework. Comprueba
qué cubre sin instalar nada: el módulo `gettext` de Python solo lee `.mo` ya compilados; extraer y
compilar exige `xgettext` y `msgfmt` (GNU gettext) o Babel. Si faltan, instalar es una decisión (R2):
preséntala con el catálogo propio (D8) como alternativa. Los `.mo` se versionan solo si el proyecto no
tiene paso de construcción, con una prueba que los compare con su `.po` por contenido (cargándolos,
p. ej. con `gettext.GNUTranslations`), no por bytes: compiladores distintos dan bytes distintos. Si
falta la herramienta, la prueba se salta y se declara.

## Catálogos y claves

**D8 Catálogo propio (solo sin ecosistema).** Un fichero por idioma, que se descubre al añadirlo: el
código no enumera los idiomas y los ficheros auxiliares (glosario, esquema) no cuentan como idioma.
Acceso con `t(clave, **datos)` o, en instrucciones, un catálogo `clave → frase` que el modelo copia
literalmente.
- Si falta una clave, cae al idioma por defecto y se registra (en pruebas, falla). Si falta también en
  el defecto, es un error de programación.
- El respaldo por clave mezcla idiomas en la salida. Un idioma solo se publica como completo cuando
  el validador lo da completo. Uno parcial puede estar en el repositorio marcado `experimental`
  (D12), con su limitación declarada; el validador lo informa como cobertura parcial, no como error.

**D9 El idioma por defecto es la referencia.** Sus frases son los literales del original: se extraen
con herramientas (P3), no se reescriben a mano. Puede llevar claves nuevas (avisos que el original no
tenía), marcadas como `origen: nuevo`.

**D10 Un literal, una clave.** Una clave por frase completa, también para encabezados, rótulos,
preguntas de parada y cada lista de opciones como unidad. No compongas frases con trozos traducidos.
- Plurales: usa las categorías CLDR del idioma (`zero`, `one`, `two`, `few`, `many`, `other`; cada
  idioma usa un subconjunto) con el mecanismo del ecosistema: plural de ICU, sufijos de i18next,
  `ngettext` con `Plural-Forms`, `<plurals>`. Dos claves (`uno`/`otros`) solo valen si todos los
  idiomas soportados y los números que se muestran usan esas dos categorías. Si no, declara la
  limitación.
- [instrucciones] Distingue «literal del catálogo: cópialo tal cual» de «instrucción entre
  corchetes: redáctala tú». Una lista de opciones entre corchetes no es una instrucción. Fija una sola
  política para los huecos entre corchetes al rellenarlos.

**D11 Metadatos por clave, en proporción.** En catálogos propios: `origen` (`original` | `nuevo`),
`fuente` (fichero y línea del original, contada sin bloques añadidos), `contexto` (una línea para
quien traduce o revisa: dónde aparece, qué significa, límite de longitud), `riesgo` (`alto` en frases
que confirman acciones irreversibles, límites o seguridad), `invariable` (justificado por el propio
texto: símbolos, códigos o nombres propios) y `maquina` (idéntica en todos los idiomas). En escala S,
basta con `contexto` y `riesgo` donde hagan falta. En formatos de ecosistema, usa su mecanismo nativo.
Forma en JSON propio: los metadatos van en la referencia como `"@clave": {"contexto": …, "riesgo": …,
"invariable": true}` (al estilo ARB), que el validador excluye de la paridad. Lo invariable en todos
los idiomas se declara ahí; lo idéntico solo en un idioma (frecuente entre lenguas próximas) se declara
en ese catálogo, en `_meta.invariables`, con su razón.

**D12 Estado de cada idioma.** `referencia`, `borrador-ia`, `experimental` o `revisado`, con quién
redactó y quién revisó. `experimental` es un `borrador-ia` incompleto o de un idioma que no se puede
juzgar: además de no estar revisado, lleva aviso reforzado (T6). `revisado` exige una persona revisora identificada; la opinión de otro modelo
no cambia el estado. Cuando haya revisión humana, basta con actualizar el campo. Dónde se registra: en catálogos JSON
propios, en `_meta`; en formatos de ecosistema que no admiten ese campo (p. ej. JSON de i18next que
la aplicación carga tal cual), en la documentación del proyecto (sección de idiomas del README) o en
un fichero de estado aparte, nunca añadiendo campos que el cargador mostraría o rechazaría.
[scripts/validar_catalogos.py](../scripts/validar_catalogos.py) comprueba esta coherencia en
catálogos JSON (`_meta.estado`, `_meta.revisado_por`).

**D13 Forma del fichero.** Primero, lo que exija el formato del ecosistema: hay formatos con
codificación declarada en la cabecera y formatos heredados que no son UTF-8, así que compruébalo en
lugar de suponerlo. Sin formato impuesto: UTF-8 sin BOM, salto de línea final, orden de claves
determinista y Unicode NFC en las traducciones nuevas. No normalices los literales de referencia si
eso cambia los bytes de la salida por defecto (D1); decláralo como limitación o pide la excepción.

## Ejecución e interpolación

**D14 Estado del idioma en ejecución.** En un proceso de una sola petición vale un idioma global
fijado al arrancar. En servidores, trabajos concurrentes o bibliotecas, el idioma va por petición o
por contexto, nunca en una variable global compartida.

**D15 Plantillas e interpolación.** Solo campos con nombre. Las llaves literales se escapan, y el dato
interpolado nunca se vuelve a interpretar como plantilla, como marcado ni como instrucción. En
instrucciones para un modelo, delimita el dato interpolado como dato (S1).

## Datos, artefactos y lógica dependiente del idioma

**D17 Textos en datos de configuración.** El idioma original se queda donde está y los demás lo
sobrescriben por clave: un único origen por texto e idioma. Si existía un campo de idioma que se
ignoraba y ahora se lee, es un cambio que va al CHANGELOG.

**D18 Artefactos (E).** Decide con la persona si el idioma elegido los afecta. Garantiza que no
mezclan idiomas y declara el idioma en los formatos que lo admiten (`lang` en HTML, metadatos en PDF).
Añadir ese atributo a la salida por defecto cambia sus bytes, así que es una excepción para aprobar
(D23).

**D19 Lo que se aconseja debe reconocerse.** Si el programa aconseja una frase en un idioma, su
detector debe reconocerla en ese idioma. Las frases que activan un modo («ejecuta», «deshaz») también
son literales del catálogo. Los valores mostrados en prosa que vuelven como entrada se reconocen por
equivalencia con el catálogo.

**D20 `--help` y errores del parser.** Suelen construirse antes de conocer el idioma: tradúcelos
resolviendo el idioma antes de construir el parser, o declara la limitación. Los mensajes de scripts
auxiliares pueden quedarse en el idioma original si se declara. Una opción nueva (`--idioma`) cambia
por sí sola la ayuda y la línea de uso en el idioma por defecto. Si la persona pidió esa opción, el
cambio es parte de lo pedido: va en la lista de cambios (D1), se dice en el resumen y el resto se
compara byte a byte. Si no la pidió (la selección es por marca o variable), no la muestres sin
aprobación: ocúltala de la ayuda (p. ej. `help=argparse.SUPPRESS`) y documéntala aparte. Oculta o
no, una opción nueva cambia las abreviaturas que acepta argparse (`--i` pasa a ser ambigua si ya
existía `--input`): elige un nombre sin prefijo común con las opciones existentes o incluye en la
línea base (P2) las abreviaturas que hoy funcionan.
