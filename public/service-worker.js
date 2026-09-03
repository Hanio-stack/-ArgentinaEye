const CACHE="argentina-eye-v10";
const DATA_KEYS=["data/latest.json","data/valuation.json"];
const CORE=["./","index.html","styles.css","valuation.css","app.js","compare.js","manifest.webmanifest","icon.svg",...DATA_KEYS];

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
  const key=DATA_KEYS.find(k=>event.request.url.includes(`/${k}`));
  if(key){
    event.respondWith(
      fetch(event.request)
        .then(response=>{
          if(response.ok){const copy=response.clone();caches.open(CACHE).then(cache=>cache.put(key,copy));}
          return response;
        })
        .catch(()=>caches.match(key))
    );
    return;
  }
  event.respondWith(caches.match(event.request).then(hit=>hit||fetch(event.request)));
});