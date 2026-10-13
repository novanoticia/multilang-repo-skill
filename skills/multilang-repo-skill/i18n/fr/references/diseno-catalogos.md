<!-- i18n fuente-sha256=12f34a8dd4e7 estado=borrador-ia -->

# Catalogues, clés et exécution (D8–D15, D17–D20)

Lisez-le avec [ecosistema], [programa] ou lorsque le projet va avoir ses propres catalogues.

## Contenu
- D'abord, l'écosystème
- D8–D13 Catalogues et clés
- D14–D15 Exécution et interpolation
- D17–D20 Données, artefacts et logique dépendante de la langue

## D'abord, l'écosystème

Si le projet a déjà de l'i18n ou si son écosystème a un standard (gettext, i18next, ICU MessageFormat ou
MessageFormat 2 s'il l'utilise déjà, Fluent, Rails I18n, `strings.xml`, String Catalogs, ARB…), utilisez
son format, son extracteur, ses règles de pluriel, son repli et son validateur. D8–D9 sont alors
superflus et votre travail porte sur la couverture, le glossaire, les tests et la revue.
`validar_catalogos.py` n'apporte quelque chose que si le format est un JSON propre ou celui d'i18next et
que le projet n'a pas de validateur (P6) ; il n'interprète ni ICU ni ARB. Reportez ce qui suit sur les
mécanismes natifs du format : contexte avec `msgctxt` et commentaires pour les traducteurs dans gettext,
`@clave` avec `description` dans ARB, notes dans XLIFF, `translatable="false"` dans Android. N'imposez
pas de champs ni d'encodages que le format n'admet pas.

Sans i18n en place, l'écosystème est le mécanisme standard du langage ou du framework. Vérifiez ce qu'il
couvre sans rien installer : le module `gettext` de Python ne lit que des `.mo` déjà compilés ; extraire
et compiler exige `xgettext` et `msgfmt` (GNU gettext) ou Babel. S'ils manquent, installer est une
décision (R2) : présentez-la avec le catalogue propre (D8) comme alternative. Les `.mo` ne sont versionnés
que si le projet n'a pas d'étape de construction, avec un test qui les compare à leur `.po` par contenu
(en les chargeant, p. ex. avec `gettext.GNUTranslations`), non par octets : des compilateurs différents
donnent des octets différents. Si l'outil manque, le test est ignoré et cela est déclaré.

## Catalogues et clés

**D8 Catalogue propre (seulement sans écosystème).** Un fichier par langue, découvert à son ajout : le
code n'énumère pas les langues et les fichiers auxiliaires (glossaire, schéma) ne comptent pas comme
langue. Accès par `t(clave, **datos)` ou, dans les instructions, un catalogue `clave → phrase` que le
modèle copie littéralement.
- Si une clé manque, on se replie sur la langue par défaut et on le consigne (dans les tests, cela
  échoue). Si elle manque aussi dans la langue par défaut, c'est une erreur de programmation.
- Le repli par clé mélange les langues dans la sortie. Une langue n'est publiée comme complète que
  lorsque le validateur la donne pour complète. Une langue partielle peut figurer dans le dépôt marquée
  `experimental` (expérimentale) (D12), avec sa limite déclarée ; le validateur la signale comme
  couverture partielle, non comme une erreur.

**D9 La langue par défaut est la référence.** Ses phrases sont les littéraux de l'original : on les
extrait avec des outils (P3), on ne les réécrit pas à la main. Elle peut porter des clés nouvelles
(avertissements que l'original n'avait pas), marquées `origen: nuevo`.

**D10 Un littéral, une clé.** Une clé par phrase complète, y compris pour les titres, les libellés, les
questions d'arrêt et chaque liste d'options prise comme une unité. Ne composez pas de phrases avec des
morceaux traduits.
- Pluriels : utilisez les catégories CLDR de la langue (`zero`, `one`, `two`, `few`, `many`, `other` ;
  chaque langue en utilise un sous-ensemble) avec le mécanisme de l'écosystème : pluriel d'ICU, suffixes
  d'i18next, `ngettext` avec `Plural-Forms`, `<plurals>`. Deux clés (`uno`/`otros`) ne valent que si
  toutes les langues prises en charge et les nombres affichés utilisent ces deux catégories. Sinon,
  déclarez la limite.
- [instrucciones] Distinguez « littéral du catalogue : copiez-le tel quel » de « instruction entre
  crochets : rédigez-la vous-même ». Une liste d'options entre crochets n'est pas une instruction. Fixez
  une seule politique pour les trous entre crochets au moment de les remplir.

**D11 Métadonnées par clé, en proportion.** Dans les catalogues propres : `origen` (`original` |
`nuevo`), `fuente` (fichier et ligne de l'original, comptée sans les blocs ajoutés), `contexto` (une
ligne pour qui traduit ou relit : où cela apparaît, ce que cela signifie, limite de longueur), `riesgo`
(`alto` (élevé) pour les phrases qui confirment des actions irréversibles, des limites ou la sécurité),
`invariable` (justifié par le texte lui-même : symboles, codes ou noms propres) et `maquina` (identique
dans toutes les langues). À l'échelle S, `contexto` et `riesgo` suffisent là où ils sont nécessaires.
Dans les formats d'écosystème, utilisez leur mécanisme natif. Forme dans un JSON propre : les
métadonnées vont dans la référence sous la forme `"@clave": {"contexto": …, "riesgo": …,
"invariable": true}` (dans le style ARB), que le validateur exclut de la parité. Ce qui est invariable
dans toutes les langues se déclare là ; ce qui n'est identique que dans une langue (fréquent entre
langues proches) se déclare dans ce catalogue, dans `_meta.invariables`, avec sa raison.

**D12 État de chaque langue.** `referencia`, `borrador-ia` (brouillon IA), `experimental` ou `revisado`,
avec qui a rédigé et qui a relu. `experimental` est un `borrador-ia` incomplet ou d'une langue que l'on
ne peut pas juger : en plus de ne pas être relu, il porte un avertissement renforcé (T6). `revisado`
exige une personne relectrice identifiée ; l'avis d'un autre modèle ne change pas l'état. Lorsqu'il y a
une relecture humaine, il suffit de mettre le champ à jour. Où on l'enregistre : dans les catalogues JSON
propres, dans `_meta` ; dans les formats d'écosystème qui n'admettent pas ce champ (p. ex. un JSON
d'i18next que l'application charge tel quel), dans la documentation du projet (section des langues du
README) ou dans un fichier d'état à part, jamais en ajoutant des champs que le chargeur afficherait ou
rejetterait.
[scripts/validar_catalogos.py](../../../scripts/validar_catalogos.py) vérifie cette cohérence dans les
catalogues JSON (`_meta.estado`, `_meta.revisado_por`).

**D13 Forme du fichier.** D'abord, ce qu'exige le format de l'écosystème : certains formats ont un
encodage déclaré dans l'en-tête et des formats hérités ne sont pas en UTF-8, donc vérifiez-le au lieu de
le supposer. Sans format imposé : UTF-8 sans BOM, saut de ligne final, ordre des clés déterministe et
Unicode NFC dans les nouvelles traductions. Ne normalisez pas les littéraux de référence si cela change
les octets de la sortie par défaut (D1) ; déclarez-le comme limite ou demandez l'exception.

## Exécution et interpolation

**D14 État de la langue à l'exécution.** Dans un processus à demande unique, une langue globale fixée au
démarrage suffit. Dans les serveurs, les tâches concurrentes ou les bibliothèques, la langue est
portée par demande ou par contexte, jamais dans une variable globale partagée.

**D15 Modèles de document et interpolation.** Uniquement des champs nommés. Les accolades littérales sont
échappées, et la donnée interpolée n'est jamais réinterprétée comme modèle, comme balisage ni comme
instruction. Dans les instructions pour un modèle, délimitez la donnée interpolée comme donnée (S1).

## Données, artefacts et logique dépendante de la langue

**D17 Textes dans les données de configuration.** La langue d'origine reste où elle est et les autres la
surchargent par clé : une seule origine par texte et par langue. S'il existait un champ de langue qui
était ignoré et qui est désormais lu, c'est un changement qui va au CHANGELOG.

**D18 Artefacts (E).** Décidez avec la personne si la langue choisie les concerne. Garantissez qu'ils ne
mélangent pas les langues et déclarez la langue dans les formats qui l'admettent (`lang` en HTML,
métadonnées dans les PDF). Ajouter cet attribut à la sortie par défaut change ses octets : c'est donc
une exception à faire approuver (D23).

**D19 Ce qui est conseillé doit être reconnu.** Si le programme conseille une phrase dans une langue, son
détecteur doit la reconnaître dans cette langue. Les phrases qui activent un mode (« ejecuta »,
« deshaz ») sont aussi des littéraux du catalogue. Les valeurs affichées en prose qui reviennent en
entrée se reconnaissent par équivalence avec le catalogue.

**D20 `--help` et erreurs du parseur.** Ils se construisent souvent avant de connaître la langue :
traduisez-les en résolvant la langue avant de construire le parseur, ou déclarez la limite. Les messages
des scripts auxiliaires peuvent rester dans la langue d'origine si cela est déclaré. Une nouvelle option
(`--idioma`) change à elle seule l'aide et la ligne d'usage dans la langue par défaut. Si la personne a
demandé cette option, le changement fait partie de ce qui était demandé : il va dans la liste des
changements (D1), il est dit dans le résumé et le reste se compare octet par octet. Si elle ne l'a pas
demandée (la sélection se fait par balise ou par variable), ne l'affichez pas sans approbation :
masquez-la de l'aide (p. ex. `help=argparse.SUPPRESS`) et documentez-la à part. Masquée ou non, une
nouvelle option change les abréviations qu'argparse accepte (`--i` devient ambiguë si `--input`
existait déjà) : choisissez un nom sans préfixe commun avec les options existantes ou incluez dans la
ligne de base (P2) les abréviations qui fonctionnent aujourd'hui.
