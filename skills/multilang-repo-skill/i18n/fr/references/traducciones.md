<!-- i18n fuente-sha256=b2f653950637 estado=borrador-ia -->

# Traductions et haut risque (T1–T7, D26)

Lisez-le en Phase 5 et chaque fois que [alto-riesgo] est actif.

**T1 Glossaire avant de traduire.** Fixez les termes et le tutoiement ou vouvoiement (`tú` ou `usted`,
`tu` ou `vous`) et utilisez-les toujours de la même façon. Surveillez-le avec un test proportionné à
l'échelle, et documentez le traitement choisi.

**T2 Conservez ce qui n'est pas de la prose.** Marqueurs, émojis, mise en forme et contrats machine restent
intacts. Ne traduisez pas les noms de produit, commandes, modes, options, chemins ni codes (B1) ; les
valeurs de vocabulaire fermé qui ne sont qu'affichées (B2) se traduisent dans la prose, avec le littéral
à côté si la personne doit les écrire. Respectez la typographie de chaque langue (guillemets « », espaces
avant certains signes en français) et notez le choix, car une relecture native peut en préférer un autre.

**T3 Langues proches.** Si votre traduction est identique à l'original et que le validateur le signale,
cherchez la formulation propre à la langue ; n'ajoutez pas d'exceptions pour que cela passe. Marquez-la
invariable seulement si le texte le justifie (symboles, codes, noms propres) et notez la raison.

**T4 Noms officiels (G).** Copiez-les depuis la source officielle dans chaque langue, en lisant la colonne
par son en-tête et non par sa position, et vérifiez qu'elle ne renvoie pas la mauvaise langue. S'il n'y a
pas de version officielle, utilisez le code plus le nom officiel disponible. Si la source est
inaccessible, appliquez R10 (`segunda-mano` (de seconde main) ou `no-comprobado` (non vérifié), et dans
les points en attente).

**T5 État honnête.** Ce que traduit une IA reste `borrador-ia` (brouillon IA) (D12) : dites-le dans le dépôt
et dans la livraison (le rapport à la personne ; un avertissement dans la sortie à l'exécution se décide
en Phase 2, D22), et ne le présentez pas comme relu. Qu'un autre modèle le relise ne le rend pas relu.
N'attribuez pas une qualité linguistique relue à ce qui n'est passé que par une IA.

**T6 Langue la moins sûre.** Dites quelle langue vous jugez avec le moins d'assurance et pourquoi. Une
langue que vous ne pouvez pas juger se livre comme `experimental` (expérimental) (ce qui implique
`borrador-ia`, D12), avec un avertissement renforcé (p. ex. bilingue) et une relecture native
indispensable, et seulement si la personne l'autorise après avoir connu le risque.

**T7 Texte libre du modèle (H).** Il ne tient pas dans un catalogue. Indiquez au modèle de le rédiger dans
la langue choisie et déclarez dans la documentation qu'il n'est pas relu.

## [alto-riesgo]

**D26 Phrases à risque.** Identifiez-les une à une (`riesgo: alto`) : confirmations d'actions
irréversibles, limites professionnelles, avertissements de sécurité, doses, délais et obligations. Ne les
« améliorez » pas en les traduisant. Soignez les constructions qui inversent le sens (questions négatives
auxquelles on répond par oui ou non, doubles négations). Dans les langues que vous ne pouvez pas juger,
signalez-les comme risque au lieu de les reformuler si cela change le contrat avec l'original.

Exigences du module :
- Deux relectures humaines distinctes avant tout usage professionnel : celle du contenu, par une personne
  spécialiste du domaine (C8), et celle de la traduction des phrases à risque, par une personne native (et
  spécialiste le cas échéant). L'une ne remplace pas l'autre. Si elle n'existe pas encore, le dépôt et la
  livraison disent « en attente de relecture humaine » au lieu de donner le travail pour terminé.
- Commits ou PR marqués pour relecture humaine du diff, en commençant par les clés `riesgo: alto`.
- Scénarios (P13) qui vérifient le sens des phrases à risque dans chaque langue, avec le niveau `simulada`
  (simulée) et sans remplacer la relecture humaine.
