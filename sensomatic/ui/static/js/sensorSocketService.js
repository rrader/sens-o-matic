'use strict';

function SocketService() {
    var service = {};

    var ws = new WebSocket("ws://" + window.location.hostname + (location.port ? ':' + location.port : '') + '/updates');
    var preConnectionRequests = [];
    var connected = false;

    var callback = null;

    ws.onopen = function () {
        connected = true;
        if (preConnectionRequests.length === 0) return;

        console.log('Sending (%d) requests', preConnectionRequests.length);
        for (var i = 0, c = preConnectionRequests.length; i < c; i++) {
            ws.send(JSON.stringify(preConnectionRequests[i]));
        }
        preConnectionRequests = [];
    };

    ws.onmessage = function (message) {
        console.log(message);

        var parsed = JSON.parse(message.data);
        // If an object exists with id in our subscriptions object, resolve it
        callback(parsed);
    };

    function subscribe(name, cb) {
        callback = cb;
        var request = {$type: 'subscribe', sensorName: name}
        if (!connected) {
            console.log('Not connected yet, saving request', request);
            preConnectionRequests.push(request);
            return;
        }

        console.log('Sending request', request);
        ws.send(JSON.stringify(request));
    }

    service.subscribe = subscribe;
    return service;
}