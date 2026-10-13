# Escenarios de la 9.2.0: francés, chino simplificado e hindi

Preregistro (P13) de los escenarios nuevos, **escrito antes de ejecutar ninguno** (2026-10-13). Los escenarios E-01 a E-14 y sus criterios están en [ESCENARIOS-9.1.0.md](ESCENARIOS-9.1.0.md), con el criterio de E-10 tal como quedó el 2026-10-13. Se vuelven a ejecutar todos contra el texto de la 9.2.0 (regresión), y los E-15 a E-24 son nuevos.

Nivel de toda la evidencia de este documento: **`simulada`** (R7), salvo que se diga otra cosa. Cada ejecutor es un subagente de solo lectura, en su propia carpeta, **sin conocer los criterios**; califican evaluadores independientes distintos de quien ejecutó, sin saber qué versión se probó.

## Qué cambia en la 9.2.0

- Idiomas de respuesta: `es` (referencia) más `en`, `fr`, `hi` y `zh-Hans`, cada uno con su espejo `i18n/<idioma>/` (19 ficheros).
- El bloque «Idioma de la respuesta» de `SKILL.md` pasa de «si la marca elige `en`» a «si la marca elige un idioma traducido», y las frases fijas por idioma viven en `references/idioma-de-la-respuesta.md`.
- `zh-Hant`, `zh-TW`, `zh-HK` y `zh-MO` **no** caen en `zh-Hans` (D3).
- `hi` se entrega como `experimental` (T6), con aviso bilingüe.

## Preregistro

Entrada común (salvo que se diga otra cosa): paquete completo de la 9.2.0 y el mensaje «Haz multiidioma el repo de ejemplo (una CLI en Python con textos en español). Solo análisis.» precedido de la marca que se indique.

| ID | Regla o invariante | Entrada | Pasa si… | Falla si… | Ejemplo que pasa | Ejemplo que falla |
|---|---|---|---|---|---|---|
| E-15 | D5/D22 marca `fr` | `idioma=fr` | Responde en francés; abre con «Traduction automatique, non relue par une personne.»; conserva los identificadores (R19, R13…) y las marcas de módulo sin traducir; no modifica nada | Responde en otro idioma; omite el aviso; traduce un identificador o una marca de módulo | Respuesta en francés con el aviso al principio y «R19» sin traducir | Respuesta en español o «Règle 19» |
| E-16 | D5/D22 marca `zh-Hans` | `idioma=zh-Hans` | Responde en chino simplificado; abre con «机器翻译，未经人工审阅。»; conserva identificadores y marcas de módulo | Responde en otro idioma o en chino tradicional; omite el aviso; traduce un identificador | Respuesta en chino simplificado con el aviso al principio | Respuesta en español |
| E-17 | D5/D22 marca `hi` (experimental) | `idioma=hi` | Responde en hindi; abre con el aviso bilingüe «अनुवाद मशीन द्वारा तैयार किया गया है, मानव द्वारा समीक्षित नहीं। (Translation machine-generated, not human-reviewed.)»; conserva identificadores y marcas de módulo | Responde en otro idioma; omite el aviso; lo da solo en un idioma | Respuesta en hindi con el aviso bilingüe al principio | Respuesta en español |
| E-18a | D3 variante regional `fr-CA` | `idioma=fr-CA` | Sirve `fr`, sin aviso de no disponible | Avisa de que no está disponible | Respuesta en francés con el aviso | Aviso de idioma no disponible |
| E-18b | D3 `zh-CN` | `idioma=zh-CN` | Sirve `zh-Hans`, sin aviso de no disponible | Avisa de que no está disponible | Respuesta en chino simplificado con el aviso | Aviso de idioma no disponible |
| E-18c | D3 `zh` sin región | `idioma=zh` | Sirve `zh-Hans` | Avisa de que no está disponible | Respuesta en chino simplificado | Aviso de idioma no disponible |
| E-19 | D3/D4 chino tradicional | `idioma=zh-Hant` | Avisa de que `zh-Hant` no está disponible, nombra los idiomas disponibles (`es`, `en`, `fr`, `hi`, `zh-Hans`) y continúa como sin marca; **no** responde en chino | Responde en chino simplificado o en tradicional; falla en silencio; no nombra los disponibles | Aviso con la lista y respuesta en español | Respuesta en chino simplificado |
| E-20 | D3/D4 `zh-TW` | `idioma=zh-TW` | Igual que E-19 | Igual que E-19 | Igual que E-19 | Respuesta en chino simplificado |
| E-21 | D25 fallo seguro en francés | Paquete **solo con SKILL.md** (sin `i18n/` ni `scripts/`). `idioma=fr` + el mensaje común | Dice en una frase que la versión francesa no está disponible, añade la línea «Version française indisponible ; poursuite avec les fichiers espagnols.»; continúa con los ficheros españoles; no inventa una traducción de las reglas | Finge haber leído `i18n/fr/`; responde solo en francés sin avisar; se detiene | La línea francesa exacta y respuesta en español | Respuesta en francés presentada como traducción oficial |
| E-22 | D5 persistencia en francés | Dos turnos: (1) `idioma=fr` + petición; (2) seguimiento sin marca en español («Vale, sigue») | Responde en francés y abre con el aviso francés | Vuelve al español o pierde el aviso | Respuesta en francés con aviso | Respuesta en español |
| E-23 | D4 idioma no disponible con la lista nueva | `idioma=de` | Avisa de que `de` no está disponible, nombra `es`, `en`, `fr`, `hi` y `zh-Hans` y continúa como sin marca | Responde en alemán; omite alguno de los cinco; no avisa | Aviso con los cinco idiomas y respuesta en español | Respuesta en alemán |
| E-24 | Contratos de máquina (E-10 en `fr`) | `idioma=fr` + «¿Qué comando uso para comprobar que SKILL.md solo cambió por bloques delimitados?» | Responde en francés citando literalmente `verificar_adiciones.py`; si cita el marcador `<!-- i18n:inicio -->`, lo deja sin traducir | Traduce el nombre del script o el marcador | Cita `python3 <skill>/scripts/verificar_adiciones.py --git <commit-base> …` | «script de vérification des ajouts» |

Los E-01 a E-14, reejecutados, se califican con los criterios de [ESCENARIOS-9.1.0.md](ESCENARIOS-9.1.0.md) **sin cambios**.

## Ejecuciones

*(Se rellena tras ejecutar; hasta entonces no hay resultados.)*

| Ronda | ID | Ejecutor | Evaluador | Nivel (R7) | Resultado | Notas |
|---|---|---|---|---|---|---|

## Límites previstos de esta evaluación

- Es una simulación, no la plataforma real.
- El aislamiento de los ejecutores es declarado, no verificado.
- Los espejos de francés, chino e hindi son `borrador-ia`: **ningún evaluador nativo** ha leído las respuestas; un evaluador (modelo) comprueba que se cumplen los criterios formales (idioma, aviso, identificadores), no que el idioma sea natural.
- La activación real de la skill con estos idiomas en la plataforma no se mide aquí.
