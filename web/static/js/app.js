
const messaging = firebase.messaging()

self.addEventListener('load', () => {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/serviceworker.js').then((registration) => {
            console.log('ServiceWorker registration successful with scope: ', registration.scope);

            messaging.useServiceWorker(registration)
            showNotificationPermission()
        }).catch((err) => {
            console.log('ServiceWorker registration failed: ', err);
        });

        navigator.serviceWorker.ready.then((registration) => {
            console.log('Service Worker Ready')
        })
    }
})

const showNotificationPermission = () => {
    messaging.requestPermission().then(() => {
        messaging.getToken().then((currentToken) => {
            console.log(currentToken)
            sentTokenToServer(currentToken)
        })
    }).catch((err) => {
        console.log('Notification Permission Denied')
    })
}

messaging.onTokenRefresh(function () {
    messaging.getToken()
        .then(function (refreshedToken) {
            console.log(refreshedToken)
            sendTokenToServer(refreshedToken);
        })
        .catch(function (err) {
            console.log('Unable to retrieve refreshed token ', err);
        });
});

const sentTokenToServer = (currentToken) => {
    console.log('Sending token to server...');
    fetch('http://localhost:8085/api/v1/device/create', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'registration_id': currentToken,
            'type': 'web',
        })
    }).then(function (response) {
        return response.json()
    })
}

messaging.onMessage((payload) => {
    title = payload.notification.title
    body = payload.notification.body
    toastr.success(body, title, { timeOut: 5000 })
})