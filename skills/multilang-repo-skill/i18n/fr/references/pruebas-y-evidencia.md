<!-- i18n fuente-sha256=d085019ed69a estado=borrador-ia -->

# Plan, ligne de base, tests, revue et tri (P1–P15)

Lisez-le dans les Phases 4 et 8. Appliquez-le selon l'échelle approuvée (tableau de R20 dans SKILL.md) et
consignez chaque vérification avec son niveau (R7) dans
[assets/evidencias-y-cierre.md](../assets/evidencias-y-cierre.md).

## Contenu
- P1–P3 Plan, ligne de base et extraction
- P4–P8 Tests et validation
- P9–P12 Paquet, CI et rythme
- P13 Évaluation des instructions par scénarios
- P14–P15 Relecture indépendante et tri

## Plan, ligne de base et extraction

**P1 Plan.** Des tâches petites, chacune avec son test, ses fichiers et son critère de « terminé ». Si le
périmètre réel est plus grand que prévu, dites-le avant de poursuivre. En mode guidé, le plan est approuvé
avant d'implémenter et chaque tâche se clôt par son résumé ; en mode autonome, il est consigné et présenté
comme une hypothèse corrigeable (R18).

**P2 Ligne de base, avant de toucher à quoi que ce soit.** Générez-la depuis le commit de base
(`git show <base>:<ruta>`), non depuis la copie de travail, et rendez-la déterministe : date et chemins
fixes, environnement contrôlé et binaires ou zips comparés par contenu.
- Programmes : sorties par langue par défaut dans les modes et les chemins d'erreur représentatifs.
- Instructions : `verificar_adiciones.py` avec la liste fermée de remplacements approuvés (vide si tout
  n'est qu'ajouts). Les lignes de version que le script de version mécanise s'approuvent avec un motif.
- Manifestes : identiques sauf la version.
- `git diff --numstat` ne suffit pas. Il compte les lignes, mais ne dit pas lesquelles ont changé :
  modifier une ligne non approuvée au lieu d'une approuvée donne le même chiffre.

**P3 Extraction avec des outils.** Dans cet ordre : l'extracteur de l'écosystème ; un script qui lit le
littéral réel (AST ou codemod lorsque le volume le justifie) ; et, en échelle S, à la main, avec une
vérification que chaque littéral existe tel quel dans l'original. L'extracteur échoue avec zéro et avec
plusieurs correspondances, et supporte les phrases répétées, coupées sur plusieurs lignes, les citations
et les blocs indentés. Couverture : tout texte visible est un littéral avec clé ou une instruction
déclarée ; ce qui est exclu est listé avec sa raison.

## Tests et validation

**P4 Pseudo-locale.** Appliquez-la lorsque le texte arrive par le code dans une interface ou une
console ; si elle n'apporte rien (peu de chaînes, toutes inventoriées), omettez-la avec son motif. Elle
génère une langue synthétique : chaque phrase enveloppée de marqueurs visibles, avec des accents et 30 %
plus longue. Ce qui sort sans marqueurs est un littéral hors du catalogue ; ce qui sort coupé, un problème
d'espace. C'est une exécution `local` (local), non une simulation. Elle n'est pas distribuée et ne
s'applique pas au texte que génère un modèle.

**P5 Tests d'abord, là où ils apportent une preuve.**
- Code au comportement nouveau (sélection, repli, formats, scripts, validateurs) : écrivez le test,
  regardez-le échouer puis implémentez.
- Tests d'invariance (sortie par défaut identique, contrats identiques) : ils passent dès le début par
  conception. Leur valeur se démontre en cassant à dessein ce qu'ils protègent (P7), non en les voyant
  en rouge.
- Contenu (catalogues) : le validateur tient lieu de test.
- Documentation : pas de TDD.

N'inventez pas de tests en rouge par cérémonie.

**P6 Validation des catalogues.** Utilisez d'abord le validateur de l'écosystème. Pour des catalogues JSON
propres ou i18next sans validateur (ni ICU ni ARB), utilisez
[scripts/validar_catalogos.py](../../../scripts/validar_catalogos.py) :

```bash
python3 <skill>/scripts/validar_catalogos.py ruta/catalogos --referencia es \
  [--marcadores llave|doble-llave|printf] [--plurales sufijo] [--idiomas es,en,fr]
```

Vérifications de base : mêmes clés ; rien de vide ni de `TODO` ; marqueurs nommés et identiques entre les
langues ; ce qui est entre accents graves identique ; listes avec le même nombre d'entrées ; textes
identiques à la référence seulement s'ils sont déclarés invariables ; état cohérent avec les relecteurs
(D12) ; forme (D13) ; et Unicode (D31). Ajoutez les règles propres au projet : glossaire, formats de
données et phrases à risque élevé avec des mots de l'original non traduits (comme heuristique, non comme
vérité ; P8). Si le validateur échoue avec votre contenu, corrigez le contenu, non le validateur.

**P7 Sabotage des vérifications que vous écrivez.** Une vérification nouvelle ne compte que si on l'a vue
échouer face à la casse qu'elle doit détecter. Cassez une copie à dessein, une chose à la fois :
- Garde : ne mesurez rien si la suite non cassée ne passe pas dans le même environnement.
- Chaque casse s'applique exactement une fois. Si elle ne trouve pas sa cible ou la trouve plusieurs
  fois, c'est une défaillance de l'outil, non un succès.
- Consignez quelle vérification détecte chaque casse. Si seul un test générique (chemins, environnement)
  la détecte, elle compte comme non détectée.
- Les survivants se ferment avec un test nouveau ou se justifient comme équivalents. On ne cite jamais
  « 100 % » ni « N sur N » avant d'avoir passé la garde.
- En échelle L, mesurez aussi avec des casses que vous n'avez pas conçues (celles d'une relecture
  indépendante), s'il y en a.
- Défaillances typiques : assertions qui acceptent une phrase répétée ailleurs, nombres qui coïncident
  par hasard, tests tautologiques, YAML lu au mauvais niveau, normalisations qui masquent des changements.
  Un test qui fige des chaînes littérales est un instantané, non un test de comportement : dites-le.
- Ne sabotez pas les outils standard de l'écosystème ni les scripts de cette skill : ils ont déjà leurs
  propres tests. Une copie adaptée au projet (D7), en revanche, est du code à vous.

**P8 Heuristiques entre langues proches.** Une heuristique de mots partagés peut être inutile entre
langues proches (espagnol, galicien, portugais, catalan). Si c'est le cas, omettez-la de façon visible
(test sauté avec son motif) et remplacez-la par des marqueurs orthographiques ou par une relecture mot à
mot. Ignorez ce qui est entre accents graves.

## Paquet, CI et rythme

**P9 [paquete] Test du paquet.** Dans une copie temporaire sans `.git` ni artefacts préalables, exécutez
l'empaquetage réel et comparez la liste avec l'attendu : pas un fichier de moins (un sous-dossier nouveau
que le script ne copie pas) ni un de plus (tests, journal de session, copies des modèles de document,
outils). Montrez la liste (`unzip -l` ou équivalent).

**P10 CI.** Utilisez celle qui existe. Proposez-en une minimale seulement si la personne le souhaite :
permissions en lecture seule, historique complet seulement si les tests comparent avec git, et les
validateurs et tests de votre échelle. Un workflow qui n'a jamais tourné n'est pas une preuve. Le nom du
check est l'`id` du job, ou son `name`, et se confirme dans une exécution réelle. Lisez les résultats avec
les outils de la plateforme, sans boucles de sondage. Sans autorisation de pousser, il n'y a pas
d'exécution : le niveau reste `local` et la CI, `pendiente` (en attente). Une affirmation sur l'état de
la CI ne peut pas être surveillée depuis le dépôt : datez-la et donnez-lui une référence (R8). Si la
personne demande « CI au vert » et qu'il n'y a ni CI ni distant, dites-le dans le message, pas seulement
dans le journal : il n'y a pas de CI qui puisse passer au vert ni moyen de le vérifier d'ici. Sans CI,
l'état est `no aplica` (sans objet) avec ce motif ; si la personne accepte un workflow minimal, il reste
`pendiente` jusqu'à ce qu'il tourne sur la plateforme. La suite au vert se rapporte comme `local`.

**P11 Tests de version maintenables.** Si un test fige le numéro de version, le prochain changement de
version mettra la CI au rouge. Faites-lui lire la version dans les manifestes.

**P12 Après chaque tâche.** Les vérifications de votre échelle, au vert : suite, validateur, ligne de base
et, si vous avez changé des vérifications, leur sabotage.

## P13 Évaluation des instructions par scénarios

Pour ce que seul un modèle peut montrer (langue de la réponse, avertissements, échec sûr, résistance aux
instructions dans des données). Modèle de document :
[assets/escenarios-evaluacion.md](../assets/escenarios-evaluacion.md).
1. **Préenregistrez** avant d'exécuter quoi que ce soit : entrée, critère de réussite, critère d'échec et
   un exemple de chacun. Les textes attendus proviennent des catalogues. Le critère tolère les variations
   légitimes (blancs remplis, nombres) sans être si faible que n'importe quelle sortie passe.
2. **Exécutez** chaque scénario dans un contexte isolé (un sous-agent nouveau, une autre session), avec le
   paquet construit par le vrai script et le message du scénario dans le prompt. Celui qui exécute ne
   connaît pas le critère de réussite. Celui qui évalue est un autre agent ou une personne. Cas fictifs,
   marqués comme tels.
3. **Lisez** les réponses et les notes, pas seulement le verdict : des constats apparaissent qu'aucun
   critère n'avait prévus. Demandez à l'exécutant quels fichiers il a lus et ce qui lui a paru ambigu.
4. Si vous changez un critère après avoir vu les résultats, consignez-le comme changement postérieur avec
   sa raison.
5. Après correction, seconde passe seulement avec les scénarios concernés, de nouveaux exécutants et les
   mêmes critères.
6. Déclarez les limites : c'est une simulation, non la plateforme réelle ; la liste des fichiers lus est
   déclarée par l'exécutant lui-même ; une exécution par scénario ne mesure pas la variabilité ; les
   modèles ne sont pas une relecture humaine. Laissez un tableau pour les exécutions réelles (plateforme,
   modèle, date, résultat).
7. S'il n'y a pas de contextes isolés ou si la personne n'autorise pas à déléguer (M1), les scénarios
   restent préenregistrés et `pendiente`. Ne les jouez pas dans votre propre contexte pour les présenter
   comme exécutés.

## Relecture indépendante et tri

**P14 Revue.** Indépendante veut dire une personne ou un relecteur au contexte vierge, avec un accès en
lecture seule, qui ne reçoit pas vos conclusions : un sous-agent s'il est disponible et autorisé (M1) ou
une personne. Sinon, faites une autorelecture et déclarez-la comme telle. Liste minimale : accolades
littérales et données avec accolades ; contamination par l'environnement de développement ; codes en forme
de locale ; format machine identique entre les langues ; catalogues incomplets ; langues mélangées dans
les sorties et les artefacts ; conseils que le détecteur propre ne reconnaît pas (D19) ; conflits entre
règles (D21) ; listes entre crochets traitées comme des instructions ; persistance de la langue ;
avertissements absents dans les chemins qui s'arrêtent ; paraphrases de noms officiels ; littéraux sans
clé ; entrées qui se dégradent en silence ; voies d'installation sans les fichiers nouveaux ; et chiffres
de la documentation qui ne cadrent plus. Avec un risque élevé, relecture humaine du critique.

**P15 Tri.** Le critique et l'important se corrigent avec un test qui échoue avant (ou avec la casse qui
démontre la vérification). Le mineur se note avec sa raison pour le rapport. Ce qui altérerait la sortie
par défaut ou le contrat avec l'original se note et ne se touche pas sans approbation. Après correction,
répétez le sabotage des vérifications nouvelles.
