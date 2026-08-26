const CACHE="argentina-eye-v4";
const DATA_KEY="data/latest.json";
const CORE=["./","index.html","styles.css","app.js","manifest.webmanifest","icon.svg",DATA_KEY];

self.addEventListener("install",event=>{
  event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(CORE)));
  self.skipWaiting();
});

self.addEventListener("activate",event=>{
  event.waitUntil(
    caches.keys()
      .then(keys=>Promise.all(keys.filter(key=>key!==CACHE).map(key=>caches.delete(key))))
      .then(()=>self.clients.claim())
  );
});

self.addEventListener("fetch",event=>{
  if(event.request.url.includes("/data/latest.json")){
    event.respondWith(
      fetch(event.request)
        .then(response=>{
          if(response.ok){
            const copy=response.clone();
            caches.open(CACHE).then(cache=>cache.put(DATA_KEY,copy));
          }
          return response;
        })
        .catch(()=>caches.match(DATA_KEY))
    );
    return;
  }
  event.respondWith(caches.match(event.request).then(hit=>hit||fetch(event.request)));
});
