// Cash Ledger offline copy: always try the newest page first, fall back to the saved copy only when offline.
const CACHE = "cash-ledger-v2";
self.addEventListener("install", e => { self.skipWaiting(); });
self.addEventListener("activate", e => {
  e.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)));
    await self.clients.claim();
  })());
});
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  if (new URL(e.request.url).origin !== location.origin) return;
  e.respondWith((async () => {
    const cache = await caches.open(CACHE);
    try {
      const fresh = await fetch(e.request, { cache: "no-cache" });
      if (fresh && fresh.ok) cache.put(e.request, fresh.clone());
      return fresh;
    } catch (err) {
      const saved = await cache.match(e.request);
      return saved || new Response("Offline and nothing saved yet. Open once with internet.", { status: 503 });
    }
  })());
});
