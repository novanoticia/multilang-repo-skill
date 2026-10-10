# Trazabilidad: v7 → MultiLang Repo Skill (v9)

## 1. Cambios sustantivos respecto a v7

| Ámbito | v7 | v9 (skill) | Motivo |
|---|---|---|---|
| Forma | Un prompt de 837 líneas para pegar en la conversación | Skill con SKILL.md de 455 líneas, 12 referencias de carga condicional, 5 plantillas y 3 scripts probados | Carga progresiva: el agente lee solo los módulos activos |
| Precedencia | Párrafo «Prelación» sin entorno ni chat (L18) | R17: entorno > persona > proyecto y repositorio > skill; en caso de choque, la opción más restrictiva | Faltaban niveles, y el repositorio era a la vez autoridad y dato |
| Alcance de la petición | No existía | R19: análisis, implementación o publicación | Una petición de análisis no puede acabar modificando el repositorio |
| Supervisión | Tarea a tarea, una pregunta por mensaje y diseño por secciones, siempre | R18: modo guiado por defecto (lo conserva) y autónomo opcional con siete puntos de parada | Se respeta la preferencia de supervisión y se ofrece una alternativa con límites |
| Preguntas | Fase 2 con lista fija | R5: solo decisiones que cambian resultado, riesgo, coste o permisos; lo que está en el repo no se pregunta | Evitar preguntar datos disponibles |
| Registro | «Libro de sesión»; «un permiso que no está en el libro no existe» | R6: memoria, no autoridad; ubicación fuera del repo o excluida; reanudación con una sola confirmación | Un fichero no puede conceder permisos (R12) |
| Permisos | R13 por acción | R13: capacidad, necesidad y autorización; los permisos permanentes no se vuelven a pedir dentro de su alcance; sin pruebas con efectos | Lo pide el encargo; elimina confirmaciones redundantes sin perder control |
| Evidencia | Cuatro niveles | R7: seis niveles (`estática`, `local`, `ci`, `simulada`, `plataforma`, `humana`) y estados; las afirmaciones de ausencia, siempre acotadas | Distinguir revisión humana y comprobación estática; prohibir lo diseñado presentado como ejecutado |
| Nota ética | En textos públicos | R16: solo en documentos públicos para personas, una vez | Sin cambio de fondo; se deja explícito que nunca va en ficheros de máquina |
| Proporcionalidad | S/M/L; «[alto riesgo] fuerza L» | R20: S/M/L por estructura y riesgo como eje aparte; tabla de exigencias por escala | Una skill de un fichero de alto riesgo no es un monorrepositorio |
| Módulos | 8 etiquetas, sin «permite omitir» ni «evidencia de cierre» | 12 módulos, cada uno con activación, exigencias, omisiones y evidencia de cierre | Lo pide el encargo |
| D1 | Byte a byte para toda salida | Dos regímenes: comparación exacta para lo determinista; texto exacto e invariantes para lo que ejecuta un modelo | La identidad de la salida de un modelo es imposible |
| D3 | Trunca al primer subcódigo | BCP 47: conserva la escritura, trata `C`/`POSIX` como ausencia, códigos retirados y eslabones explícitos o de CLDR | `zh-Hant` ≠ `zh-Hans`; `es-AR` → `es-419` no sale de truncar |
| D4 | «No rompe nada» y «error de uso» a la vez | Entrada explícita frente a ambiental | Un error ante `LANG` rompería el programa |
| D8 | Respaldo por clave | + publicar idiomas completos; los incompletos, `experimental` | Evitar la mezcla de idiomas |
| D10 | «O con dos claves» | Categorías CLDR mediante el ecosistema | Árabe, polaco, ruso… |
| D11, D13 | Metadatos y forma universales | Proporcionales y por mecanismo nativo; NFC no se aplica a los literales de referencia | Compatibilidad con ecosistemas y con D1 |
| D16 → D16/D30/D31 | Formatos y RTL juntos | D16 formatos (el defecto conserva su formato; mayúsculas invariantes en contratos), D30 RTL, D31 política Unicode | Más detalle y no eliminar Unicode legítimo |
| D18, D22, D23 | `lang` obligatorio; avisos sin límite de formato | `lang` en el defecto = excepción; avisos nunca en formatos de máquina | Coherencia con D1 y con los contratos |
| P2 | `numstat` como comprobación | `verificar_adiciones.py`, comparación exacta | `numstat` no demuestra qué cambió |
| P3 | Herramientas (AST, codemod, script) | Primero el extractor del ecosistema; AST solo si compensa | Proporcionalidad |
| P4, P5, P7 | Universales según la escala | Pseudo-locale solo con código; TDD donde hay comportamiento; las invariancias se demuestran con sabotaje; el sabotaje se aplica a lo que escribes | Controles con valor real |
| P10 | CI en verde leído en la plataforma como criterio | El CI queda `pendiente` declarado si no hay permiso para subir o no hay CI | No era posible cumplirlo sin publicar |
| Fase 8 | Sin identificadores | P13 (escenarios), P14 (revisión), P15 (triaje) | Citables y eximibles |
| Fase 7 | Sin identificadores | Doc1–Doc9 | Ídem |
| Seguridad | R12 y D24 | + módulo [seguridad]: S1–S4, S6 | Recoge lo útil de v8 de forma proporcional |
| Contenido | C1–C8 | + C9: rigor proporcional al riesgo, referencias recuperables, nada de marcas de cita sin fuente | Lo pide el encargo |
| Traducciones | T1–T6 | + T7 (texto libre del modelo); el pronombre de T6, corregido | Categoría H explícita |
| Multi-modelo | Módulo M acoplado a `alternancia-modelos` | [delegación] M1–M7: paralelo, revisión, escenarios y secuencial; sin depender de modelos concretos | No depender de otra skill ni de un modelo |
| Dominios de red | Entrega obligatoria al principio | Solo si hacen falta fuentes externas y la red está restringida | Ceremonia sin valor en repos sin red |
| Criterios de aceptación | Lista universal | Criterios del núcleo + cierre por módulo con `pendiente` permitido y motivado | Algunos criterios eran imposibles (CI sin permiso) |
| Datos | Bloque para rellenar dentro del prompt | Plantilla `assets/datos-y-alcance.md` con el origen de cada dato | Separar la plantilla de las reglas |
| Categoría B | Contratos de máquina en un solo grupo | B1 (siempre literal) y B2 (vocabulario cerrado que se traduce en prosa) | Las reglas sobre contratos en prosa se contradecían |
| Dato no comprobado | Reglas en R10, C3, C8 y T4 con matices distintos | Regla única en R10 y vocabulario `oficial`, `segunda-mano`, `no-comprobado` | Coherencia |
| D7 (híbrido) | Heredoc con delimitador entre comillas | Fichero temporal escrito sin shell y redirigido | El heredoc de delimitador fijo admite inyección (demostrado) |
| R4, R17, Fase 2 | Sin regla para «sigue hasta terminar», «hazlo» ni órdenes que causan daño | «Sigue hasta terminar» = encadenar tareas locales con paradas; un «hazlo» no decide por la persona; una orden que causa daño probable se confirma antes | Ambigüedades recurrentes en los escenarios |
| R18, Fase 2, P1 | Paradas fijas en las dos formas de trabajo | Regla única por modo: en guiado, dos paradas antes de tocar nada y una tras cada tarea; en autónomo, lo entendido, el diseño y el plan se declaran como supuestos corregibles con el valor por defecto más prudente, y solo se para en siete puntos. «Hazlo» fija el alcance, no el modo | La versión anterior se contradecía: un ejecutor en autónomo se detuvo sin entregar nada (E3) y otro en guiado implementó todo de una vez (E1, ronda 2) |
| D1, D23, D20 | Sin pauta para avisos con marca ni para opciones nuevas | Un aviso que solo sale con marca no cambia la salida sin marca; una opción nueva que altera `--help` es parte de lo pedido si la persona la pidió, y si no, se oculta | Escenarios E3 y E6 |
| D4, D6 | Error de entrada explícita en el idioma por defecto; la primera marca repetida gana | Error en el idioma que resultaría sin esa entrada; en opciones de línea de órdenes, la convención del parser | Coherencia con D2 y con argparse (E6) |
| P10 | Sin pauta para «CI en verde» sin CI | Se dice en el mensaje que no hay CI ni forma de comprobarlo; la suite verde es `local`; el workflow, decisión aparte | Escenario E6 |
| R10, C1, [alto-riesgo] | Dato de alto riesgo sin fuente: no entra, sin más | Si la persona insiste, se explica el riesgo y se pide la fuente; si lo ordena, R17 y marca `no-comprobado` en el texto. El índice de fuentes es la alternativa, con las de memoria marcadas | Escenario E8, ronda 2 |
| R6, R19 | Registro siempre en disco; commits según convenciones | Ubicación por orden (fuera; dentro, excluido con `git rev-parse --git-path info/exclude`; si no, al final de cada resumen); por defecto, rama de trabajo y un commit por tarea; sin git, copia del original como línea base | Escenarios E3 y E6; revisión final |
| R4, R18 | «Sigue hasta terminar» sin efecto definido | Pasa a autónomo hasta cerrar el plan en curso y luego vuelve el modo anterior | Revisión final |
| D3, `resolver_idioma.py` | Descarta el modificador POSIX | `@latin`/`@cyrillic`/`@devanagari` → escritura; `@valencia` → variante | `sr_RS@latin` perdía la escritura (revisión final) |
| Ecosistema sin i18n | «gettext de Python sin dependencias» | El módulo solo lee `.mo`; compilar exige herramientas; instalar es decisión; `.mo` comparados por contenido | Afirmación técnica falsa (revisión final) |
| D22, T5, D29 | Aviso de IA en ejecución «obligatorio» y a la vez decidible | «Idioma no disponible», obligatorio; el aviso de IA en ejecución se decide en la Fase 2 (en autónomo, solo en los idiomas traducidos) | Revisión final |

Se conservan sin cambios de fondo: R1, R3, R8–R12, R14, R15, D2, D5–D7, D9, D12, D14, D15,
D17, D19–D21, D24–D29, P1, P6, P8, P9, P11, P12, T1–T5, C1–C8, G1–G9, Doc (antes Fase 7), el orden
del informe final y la tabla de evidencias.

## 2. Propuestas de v8

| Propuesta de v8 | Decisión | Cómo queda |
|---|---|---|
| Fase 7 de seguridad (S1–S5) | Modificada | Módulo [seguridad] condicional; el núcleo R12 sigue siempre vigente |
| S1 escáner de patrones de inyección | Modificada | S2 (triaje de diffs) y S3 (escenarios adversariales multilingües); nunca como prueba de ausencia (S6) |
| S2 filtrar y bloquear invisibles | Descartada tal cual | D31: señalar y no eliminar; el validador informa por escritura y contexto |
| S3 carga aislada sin escalar privilegios | Aceptada y concretada | S1 (límite de confianza) más S3 (prueba adversarial) |
| S4 manifiesto TBOM que bloquea el pipeline | Modificada | S4 proporcional: solo para catálogos que llegan de fuera en la construcción |
| S5 aislamiento de variables interpoladas | Fusionada | Ya era D15; S5 se retira |
| Escala XS/S/M/L/XL | Descartada | S/M/L por estructura; riesgo aparte (R20) |
| Presupuesto de tokens y «densidad de información» | Modificada | D28: bytes o líneas; los tokens, solo como estimación con un tokenizador nombrado; la «densidad», descartada por no estar definida |
| Cadenas de respaldo multinivel (`es-AR` → `es-419` → `es`) | Aceptada y corregida | D3: eslabones explícitos o datos CLDR, nunca por truncamiento |
| Soporte RTL ampliado | Aceptada | D30 y D31 |
| Compatibilidad obligatoria con MessageFormat 2.0 | Modificada | Se usa si el ecosistema ya lo usa; no se impone |
| Renumeración de fases (seguridad = 7; documentación, revisión y publicación = 8–10) | Descartada | Fases 0–9 como en v7 |
| Prefijos S y Doc | Aceptados | Declarados en `references/identificadores.md` |
| R7 con niveles numerados 1–4 | Modificada | Seis niveles con nombre y sin jerarquía implícita |
| R16 nota ética en todo archivo | Descartada | Alcance de v7 |
| D17 aviso al inicio estricto de toda interacción | Modificada | D22 y D23 |
| D11 metadatos obligatorios en toda entrada | Modificada | Proporcionales y por mecanismo nativo |
| D4 «jamás interrumpe» | Modificada | Explícita frente a ambiental |
| Roles de modelo (Primario, Revisor, Simulador) | Modificada | M2 y M3; la decisión de publicar es siempre de la persona |
| M6 triaje con categoría «Incompatible» | Aceptada | P15 |
| Libro de sesión `.session_book.md` en el repo | Modificada | Fuera del repo o excluido con `.git/info/exclude`; nunca en el paquete |
| Campo de Datos «Cadena de respaldo» | Aceptado | `assets/datos-y-alcance.md` |
| Permisos de fusión o Release concedidos de antemano en Datos | Modificada | Permisos permanentes con cita, alcance y vigencia (R13) |
| C5 discrepancias «sin inclinarse por ninguna» | Descartada | C6 de v7 (peso de cada fuente) |
| T6 «absoluta certeza» | Descartada | T6 de v7 (autorización tras explicar el riesgo) |
| P8 paquete sin herramientas de desarrollo | Modificada | P9 de v7: «ni uno menos ni uno más» |
| Doc6 manual en PDF | Aceptada | Doc9, condicional |
| Matriz de permisos detectados frente a bloqueados en la Fase 0 | Modificada | Limitaciones con comprobaciones de solo lectura (R13) |
| Tabla de evidencia con resultados ya rellenos | Descartada | Plantilla vacía con estados |
| Escáner como barrera «DevSecOps» obligatoria | Descartada | S2 y S3 proporcionales |
| Marcas «[cite: n]» | Eliminadas | C9 |
| Garantías absolutas | Eliminadas | R7 y S6 |

## 3. Decisiones provisionales que tomé (ambigüedades no bloqueantes)

| Decisión | Alternativa | Coste si estaba mal |
|---|---|---|
| `description` de 960 caracteres (límite de la especificación y de Claude Code: 1024) | Recortarla a 200, como dice el centro de ayuda de claude.ai | En claude.ai la subida podría rechazarla: el informe incluye una versión corta para ese caso |
| `metadata.version: "9.0.0"` | Sin `metadata` | Ninguno conocido: el campo está en la especificación y lo acepta el validador del entorno |
| Pruebas de los scripts dentro del paquete (`scripts/tests/`) | Fuera del paquete | Unos 30 KB más; Claude no las lee salvo que modifique un script |
| Escalas S/M/L conservadas con sentido nuevo | Letras nuevas | Alguien acostumbrado a v7 podría leer «L» como «alto riesgo»; `identificadores.md` lo aclara |
| Etiquetas de módulo con guion (`[alto-riesgo]`) | Con espacio, como v7 | Ninguno funcional |
