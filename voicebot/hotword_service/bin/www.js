#!usr/bin/env node

import http from "http";
import https from "https";
import fs from "fs";

import app from "../src/app";

app.use((err, req, res, _) => {
    console.error("Error", err);
    res.status(500).send("Internal server error");
});

startServer(http.createServer(app), normalizePort(process.env.PORT || "6006"));

function startServer(server, port) {
    server.listen(port);
    server.on("error", (error) => {
        if (error.syscall !== "listen") {
            console.error("Critical error", error);
            throw "Internal Server error";
        }

        let bind = typeof port === "string" ? "Pipe " + port : "Port " + port;

        switch (error.code) {
            case "EACCES":
                console.error(bind + " requires elevated privileges");
                process.exit(1);
                break;
            case "EADDRINUSE":
                console.error(bind + " is already in use");
                process.exit(1);
                break;
            default:
                console.error("Critical error", error);
                throw "Internal Server error";
        }
    });

    server.on("listening", () => {
        let addr = server.address();
        let bind = typeof addr === "string" ? "pipe " + addr : "port " + addr.port;
        console.log("Listening on " + bind);
    });
}

function normalizePort(val) {
    let port = parseInt(val, 10);

    if (isNaN(port)) {
        // named pipe
        return val;
    }

    if (port >= 0) {
        // port number
        return port;
    }

    return false;
}