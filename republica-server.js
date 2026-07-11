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

wss.on('connection', (ws) => {
  const id = nextId++;
  let roomCode = null;

  ws.on('message', (raw) => {
    let msg;
    try { msg = JSON.parse(raw); } catch { return; }
    const room = roomCode ? rooms[roomCode] : null;

    switch (msg.t) {
      // ---- créer un salon : {t:'create', name} ----
      case 'create': {
        const code = makeCode();
        rooms[code] = { hostId: id, clients: new Map(), started: false };
        rooms[code].clients.set(id, { ws, name: String(msg.name || 'Ministre').slice(0, 16) });
        roomCode = code;
        send(ws, { t: 'created', code, you: id });
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
        r.clients.set(id, { ws, name: String(msg.name || 'Ministre').slice(0, 16) });
        roomCode = code;
        send(ws, { t: 'joined', code, you: id });
        broadcast(r, lobbyState(code));
        send(ws, lobbyState(code));
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
    room.clients.delete(id);
    if (room.clients.size === 0) { delete rooms[roomCode]; return; }
    if (room.hostId === id) room.hostId = [...room.clients.keys()][0];   // l'hôte suivant reprend
    broadcast(room, lobbyState(roomCode));
    broadcast(room, { t: 'left', id });
  });
});

server.listen(PORT, () => console.log('REPÚBLICA ONLINE sur le port ' + PORT));
