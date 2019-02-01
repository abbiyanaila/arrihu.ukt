const paths = [
    '/offline.html',
    '/static/css/app.css',
    '/static/js/app.js',
]

self.addEventListener('install', function (event) {
    event.waitUntil(
        caches.open('offline-v1')
            .then(function (cache) {
                return cache.addAll(paths);
            })
    );
    event.waitUntil(self.skipWaiting());
});

function fetchAndCache(url, cache) {
    return fetch(url).then(function (response) {
        if (response.status < 400) {
            cache.put(url, response.clone());
        }
        return response.text();
    })
}

self.addEventListener("fetch", function (event) {
    event.respondWith(
        fetch(event.request).catch(function () {
            return caches.match(event.request).then(function (response) {
                if (response) {
                    return response;
                } else if (event.request.headers.get("accept").includes("text/html")) {
                    return caches.match("/offline.html");
                }
            });
        })
    );
});

// self.addEventListener('fetch', function (event) {
//     var requestURL = new URL(event.request.url);

//     if (requestURL == '/') {
//         event.respondWith(
//             fetch(event.request).then(function () {
//                 return caches.match(event.request);
//             }).catch(function () {
//                 return caches.match('/offline.html');
//             })
//         );
//     }

//     event.respondWith(
//         caches.match(event.request).then(function (response) {
//             return response || fetch(event.request);
//         }).catch(function () {
//             return caches.match('/offline.html');
//         })
//     );
// });

importScripts('https://www.gstatic.com/firebasejs/4.12.1/firebase.js')

firebase.initializeApp({
    messagingSenderId: "570435412084"
});

messaging = firebase.messaging()
messaging.setBackgroundMessageHandler((payload) => {
    console.log('[sw.js] Receive background message : ', payload)

    const notificationTitle = 'Background Message Title';
    const notificationOptions = {
        body: 'Background Message body.',
        icon: '/firebase-logo.png'
    };

    return self.registration.showNotification(notificationTitle,
        notificationOptions);
})