importScripts('cache-polyfill.js');
self.addEventListener('install', function(e) {
    e.waitUntil(
        caches.open('belfast-cares').then(function(cache) {
            return cache.addAll([
                '/',
                '/?homescreen=1',
                '/static/css/style.css',
                '/static/css/responsive.css',
                '/static/css/bootstrap-margin-padding.css',
                '/static/img/bg/home_hero_1.jpg',
                '/static/img/bg/home_hero_2.jpg',
                '/static/img/resources/logo.png'
            ]);
        })
    );
});
self.addEventListener('fetch', function(event) {
    console.log(event.request.url);
    event.respondWith(
        caches.match(event.request).then(function(response) {
            return response || fetch(event.request);
        })
    );
});