<!-- i18n fuente-sha256=5741eaf9c542 estado=borrador-ia -->

# Langue de la réponse de cette skill

Détail du bloc « Langue de la réponse » de `SKILL.md`. Lisez-le quand la personne demande une langue
avec `idioma=xx` ou `lang=xx`, ou quand vous avez un doute sur la manière dont une balise se résout, sur
la phrase fixe de chaque langue ou sur ce qui n'est pas traduit. Les règles de sélection et l'échec sûr
sont dans le bloc ; ici figure ce qui le complète.

## Contenu
- Langues disponibles et état
- Comment se résout une balise
- Phrases fixes de chaque langue
- Ce qui n'est pas traduit

## Langues disponibles et état

| Langue | Dossier | État |
|---|---|---|
| `es` | les fichiers originaux | référence |
| `en` | `i18n/en/` | `borrador-ia` (brouillon IA) |
| `fr` | `i18n/fr/` | `borrador-ia` |
| `zh-Hans` (chinois mandarin simplifié) | `i18n/zh-Hans/` | `borrador-ia` |
| `hi` (hindi) | `i18n/hi/` | `experimental` (expérimental) : relecture par une personne native indispensable (T6) |

Aucune traduction n'a été relue par une personne (T5). La balise choisit la langue de la réponse, non les
langues dans lesquelles un dépôt est traduit.

## Comment se résout une balise

Sans distinguer les majuscules et en retirant le jeu de caractères (`en_US.UTF-8` devient `en-US`) :

| Balise | Résultat |
|---|---|
| `en`, `en-GB`, `en-US` | `en` |
| `fr`, `fr-CA`, `fr-FR` | `fr` |
| `hi`, `hi-IN` | `hi` |
| `zh`, `zh-CN`, `zh-SG`, `zh-Hans`, `zh-Hans-CN` | `zh-Hans` |
| `zh-Hant`, `zh-TW`, `zh-HK`, `zh-MO` | indisponible (D4) : on ne sert pas de chinois simplifié à qui demande du traditionnel (D3) |
| toute autre (`de`, `pt-BR`…) | indisponible (D4) : dites-le, nommez les langues disponibles et continuez comme sans balise |

[scripts/resolver_idioma.py](../../../scripts/resolver_idioma.py) implémente cette règle ; son origine
`defecto` signifie « sans balise », non « répond en espagnol ». Pour cette liste :

```
python3 <skill>/scripts/resolver_idioma.py --disponibles es,en,fr,hi,zh-Hans --defecto es --respaldo zh=zh-Hans --respaldo zh-CN=zh-Hans --respaldo zh-SG=zh-Hans --respaldo zh-TW=zh-Hant --respaldo zh-HK=zh-Hant --respaldo zh-MO=zh-Hant
```

## Phrases fixes de chaque langue

Elles ne s'affichent que lorsque la balise choisit cette langue (D22) : l'avertissement ouvre chaque
réponse, et la ligne d'échec sûr s'ajoute si vous ne pouvez pas lire `i18n/<langue>/` (D25).

| Langue | Avertissement de traduction automatique | Ligne d'échec sûr |
|---|---|---|
| `en` | `Translation machine-generated, not human-reviewed.` | `English version unavailable; continuing with the Spanish files.` |
| `fr` | `Traduction automatique, non relue par une personne.` | `Version française indisponible ; poursuite avec les fichiers espagnols.` |
| `zh-Hans` | `机器翻译，未经人工审阅。` | `简体中文版本不可用；继续使用西班牙语文件。` |
| `hi` | `अनुवाद मशीन द्वारा तैयार किया गया है, मानव द्वारा समीक्षित नहीं। (Translation machine-generated, not human-reviewed.)` | `हिन्दी संस्करण उपलब्ध नहीं है; स्पैनिश फ़ाइलों के साथ आगे बढ़ा जा रहा है।` |

L'avertissement du hindi est bilingue parce que cette langue est livrée comme `experimental` (T6).

## Ce qui n'est pas traduit

Identifiants (R1…Doc9), marqueurs de module, noms de fichier et de script, options, codes
d'avertissement, commandes et blocs de code. Les messages des scripts restent en espagnol.
