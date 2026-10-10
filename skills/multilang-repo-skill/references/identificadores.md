# Índice de identificadores

Sirve para localizar una regla por su identificador, citarla o eximir de ella. Los identificadores
son estables: una regla retirada no se reutiliza con otro significado.

## Contenido
- Dónde está cada regla
- Cambios respecto al marco anterior (v7)

## Dónde está cada regla

| Prefijo | Ámbito | Identificadores | Fichero |
|---|---|---|---|
| R | Núcleo: trabajo, permisos, evidencia | R1–R20 | SKILL.md |
| D | Diseño | D1 | SKILL.md (Fase 3) |
| | | D2–D7 | references/seleccion-idioma.md |
| | | D8–D15, D17–D20 | references/diseno-catalogos.md |
| | | D16, D30, D31 | references/formatos-rtl-unicode.md |
| | | D21–D23, D25, D27–D29 | references/instrucciones-y-agentes.md |
| | | D24 | references/seguridad.md |
| | | D26 | references/traducciones.md |
| P | Pruebas, revisión y triaje | P1–P15 | references/pruebas-y-evidencia.md |
| T | Traducciones | T1–T7 | references/traducciones.md |
| C | Contenido externo | C1–C9 | references/contenido-externo.md |
| S | Seguridad | S1–S4, S6 (S5 retirada) | references/seguridad.md |
| Doc | Documentación y paquete | Doc1–Doc9 | references/documentacion-y-paquete.md |
| G | Publicación | G1–G9 | references/publicacion.md |
| M | Delegación | M1–M7 | references/delegacion.md |

Las fases conservan la numeración 0–9. Las categorías del inventario son letras sueltas (A–H) y no
deben confundirse con identificadores de regla.

## Cambios respecto al marco anterior (v7)

Se conservan el número y el sentido de R1–R16, D1–D29, P1–P12, T1–T6, C1–C8, G1–G9 y M1–M7. Algunas
reglas amplían o acotan su alcance sin cambiar su objeto:

| Identificador | Cambio |
|---|---|
| R4, R5 | El ritmo de los resúmenes y de las preguntas depende del modo de supervisión (R18). |
| R6 | Añade la ubicación del registro y la reanudación con una sola confirmación. |
| R7 | Seis niveles: añade `estática` y `humana` y distingue `ci` de `local`. |
| R13 | Distingue capacidad, necesidad y autorización; los permisos permanentes no se vuelven a pedir. |
| R16 | La nota de IA solo va en documentos públicos para personas, nunca en ficheros de máquina. |
| D1 | Distingue salidas deterministas (comparación exacta) de instrucciones para modelos (texto exacto e invariantes). |
| D3 | Conserva la subetiqueta de escritura, trata `C`/`POSIX` como ausencia y admite eslabones explícitos. |
| D4 | Distingue entrada explícita de entrada ambiental. |
| D13 | Primero, el formato del ecosistema; NFC no se impone a los literales de referencia. |
| D16 | Ya no incluye RTL, que pasa a D30. |
| D18 | Añadir `lang` a la salida por defecto requiere excepción (D23). |
| D22 | Los avisos nunca van dentro de formatos de máquina. |
| P4 | No aplica a texto generado por modelos; es nivel `local`. |
| P5 | Las pruebas de invariancia se validan con sabotaje, no viéndolas en rojo. |
| P7 | Se aplica a las comprobaciones que escribes, en proporción a la escala. |
| M1–M7 | El módulo [multi-modelo] pasa a ser [delegación] y deja de depender de un protocolo externo. |

Identificadores nuevos: R17 (precedencia, antes un párrafo sin identificador), R18 (modos), R19
(alcance de la petición), R20 (proporcionalidad, antes un párrafo y la tabla de la Fase 1.8), D30,
D31, P13–P15 (antes Fases 8.2, 8.1 y 8.3, sin identificador), T7, C9, S1–S4, S6, y Doc1–Doc9 (antes
la Fase 7, sin identificadores).

Etiquetas de módulo: `[alto riesgo]` pasa a ser `[alto-riesgo]` y ya no fuerza la escala L;
`[multi-modelo]` pasa a ser `[delegación]`; `[release]` se reparte entre `[paquete]` y
`[publicación]`. Son nuevas `[ecosistema]`, `[rtl-escrituras]`, `[seguridad]` y `[documentación]`.
Las escalas S, M y L conservan sus letras, pero ahora miden solo la estructura; el riesgo es un eje
aparte.
