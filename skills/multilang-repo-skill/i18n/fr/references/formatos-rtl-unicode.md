<!-- i18n fuente-sha256=ddb207eacaa3 estado=borrador-ia -->

# Formats, RTL et Unicode (D16, D30, D31)

Lisez-le si le projet formate des dates, des nombres, des monnaies ou trie du texte ([programa]), et
toujours avec [rtl-escrituras]. Lorsqu'une norme est déterminante pour une décision, consultez-la dans sa
source (R10) : BCP 47 (RFC 5646 et RFC 4647), CLDR, UAX #9 (bidirectionnalité), UAX #15 (normalisation)
et UTS #39 (mécanismes de sécurité Unicode).

## Contenu
- D16 Formats dépendant de la locale
- D30 Texte de droite à gauche et écritures complexes
- D31 Politique Unicode : signaler, ne pas supprimer

## D16 Formats dépendant de la locale

- Dates, heures, nombres, monnaies, unités, tri et changement de casse avec le mécanisme de l'écosystème
  (`Intl`, ICU, Babel, `java.text`…) et la locale choisie. Ne les réimplémentez pas.
- La langue par défaut conserve **exactement** son format actuel (D1). Si le passage au formateur de
  l'écosystème change ses octets, continuez à utiliser le format actuel pour la langue par défaut ou
  demandez l'exception. La ligne de base le détecte.
- Les opérations sur les contrats machine (clés, commandes, identifiants) ne dépendent pas de la locale.
  En Java, `"i".toUpperCase()` avec la locale par défaut en turc donne `İ`, et en JavaScript
  `toLocaleUpperCase("tr")` fait de même : comparez et transformez ces contrats avec des opérations
  invariantes (`toUpperCase(Locale.ROOT)`, `toUpperCase()` en JavaScript).
- Les chaînes s'allongent à la traduction. Réservez de l'espace, ne tronquez pas en silence et testez avec
  une pseudo-locale (P4).

## D30 Texte de droite à gauche et écritures complexes

- Déclarez la direction dans le support : `dir="rtl"` et `lang` en HTML, et propriétés logiques de CSS
  (`margin-inline-start` au lieu de `margin-left`). Reflétez les icônes directionnelles.
- Isolez les valeurs de direction contraire qui sont interpolées (noms, chemins, commandes, nombres) avec
  `<bdi>`, avec les isolats U+2068…U+2069 ou avec l'isolation que le framework applique déjà. Ainsi, un
  contrat en caractères latins ne se désordonne pas à l'intérieur d'une phrase en arabe ou en hébreu.
- Vérifiez l'affichage réel : liaison des lettres en arabe, consonnes conjointes en écritures indiennes, tableaux et
  Markdown en RTL. Beaucoup de terminaux n'appliquent pas l'algorithme bidirectionnel : dans les outils de
  console, testez ou déclarez la limite.
- Terminez par un test d'affichage (capture ou sortie rendue relue) ou par la limite déclarée. Si la
  personne qui relit ne lit pas la langue, dites-le.

## D31 Politique Unicode : signaler, ne pas supprimer

Beaucoup de caractères invisibles sont légitimes et nécessaires. Les supprimer sans discernement casse des
langues réelles :

| Caractère | Usage légitime |
|---|---|
| ZWNJ U+200C | Orthographe persane et d'autres langues (`می‌خواهم`) |
| ZWJ U+200D | Consonnes conjointes en écritures indiennes ; séquences d'émojis (👨‍👩‍👧) |
| LRM/RLM U+200E/U+200F, ALM U+061C, isolats U+2066–U+2069 | Texte bidirectionnel bien formé |
| Sélecteurs de variation U+FE00–U+FE0F, U+E0100–U+E01EF | Présentation des émojis ; variantes d'idéogrammes |
| U+200B | Coupures de ligne dans les langues sans espaces (thaï, khmer, lao, birman) |
| U+00AD | Césure optionnelle |
| Étiquettes U+E0020–U+E007F après U+1F3F4 | Drapeaux de subdivision (p. ex. celui de l'Écosse) |

Méritent une relecture, et sont donc signalés :
- Les incorporations et surcharges bidirectionnelles U+202A–U+202E. Elles peuvent afficher un ordre
  visuel différent de l'ordre logique et cacher le contenu réel à la personne qui relit (le vecteur des
  attaques « Trojan Source »). Dans le texte RTL, les isolats suffisent en général.
- Les contrôles bidirectionnels sans pendant à l'intérieur d'une valeur.
- Les caractères d'étiquette U+E0000–U+E007F en dehors d'un drapeau : invisibles, ils peuvent cacher du
  texte.
- Tout invisible, contrôle ou mélange d'écritures à l'intérieur d'un **contrat machine** (clé, marqueur,
  commande, option, URL) : là, c'est une erreur, car un homoglyphe ou un invisible change l'identité du
  contrat.

Procédure : générez le rapport avec [scripts/validar_catalogos.py](../../../scripts/validar_catalogos.py),
relisez chaque cas avec son contexte, décidez avec la personne et corrigez seulement le cas concret. Le
script ne modifie jamais de fichiers. Un rapport sans constats signifie que ces motifs n'ont pas été
trouvés, non que le texte soit sûr (S6).
