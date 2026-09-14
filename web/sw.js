/**
 * Service Worker Oficial - IBPM CR Super-App PWA
 * Estratégia de Cache: Stale-While-Revalidate + Cache-First para recursos estáticos.
 * Suporte completo ao funcionamento 100% Offline.
 */

const CACHE_NAME = 'ibpmcr-pwa-v1.0.0';
const STATIC_ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './css/styles.css',
  './css/components.css',
  './js/app.js',
  './js/state.js',
  './js/audio-player.js',
  './js/pwa-install.js',
  './js/views/home.js',
  './js/views/oracao.js',
  './js/views/palavra.js',
  './js/views/midia.js',
  './js/views/lojinha.js',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/icon-maskable.png',
  './icons/apple-touch-icon.png',
  './icons/favicon.png',
  './icons/favicon.ico'
];

// 1. Instalação: Cache dos arquivos essenciais
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[SW] Fazendo pré-cache dos assets estáticos...');
      return cache.addAll(STATIC_ASSETS);
    }).then(() => self.skipWaiting())
  );
});

// 2. Ativação: Limpeza de caches antigos
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((name) => {
          if (name !== CACHE_NAME) {
            console.log('[SW] Removendo cache obsoleto:', name);
            return caches.delete(name);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// 3. Interceptação de Requisições: Stale-While-Revalidate com Fallback Offline
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // Ignora chamadas de áudio contínuo/stream e APIs de terceiros se não quiser cachear tudo
  if (event.request.url.includes('stream') || event.request.url.includes('audio_stream')) {
    return;
  }

  // Requisições GET
  if (event.request.method === 'GET') {
    event.respondWith(
      caches.match(event.request).then((cachedResponse) => {
        // Se encontrou no cache, retorna e busca versão fresca em segundo plano
        const fetchPromise = fetch(event.request)
          .then((networkResponse) => {
            if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
              const responseToCache = networkResponse.clone();
              caches.open(CACHE_NAME).then((cache) => {
                cache.put(event.request, responseToCache);
              });
            }
            return networkResponse;
          })
          .catch(() => {
            // Em caso de falha de rede total (offline), o cache já respondeu
            if (event.request.mode === 'navigate') {
              return caches.match('./index.html');
            }
          });

        return cachedResponse || fetchPromise;
      })
    );
  }
});
