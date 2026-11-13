# Revisión de PR con Mistral

El workflow `Mistral PR Review` añade un revisor automatizado mediante la API de
[Mistral AI](https://github.com/mistralai). Analiza el diff y las reglas de
`REVIEW.md`, `AGENTS.md` o `CLAUDE.md`, por ese orden. Mistral solo analiza y
comenta: las reparaciones corresponden a Claude y al mantenedor.

## Activación

Después de fusionar la instalación, comprueba en Settings → Secrets and
variables → Actions que exista el secreto `MISTRAL_API_KEY`. Su valor nunca se
incluye en los informes. Opcionalmente, configura la variable `MISTRAL_MODEL`;
el valor predeterminado es `mistral-large-latest`.

La integración utilizada para preparar este cambio no permite consultar los
secretos ni las variables de Actions: su configuración está pendiente de
confirmación. Si falta la clave, el resumen indica «revisión omitida», que no
equivale a una evaluación sin hallazgos. GitHub no entrega secretos a PR de forks.

El script se ejecuta desde la rama predeterminada, no desde el código del PR.
Por eso, durante el propio PR de instalación, el paso de la API se omite si el
script aún no existe en esa rama. Los tests del revisor y de la skill sí se
ejecutan en un job separado, sin la clave de Mistral.

## Informes y límites

Se revisa al abrir, actualizar, editar, reabrir o marcar listo un PR. Cada
resultado añade un comentario nuevo con el modelo, el SHA y el enlace al intento
de Actions. No sobrescribe los anteriores. Un push cancela una revisión anterior
en curso; una ejecución cancelada antes de publicar puede no dejar comentario.

Hay un informe válido por base y cabeza: editar el PR o marcarlo listo no repite
la revisión de un commit que ya tiene informe válido. «Re-run jobs» sí vuelve a
revisar. Solo cuenta la marca al principio de un comentario de GitHub Actions; un
informe «no completado» no la lleva, así que no impide el reintento.

El informe empieza por una línea **Resultado** con los recuentos; después van los
hallazgos y las comprobaciones pendientes, y las comprobaciones sin defecto
aparente quedan plegadas.

El modelo devuelve escenarios examinados por lectura, comprobaciones pendientes
y hallazgos con citas literales. El validador comprueba las citas contra el diff
enviado; la sangría y los espacios de los extremos de cada línea citada no
cuentan, el resto es literal. Las comprobaciones de rutas admiten renombrados,
permisos y binarios sin hunks. Una respuesta inválida hace fallar el check, pero
no equivale a un defecto demostrado en la skill. Si la API corta la respuesta, el
informe añade su código de causa (`length` cuando se agota el margen de 16.000
tokens de salida), sin copiar nada del contenido.

El prompt pide que cada comprobación intente romper el cambio y que cada hallazgo
se intente refutar antes de publicarlo.

**Segunda solicitud.** Si la respuesta llega pero no valida (esquema o citas
fuera del diff), se pide una vez más; un fallo de API no se repite por esta vía.
El registro de Actions y el comentario nombran la regla incumplida, nunca el
contenido de la respuesta.

**Modelos que razonan.** `mistral-large-latest` pasó a razonar antes de
responder: devuelve el contenido en bloques (`thinking` y `text`) y gastaba el
margen de salida entero en razonar, de ahí los informes «no completada»
(medido en `email-triage-plugin#202`: 31.129 caracteres de razonamiento y
ninguno de respuesta con 8.000 tokens). El revisor lee solo los bloques `text`,
envía `reasoning_effort: "low"` —si el modelo no admite el parámetro, lo retira
y repite— y da un margen de 16.000 tokens. Si la API corta la respuesta, el
informe añade su código de causa (`length`) y el registro de Actions dice el
modelo servido y cuánto ocupó el razonamiento y cuánto la respuesta: solo
recuentos, nada del contenido. Cada revisión consume así del orden de 10.000
tokens de salida; para evitarlo, fija un modelo sin razonamiento en
`MISTRAL_MODEL`. Que 16.000 basten para diffs mucho mayores no está medido.

No se excluyen las traducciones del diff. El límite es de 150.000 caracteres
para el diff, 20.000 para la guía y 10.000 por archivo de contexto Python,
40.000 en conjunto. Como contexto se envían las funciones completas de la versión
nueva que contienen las líneas cambiadas, con sus números de línea y el código
antes que las pruebas; no el principio del archivo. Los recortes se indican. Que una cita exista no demuestra
que el razonamiento sea cierto: revisa los avisos con el código y las pruebas.

El revisor vive en `.github/`, fuera de la skill distribuida. Usa solo la
biblioteca estándar y tiene permisos `contents: read` y `pull-requests: write`.
No ejecuta el contenido del PR, aplica parches, crea commits ni fusiona cambios.
Su escritura local se limita al resumen de Actions; las funciones de apoyo de
la skill siguen sin escribir archivos. Los textos de los informes de CI viven
en `.github/scripts/mistral_review_es.json`.

## Evidencia

- **Local:** 96 tests del revisor y 149 tests existentes de los scripts de la
  skill pasan. Las pruebas del revisor fallaron antes de añadir su implementación;
  además, una prueba detectó un validador saboteado que aceptaba cualquier respuesta.
- **Simulada:** los tests sustituyen las llamadas a Mistral y la publicación en
  GitHub; validan transporte, formato, citas y conservación del historial.
- **Pendiente, plataforma:** primera revisión mediante la API real después del
  merge y de confirmar la clave. No se ha medido la calidad de los hallazgos, ni
si el prompt que pide romper el cambio mejora el juicio del modelo.

Los informes no autorizan reparaciones automáticas. Un resultado sin hallazgos
no demuestra que el PR esté libre de defectos.
