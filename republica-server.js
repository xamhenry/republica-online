// =====================================================================
// REPÚBLICA ONLINE — serveur de salons (Node.js + WebSocket)
// Fournit : salons à code, pseudos, tchat relayé, signalisation WebRTC
// (pour le vocal pair-à-pair), et le canal d'actions de jeu
// (architecture "hôte autoritaire" : le créateur du salon fait tourner
// la logique du jeu, les autres envoient leurs actions et reçoivent l'état).
//
// Lancer :   npm install ws   puis   node republica-server.js
// Héberger : Render / Railway / Fly.io (offre gratuite suffisante)
// =====================================================================
"use strict";
const http = require('http');
const crypto = require('crypto');
const { WebSocketServer } = require('ws');

const PORT = process.env.PORT || 8080;
const MAX_PLAYERS = 7;

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain; charset=utf-8' });
  res.end('REPÚBLICA ONLINE — serveur de salons opérationnel.\n');
});
const wss = new WebSocketServer({ server });

// rooms[code] = { hostId, clients: Map<id, {ws, name}>, started }
const rooms = {};
let nextId = 1;

function send(ws, msg){ if (ws.readyState === 1) ws.send(JSON.stringify(msg)); }
function broadcast(room, msg, exceptId){
  room.clients.forEach((c, id) => { if (id !== exceptId) send(c.ws, msg); });
}
function lobbyState(code){
  const room = rooms[code];
  return {
    t: 'lobby',
    code,
    hostId: room.hostId,
    players: [...room.clients.entries()].map(([id, c]) => ({ id, name: c.name })),
    started: room.started,
  };
}
function makeCode(){
  const letters = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';
  let c = '';
  for (let i = 0; i < 5; i++) c += letters[Math.floor(Math.random() * letters.length)];
  return rooms[c] ? makeCode() : c;
}

const GHOST_TTL = 15 * 60 * 1000;   // 15 min pour revenir après une déconnexion en partie

// détection des connexions mortes : derrière le proxy (Render/Cloudflare), une
// coupure brutale (téléphone en veille) n'émet pas toujours de 'close'. Les clients
// envoient {t:'ping'} toutes les 15 s ; sans nouvelle d'une connexion depuis 35 s,
// on la termine — ce qui déclenche le 'close' et donc la mise en pause côté hôte.
setInterval(() => {
  wss.clients.forEach((c) => {
    if (Date.now() - (c.lastSeen || 0) > 35000) return c.terminate();
    try { c.ping(); } catch (e) {}
  });
}, 10000);

wss.on('connection', (ws) => {
  let id = nextId++;                 // réassigné si le client reprend un siège (rejoin)
  let roomCode = null;
  ws.lastSeen = Date.now();
  ws.on('pong', () => { ws.lastSeen = Date.now(); });

  ws.on('message', (raw) => {
    ws.lastSeen = Date.now();
    let msg;
    try { msg = JSON.parse(raw); } catch { return; }
    const room = roomCode ? rooms[roomCode] : null;

    switch (msg.t) {
      // ---- créer un salon : {t:'create', name} ----
      case 'create': {
        const code = makeCode();
        const token = crypto.randomBytes(8).toString('hex');
        rooms[code] = { hostId: id, clients: new Map(), ghosts: {}, started: false };
        rooms[code].clients.set(id, { ws, name: String(msg.name || 'Ministre').slice(0, 16), token });
        roomCode = code;
        send(ws, { t: 'created', code, you: id, token });
        send(ws, lobbyState(code));
        break;
      }
      // ---- rejoindre : {t:'join', code, name} ----
      case 'join': {
        const code = String(msg.code || '').toUpperCase();
        const r = rooms[code];
        if (!r)            return send(ws, { t: 'error', error: 'Salon introuvable.' });
        if (r.started)     return send(ws, { t: 'error', error: 'La partie a déjà commencé.' });
        if (r.clients.size >= MAX_PLAYERS) return send(ws, { t: 'error', error: 'Salon complet (7 max).' });
        const token = crypto.randomBytes(8).toString('hex');
        r.clients.set(id, { ws, name: String(msg.name || 'Ministre').slice(0, 16), token });
        roomCode = code;
        send(ws, { t: 'joined', code, you: id, token });
        broadcast(r, lobbyState(code));
        send(ws, lobbyState(code));
        break;
      }
      // ---- reprendre sa place après une coupure : {t:'rejoin', code, token} ----
      // le siège d'un joueur déconnecté en pleine partie est gardé GHOST_TTL ;
      // il revient avec le MÊME id, l'hôte le re-promeut d'IA à humain.
      case 'rejoin': {
        const code = String(msg.code || '').toUpperCase();
        const r = rooms[code];
        const g = r && r.ghosts && r.ghosts[String(msg.token || '')];
        if (!g) return send(ws, { t: 'error', error: 'Impossible de reprendre la partie (siège expiré ou salon fermé).' });
        clearTimeout(g.timer);
        delete r.ghosts[String(msg.token)];
        id = g.id;
        roomCode = code;
        r.clients.set(id, { ws, name: g.name, token: String(msg.token) });
        send(ws, { t: 'rejoined', code, you: id });
        broadcast(r, { t: 'back', id }, id);
        broadcast(r, lobbyState(code));
        break;
      }
      // ---- tchat : {t:'chat', text} → relayé à tout le salon ----
      case 'chat': {
        if (!room) return;
        const c = room.clients.get(id);
        broadcast(room, { t: 'chat', from: id, name: c.name, text: String(msg.text || '').slice(0, 200) });
        send(ws, { t: 'chat', from: id, name: c.name, text: String(msg.text || '').slice(0, 200) });
        break;
      }
      // ---- lancement (hôte uniquement) : {t:'start', config:{count, difficulty}} ----
      case 'start': {
        if (!room || room.hostId !== id) return;
        room.started = true;
        broadcast(room, { t: 'start', config: msg.config || {} });
        send(ws, { t: 'start', config: msg.config || {} });
        break;
      }
      // ---- jeu, modèle hôte-autoritaire :
      // les joueurs envoient leurs actions {t:'action', data} → relayées à l'hôte ;
      // l'hôte fait tourner la logique et diffuse {t:'state', data} / {t:'event', data}.
      case 'action': {
        if (!room) return;
        const host = room.clients.get(room.hostId);
        if (host) send(host.ws, { t: 'action', from: id, data: msg.data });
        break;
      }
      case 'state':
      case 'event': {
        if (!room || room.hostId !== id) return;   // seul l'hôte diffuse l'état
        broadcast(room, { t: msg.t, data: msg.data }, id);
        break;
      }
      // ---- signalisation WebRTC pour le VOCAL : {t:'signal', to, data} ----
      // le vocal est pair-à-pair (mesh) : le serveur ne fait que transmettre
      // les offres/réponses/candidats ICE entre navigateurs.
      case 'signal': {
        if (!room) return;
        const target = room.clients.get(msg.to);
        if (target) send(target.ws, { t: 'signal', from: id, data: msg.data });
        break;
      }
    }
  });

  ws.on('close', () => {
    if (!roomCode || !rooms[roomCode]) return;
    const room = rooms[roomCode];
    const code = roomCode;
    const me = room.clients.get(id);
    room.clients.delete(id);

    // partie en cours : on garde le siège au chaud (ghost), l'hôte reste hôte
    if (room.started && me) {
      const gid = id;
      const g = { id: gid, name: me.name };
      g.timer = setTimeout(() => {
        if (!rooms[code]) return;
        delete room.ghosts[me.token];
        if (room.clients.size === 0 && !Object.keys(room.ghosts).length) { delete rooms[code]; return; }
        if (room.hostId === gid && room.clients.size) {   // l'hôte ne reviendra plus
          room.hostId = [...room.clients.keys()][0];
          broadcast(room, lobbyState(code));
        }
      }, GHOST_TTL);
      room.ghosts[me.token] = g;
      broadcast(room, lobbyState(code));
      broadcast(room, { t: 'left', id });
      return;
    }

    if (room.clients.size === 0) { delete rooms[code]; return; }
    if (room.hostId === id) room.hostId = [...room.clients.keys()][0];   // l'hôte suivant reprend
    broadcast(room, lobbyState(code));
    broadcast(room, { t: 'left', id });
  });
});

server.listen(PORT, () => console.log('REPÚBLICA ONLINE sur le port ' + PORT));
