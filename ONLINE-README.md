# REPÚBLICA ONLINE — guide de mise en route

## Ce qui est prêt
- **republica-server.js** : le serveur de salons complet — codes de salon à 5 lettres,
  pseudos, tchat relayé, canal d'actions de jeu (modèle hôte-autoritaire), et
  signalisation WebRTC pour le vocal pair-à-pair. Jusqu'à 7 joueurs par salon.
- **republica3d.html** : le jeu contient déjà la saisie du nom et la barre de tchat ;
  la fonction `sendChat()` est annotée à l'endroit exact où brancher le réseau.

## Étape 1 — Héberger le serveur (10 minutes, gratuit)
1. Créer un dossier avec `republica-server.js` et un `package.json` :
   ```json
   { "name": "republica-online", "scripts": { "start": "node republica-server.js" },
     "dependencies": { "ws": "^8.0.0" } }
   ```
2. Pousser sur un dépôt GitHub, puis créer un service sur **Render.com** (ou Railway) :
   "New Web Service" → connecter le dépôt → il détecte Node et lance `npm start`.
3. Render fournit une URL du type `https://republica-online.onrender.com` ;
   le WebSocket sera `wss://republica-online.onrender.com`.

## Étape 2 — Le protocole (déjà implémenté côté serveur)
| Message client → serveur                | Effet                                           |
|-----------------------------------------|-------------------------------------------------|
| `{t:'create', name}`                     | crée un salon, renvoie `{t:'created', code}`     |
| `{t:'join', code, name}`                 | rejoint ; tous reçoivent `{t:'lobby', players}`  |
| `{t:'chat', text}`                       | relayé à tout le salon                           |
| `{t:'start', config}` (hôte)             | lance la partie pour tous                        |
| `{t:'action', data}`                     | action d'un joueur → transmise à l'hôte          |
| `{t:'state'/'event', data}` (hôte)       | l'hôte diffuse l'état du jeu à tous              |
| `{t:'signal', to, data}`                 | signalisation WebRTC (vocal) entre deux joueurs  |

**Modèle hôte-autoritaire** : le créateur du salon fait tourner la logique du jeu
(celle qui existe déjà dans republica3d.html) ; les autres clients affichent l'état
reçu et envoient leurs choix (vote, planque, déploiement...). C'est le modèle le plus
simple et suffisant entre amis.

## Étape 3 — Le vocal (WebRTC mesh)
Le serveur relaie déjà la signalisation. Côté client, pour chaque paire de joueurs :
```js
const pc = new RTCPeerConnection({ iceServers: [{ urls: 'stun:stun.l.google.com:19302' }] });
navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
  stream.getTracks().forEach(tr => pc.addTrack(tr, stream));
});
pc.ontrack = e => { const audio = new Audio(); audio.srcObject = e.streams[0]; audio.play(); };
pc.onicecandidate = e => e.candidate && ws.send(JSON.stringify({ t:'signal', to: peerId, data:{ ice: e.candidate } }));
// offre/réponse échangées via {t:'signal'} — le serveur transmet, les navigateurs se parlent en direct.
```
À 7 joueurs max, le maillage complet (chacun connecté à chacun) fonctionne très bien.

## Étape 4 — Brancher le jeu (la prochaine grosse session)
Dans republica3d.html, il reste à :
1. Ajouter l'écran "Créer / Rejoindre un salon" (avant l'écran titre actuel).
2. Remplacer les réponses IA du tchat par l'envoi `{t:'chat'}` (repère `NOTE ONLINE` dans le code).
3. Chez l'hôte : à chaque `await ask(...)` destiné à un autre joueur, envoyer la question
   via `{t:'event'}` et attendre son `{t:'action'}` — les joueurs manquants restent des IA.
4. Diffuser l'état (argent visible, pions, unités, journal) après chaque phase.

C'est l'étape la plus longue (~ le volume du système de coup d'État), mais toute
l'architecture est en place pour la recevoir.
