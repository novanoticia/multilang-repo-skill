<!-- i18n fuente-sha256=22bfd9e76ce2 estado=borrador-ia -->

# Index des identifiants

Il sert à localiser une règle par son identifiant, à la citer ou à en dispenser. Les identifiants sont
stables : une règle retirée n'est pas réutilisée avec un autre sens.

## Contenu
- Où se trouve chaque règle
- Changements par rapport au cadre précédent (v7)

## Où se trouve chaque règle

| Préfixe | Domaine | Identifiants | Fichier |
|---|---|---|---|
| R | Noyau : travail, autorisations, preuve | R1–R20 | SKILL.md |
| D | Conception | D1 | SKILL.md (Phase 3) |
| | | D2–D7 | references/seleccion-idioma.md |
| | | D8–D15, D17–D20 | references/diseno-catalogos.md |
| | | D16, D30, D31 | references/formatos-rtl-unicode.md |
| | | D21–D23, D25, D27–D29 | references/instrucciones-y-agentes.md |
| | | D24 | references/seguridad.md |
| | | D26 | references/traducciones.md |
| P | Tests, revue et tri (triage) | P1–P15 | references/pruebas-y-evidencia.md |
| T | Traductions | T1–T7 | references/traducciones.md |
| C | Contenu externe | C1–C9 | references/contenido-externo.md |
| S | Sécurité | S1–S4, S6 (S5 retirée) | references/seguridad.md |
| Doc | Documentation et paquet | Doc1–Doc9 | references/documentacion-y-paquete.md |
| G | Publication | G1–G9 | references/publicacion.md |
| M | Délégation | M1–M7 | references/delegacion.md |

Les phases conservent la numérotation 0–9. Les catégories de l'inventaire sont des lettres isolées (A–H)
et ne doivent pas être confondues avec des identifiants de règle.

## Changements par rapport au cadre précédent (v7)

Le numéro et le sens de R1–R16, D1–D29, P1–P12, T1–T6, C1–C8, G1–G9 et M1–M7 sont conservés. Certaines
règles étendent ou restreignent leur périmètre sans changer d'objet :

| Identifiant | Changement |
|---|---|
| R4, R5 | Le rythme des résumés et des questions dépend du mode de supervision (R18). |
| R6 | Ajoute l'emplacement du journal et la reprise avec une seule confirmation. |
| R7 | Six niveaux : ajoute `estática` (statique) et `humana` (humaine) et distingue `ci` (CI) de `local` (local). |
| R13 | Distingue capacité, besoin et autorisation ; les autorisations permanentes ne sont pas redemandées. |
| R16 | La note d'IA ne figure que dans les documents publics destinés aux personnes, jamais dans les fichiers machine. |
| D1 | Distingue les sorties déterministes (comparaison exacte) des instructions pour les modèles (texte exact et invariants). |
| D3 | Conserve le sous-tag d'écriture, traite `C`/`POSIX` comme une absence et admet des maillons explicites. |
| D4 | Distingue l'entrée explicite de l'entrée ambiante. |
| D13 | D'abord, le format de l'écosystème ; NFC n'est pas imposé aux littéraux de référence. |
| D16 | N'inclut plus le RTL, qui passe à D30. |
| D18 | Ajouter `lang` à la sortie par défaut exige une exception (D23). |
| D22 | Les avertissements ne vont jamais dans des formats machine. |
| P4 | Ne s'applique pas au texte généré par des modèles ; c'est un niveau `local`. |
| P5 | Les tests d'invariance se valident par sabotage, non en les voyant échouer. |
| P7 | S'applique aux vérifications que vous écrivez, en proportion de l'échelle. |
| M1–M7 | Le module [multi-modelo] devient [delegación] et ne dépend plus d'un protocole externe. |

Identifiants nouveaux : R17 (priorité, auparavant un paragraphe sans identifiant), R18 (modes), R19
(périmètre de la demande), R20 (proportionnalité, auparavant un paragraphe et le tableau de la Phase 1.8),
D30, D31, P13–P15 (auparavant Phases 8.2, 8.1 et 8.3, sans identifiant), T7, C9, S1–S4, S6, et Doc1–Doc9
(auparavant la Phase 7, sans identifiants).

Balises de module : `[alto riesgo]` devient `[alto-riesgo]` et ne force plus l'échelle L ;
`[multi-modelo]` devient `[delegación]` ; `[release]` est réparti entre `[paquete]` et
`[publicación]`. Sont nouvelles `[ecosistema]`, `[rtl-escrituras]`, `[seguridad]` et `[documentación]`.
Les échelles S, M et L conservent leurs lettres, mais mesurent désormais seulement la structure ; le
risque est un axe à part.
