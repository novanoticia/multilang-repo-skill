<!-- i18n fuente-sha256=a3513292736f estado=borrador-ia -->

# Preuves et clôture

Une ligne par critère. L'état `superada` (réussie) n'est utilisé que si la vérification a réellement été
exécutée et avec ce résultat. Ce qui est conçu et non exécuté reste `pendiente` (en attente), et ce qui
ne s'applique pas, `no aplica` (sans objet) avec son motif.

## Tableau des preuves

| Critère | Module / règle | Preuve (commande exacte ou artefact) | Niveau (R7) | État | Référence (commit, exécution, date) | Notes |
|---|---|---|---|---|---|---|
| Sortie par défaut ou original sans changements non approuvés | D1, P2 | | | | | |
| Contrats machine identiques dans toutes les langues | B, P6 | | | | | |
| Langues demandées dans tous les modes et chemins d'erreur | [programa] | | | | | |
| Invariants des instructions par langue | [instrucciones], P13 | | | | | |
| Sélection de la langue : tableau des cas et totalité | D6, D7 | | | | | |
| Ajouter une langue = déposer un fichier ; le validateur dit ce qui manque | D8, P6 | | | | | |
| Pas de littéraux hors du catalogue | P3, P4 | | | | | |
| Vérifications propres sabotées, avec garde | P7 | | | | | |
| État des traductions véridique | D12, T5 | | | | | |
| Revue indépendante ou autorevue déclarée | P14 | | | | | |
| Paquet avec exactement les fichiers attendus | [paquete], P9 | | | | | |
| CI de la plateforme | P10 | | | | | |
| Contenu externe avec niveau de source et vigueur | [contenido] | | | | | |
| Scénarios adverses | [seguridad], S3 | | | | | |
| Relecture humaine des phrases à risque | [alto-riesgo] | | | | | |
| Chaque publication, autorisée et consignée | R13, G | | | | | |

## Rapport final

1. **Ce qui existe maintenant.**
2. **Erreurs propres et corrections :** chiffres retirés, données de mémoire qui se sont révélées
   fausses, tests invalides, critères changés après avoir vu les résultats, et leur effet.
3. **Décisions que vous avez prises au nom de la personne** et leur coût si elles étaient erronées.
4. **Écarts par rapport à la skill**, en citant les identifiants et le motif.
5. **Tableau des preuves** (ci-dessus).
6. **Limites connues.**
7. **Points en attente**, avec leur motif.
8. **Ce qui revient à la personne :** fusionner, Release, protection de branche, relecture humaine,
   tests sur la plateforme réelle, domaines ou identifiants d'accès.
9. **Délégation :** journal M7, ou « il n'y a pas eu de délégation ».

Si la session a été compactée en chemin, reconstruisez le rapport à partir du journal de session, non de
mémoire.
