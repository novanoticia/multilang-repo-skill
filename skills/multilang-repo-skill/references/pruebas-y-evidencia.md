# Plan, línea base, pruebas, revisión y triaje (P1–P15)

Léelo en las Fases 4 y 8. Aplica según la escala aprobada (tabla de R20 en SKILL.md) y registra cada
comprobación con su nivel (R7) en [assets/evidencias-y-cierre.md](../assets/evidencias-y-cierre.md).

## Contenido
- P1–P3 Plan, línea base y extracción
- P4–P8 Pruebas y validación
- P9–P12 Paquete, CI y ritmo
- P13 Evaluación de instrucciones por escenarios
- P14–P15 Revisión independiente y triaje

## Plan, línea base y extracción

**P1 Plan.** Tareas pequeñas, cada una con su prueba, sus ficheros y su criterio de «hecho». Si el
alcance real es mayor de lo previsto, dilo antes de seguir. En modo guiado, el plan se aprueba antes
de implementar y cada tarea se cierra con su resumen; en el autónomo, se registra y se presenta como
supuesto corregible (R18).

**P2 Línea base, antes de tocar nada.** Genérala desde el commit base (`git show <base>:<ruta>`), no
desde la copia de trabajo, y hazla determinista: fecha y rutas fijas, entorno controlado y binarios
o zips comparados por contenido.
- Programas: salidas por idioma por defecto en los modos y caminos de error representativos.
- Instrucciones: `verificar_adiciones.py` con la lista cerrada de reemplazos aprobados (vacía si
  todo son adiciones). Las líneas de versión que mecaniza el script de versión se aprueban con un
  patrón.
- Manifiestos: iguales salvo la versión.
- `git diff --numstat` no basta. Cuenta líneas, pero no dice cuáles cambiaron: cambiar una línea no
  aprobada en lugar de una aprobada da la misma cifra.

**P3 Extracción con herramientas.** En este orden: el extractor del ecosistema; un script que lea el
literal real (AST o codemod cuando el volumen lo justifique); y, en escala S, a mano, con una
comprobación de que cada literal existe tal cual en el original. El extractor falla con cero y con
varias coincidencias, y aguanta frases repetidas, partidas en varias líneas, citas y bloques
indentados. Cobertura: todo texto visible es un literal con clave o una instrucción declarada; lo
excluido se lista con su razón.

## Pruebas y validación

**P4 Pseudo-locale.** Aplícala cuando el texto llega por código a una interfaz o consola; si no aporta
(pocas cadenas y todas inventariadas), omítela con su motivo. Genera un idioma sintético: cada frase
envuelta en marcas visibles, con acentos y un 30 % más larga. Lo que salga sin marcas es un literal
fuera del catálogo; lo que salga cortado, un problema de espacio. Es una ejecución `local`, no una
simulación. No se distribuye y no aplica al texto que genera un modelo.

**P5 Pruebas primero, donde aportan evidencia.**
- Código con comportamiento nuevo (selección, respaldo, formatos, scripts, validadores): escribe la
  prueba, mírala fallar y luego implementa.
- Pruebas de invariancia (salida por defecto igual, contratos iguales): pasan desde el principio por
  diseño. Su valor se demuestra rompiendo a propósito lo que protegen (P7), no viéndolas en rojo.
- Contenido (catálogos): el validador hace de prueba.
- Documentación: sin TDD.

No inventes pruebas en rojo por ceremonia.

**P6 Validación de catálogos.** Usa primero el validador del ecosistema. Para catálogos JSON propios o
de i18next sin validador (no ICU ni ARB), usa
[scripts/validar_catalogos.py](../scripts/validar_catalogos.py):

```bash
python3 <skill>/scripts/validar_catalogos.py ruta/catalogos --referencia es \
  [--marcadores llave|doble-llave|printf] [--plurales sufijo] [--idiomas es,en,fr]
```

Comprobaciones básicas: mismas claves; nada vacío ni `TODO`; marcadores con nombre e idénticos entre
idiomas; lo que va entre comillas invertidas idéntico; listas con el mismo número de entradas; textos
idénticos a la referencia solo si se declaran invariables; estado coherente con los revisores (D12);
forma (D13); y Unicode (D31). Añade las reglas propias del proyecto: glosario, formatos de datos y
frases de riesgo alto con palabras del original sin traducir (como heurística, no como verdad; P8). Si
el validador falla con tu contenido, corrige el contenido, no el validador.

**P7 Sabotaje de las comprobaciones que escribes.** Una comprobación nueva solo cuenta si se ha visto
fallar ante la rotura que debe detectar. Rompe una copia a propósito, una cosa cada vez:
- Guarda: no midas nada si la suite sin romper no pasa en el mismo entorno.
- Cada rotura se aplica exactamente una vez. Si no encuentra su blanco o lo encuentra varias veces, es
  un fallo de la herramienta, no un éxito.
- Registra qué comprobación detecta cada rotura. Si solo la detecta una prueba genérica (rutas,
  entorno), cuenta como no detectada.
- Los supervivientes se cierran con una prueba nueva o se razonan como equivalentes. Nunca se cita
  «100 %» ni «N de N» antes de pasar la guarda.
- En escala L, mide también con roturas que no hayas diseñado tú (las de un revisor independiente),
  si lo hay.
- Fallos típicos: aserciones que aceptan una frase repetida en otro sitio, números que coinciden por
  azar, pruebas tautológicas, YAML leído en el nivel equivocado, normalizaciones que ocultan cambios.
  Una prueba que fija cadenas literales es una instantánea, no una prueba de comportamiento: dilo.
- No sabotees las herramientas estándar del ecosistema ni los scripts de esta skill: ya tienen sus
  propias pruebas. Una copia adaptada al proyecto (D7) sí es código tuyo.

**P8 Heurísticas entre lenguas próximas.** Una heurística de palabras compartidas puede ser inútil
entre lenguas cercanas (español, gallego, portugués, catalán). Si lo es, omítela de forma visible
(prueba saltada con su motivo) y sustitúyela por marcadores ortográficos o por una revisión palabra a
palabra. Ignora lo que va entre comillas invertidas.

## Paquete, CI y ritmo

**P9 [paquete] Prueba del paquete.** En una copia temporal sin `.git` ni artefactos previos, ejecuta
el empaquetado real y compara el listado con lo esperado: ni un fichero de menos (una subcarpeta
nueva que el script no copia) ni uno de más (pruebas, registro de sesión, copias de las plantillas,
herramientas). Muestra el listado (`unzip -l` o equivalente).

**P10 CI.** Usa el que haya. Propón uno mínimo solo si la persona lo quiere: permisos de solo lectura,
historial completo solo si las pruebas comparan con git, y los validadores y pruebas de tu escala. Un
workflow que nunca ha corrido no es evidencia. El nombre del check es el `id` del job, o su `name`, y
se confirma en una ejecución real. Lee los resultados con las herramientas de la plataforma, sin
bucles de sondeo. Sin permiso para subir no hay ejecución: el nivel queda en `local` y el CI,
`pendiente`. Una afirmación sobre el estado del CI no se puede vigilar desde el repositorio: ponle
fecha y referencia (R8). Si la persona pide «CI en verde» y no hay CI o remoto, dilo en el mensaje, no
solo en el registro: no hay CI que pueda ponerse en verde ni forma de comprobarlo desde aquí. Sin CI,
el estado es `no aplica` con ese motivo; si la persona acepta un workflow mínimo, queda `pendiente`
hasta que corra en la plataforma. La suite en verde se informa como `local`.

**P11 Pruebas de versión mantenibles.** Si una prueba fija el número de versión, el siguiente cambio
de versión pondrá el CI en rojo. Haz que lea la versión de los manifiestos.

**P12 Tras cada tarea.** Las comprobaciones de tu escala, en verde: suite, validador, línea base y,
si cambiaste comprobaciones, su sabotaje.

## P13 Evaluación de instrucciones por escenarios

Para lo que solo un modelo puede mostrar (idioma de respuesta, avisos, fallo seguro, resistencia a
instrucciones en datos). Plantilla: [assets/escenarios-evaluacion.md](../assets/escenarios-evaluacion.md).
1. **Preregistra** antes de ejecutar nada: entrada, criterio de paso, criterio de fallo y un ejemplo
   de cada. Los textos esperados salen de los catálogos. El criterio tolera variaciones legítimas
   (huecos rellenados, números) sin ser tan débil que cualquier salida pase.
2. **Ejecuta** cada escenario en un contexto aislado (un subagente nuevo, otra sesión), con el
   paquete construido por el script real y el mensaje del escenario en el prompt. Quien ejecuta no
   conoce el criterio de paso. Quien evalúa es otro agente o una persona. Casos ficticios, marcados
   como tales.
3. **Lee** respuestas y notas, no solo el veredicto: aparecen hallazgos que ningún criterio preveía.
   Pide al ejecutor qué ficheros leyó y qué le pareció ambiguo.
4. Si cambias un criterio después de ver resultados, regístralo como cambio posterior con su razón.
5. Tras corregir, segunda ronda solo con los escenarios afectados, ejecutores nuevos y los mismos
   criterios.
6. Declara los límites: es una simulación, no la plataforma real; la lista de ficheros leídos la
   declara el propio ejecutor; una ejecución por escenario no mide la variabilidad; los modelos no son
   revisión humana. Deja una tabla para las ejecuciones reales (plataforma, modelo, fecha, resultado).
7. Si no hay contextos aislados o la persona no autoriza delegar (M1), los escenarios quedan
   preregistrados y `pendiente`. No los representes en tu propio contexto para presentarlos como
   ejecutados.

## Revisión independiente y triaje

**P14 Revisión.** Independiente quiere decir un revisor de contexto limpio, con acceso de solo
lectura, que no recibe tus conclusiones: un subagente si está disponible y autorizado (M1) o una
persona. Si no, haz una autorrevisión y declárala como tal. Lista mínima: llaves literales y datos con
llaves; contaminación por el entorno de desarrollo; códigos con forma de locale; formato de máquina
igual entre idiomas; catálogos incompletos; idiomas mezclados en salidas y artefactos; consejos que el
detector propio no reconoce (D19); conflictos entre reglas (D21); listas entre corchetes tratadas como
instrucciones; persistencia del idioma; avisos ausentes en caminos que paran; paráfrasis de nombres
oficiales; literales sin clave; entradas que degradan en silencio; vías de instalación sin los
ficheros nuevos; y cifras de la documentación que ya no cuadran. Con riesgo alto, revisión humana de
lo crítico.

**P15 Triaje.** Lo crítico y lo importante se corrige con una prueba que falle antes (o con la rotura
que demuestre la comprobación). Lo menor se anota con su razón para el informe. Lo que alteraría la
salida por defecto o el contrato con el original se anota y no se toca sin aprobación. Tras corregir,
repite el sabotaje de las comprobaciones nuevas.
