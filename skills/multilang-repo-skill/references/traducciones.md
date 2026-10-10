# Traducciones y alto riesgo (T1–T7, D26)

Léelo en la Fase 5 y siempre que esté activo [alto-riesgo].

**T1 Glosario antes de traducir.** Fija los términos y el tratamiento (tú o usted, tu o vous) y úsalos
siempre igual. Vigílalo con una prueba en proporción a la escala, y documenta el tratamiento elegido.

**T2 Conserva lo que no es prosa.** Marcadores, emojis, formato y contratos de máquina quedan intactos.
No traduzcas nombres de producto, comandos, modos, opciones, rutas ni códigos (B1); los valores de
vocabulario cerrado que solo se muestran (B2) se traducen en la prosa, con el literal al lado si la
persona tiene que escribirlo. Respeta la tipografía
de cada idioma (comillas «», espacios antes de ciertos signos en francés) y anota la elección, porque
una revisión nativa puede preferir otra.

**T3 Lenguas próximas.** Si tu traducción queda idéntica al original y el validador lo señala, busca
la formulación propia del idioma; no añadas excepciones para que pase. Márcala invariable solo si el
texto lo justifica (símbolos, códigos, nombres propios) y anota la razón.

**T4 Nombres oficiales (G).** Cópialos de la fuente oficial en cada idioma, leyendo la columna por su
encabezado y no por su posición, y comprueba que no devuelve el idioma equivocado. Si no hay versión
oficial, usa el código más el nombre oficial disponible. Si la fuente es inaccesible, aplica R10
(`segunda-mano` o `no-comprobado`, y a pendientes).

**T5 Estado honesto.** Lo que traduce una IA queda como `borrador-ia` (D12): dilo en el repositorio y
en la entrega (el informe a la persona; un aviso en la salida en ejecución se decide en la Fase 2, D22), y no
lo presentes como revisado. Que otro modelo lo revise no lo convierte en revisado.
No atribuyas calidad lingüística revisada a lo que solo ha pasado por una IA.

**T6 Idioma menos seguro.** Di qué idioma juzgas con menos seguridad y por qué. Un idioma que no puedes
juzgar se entrega como `experimental` (que implica `borrador-ia`, D12), con un aviso reforzado (p. ej.
bilingüe) y revisión nativa imprescindible, y solo si la persona lo autoriza tras conocer el riesgo.

**T7 Texto libre del modelo (H).** No cabe en un catálogo. Indica al modelo que lo redacte en el
idioma elegido y declara en la documentación que no está revisado.

## [alto-riesgo]

**D26 Frases de riesgo.** Identifícalas una a una (`riesgo: alto`): confirmaciones de acciones
irreversibles, límites profesionales, advertencias de seguridad, dosis, plazos y obligaciones. No las
«mejores» al traducirlas. Cuida las construcciones que invierten el sentido (preguntas negativas que
se responden con sí o no, dobles negaciones). En idiomas que no puedes juzgar, señálalas como riesgo
en lugar de reformularlas si eso cambia el contrato con el original.

Exigencias del módulo:
- Dos revisiones humanas distintas antes de cualquier uso profesional: la del contenido, por una
  persona especialista del dominio (C8), y la de la traducción de las frases de riesgo, por una persona
  nativa (y especialista cuando proceda). Una no sustituye a la otra. Si aún no la hay, el repositorio y la entrega dicen «pendiente de
  revisión humana» en lugar de dar el trabajo por cerrado.
- Commits o PR marcados para revisión humana del diff, empezando por las claves `riesgo: alto`.
- Escenarios (P13) que comprueben el sentido de las frases de riesgo en cada idioma, con nivel
  `simulada` y sin sustituir a la revisión humana.
