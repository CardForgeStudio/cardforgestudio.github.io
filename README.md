# CardForgeStudio – site web

Site statique (GitHub Pages) du studio CardForgeStudio : accueil + règles des jeux, en 5 langues (fr, en, de, es, it).
URL : https://cardforgestudio.github.io/ — Play Store : com.cardforgestudio.tarotafricain

## Principe
Les pages HTML sont **générées** par `gen.py` à partir des fichiers JSON de `content/`. Ne jamais éditer à la main les fichiers
`index.html`, `<slug>.html`, `en/ de/ es/ it/`, `sitemap.xml`, `robots.txt` : ils sont écrasés à chaque génération.

```
python gen.py        # régénère toutes les pages + sitemap.xml + robots.txt
```
Le script affiche `ATTENTION, captures introuvables` si une capture manque. Puis `git add . && git commit && git push` (déploiement automatique).

## Arborescence
| Chemin | Rôle |
|---|---|
| `content/site.json` | Textes communs par langue (accueil, menus, pied de page, éventail de cartes `fan`) |
| `content/games/<slug>.json` | Un fichier par jeu : fiche accueil + règles (sections), champs `aka` (autres noms, SEO) |
| `gen.py` | Générateur. Constantes en tête : `BASE`, `UTM_SOURCE`, `VERIF` (balise Search Console) |
| `styles.css` | Thème unique (feutre vert/or) |
| `images/screenshots/<lang>/` | Captures `bidding`, `excuse`, `partie`, `variante` (png, jpg, jpeg ou webp, détecté automatiquement) |
| `images/cards/` | SVG de l'éventail de la page d'accueil |
| `images/logo/` | Badge Google Play (SVG recadré 135×40) |
| `favicon.*`, `icon-192.png`, `apple-touch-icon.png` | Icônes d'onglet |
| `privacy-policy.html` | Politique de confidentialité FR/EN, **éditée à la main** (pas générée), liée depuis Play Console |

## Tâches courantes
- **Modifier un texte** : éditer le JSON (toutes les langues : `fr`, `en`, `de`, `es`, `it`), relancer `gen.py`.
- **Ajouter un jeu** : copier `content/games/tarot-africain.json` en `content/games/<slug>.json`, changer `slug`, `order`, `play`, `hero`, et traduire `lang.*`. Ajouter les captures dans `images/screenshots/<lang>/`. Lancer `gen.py` : page de règles, fiche accueil, sitemap sont créés.
- **Sections de règles** : liste `sections` ; chaque bloc est `{"p":…}`, `{"note":…}`, `{"table":{"head":[…],"rows":[[…]]}}` ou `{"fig":{"img":"nom","cap":"légende"}}`. `id` = ancre du sommaire.
- **Ajouter une langue** : ajouter le code dans `LANGS` (gen.py), une entrée dans `site.json` et dans chaque jeu.
- **Nom du studio** : constante `brand` de `site.json` + logo dans `gen.py` (`Card<span>Forge</span>Studio`).

## SEO
- `BASE` (gen.py) alimente canonical, hreflang (+ x-default), `sitemap.xml` et `robots.txt`.
- Autres noms du jeu (Whist 22, tarot mexicain) : champ `aka`, titre `t_r`, ligne « mexicaine » du tableau des variantes.
- Search Console : soumettre `https://cardforgestudio.github.io/sitemap.xml`. La balise de vérification est dans `VERIF` (page d'accueil FR uniquement).

## Suivi des clics vers le Play Store
Chaque badge pointe vers `…&referrer=utm_source=cardforgestudio-site&utm_medium=website&utm_campaign=<slug>_<lang>&utm_content=<emplacement>` (encodé).
Emplacements : `index_hero`, `index_card`, `index_banner`, `rules_header`, `rules_banner`. Aucun cookie ni script de suivi : la politique de confidentialité reste exacte. Ajouter un outil d'analyse (ex. Google Analytics) imposerait de mettre à jour `privacy-policy.html`.

## Règles à respecter
- Texte en français pour les commentaires ; typographie française dans les textes `fr`.
- Pas de JavaScript ni de ressource externe (polices, CDN) sans nécessité : site 100 % statique.
- Après chaque changement de contenu : `python gen.py`, ouvrir `index.html` et une page de règles dans le navigateur, vérifier qu'aucune capture n'est signalée manquante.
