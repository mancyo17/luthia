/* Service worker del Pokédex di Aethera.
   Tiene l'app in cache così funziona anche senza connessione, ma controlla
   sempre se ne esiste una versione più nuova: quando la trova, l'app avvisa
   il giocatore con un pulsante «Aggiorna».
   I salvataggi vivono in localStorage e non vengono mai toccati da qui. */

const VERSION = '2.2';
const CACHE = 'aethera-' + VERSION;
const ASSETS = ['./', './index.html', './manifest.json',
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

/* L'app è un file solo: per lei si prova prima la rete (così gli aggiornamenti
   arrivano), con la cache come rete di sicurezza. Per tutto il resto si parte
   dalla cache, che è più veloce. */
function isShell(req) {
  return req.mode === 'navigate' ||
         req.url.endsWith('/') ||
         req.url.endsWith('index.html');
}

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET' || !req.url.startsWith(self.location.origin)) return;

  if (isShell(req)) {
    e.respondWith(
      fetch(req).then(res => {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(req, copy)).catch(() => {});
        return res;
      }).catch(() => caches.match(req).then(hit => hit || caches.match('./index.html')))
    );
    return;
  }

  e.respondWith(
    caches.match(req).then(hit => hit || fetch(req).then(res => {
      const copy = res.clone();
      caches.open(CACHE).then(c => c.put(req, copy)).catch(() => {});
      return res;
    }).catch(() => caches.match('./index.html')))
  );
});
