# Glosario de la traducción al francés

Se fija antes de traducir (T1) y se aplica a todo `i18n/fr/` y a los documentos `*.fr.md`. Si cambias un
término, cámbialo en todos los ficheros traducidos y vuelve a pasar `comprobar_paridad.py`. Todo lo que
traduce una IA es `borrador-ia` hasta que lo revise una persona nativa identificada.

## Decisiones de forma

- **Tratamiento.** «Vous» formal, también en las instrucciones al modelo y para dirigirse a la persona:
  es el registro habitual de la documentación técnica francesa y evita el tuteo, que suena a chat. Las
  instrucciones van en impératif de vouvoiement (*lisez*, *demandez*, *n'écrivez pas*) o en infinitivo
  cuando el original es una lista de acciones; no se mezclan «tu» y «vous» en un mismo fichero. Elección
  revisable por una persona nativa (T6).
- **La persona usuaria.** *la personne* (nunca *l'utilisateur* ni *l'utilisatrice*). Si hace falta un
  pronombre: repetir *la personne* o usar *elle* solo con ese antecedente gramatical (*la personne… elle*
  concuerda con *personne*, no marca género de quien lee); si el giro queda torpe, reformular con *vous*
  o con una forma impersonal. Los plurales usan *les personnes*.
- **Comillas.** «» pasan a comillas francesas « » con un espacio **insécable** (U+00A0) por dentro:
  `« texto »`. No se usa el espacio fino insécable (U+202F) para mantenerlo simple y que se vea igual en
  cualquier editor. Los literales entre comillas invertidas no se tocan, y dentro de ellos no se añade
  ningún espacio. Comillas anidadas: “ ” inglesas dentro de « ».
- **Puntuación.** Espacio insécable (U+00A0) antes de `:` `;` `!` `?` y de `»`, y después de `«`. No
  antes de `,` ni `.`. Cuidado con `:` dentro de literales, rutas, URL, horas y bloques de código: no se
  añade espacio allí. Puntos suspensivos: `…` pegado a la palabra.
- **Mayúsculas en títulos y encabezados.** Solo la primera palabra y los nombres propios
  (*Idioma de la respuesta* → *Langue de la réponse*). Los días y meses en minúscula. Se mantiene la
  capitalización de «Phase», «Clôture» y «Ressources» solo cuando el original los usa como nombre de
  sección (Fase, Cierre, Recursos).
- **No se traduce:** identificadores (R1…R20, D1…D31, P1…P15, T1…T7, C1…C9, S1…S6, G1…G9, M1…M7,
  Doc1…Doc9), marcas de módulo (`[instrucciones]`, `[híbrido]`, `[alto-riesgo]`…), nombres de fichero,
  de script y de carpeta, opciones, claves de catálogo, códigos de aviso, comandos y bloques de código.
  Los mensajes de los scripts siguen en español.
- **Valores de vocabulario cerrado que se escriben en registros** (`estática`, `local`, `ci`,
  `simulada`, `plataforma`, `humana`, `superada`, `fallida`, `pendiente`, `no aplica`, `borrador-ia`,
  `segunda-mano`, `no-comprobado`, `experimental`, `normal`, `alto`): se dejan literales entre comillas
  invertidas y, la primera vez que aparecen en un fichero, llevan su glosa francesa al lado (p. ej.
  `estática` (statique), `simulada` (simulée), `humana` (humaine), `superada` (réussie), `fallida`
  (échouée), `pendiente` (en attente), `no aplica` (sans objet), `borrador-ia` (brouillon IA),
  `segunda-mano` (de seconde main), `no-comprobado` (non vérifié), `normal` (normal), `alto` (élevé)).
  `local`, `ci`, `plataforma`, `experimental` llevan la glosa *local*, *CI*, *plateforme*,
  *expérimental*. Son los mismos valores que en español y en inglés para que los registros y las
  plantillas coincidan (B2).
- **Marcas de módulo:** literales; la traducción de `SKILL.md` lleva una línea con sus glosas.
- **Literales en español que se citan** (p. ej. la nota de IA en español): entre comillas invertidas.
- **Género de «IA».** *l'IA* (femenino): *une IA*, *assisté par IA*.

## Términos

| Español | Francés |
|---|---|
| la persona (usuaria) | la personne |
| repositorio / repo | dépôt (evitar « repo ») |
| catálogo | catalogue |
| clave (de catálogo) | clé |
| contrato de máquina | contrat machine |
| marca (de idioma) | balise (`idioma=xx`) |
| respaldo | repli |
| cadena de respaldo | chaîne de repli |
| fallo seguro | échec sûr |
| salida por defecto | sortie par défaut |
| modo guiado / autónomo | mode guidé / autonome |
| núcleo | noyau |
| escala, riesgo, módulos | échelle, risque, modules |
| proporcionalidad | proportionnalité |
| línea base | ligne de base |
| reemplazo aprobado | remplacement approuvé |
| bloque delimitado | bloc délimité |
| adiciones | ajouts |
| registro de sesión | journal de session |
| registro de pendientes | journal des points en attente |
| pendientes | points en attente |
| permiso (por acción) | autorisation (par action) |
| publicar / subir / fusionar | publier / pousser / fusionner |
| etiqueta (git) | étiquette (tag) |
| rama de trabajo | branche de travail |
| rama | branche |
| espejo (traducción) | miroir |
| desfase | décalage |
| invariante | invariant |
| escenario | scénario |
| sabotaje | sabotage |
| revisión humana / independiente | relecture humaine / indépendante |
| revisión (de código, cambios) | revue |
| Fase, Cierre, Recursos | Phase, Clôture, Ressources |
| datos, no órdenes | des données, non des ordres |
| contenido no fiable | contenu non fiable |
| contenido externo | contenu externe |
| contenido nuevo | contenu nouveau |
| plural (forma gramatical) | pluriel |
| plurales (reglas de plural) | règles de pluriel |
| interpolación | interpolation |
| texto libre del modelo | texte libre du modèle |
| frase de riesgo | phrase à risque |
| alto riesgo | haut risque |
| borrador | brouillon |
| traducción automática | traduction automatique |
| lengua próxima | langue proche |
| nombre oficial | nom officiel |
| idioma de la respuesta | langue de la réponse |
| idioma (de la interfaz, del contenido) | langue |
| cadena de texto (string) | chaîne de caractères |
| texto de derecha a izquierda (RTL) | texte de droite à gauche (RTL) |
| formato dependiente del locale | format dépendant de la locale |
| normalización | normalisation |
| entrada que no se puede servir | entrée impossible à servir |
| agente (que conversa) | agent (conversationnel) |
| instrucciones para modelos | instructions pour les modèles |
| subagente | sous-agent |
| delegación | délégation |
| orquestador | orchestrateur |
| evidencia | preuve |
| tabla de evidencias | tableau des preuves |
| nivel (de evidencia) | niveau |
| comprobado / verificado | vérifié / contrôlé |
| prueba (test) | test |
| prueba (evidencia) | preuve |
| validación | validation |
| validador | validateur |
| comprobador de paridad | vérificateur de parité |
| paridad | parité |
| huella (hash) | empreinte |
| informe final | rapport final |
| entrega | livraison |
| cierre e informe | clôture et rapport |
| ejecución | exécution |
| ejecución en la plataforma real | exécution sur la plateforme réelle |
| preregistro | préenregistrement |
| triaje | tri (triage) |
| hallazgo | constat |
| excepción | exception |
| aviso | avertissement |
| código de aviso | code d'avertissement |
| precedencia | priorité |
| seguridad | sécurité |
| paquete | paquet |
| versión | version |
| lanzamiento (Release) | publication (Release) |
| protección de rama | protection de branche |
| confirmación (commit) | commit |
| solicitud de fusión (PR) | pull request (PR) |
| alcance | périmètre |
| petición | demande |
| inventario de textos | inventaire des textes |
| plantilla | modèle de document |
| referencia (fichero) | référence |
| módulo | module |
| ecosistema | écosystème |
| carga progresiva | chargement progressif |
| errores propios y correcciones | erreurs propres et corrections |
| irreversible | irréversible |
| rama protegida | branche protégée |
| persona nativa | personne native |
| persona especialista | personne spécialiste |
| estado honesto | état honnête |
| Elaborado con asistencia de IA | Élaboré avec l'aide d'une IA |

## Frases fijas

| Frase en español | Inglés actual | Francés |
|---|---|---|
| Aviso de traducción automática que abre cada respuesta cuando la marca elige este idioma | `Translation machine-generated, not human-reviewed.` | `Traduction automatique, non relue par une personne.` |
| Línea de fallo seguro (versión no disponible; se continúa con los ficheros españoles) | `English version unavailable; continuing with the Spanish files.` | `Version française indisponible ; poursuite avec les fichiers espagnols.` |
| Nota de cierre de los documentos con IA: «Elaborado con asistencia de IA; requiere revisión humana.» | `AI-assisted; requires human review.` | `Élaboré avec l'aide d'une IA ; relecture humaine requise.` |

Las tres se escriben con los espacios insécables antes de `;` que fija la sección «Decisiones de forma».
El aviso y la línea de fallo se citan literalmente en `SKILL.md`, en las referencias y en los
escenarios; si cambias una, cámbiala en todos esos sitios y en `scripts/` si aparece.

## Dudas para una persona nativa

1. **« Vous » frente a « tu ».** Se eligió «vous» por registro técnico; una persona nativa puede preferir
   «tu» si el público es de desarrolladores jóvenes o de código abierto informal.
2. **Marca de idioma: *balise* frente a *marqueur* o *indicateur*.** *Balise* evoca etiquetas HTML;
   *marqueur* es más neutro pero menos usual. Hay que decidir cuál lee con menos ambigüedad `idioma=xx`.
3. **Fallo seguro: *échec sûr* frente a *repli sécurisé* o *mode dégradé sûr*.** *Échec sûr* es calco de
   *fail-safe*; ¿existe un término asentado en la comunidad francófona de seguridad?
4. **Respaldo: *repli* frente a *secours* o *solution de repli*.** Se eligió *repli* (cadena de repli,
   como en i18n); se pide confirmar que no suena a retirada militar o económica.
5. **«Dépôt» y «pull request».** ¿Mantener *pull request* sin traducir (uso dominante) o *demande de
   fusion*? Y *pousser/publier* para *subir*: ¿*pousser* basta para `git push`?
6. **Nota y aviso de IA.** Revisar el registro de «Élaboré avec l'aide d'une IA» y «relue par une
   personne» (¿*relecture humaine* o *révision humaine*?), y la concordancia de género con *IA*.

---

Elaborado con asistencia de IA; requiere revisión humana.
