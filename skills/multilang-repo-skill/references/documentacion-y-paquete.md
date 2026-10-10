# Documentación, versión y paquete (Doc1–Doc9)

Léelo en la Fase 7, con [documentación] o con [paquete]. Sigue las convenciones del repositorio (R17):
si no usa CHANGELOG, `AGENTS.md` o registro de pendientes, propón crearlos antes de hacerlo.

**Doc1 README.** Cómo elegir idioma, qué se traduce y qué no (contratos de máquina, texto libre del
modelo), cómo añadir un idioma, casos límite, limitaciones (lo que no cubre un detector, idiomas
experimentales) y el estado real de las traducciones (`borrador-ia`, `revisado`…), una vez por
idioma. La nota de autoría con IA sigue R16. Si el alcance es corto, basta una sección multilingüe; no traduzcas el README entero salvo
que se pida. Al traducir documentación, conserva intactos los bloques de código, los comandos, las
anclas y los enlaces.

**Doc2 Vías de instalación manuales.** Si alguna consiste en copiar ficheros a mano, añade los nuevos
(catálogos, scripts) a su lista. Sin ellos, la función no existe para quien instale así.

**Doc3 `AGENTS.md` o `CLAUDE.md`.** Si existen: no escribir literales nuevos fuera del catálogo;
bloques delimitados; frontmatter intacto; ficheros intocables; revisión humana de los diffs de riesgo
alto; comandos de validación; no fusionar con el CI en rojo; qué hacer en el siguiente cambio de
versión; y pendientes ajenos conocidos. Si solo existe uno, comprueba si enlaza al otro.

**Doc4 Versión.** Según la política del proyecto (p. ej. semver: una función compatible es minor), con
su script si existe, en todos los manifiestos a la vez y con una prueba que los compare (P11).

**Doc5 CHANGELOG.** Añadido, Cambiado, Corregido y Limitaciones, incluidas las excepciones aprobadas
(D23) y las líneas del original que cambian. Antes de cerrar, busca cada cifra citada (claves,
roturas, escenarios, tamaños) y compárala con el estado actual (R9).

**Doc6 Registro de pendientes** (`PENDIENTES.md` o el equivalente del repositorio). Solo lo
comprobado: qué requiere a una persona (revisión, credenciales), qué requiere otra sesión o acceso a
dominios, qué fuentes faltan, qué escenarios no se han ejecutado y qué cambios aún no están en la rama
principal.

**Doc7 [paquete] Contenido del paquete.** El script de empaquetado incluye todos los ficheros nuevos y
nada más, demostrado con P9. Si hay paquetes antiguos ya descargados, la nota de la versión dice que
hay que reinstalar el paquete completo.

**Doc8 [paquete] Nombres de los adjuntos.** Si el README enlaza un adjunto por nombre (p. ej.
`releases/latest/download/<nombre>.zip`), el adjunto se llama exactamente así: un sufijo de versión
rompe el enlace.

**Doc9 Manual de uso, si existe.** Léelo entero antes de cambiarlo. Conserva su estructura y su
numeración, porque otras partes remiten a ellas; añade lo nuevo al final, con un recuadro de novedades
al principio. Si se genera un PDF (p. ej. desde HTML con un navegador sin interfaz), revisa a ojo la
portada y una página con tabla. Lleva la nota de IA (R16) y conserva la versión anterior como
historial.
