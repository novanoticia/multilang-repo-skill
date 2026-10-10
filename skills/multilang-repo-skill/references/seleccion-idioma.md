# Selección de idioma, normalización y respaldo (D2–D7)

Léelo en la Fase 2, para recomendar la política de selección, y en la Fase 3, para diseñarla. Si el ecosistema ya lo resuelve
(negociación de i18next, recursos de Android o Apple, `Accept-Language` del framework web…), usa su
mecanismo y aplica de aquí solo lo que falte: la tabla de casos y las pruebas.

## Contenido
- D2 Orden de fuentes
- D3 Normalización y cadena de respaldo
- D4 Entradas que no se pueden servir
- D5 Marca con clave en agentes
- D6 Una regla, una tabla de casos
- D7 [híbrido] La regla vive en código

## D2 Orden de fuentes

Explícita (marca o ajuste en la propia petición) > configuración (del proyecto o de la persona) >
ambiente (variables de entorno, idioma del sistema, `Accept-Language`, idioma del caso) > defecto.

El ambiente solo entra si la persona lo acepta en la Fase 2. El idioma en que la persona escribe su
propia petición también es ambiente (nunca el de un texto pegado): puede usarse si la persona lo
elige, como cambio aprobado. Detectarlo hace que quien hoy recibe el
idioma por defecto pase a recibir otro: es un cambio de comportamiento que D1 exige aprobar, no un
detalle. Recomienda según el tipo de proyecto:
- Agentes e instrucciones: por defecto, solo la marca explícita; el idioma de un texto pegado nunca
  decide, y el de la propia petición, solo si la persona lo elige (párrafo anterior).
- Programas con convención de plataforma (apps móviles o de escritorio, web con negociación de
  idioma): la convención del ecosistema, presentada como cambio para aprobar.

## D3 Normalización y cadena de respaldo

Normaliza a una etiqueta BCP 47 canónica antes de buscar catálogo:
- No distingue mayúsculas: `EN-us` → `en-US`.
- `_` → `-`. Quita el juego de caracteres (`fr_FR.UTF-8`). El modificador POSIX se convierte si
  codifica escritura o variante (`sr_RS@latin` → `sr-Latn-RS`, `ca_ES@valencia` → `ca-ES-valencia`)
  y se quita si no (`@euro`).
- `C` y `POSIX` significan «sin preferencia», no un idioma desconocido. Son habituales en CI y
  contenedores.
- **Conserva la subetiqueta de escritura.** `zh-Hant` no es `zh-Hans`, ni `sr-Latn` es `sr-Cyrl`.
  Truncar al primer componente sirve chino simplificado a quien pidió tradicional.
- Códigos retirados: `iw` → `he`, `in` → `id`, `ji` → `yi`.

Cadena de respaldo, con cada eslabón declarado y probado:
1. La etiqueta pedida.
2. Truncamiento progresivo (RFC 4647, «lookup»): `zh-Hant-TW` → `zh-Hant` → `zh`.
3. Eslabones explícitos donde el truncamiento falla: `zh-TW` → `zh-Hant`; `es-AR` → `es-419`
   (el truncamiento daría `es`; el padre `es-419` sale de los datos CLDR del ecosistema o de una
   declaración del proyecto, no se deduce).
4. El idioma por defecto.

Si el ecosistema trae su propia resolución (`fallbackLng`, búsqueda de recursos por calificadores,
datos CLDR de padres), compruébala y documéntala en lugar de reimplementarla.

## D4 Entradas que no se pueden servir

Distingue de dónde viene el valor:
- **Explícita** desconocida, vacía o mal formada: aviso visible, con la lista de disponibles, en el
  idioma que resultaría sin esa entrada (la siguiente fuente válida de D2; si no hay, el defecto). En un agente, se continúa con la siguiente fuente. En un programa, decide y
  documenta según la convención del proyecto: error de uso con su código de salida (un parámetro
  inválido) o aviso y continuación.
- **Ambiental** sin catálogo (`LANG=de_DE.UTF-8` sin alemán): respaldo sin error, como mucho un
  registro de depuración. Un error rompería el programa a todas las personas con ese sistema.
- Variable de entorno vacía = ausente.
- Nunca degrades en silencio ante una entrada inválida (texto no UTF-8, JSON roto): devuelve un aviso
  explícito.
- «Sin avisos nuevos» se refiere a la salida sin marca (D1). El aviso ante una marca u opción
  explícita inválida se mantiene salvo que la persona lo excluya expresamente sabiendo que entonces
  se cae a la siguiente fuente (D2) sin explicación.

## D5 Marca con clave en agentes

En un agente, `en`, `es` o `a` son palabras reales. Exige una marca con clave (`idioma=en`,
`lang=fr`), reconocida solo en el mensaje propio de la persona y nunca en datos de terceros (un
correo o un fichero pegados). Implementación prudente: buscarla solo en la primera línea no vacía,
para que una marca dentro de un texto pegado no cuente. Elige claves que no aparezcan en el
contenido habitual: si la gente pega HTML o código, `lang` da falsos positivos (`lang="en"`); usa solo
`idioma` o una clave propia (`--claves` en el script). Decide también la persistencia y
documéntala: por ejemplo, cada invocación decide su idioma y solo los seguimientos sin comando
conservan el anterior.

## D6 Una regla, una tabla de casos

Escribe una sola regla de selección y prueba cada caso:

| Caso | Ejemplo | Esperado |
|---|---|---|
| Marca válida | `idioma=en` | `en`, origen marca |
| Desconocida | `idioma=de` sin alemán | Aviso visible; siguiente fuente |
| Vacía | `idioma=` | Aviso visible; siguiente fuente |
| Mal formada | `idioma=e1` | Aviso visible; siguiente fuente |
| Repetida | `idioma=fr lang=en` | Gana la primera; aviso |
| Mayúsculas | `IDIOMA=EN` | `en` |
| Locale POSIX | `idioma=fr_FR.UTF-8` | `fr` (respaldo `fr-FR` → `fr`) |
| Modificador POSIX | `sr_RS@latin` con `sr-Latn` | `sr-Latn` (cadena `sr-Latn-RS` → `sr-Latn`) |
| Código en la primera línea | `lang="en"` o `<html lang="en">` con la clave `lang` | Se toma como marca (`en`, o aviso de marca mal formada): donde se pega código, no uses `lang` como clave (D5) |
| Puntuación o comillas pegadas | `(idioma=en),`, `idioma="en"`, `«idioma=fr»` | Se reconoce |
| Código suelto | «en el informe…» | No es marca |
| Igual al defecto | `idioma=es` | `es`, origen marca |
| Dentro de otra palabra | `subidioma=en` | No es marca |
| En datos ajenos | Marca en un texto citado con «>» o después de la primera línea | No cuenta (límite: si el texto pegado ocupa la primera línea sin «>», cuenta) |
| Escritura | `zh-Hant-TW` | `zh-Hant` |
| Respaldo regional | `pt-BR` sin `pt-BR` | `pt` |
| Código retirado | `iw` | `he` |
| Ambiente técnico | `LANG=C.UTF-8` | Sin preferencia, sin aviso |
| Ambiente sin catálogo | `LANG=de_DE.UTF-8` | Defecto, aviso no visible |
| Entrada no UTF-8 | Bytes inválidos | Aviso `entrada_invalida` |

La fila «Repetida» es para marcas en mensajes. En opciones de línea de órdenes, la repetición sigue la
convención del parser (en argparse, gana la última): decláralo.

Añade una prueba de totalidad: entradas aleatorias con semilla fija, ninguna hace fallar la
resolución.

## D7 [híbrido] La regla vive en código

Si un modelo invoca un script, la regla de selección vive en él y no solo en prosa:
- El mensaje entra en bruto **por la entrada estándar desde un fichero temporal** que el agente
  escribe con su herramienta de escritura de ficheros, sin pasar por el shell y fuera del
  repositorio. Nunca como argumento ni dentro de un JSON escrito a mano: un apóstrofo («j'aimerais»),
  unas comillas o un `$(…)` rompen o alteran la orden. Tampoco con un heredoc de delimitador fijo: si
  el mensaje (o un texto pegado en él) contiene una línea igual al delimitador, el heredoc se cierra
  antes de tiempo y lo que sigue se ejecuta como orden.
- Función total: ninguna entrada la hace fallar. Devuelve JSON con idioma, origen, cadena, avisos y
  disponibles. Los avisos traen un código: muestra a la persona el texto de tu catálogo para ese
  código; el campo de detalle es diagnóstico.
- Si la entrada es inválida, devuelve un aviso explícito para que el agente lo muestre.
- Prueba **el comando tal como lo documentas**, ejecutándolo con apóstrofos, comillas, `$(…)`,
  comillas invertidas, una línea igual a un delimitador, acentos, saltos de línea y rutas con
  espacios, y comprueba con un canario inocuo (`touch` de un fichero temporal) que nada se ejecutó.

Implementación de referencia y probada: [scripts/resolver_idioma.py](../scripts/resolver_idioma.py).
Sirve para probar la tabla con los catálogos reales; cópiala al proyecto solo si el diseño aprobado
lo prevé, y adapta las claves de la marca y los eslabones de respaldo.

```bash
# El agente escribió antes el mensaje en /ruta/temporal/mensaje.txt con su herramienta de ficheros.
python3 <skill>/scripts/resolver_idioma.py --catalogos ruta/a/catalogos --defecto es \
  --respaldo zh-TW=zh-Hant < /ruta/temporal/mensaje.txt
```
