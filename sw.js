/* ATTENZIONE: questo NON è più il service worker dell'app.
   È un demolitore.

   Le prime versioni del Pokédex avevano un service worker difettoso che
   salvava anche le risposte fallite: su alcuni telefoni è rimasta incastrata
   una copia rotta dell'app, e chi ce l'ha non riesce più ad aprirla.

   Il browser ricontrolla da solo questo file a ogni apertura. Trovandolo
   cambiato lo installa — e questo, appena si attiva, cancella tutto quello
   che le vecchie versioni avevano salvato, si disinstalla e ricarica la
   pagina. Da lì l'app riparte pulita e registra il service worker nuovo,
   che si chiama sw-v3.js.

   Non va rimosso: serve a tutti i dispositivi che aprono il link con la
   vecchia versione ancora addosso. */

self.addEventListener('install', () => self.skipWaiting());

self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    try {
      const chiavi = await caches.keys();
      await Promise.all(chiavi.map(k => caches.delete(k)));
    } catch (e) {}
    try { await self.registration.unregister(); } catch (e) {}
    try {
      const clients = await self.clients.matchAll({ type: 'window' });
      for (const c of clients) {
        if ('navigate' in c) c.navigate(c.url);
      }
    } catch (e) {}
  })());
});

/* Finché è in vita non tocca niente: ogni richiesta va dritta in rete. */
self.addEventListener('fetch', () => {});
