# 📊 ROYAUME — collecter les stats de partie dans un Google Sheet

Le jeu peut envoyer **une ligne par partie** à un Google Sheet que vous possédez :
durée, nombre de tours, vainqueur, **cupidité moyenne du Roi**, répartition des
nuits, révoltes et leur issue, assassinats, etc. Seul l'**hôte** (ou le joueur
solo) envoie — donc une seule ligne par partie, jamais de doublon.

Par défaut c'est **désactivé** (aucune donnée n'est envoyée) tant que vous n'avez
pas collé votre propre URL. Voici comment l'activer en 5 minutes.

## 1. Créer le Google Sheet + le script

1. Ouvrez un nouveau classeur : tapez **sheets.new** dans votre navigateur.
2. Menu **Extensions → Apps Script**.
3. Effacez le code par défaut, collez celui-ci, puis **enregistrez** (💾) :

```javascript
function doPost(e) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName('Parties') || ss.insertSheet('Parties');
  var data = JSON.parse(e.postData.contents);
  var lastCol = sheet.getLastColumn();
  var headers = lastCol ? sheet.getRange(1, 1, 1, lastCol).getValues()[0].filter(String) : [];
  if (headers.length === 0) {
    headers = Object.keys(data);
    sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
    sheet.setFrozenRows(1);
  }
  var row = headers.map(function (h) {
    var v = data[h];
    if (v === null || v === undefined) return '';
    return (typeof v === 'object') ? JSON.stringify(v) : v;
  });
  sheet.appendRow(row);
  return ContentService.createTextOutput('ok');
}
```

## 2. Déployer le script en « Web App »

1. En haut à droite : **Déployer → Nouveau déploiement**.
2. Roue crantée ⚙ → **Application Web**.
3. Réglages :
   - **Exécuter en tant que** : *Moi*
   - **Qui a accès** : *Tout le monde*
4. **Déployer** → autorisez l'accès (choisissez votre compte, « Autoriser »).
5. Copiez l'**URL de l'application Web** (elle finit par `/exec`).

## 3. Brancher l'URL dans le jeu

1. Ouvrez `republica3d.html`, cherchez la ligne :
   ```js
   const STATS_URL = '';   // ← collez ici l'URL de votre Google Apps Script (voir notice)
   ```
2. Collez votre URL entre les guillemets :
   ```js
   const STATS_URL = 'https://script.google.com/macros/s/AKfy.../exec';
   ```
3. Enregistrez, poussez sur GitHub (Render se redéploie), et **renvoyez le fichier**
   à jour à vos amis. C'est tout : chaque partie terminée ajoutera une ligne.

## Ce qui est enregistré (une colonne chacun)

`date`, `duree_min`, `tours`, `joueurs`, `humains`, `ia`, `difficulte`,
`vainqueur`, `vainqueur_humain`, `score_1er`, `score_2e`, `ecart`,
**`cupidite_roi_pct`** (part de la taille que le Roi se garde, en moyenne),
`nuits_manoir` / `nuits_templiers` / `nuits_favorite` / `nuits_monastere`,
`votes_pour`, `votes_contre`, `budgets_rejetes`,
`revoltes`, `revoltes_felons_gagnees`, `assassinats`, `morts`,
et `detail_json` (le détail complet par joueur + la chronologie tour par tour,
pour les analyses fines).

## Analyser

Dans le Sheet, sélectionnez les colonnes et utilisez **Insertion → Graphique**
ou un **tableau croisé dynamique** :
- durée moyenne des parties, distribution du nombre de tours ;
- cupidité moyenne des Rois, et son lien avec le taux de révolte ;
- quelle planque de nuit domine (Manoir / Templiers / Favorite / Monastère) ;
- taux de victoire des félons dans les révoltes.

> Astuce : filtrez `humains >= 2` pour ne garder que les vraies parties entre
> amis (et exclure vos tests en solo contre les IA).

## Vie privée

Les données partent **uniquement vers votre Sheet** (aucun tiers). Elles
contiennent les pseudos choisis par les joueurs et leurs choix de jeu — rien de
personnel. Pour tout couper, remettez `const STATS_URL = '';`.
