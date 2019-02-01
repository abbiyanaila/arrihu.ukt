/*
 Copyright 2015 Google Inc. All Rights Reserved.
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
 http://www.apache.org/licenses/LICENSE-2.0
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
*/

'use strict';

const CACHE_VERSION = 1;
const OFFLINE_URL = '/offline.html';
let CURRENT_CACHES = {
    offline: 'offline-v' + CACHE_VERSION
};

const CACHES = [
    '/offline.html',
    '/static/css/app.css',
    '/static/components/bootstrap/dist/css/bootstrap.min.css',
    '/static/components/font-awesome/css/font-awesome.min.css',
    '/static/components/admin-lte/plugins/iCheck/all.css',
    '/static/components/select2/dist/css/select2.min.css',
    '/static/components/admin-lte/dist/css/AdminLTE.min.css',
    '/static/components/admin-lte/dist/css/skins/_all-skins.min.css',
    '/static/components/datatables.net-bs/css/dataTables.bootstrap.min.css',
    '/static/components/bootstrap-daterangepicker/daterangepicker.css',
    '/static/components/toastr/toastr.min.css',
    '/static/js/app.js',
    'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/platform/1.3.5/platform.min.js'
]

function createCacheBustedRequest(url) {
    let request = new Request(url, { cache: 'reload' });
    if ('cache' in request) {
        return request;
    }

    let bustedUrl = new URL(url, self.location.href);
    bustedUrl.search += (bustedUrl.search ? '&' : '') + 'cachebust=' + Date.now();
    return new Request(bustedUrl);
}

self.addEventListener('install', event => {
    event.waitUntil(
        fetch(createCacheBustedRequest(OFFLINE_URL)).then(function (response) {
            return caches.open(CURRENT_CACHES.offline).then(function (cache) {
                return cache.put(OFFLINE_URL, response);
            });
        })
    );

    event.waitUntil(self.skipWaiting())
});

self.addEventListener('activate', event => {
    let expectedCacheNames = Object.keys(CURRENT_CACHES).map(function (key) {
        return CURRENT_CACHES[key];
    });

    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (expectedCacheNames.indexOf(cacheName) === -1) {
                        console.log('Deleting out of date cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

self.addEventListener('fetch', event => {
    if (event.request.mode === 'navigate' ||
        (event.request.method === 'GET' &&
            event.request.headers.get('accept').includes('text/html'))) {
        console.log('Handling fetch event for', event.request.url);
        event.respondWith(
            fetch(event.request).catch(error => {
                console.log('Fetch failed; returning offline page instead.', error);
                return caches.match(OFFLINE_URL);
            })
        );
    }
});