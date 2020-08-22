let port = window.location.port;
if (port === "6060") {
    port = 2000;
}

window.BACKEND_URL = `${window.location.protocol}//${window.location.hostname}:${port}`;