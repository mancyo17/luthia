/* Service worker del Pokédex di Aethera.
   Tiene l'app sul dispositivo così funziona anche senza connessione, ma
   controlla sempre se ne esiste una versione più nuova: quando la trova,
   l'app avvisa con un pulsante «Aggiorna».
   I salvataggi vivono in localStorage e non vengono mai toccati da qui. */

const VERSION = '3.4';
const CACHE = 'aethera-' + VERSION;
const ASSETS = ['./', './index.html', './p5e-data.js?v=3', './p5e-gen8.js?v=3', './manifest.json',
  './icon-192.png', './icon-512.png', './apple-touch-icon.png'];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => Promise.allSettled(ASSETS.map(a => c.add(a))))
  );
  /* niente skipWaiting automatico: la nuova versione entra quando lo decide
     il giocatore, così non si ritrova la pagina ricaricata a metà di una lotta */
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('message', e => {
  if (e.data && e.data.type === 'SKIP_WAITING') self.skipWaiting();
});

/* In cache ci finisce SOLO quello che è arrivato davvero: mai un 404, mai una
   risposta incompleta. Altrimenti un errore momentaneo resterebbe lì per sempre. */
function cacheable(res) {
  return res && res.ok && res.status === 200 &&
         (res.type === 'basic' || res.type === 'default');
}
function putIfGood(req, res) {
  if (!cacheable(res)) return;
  const copy = res.clone();
  caches.open(CACHE).then(c => c.put(req, copy)).catch(() => {});
}

function isShell(req) {
  return req.mode === 'navigate' ||
         req.url.endsWith('/') ||
         req.url.endsWith('index.html');
}

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET' || !req.url.startsWith(self.location.origin)) return;

  /* La pagina: prima la rete, così gli aggiornamenti arrivano subito;
     se la rete manca, la copia salvata. */
  if (isShell(req)) {
    e.respondWith(
      fetch(req)
        .then(res => { putIfGood(req, res); return res; })
        .catch(() => caches.match(req).then(hit => hit || caches.match('./index.html')))
    );
    return;
  }

  /* Tutto il resto: prima la copia salvata perché è più veloce, altrimenti la
     rete. Se la rete fallisce si restituisce l'errore vero: mai la pagina HTML
     al posto di uno script, che darebbe un guasto silenzioso e inspiegabile. */
  e.respondWith(
    caches.match(req).then(hit => {
      if (hit) return hit;
      return fetch(req).then(res => { putIfGood(req, res); return res; });
    })
  );
});
