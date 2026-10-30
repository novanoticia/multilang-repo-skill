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

El modelo devuelve escenarios examinados por lectura, comprobaciones pendientes
y hallazgos con citas literales. El validador comprueba las citas contra el diff
enviado. Las comprobaciones de rutas admiten renombrados, permisos y binarios
sin hunks. Una respuesta inválida hace fallar el check, pero no equivale a un
defecto demostrado en la skill.

No se excluyen las traducciones del diff. El límite es de 150.000 caracteres
para el diff, 20.000 para la guía y 10.000 por archivo de contexto Python,
40.000 en conjunto. Los recortes se indican. Que una cita exista no demuestra
que el razonamiento sea cierto: revisa los avisos con el código y las pruebas.

El revisor vive en `.github/`, fuera de la skill distribuida. Usa solo la
biblioteca estándar y tiene permisos `contents: read` y `pull-requests: write`.
No ejecuta el contenido del PR, aplica parches, crea commits ni fusiona cambios.
Su escritura local se limita al resumen de Actions; las funciones de apoyo de
la skill siguen sin escribir archivos. Los textos de los informes de CI viven
en `.github/scripts/mistral_review_es.json`.

## Evidencia

- **Local:** 50 tests del revisor y 149 tests existentes de los scripts de la
  skill pasan. Las pruebas del revisor fallaron antes de añadir su implementación;
  además, una prueba detectó un validador saboteado que aceptaba cualquier respuesta.
- **Simulada:** los tests sustituyen las llamadas a Mistral y la publicación en
  GitHub; validan transporte, formato, citas y conservación del historial.
- **Pendiente, plataforma:** primera revisión mediante la API real después del
  merge y de confirmar la clave. No se ha medido la calidad de los hallazgos.

Los informes no autorizan reparaciones automáticas. Un resultado sin hallazgos
no demuestra que el PR esté libre de defectos.
