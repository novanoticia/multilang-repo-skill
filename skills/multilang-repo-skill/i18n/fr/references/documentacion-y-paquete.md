<!-- i18n fuente-sha256=07e40f3e506e estado=borrador-ia -->

# Documentation, version et paquet (Doc1–Doc9)

Lisez-le en Phase 7, avec [documentación] ou avec [paquete]. Suivez les conventions du dépôt (R17) :
s'il n'utilise ni CHANGELOG, ni `AGENTS.md`, ni journal des points en attente, proposez de les créer avant de le faire.

**Doc1 README.** Comment choisir la langue, ce qui est traduit et ce qui ne l'est pas (contrats machine,
texte libre du modèle), comment ajouter une langue, cas limites, limitations (ce qu'un détecteur ne couvre pas, langues
expérimentales) et l'état réel des traductions (`borrador-ia` (brouillon IA), `revisado` (relu)…), une fois par
langue. La note d'élaboration avec IA suit R16. Si le périmètre est court, une section multilingue suffit ; ne traduisez pas le README en entier sauf
si on le demande. En traduisant de la documentation, conservez intacts les blocs de code, les commandes, les
ancres et les liens.

**Doc2 Voies d'installation manuelles.** Si l'une consiste à copier des fichiers à la main, ajoutez-y les nouveaux
(catalogues, scripts). Sans eux, la fonction n'existe pas pour qui installe ainsi.

**Doc3 `AGENTS.md` ou `CLAUDE.md`.** S'ils existent : ne pas écrire de nouveaux littéraux hors du catalogue ;
blocs délimités ; frontmatter intact ; fichiers intouchables ; relecture humaine des diffs à haut
risque ; commandes de validation ; ne pas fusionner avec la CI au rouge ; que faire lors du prochain changement
de version ; et points en attente extérieurs connus. S'il n'en existe qu'un, vérifiez s'il renvoie vers l'autre.

**Doc4 Version.** Selon la politique du projet (p. ex. semver : une fonction compatible est minor), avec
son script s'il existe, dans tous les manifestes à la fois et avec un test qui les compare (P11).

**Doc5 CHANGELOG.** Ajouté, Modifié, Corrigé et Limitations, y compris les exceptions approuvées
(D23) et les lignes de l'original qui changent. Avant de clore, cherchez chaque chiffre cité (clés,
ruptures, scénarios, tailles) et comparez-le à l'état actuel (R9).

**Doc6 Journal des points en attente** (`PENDIENTES.md` ou l'équivalent du dépôt). Seulement ce qui est
vérifié : ce qui requiert une personne (relecture, identifiants), ce qui requiert une autre session ou l'accès à des
domaines, quelles sources manquent, quels scénarios n'ont pas été exécutés et quels changements ne sont pas encore sur la branche
principale.

**Doc7 [paquete] Contenu du paquet.** Le script d'empaquetage inclut tous les nouveaux fichiers et
rien d'autre, démontré avec P9. S'il existe d'anciens paquets déjà téléchargés, la note de version dit qu'il
faut réinstaller le paquet complet.

**Doc8 [paquete] Noms des pièces jointes.** Si le README renvoie vers une pièce jointe par son nom (p. ex.
`releases/latest/download/<nombre>.zip`), la pièce jointe s'appelle exactement ainsi : un suffixe de version
casse le lien.

**Doc9 Manuel d'utilisation, s'il existe.** Lisez-le en entier avant de le modifier. Conservez sa structure et sa
numérotation, car d'autres parties y renvoient ; ajoutez le nouveau à la fin, avec un encadré de nouveautés
au début. Si un PDF est généré (p. ex. depuis du HTML avec un navigateur sans interface), vérifiez à l'œil la
couverture et une page avec tableau. Il porte la note d'IA (R16) et conserve la version précédente comme
historique.
