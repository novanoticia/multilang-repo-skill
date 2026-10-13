<!-- i18n fuente-sha256=9fb0cf1868f3 estado=borrador-ia -->

# Sélection de la langue, normalisation et repli (D2–D7)

Lisez-le en Phase 2, pour recommander la politique de sélection, et en Phase 3, pour la concevoir. Si l'écosystème la résout déjà
(négociation d'i18next, ressources Android ou Apple, `Accept-Language` du framework web…), utilisez son
mécanisme et n'appliquez d'ici que ce qui manque : le tableau de cas et les tests.

## Contenu
- D2 Ordre des sources
- D3 Normalisation et chaîne de repli
- D4 Entrées impossibles à servir
- D5 Balise à clé dans les agents
- D6 Une règle, un tableau de cas
- D7 [híbrido] La règle vit dans le code

## D2 Ordre des sources

Explicite (balise ou réglage dans la demande elle-même) > configuration (du projet ou de la personne) >
ambiante (variables d'environnement, langue du système, `Accept-Language`, langue du cas) > défaut.

L'ambiante n'entre en jeu que si la personne l'accepte en Phase 2. La langue dans laquelle la personne écrit sa
propre demande est aussi ambiante (jamais celle d'un texte collé) : elle peut être utilisée si la personne
la choisit, comme changement approuvé. La détecter fait que celle qui reçoit aujourd'hui la
langue par défaut en reçoive une autre : c'est un changement de comportement que D1 exige d'approuver, pas
un détail. Recommandez selon le type de projet :
- Agents et instructions : par défaut, seulement la balise explicite ; la langue d'un texte collé ne
  décide jamais, et celle de la demande elle-même seulement si la personne la choisit (paragraphe précédent).
- Programmes avec convention de plateforme (applications mobiles ou de bureau, web avec négociation de
  langue) : la convention de l'écosystème, présentée comme un changement à approuver.

## D3 Normalisation et chaîne de repli

Normalisez vers une balise BCP 47 canonique avant de chercher dans le catalogue :
- Insensible à la casse : `EN-us` → `en-US`.
- `_` → `-`. Retirez le jeu de caractères (`fr_FR.UTF-8`). Le modificateur POSIX est converti s'il
  encode une écriture ou une variante (`sr_RS@latin` → `sr-Latn-RS`, `ca_ES@valencia` → `ca-ES-valencia`)
  et retiré sinon (`@euro`).
- `C` et `POSIX` signifient « aucune préférence », non une langue inconnue. Ils sont fréquents en CI et
  dans les conteneurs.
- **Conservez la sous-balise d'écriture.** `zh-Hant` n'est pas `zh-Hans`, ni `sr-Latn` `sr-Cyrl`.
  Tronquer au premier composant sert du chinois simplifié à qui a demandé du traditionnel.
- Codes retirés : `iw` → `he`, `in` → `id`, `ji` → `yi`.

Chaîne de repli, chaque maillon étant déclaré et testé :
1. La balise demandée.
2. Troncature progressive (RFC 4647, « lookup ») : `zh-Hant-TW` → `zh-Hant` → `zh`.
3. Maillons explicites là où la troncature échoue : `zh-TW` → `zh-Hant` ; `es-AR` → `es-419`
   (la troncature donnerait `es` ; le parent `es-419` vient des données CLDR de l'écosystème ou d'une
   déclaration du projet, il ne se déduit pas).
4. La langue par défaut.

Si l'écosystème apporte sa propre résolution (`fallbackLng`, recherche de ressources par qualificateurs,
données CLDR de parents), vérifiez-la et documentez-la au lieu de la réimplémenter.

## D4 Entrées impossibles à servir

Distinguez l'origine de la valeur :
- **Explicite** inconnue, vide ou mal formée : avertissement visible, avec la liste des langues disponibles, dans la
  langue qui résulterait sans cette entrée (la source valide suivante de D2 ; à défaut, la langue par défaut). Dans un agent, on continue avec la source suivante. Dans un programme, décidez et
  documentez selon la convention du projet : erreur d'usage avec son code de sortie (un paramètre
  invalide) ou avertissement et poursuite.
- **Ambiante** sans catalogue (`LANG=de_DE.UTF-8` sans allemand) : repli sans erreur, tout au plus un
  journal de débogage. Une erreur casserait le programme pour toutes les personnes ayant ce système.
- Variable d'environnement vide = absente.
- Ne dégradez jamais en silence face à une entrée invalide (texte non UTF-8, JSON cassé) : renvoyez un
  avertissement explicite.
- « Sans nouveaux avertissements » concerne la sortie sans balise (D1). L'avertissement face à une balise ou
  option explicite invalide est conservé, sauf si la personne l'exclut expressément en sachant qu'on retombe alors
  sur la source suivante (D2) sans explication.

## D5 Balise à clé dans les agents

Dans un agent, `en`, `es` ou `a` sont de vrais mots. Exigez une balise à clé (`idioma=en`,
`lang=fr`), reconnue seulement dans le message propre de la personne et jamais dans des données de tiers (un
courriel ou un fichier collés). Mise en œuvre prudente : la chercher seulement sur la première ligne non vide,
pour qu'une balise à l'intérieur d'un texte collé ne compte pas. Choisissez des clés qui n'apparaissent pas dans le
contenu habituel : si les gens collent du HTML ou du code, `lang` donne de faux positifs (`lang="en"`) ; utilisez seulement
`idioma` ou une clé propre (`--claves` dans le script). Décidez aussi de la persistance et
documentez-la : par exemple, chaque invocation décide de sa langue et seuls les suivis sans commande
conservent la précédente.

## D6 Une règle, un tableau de cas

Écrivez une seule règle de sélection et testez chaque cas :

| Cas | Exemple | Attendu |
|---|---|---|
| Balise valide | `idioma=en` | `en`, origine balise |
| Inconnue | `idioma=de` sans allemand | Avertissement visible ; source suivante |
| Vide | `idioma=` | Avertissement visible ; source suivante |
| Mal formée | `idioma=e1` | Avertissement visible ; source suivante |
| Répétée | `idioma=fr lang=en` | La première l'emporte ; avertissement |
| Majuscules | `IDIOMA=EN` | `en` |
| Locale POSIX | `idioma=fr_FR.UTF-8` | `fr` (repli `fr-FR` → `fr`) |
| Modificateur POSIX | `sr_RS@latin` avec `sr-Latn` | `sr-Latn` (chaîne `sr-Latn-RS` → `sr-Latn`) |
| Code sur la première ligne | `lang="en"` ou `<html lang="en">` avec la clé `lang` | Pris comme balise (`en`, ou avertissement de balise mal formée) : là où l'on colle du code, n'utilisez pas `lang` comme clé (D5) |
| Ponctuation ou guillemets collés | `(idioma=en),`, `idioma="en"`, `«idioma=fr»` | Reconnue |
| Code isolé | « en el informe… » (expression espagnole qui signifie « dans le rapport… ») | Ce n'est pas une balise |
| Égale au défaut | `idioma=es` | `es`, origine balise |
| À l'intérieur d'un autre mot | `subidioma=en` | Ce n'est pas une balise |
| Dans des données de tiers | Balise dans un texte cité avec « > » ou après la première ligne | Ne compte pas (limite : si le texte collé occupe la première ligne sans « > », il compte) |
| Écriture | `zh-Hant-TW` | `zh-Hant` |
| Repli régional | `pt-BR` sans `pt-BR` | `pt` |
| Code retiré | `iw` | `he` |
| Ambiante technique | `LANG=C.UTF-8` | Sans préférence, sans avertissement |
| Ambiante sans catalogue | `LANG=de_DE.UTF-8` | Défaut, avertissement non visible |
| Entrée non UTF-8 | Octets invalides | Avertissement `entrada_invalida` |

La ligne « Répétée » concerne les balises dans les messages. Dans les options de ligne de commande, la répétition suit la
convention de l'analyseur (dans argparse, la dernière l'emporte) : déclarez-le.

Ajoutez un test de totalité : des entrées aléatoires avec une graine fixe, aucune ne fait échouer la
résolution.

## D7 [híbrido] La règle vit dans le code

Si un modèle invoque un script, la règle de sélection vit en lui et pas seulement en prose :
- Le message entre brut **par l'entrée standard depuis un fichier temporaire** que l'agent
  écrit avec son outil d'écriture de fichiers, sans passer par le shell et hors du
  dépôt. Jamais en argument ni dans un JSON écrit à la main : une apostrophe (« j'aimerais »),
  des guillemets ou un `$(…)` cassent ou altèrent la commande. Pas non plus avec un heredoc à délimiteur fixe : si
  le message (ou un texte collé dedans) contient une ligne égale au délimiteur, le heredoc se ferme
  trop tôt et ce qui suit est exécuté comme une commande.
- Fonction totale : aucune entrée ne la fait échouer. Elle renvoie du JSON avec langue, origine, chaîne, avertissements et
  langues disponibles. Les avertissements portent un code : montrez à la personne le texte de votre catalogue pour ce
  code ; le champ de détail est diagnostique.
- Si l'entrée est invalide, elle renvoie un avertissement explicite pour que l'agent l'affiche.
- Testez **la commande telle que vous la documentez**, en l'exécutant avec des apostrophes, des guillemets, `$(…)`,
  des accents graves, une ligne égale à un délimiteur, des accents, des sauts de ligne et des chemins avec
  des espaces, et vérifiez avec un canari inoffensif (`touch` d'un fichier temporaire) que rien ne s'est exécuté.

Mise en œuvre de référence et testée : [scripts/resolver_idioma.py](../../../scripts/resolver_idioma.py).
Elle sert à tester le tableau avec les vrais catalogues ; copiez-la dans le projet seulement si la conception approuvée
le prévoit, et adaptez les clés de la balise et les maillons de repli.

```bash
# El agente escribió antes el mensaje en /ruta/temporal/mensaje.txt con su herramienta de ficheros.
python3 <skill>/scripts/resolver_idioma.py --catalogos ruta/a/catalogos --defecto es \
  --respaldo zh-TW=zh-Hant < /ruta/temporal/mensaje.txt
```
