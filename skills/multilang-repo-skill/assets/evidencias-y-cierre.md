# Evidencias y cierre

Una fila por criterio. Estado `superada` solo si la comprobación se ha ejecutado de verdad y con ese
resultado. Lo diseñado y no ejecutado queda `pendiente`, y lo que no corresponde, `no aplica` con su
motivo.

## Tabla de evidencias

| Criterio | Módulo / regla | Evidencia (comando exacto o artefacto) | Nivel (R7) | Estado | Referencia (commit, ejecución, fecha) | Notas |
|---|---|---|---|---|---|---|
| Salida por defecto u original sin cambios no aprobados | D1, P2 | | | | | |
| Contratos de máquina iguales en todos los idiomas | B, P6 | | | | | |
| Idiomas pedidos en todos los modos y caminos de error | [programa] | | | | | |
| Invariantes de las instrucciones por idioma | [instrucciones], P13 | | | | | |
| Selección de idioma: tabla de casos y totalidad | D6, D7 | | | | | |
| Añadir un idioma = soltar un fichero; el validador dice qué falta | D8, P6 | | | | | |
| Sin literales fuera del catálogo | P3, P4 | | | | | |
| Comprobaciones propias saboteadas, con guarda | P7 | | | | | |
| Estado de traducciones veraz | D12, T5 | | | | | |
| Revisión independiente o autorrevisión declarada | P14 | | | | | |
| Paquete con exactamente los ficheros esperados | [paquete], P9 | | | | | |
| CI de la plataforma | P10 | | | | | |
| Contenido externo con nivel de fuente y vigencia | [contenido] | | | | | |
| Escenarios adversariales | [seguridad], S3 | | | | | |
| Revisión humana de las frases de riesgo | [alto-riesgo] | | | | | |
| Cada publicación, autorizada y registrada | R13, G | | | | | |

## Informe final

1. **Qué hay ahora.**
2. **Errores propios y correcciones:** cifras retiradas, datos de memoria que resultaron falsos,
   pruebas inválidas, criterios cambiados tras ver resultados, y su efecto.
3. **Decisiones que tomaste en nombre de la persona** y su coste si estaban mal.
4. **Desviaciones de la skill**, citando identificadores y el motivo.
5. **Tabla de evidencias** (arriba).
6. **Limitaciones conocidas.**
7. **Pendientes**, con su motivo.
8. **Qué le toca hacer a la persona:** fusionar, Release, protección de rama, revisión humana,
   pruebas en la plataforma real, dominios o credenciales.
9. **Delegación:** registro M7, o «no hubo delegación».

Si la sesión se compactó por el camino, reconstruye el informe desde el registro de sesión, no de
memoria.
